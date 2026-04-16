from rest_framework import status, views, generics
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, BookListSerializer
from .ai_insights import generate_book_insights
from .rag import index_book, ask_rag_question, get_relevant_chunks
import threading

class BookListCreateView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookListSerializer

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUploadView(views.APIView):
    """
    Accepts book data, saves to DB, then triggers AI insights and indexing.
    """
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Check for duplicates by URL or title
            title = serializer.validated_data.get('title')
            book_url = serializer.validated_data.get('book_url')
            
            existing_book = Book.objects.filter(book_url=book_url).first()
            if existing_book:
                return Response(BookSerializer(existing_book).data, status=status.HTTP_200_OK)
            
            book = serializer.save()
            
            # Trigger AI Insights (can be async in real prod, here synchronous for simplicity or threading)
            # We'll use a simple thread to not block the response if possible, 
            # though the brief implies it happens on upload.
            
            def process_book(b_id):
                b = Book.objects.get(id=b_id)
                # 1. Generate AI Insights
                insights = generate_book_insights(b.description)
                b.ai_summary = insights.get('summary')
                b.genre = insights.get('genre')
                b.sentiment = insights.get('sentiment')
                b.save()
                
                # 2. Index for RAG
                index_book(b_id)
            
            # For demonstration purposes, we run it in a thread
            thread = threading.Thread(target=process_book, args=(book.id,))
            thread.start()
            
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookRecommendationView(views.APIView):
    """
    Returns 5 similar books based on embedding similarity.
    """
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            
            # Simple recommendation: same genre + some random others
            # Bonus: use ChromaDB to find similar books based on average embeddings
            # For now, let's just use genre and nearest neighbors from ChromaDB
            
            # Get chunks from this book to query for other books
            collection = get_relevant_chunks(book.title + " " + (book.genre or ""), top_k=6)
            
            book_ids = set()
            for chunk in collection:
                bid = chunk["metadata"]["book_id"]
                if bid != book.id:
                    book_ids.add(bid)
            
            # Fallback to genre if not enough from embeddings
            if len(book_ids) < 5:
                genre_books = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:5]
                for gb in genre_books:
                    book_ids.add(gb.id)
            
            recommended = Book.objects.filter(id__in=list(book_ids)[:5])
            serializer = BookListSerializer(recommended, many=True)
            return Response(serializer.data)
            
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class AskQuestionView(views.APIView):
    """
    RAG query endpoint.
    """
    def post(self, request):
        question = request.data.get('question')
        book_id = request.data.get('book_id')
        
        if not question:
            return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        result = ask_rag_question(question, book_id)
        return Response(result, status=status.HTTP_200_OK)