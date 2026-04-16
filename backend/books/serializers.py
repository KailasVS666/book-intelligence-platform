from rest_framework import serializers
from .models import Book, BookChunk

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'rating', 'review_count', 
            'description', 'book_url', 'cover_image_url', 
            'genre', 'ai_summary', 'sentiment', 'created_at'
        ]

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'rating', 'review_count', 
            'genre', 'cover_image_url', 'book_url'
        ]