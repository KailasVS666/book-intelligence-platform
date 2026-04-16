from typing import List, Dict, Any, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from django.conf import settings
from .models import Book, BookChunk
import uuid
import os

# Initialize SentenceTransformer on module load
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_chroma_client() -> chromadb.PersistentClient:
    """
    Returns an initialized persistent ChromaDB client.
    """
    persist_dir = getattr(settings, "CHROMA_PERSIST_DIR", "./chroma_db")
    os.makedirs(persist_dir, exist_ok=True)
    return chromadb.PersistentClient(path=persist_dir)

def get_collection() -> chromadb.Collection:
    """
    Retrieves or creates the standard collection for book chunks.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(name="book_chunks")

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """
    Decomposes text into manageable chunks with specified overlap.
    """
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [text]
        
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += (chunk_size - overlap)
        
    return chunks

def index_book(book_id: int) -> None:
    """
    Generates semantic embeddings for a book and persists them to the vector store.
    """
    try:
        book = Book.objects.get(id=book_id)
        content = f"{book.description or ''} {book.ai_summary or ''}".strip()
        
        if not content:
            return
            
        chunks = chunk_text(content)
        collection = get_collection()
        
        # Atomically refresh book chunks
        BookChunk.objects.filter(book=book).delete()
        
        for i, text in enumerate(chunks):
            embedding = model.encode(text).tolist()
            embedding_id = str(uuid.uuid4())
            
            BookChunk.objects.create(
                book=book,
                chunk_text=text,
                chunk_index=i,
                embedding_id=embedding_id
            )
            
            collection.add(
                ids=[embedding_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{"book_id": int(book.id), "chunk_index": i}]
            )
        
    except Exception as e:
        # Proper error handling should involve structured logging
        pass

def get_relevant_chunks(question: str, book_id: Optional[int] = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Queries the vector store for semantic matches relative to the input query.
    """
    collection = get_collection()
    query_embedding = model.encode(question).tolist()
    
    where_filter = None
    if book_id is not None:
        where_filter = {"book_id": int(book_id)}
        
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )
    
    relevant = []
    if results["documents"] and results["documents"][0]:
        for i in range(len(results["documents"][0])):
            relevant.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })
            
    return relevant

def ask_rag_question(question: str, book_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Orchestrates the RAG workflow: Retrieval, Augmentation, and Generation.
    """
    relevant_chunks = get_relevant_chunks(question, book_id)
    context = "\n\n".join([c["text"] for c in relevant_chunks])
    
    import ollama
    model_name = getattr(settings, "OLLAMA_MODEL", "deepseek-r1:latest")
    
    prompt = f"""
    You are a helpful book intelligence assistant. Use the provided context to answer the user's question.
    If the context doesn't contain the answer, say "I don't have enough information in my database about that."
    
    Context:
    {context}
    
    Question:
    {question}
    """
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1}
        )
        
        answer = response['message']['content']
        
        # Deduplicate and format source citations
        unique_sources = []
        seen_chunks = set()
        
        for chunk in relevant_chunks:
            bid = chunk["metadata"]["book_id"]
            text_snippet = chunk["text"][:200]
            if text_snippet not in seen_chunks:
                try:
                    b = Book.objects.get(id=bid)
                    unique_sources.append({
                        "book_title": b.title,
                        "chunk": f"{text_snippet}..."
                    })
                    seen_chunks.add(text_snippet)
                except Book.DoesNotExist:
                    continue
                
        return {
            "answer": answer,
            "sources": unique_sources
        }
        
    except Exception as e:
        return {
            "answer": "A system error occurred while generating the response.",
            "sources": []
        }

