from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['GET'])
def recommend_books(request, pk):
    books = Book.objects.exclude(id=pk)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

    