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
    try:
        target_book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    keywords = target_book.description.lower().split()

    books = Book.objects.exclude(id=pk)

    scored_books = []

    for book in books:
        score = 0
        if book.description:
            for word in keywords:
                if word in book.description.lower():
                    score += 1

        scored_books.append((book, score))

    # sort by score descending
    scored_books.sort(key=lambda x: x[1], reverse=True)

    # get only books (ignore score)
    recommended = [book for book, score in scored_books if score > 0]

    serializer = BookSerializer(recommended, many=True)
    return Response(serializer.data)

