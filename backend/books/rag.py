import chromadb
from sentence_transformers import SentenceTransformer
from django.conf import settings
from .models import Book, BookChunk
import uuid
import os

# Initialize SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_chroma_client():
    persist_dir = getattr(settings, "CHROMA_PERSIST_DIR", "./chroma_db")
    os.makedirs(persist_dir, exist_ok=True)
    return chromadb.PersistentClient(path=persist_dir)

def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name="book_chunks")

def chunk_text(text, chunk_size=200, overlap=50):
    """
    Splits text into chunks of specified token count with overlap.
    Simplification: using word count instead of true tokens for basic version.
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

def index_book(book_id):
    """
    Chunks book description + summary, generates embeddings, and stores in ChromaDB.
    """
    try:
        book = Book.objects.get(id=book_id)
        full_text = f"{book.description or ''} {book.ai_summary or ''}".strip()
        
        if not full_text:
            return
            
        chunks = chunk_text(full_text)
        collection = get_collection()
        
        # Clear existing chunks if any (re-indexing)
        BookChunk.objects.filter(book=book).delete()
        
        for i, text in enumerate(chunks):
            embedding = model.encode(text).tolist()
            embedding_id = str(uuid.uuid4())
            
            # Save to BookChunk model
            BookChunk.objects.create(
                book=book,
                chunk_text=text,
                chunk_index=i,
                embedding_id=embedding_id
            )
            
            # Save to ChromaDB
            collection.add(
                ids=[embedding_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{"book_id": book.id, "chunk_index": i}]
            )
            
        print(f"Indexed book {book.id}: {len(chunks)} chunks created.")
        
    except Exception as e:
        print(f"Error indexing book {book_id}: {e}")

def get_relevant_chunks(question, book_id=None, top_k=5):
    """
    Searches ChromaDB for chunks relevant to the question.
    """
    collection = get_collection()
    query_embedding = model.encode(question).tolist()
    
    where_filter = None
    if book_id:
        where_filter = {"book_id": int(book_id)}
        
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )
    
    relevant_chunks = []
    if results["documents"]:
        for i in range(len(results["documents"][0])):
            relevant_chunks.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })
            
    return relevant_chunks

def ask_rag_question(question, book_id=None):
    """
    Complete RAG flow: Retrieve -> Augment -> Generate.
    """
    relevant_chunks = get_relevant_chunks(question, book_id)
    
    context = "\n\n".join([c["text"] for c in relevant_chunks])
    
    import ollama
    model_name = getattr(settings, "OLLAMA_MODEL", "llama3")
    
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
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0
            }
        )
        
        answer = response['message']['content']
        
        # Format sources

        sources = []
        for chunk in relevant_chunks:
            bid = chunk["metadata"]["book_id"]
            try:
                b = Book.objects.get(id=bid)
                sources.append({
                    "book_title": b.title,
                    "chunk": chunk["text"][:200] + "..."
                })
            except:
                continue
                
        # Remove duplicates from sources based on snippet
        seen = set()
        unique_sources = []
        for s in sources:
            if s["chunk"] not in seen:
                unique_sources.append(s)
                seen.add(s["chunk"])
                
        return {
            "answer": answer,
            "sources": unique_sources
        }
        
    except Exception as e:
        print(f"Error in RAG: {e}")
        return {
            "answer": "Sorry, I encountered an error while processing your question.",
            "sources": []
        }
