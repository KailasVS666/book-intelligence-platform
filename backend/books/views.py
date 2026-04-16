from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
book_embeddings = {}

def generate_insights():
    books = Book.objects.all()

    for book in books:
        if not book.summary:
            book.summary = generate_summary(book.description)

        if not book.genre:
            book.genre = classify_genre(book.description)

        book.save()

def generate_summary(text):
    if not text:
        return "No description available"
    
    # simple summary (first 20 words)
    words = text.split()
    return " ".join(words[:20])


def classify_genre(text):
    if not text:
        return "Unknown"

    text = text.lower()

    if "history" in text:
        return "History"
    elif "science" in text:
        return "Science"
    elif "fiction" in text:
        return "Fiction"
    elif "romance" in text:
        return "Romance"
    elif "business" in text or "productivity" in text:
        return "Self-Help"
    else:
        return "General"

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

@api_view(['POST'])
def upload_book(request):
    data = request.data
    
    if isinstance(data, list):
        created_books = []
        for item in data:
            if not Book.objects.filter(title=item.get('title'), author=item.get('author')).exists():
                serializer = BookSerializer(data=item)
                if serializer.is_valid():
                    book = serializer.save()
                    if not book.summary:
                        book.summary = generate_summary(book.description)
                    if not book.genre:
                        book.genre = classify_genre(book.description)
                    book.save()
                    # Trigger embedding refresh (simple way)
                    book_embeddings[book.id] = model.encode(book.description)
                    created_books.append(serializer.data)
        return Response(created_books, status=201)
    else:
        if Book.objects.filter(title=data.get('title'), author=data.get('author')).exists():
            return Response({"error": "Book already exists"}, status=400)
        
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            book = serializer.save()
            if not book.summary:
                book.summary = generate_summary(book.description)
            if not book.genre:
                book.genre = classify_genre(book.description)
            book.save()
            book_embeddings[book.id] = model.encode(book.description)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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

    if not book_embeddings:
        load_book_embeddings()

    target_embedding = book_embeddings.get(pk)
    
    scored_books = []

    for book in books:
        score = 0
        if book.id in book_embeddings and target_embedding is not None:
            book_embedding = book_embeddings[book.id]
            # cosine similarity
            similarity = (target_embedding @ book_embedding) / (
                (target_embedding @ target_embedding) ** 0.5 *
                (book_embedding @ book_embedding) ** 0.5
            )
            score = float(similarity)
        
        scored_books.append((book, score))

    # sort by similarity score descending
    scored_books.sort(key=lambda x: x[1], reverse=True)

    # get top 5 recommended books
    recommended = [book for book, score in scored_books[:5] if score > 0.3]

    serializer = BookSerializer(recommended, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question", "")
    if not question:
        return Response({"error": "Question is required"}, status=400)

    if not book_embeddings:
        load_book_embeddings()

    books = Book.objects.all()

    best_match = None
    best_score = 0

    question_embedding = model.encode(question)

    for book in books:
        if not book.description:
            continue

        book_embedding = book_embeddings.get(book.id)
        if book_embedding is None:
            continue

        # cosine similarity
        similarity = (question_embedding @ book_embedding) / (
            (question_embedding @ question_embedding) ** 0.5 *
            (book_embedding @ book_embedding) ** 0.5
        )

        score = float(similarity)

        if score > best_score:
            best_score = score
            best_match = book

    if best_match and best_score > 0.2:
        return Response({
            "question": question,
            "answer": best_match.description, # Using description as context/answer for now
            "book": best_match.title,
            "confidence": round(best_score, 4)
        })

    return Response({
        "question": question,
        "answer": "I'm sorry, I couldn't find a relevant book to answer your question.",
        "book": "None",
        "confidence": round(best_score, 4)
    })

# load_book_embeddings()