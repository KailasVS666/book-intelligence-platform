from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    book_url = models.URLField(max_length=500)
    cover_image_url = models.URLField(max_length=500, null=True, blank=True)
    
    # AI generated fields
    genre = models.CharField(max_length=100, null=True, blank=True)
    ai_summary = models.TextField(null=True, blank=True)
    sentiment = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookChunk(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    embedding_id = models.CharField(max_length=255) # Reference to ChromaDB ID

    def __str__(self):
        return f"{self.book.title} - Chunk {self.chunk_index}"