from typing import Any, Dict
from rest_framework import status, views, generics
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, BookListSerializer
from .ai_insights import generate_book_insights
from .rag import index_book, ask_rag_question, get_relevant_chunks
import threading

class BookListCreateView(generics.ListAPIView):
    """
    Exposes a list of all indexed books ordered by creation date.
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookListSerializer

class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves detailed metadata for a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUploadView(views.APIView):
    """
    Handles book ingestion, metadata storage, and initiates downstream AI processing.
    """
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        book_url = serializer.validated_data.get('book_url')
        existing_book = Book.objects.filter(book_url=book_url).first()
        
        if existing_book:
            return Response(BookSerializer(existing_book).data, status=status.HTTP_200_OK)
        
        book = serializer.save()
        
        # Initiate background processing for AI insights and RAG indexing
        threading.Thread(target=self._process_book_background, args=(book.id,)).start()
        
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

    def _process_book_background(self, book_id: int) -> None:
        """
        Private method to handle asynchronous AI analysis and indexing.
        """
        try:
            book = Book.objects.get(id=book_id)
            insights = generate_book_insights(book.description)
            
            book.ai_summary = insights.get('summary')
            book.genre = insights.get('genre')
            book.sentiment = insights.get('sentiment')
            book.save()
            
            index_book(book_id)
        except Book.DoesNotExist:
            pass
        except Exception as e:
            # In a production environment, use a logger here
            print(f"Background processing error for book {book_id}: {e}")

class BookRecommendationView(views.APIView):
    """
    Generates intelligent book recommendations using semantic similarity.
    """
    def get(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        try:
            book = Book.objects.get(pk=pk)
            
            # Retrieve semantic neighbors from vector store
            query_context = f"{book.title} {book.genre or ''}"
            chunks = get_relevant_chunks(query_context, top_k=6)
            
            book_ids = {chunk["metadata"]["book_id"] for chunk in chunks if chunk["metadata"]["book_id"] != book.id}
            
            # Fill remaining recommendations using genre overlap (fallback)
            if len(book_ids) < 5:
                genre_matches = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:5]
                book_ids.update(gb.id for gb in genre_matches)
            
            recommended_books = Book.objects.filter(id__in=list(book_ids)[:5])
            serializer = BookListSerializer(recommended_books, many=True)
            return Response(serializer.data)
            
        except Book.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

class AskQuestionView(views.APIView):
    """
    Entry point for RAG-based natural language queries against book intelligence.
    """
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        question = request.data.get('question')
        book_id = request.data.get('book_id')
        
        if not question:
            return Response({"error": "Question parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        result = ask_rag_question(question, book_id)
        return Response(result, status=status.HTTP_200_OK)