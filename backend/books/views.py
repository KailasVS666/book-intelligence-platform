from typing import Any
from rest_framework import status, views, generics
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, BookListSerializer
from .services import BookService
from .rag import ask_rag_question, get_relevant_chunks

class BookListCreateView(generics.ListAPIView):
    """List all books, powered by the service layer."""
    serializer_class = BookListSerializer
    
    def get_queryset(self):
        return BookService.get_all_books()

class BookDetailView(generics.RetrieveAPIView):
    """Retrieve individual book forensics."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUploadView(views.APIView):
    """Ingest new books into the intelligence pipeline."""
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Offload logic to specialized service
        book = BookService.ingest_book_metadata(serializer.validated_data)
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

class BookRecommendationView(views.APIView):
    """Intelligent neighbor discovery via vector search and metadata heuristics."""
    def get(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        book = BookService.get_book_by_id(pk)
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # 1. Semantic Neighbors
        query_context = f"{book.title} {book.genre or ''}"
        chunks = get_relevant_chunks(query_context, top_k=8)
        
        book_ids = {
            chunk["metadata"]["book_id"] 
            for chunk in chunks 
            if chunk["metadata"]["book_id"] != book.id
        }
        
        # 2. Heuristic Fallback (Genre overlap)
        if len(book_ids) < 5:
            genre_matches = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:5]
            book_ids.update(gb.id for gb in genre_matches)
        
        recommended_books = Book.objects.filter(id__in=list(book_ids)[:5])
        serializer = BookListSerializer(recommended_books, many=True)
        return Response(serializer.data)

class AskQuestionView(views.APIView):
    """Query the RAG pipeline for book-specific or library-wide intelligence."""
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        question = request.data.get('question')
        book_id = request.data.get('book_id')
        
        if not question:
            return Response({"error": "Question parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        result = ask_rag_question(question, book_id)
        return Response(result, status=status.HTTP_200_OK)