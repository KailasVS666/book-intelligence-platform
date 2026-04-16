from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
book_embeddings = {}

def load_book_embeddings():
    books = Book.objects.all()
    for book in books:
        if book.description:
            book_embeddings[book.id] = model.encode(book.description)

def chunk_text(text, chunk_size=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

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

@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question", "").lower()

    books = Book.objects.all()

    best_match = None
    best_score = 0

    question_embedding = model.encode(question)

    for book in books:
        if not book.description:
            continue

        book_embedding = book_embeddings.get(book.id)

        # cosine similarity
        similarity = (question_embedding @ book_embedding) / (
            (question_embedding @ question_embedding) ** 0.5 *
            (book_embedding @ book_embedding) ** 0.5
        )

        score = similarity

        if score > best_score:
            best_score = score
            best_match = book

    if best_match:
        return Response({
            "answer": best_match.description,
            "book": best_match.title
        })

    return Response({"answer": "No relevant book found"})

load_book_embeddings()