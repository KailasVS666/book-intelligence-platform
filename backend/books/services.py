from typing import Any, Dict, Optional
import logging
import threading
from django.db import transaction
from .models import Book
from .ai_insights import generate_book_insights
from .rag import index_book

logger = logging.getLogger(__name__)

class BookService:
    @staticmethod
    def get_all_books():
        """Returns all books ordered by creation date."""
        return Book.objects.all().order_by('-created_at')

    @staticmethod
    def get_book_by_id(book_id: int) -> Optional[Book]:
        """Retrieves a book by ID or returns None."""
        try:
            return Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def ingest_book_metadata(data: Dict[str, Any]) -> Book:
        """
        Handles the deduplication and ingestion of book metadata.
        Returns the existing book if found, or creates a new one.
        """
        book_url = data.get('book_url')
        
        with transaction.atomic():
            existing_book = Book.objects.filter(book_url=book_url).first()
            if existing_book:
                logger.info(f"Book already exists: {existing_book.title}")
                return existing_book
            
            # Create new book
            book = Book.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                rating=data.get('rating'),
                review_count=data.get('review_count'),
                description=data.get('description'),
                book_url=book_url,
                cover_image_url=data.get('cover_image_url')
            )
            
            # Trigger background enrichment
            BookService._trigger_enrichment(book.id)
            return book

    @staticmethod
    def _trigger_enrichment(book_id: int) -> None:
        """Dispatches the enrichment process to a background thread."""
        logger.info(f"Triggering background enrichment for book {book_id}")
        thread = threading.Thread(
            target=BookService._process_enrichment_worker, 
            args=(book_id,),
            name=f"EnrichmentWorker-{book_id}"
        )
        thread.start()

    @staticmethod
    def _process_enrichment_worker(book_id: int) -> None:
        """
        Background worker that performs AI analysis and RAG indexing.
        In a production environment, this would be a Celery or RQ task.
        """
        try:
            book = Book.objects.get(id=book_id)
            
            # Phase 1: AI Analysis
            logger.info(f"Generating AI insights for: {book.title}")
            insights = generate_book_insights(book.description)
            
            book.ai_summary = insights.get('summary')
            book.genre = insights.get('genre')
            book.sentiment = insights.get('sentiment')
            book.save()
            
            # Phase 2: RAG Indexing
            logger.info(f"indexing book in vector store: {book.title}")
            index_book(book_id)
            
            logger.info(f"Successfully enriched book: {book.title}")
            
        except Book.DoesNotExist:
            logger.error(f"Book {book_id} vanished during enrichment.")
        except Exception as e:
            logger.error(f"Enrichment failure for book {book_id}: {str(e)}", exc_info=True)
