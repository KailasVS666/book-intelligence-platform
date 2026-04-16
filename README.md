# Document Intelligence Platform

A full-stack web application designed for processing book data, generating AI-based insights, and enabling context-aware Q&A using a Retrieval-Augmented Generation (RAG) pipeline.

## 🏗 Architecture Overview

```ascii
[ Selenium Scraper ]  --> [ books_raw.json ] --> [ Loader Script ]
                                                       |
                                                       v
[ Next.js Frontend ] <--> [ Django REST API ] <--> [ MySQL DB ]
                                 |         |
                                 v         v
                         [ Claude 3.5 ] [ ChromaDB Vector Store ]
```

## 🚀 Features

- **Multi-page Web Scraping**: Automated data collection using Selenium.
- **AI Insights**: Automated generation of book summaries, genre classification, and sentiment analysis via Claude 3.5 Sonnet.
- **RAG Pipeline**: Semantic search across book descriptions using `sentence-transformers` and ChromaDB.
- **Contextual Q&A**: Ask detailed questions about specific books or the entire library.
- **Premium UI**: Modern dark-mode interface with glassmorphism and responsive design.

## 🛠 Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL Server
- Anthropic API Key

### Backend Setup
1. Navigate to `backend/`
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env` file (see below).
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to `frontend/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

### Scraper Setup
1. Navigate to `scraper/`
2. Run the scraper:
   ```bash
   python scrape_books.py
   ```
3. Load data to database:
   ```bash
   python load_to_db.py
   ```

## 📄 API Documentation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/books/` | GET | List all books with basic metadata. |
| `/api/books/{id}/` | GET | Full detail of a book including AI summary & sentiment. |
| `/api/books/{id}/recommendations/` | GET | Returns 5 similar books based on vector similarity. |
| `/api/books/upload/` | POST | Accept JSON body, save to DB, trigger AI analysis & indexing. |
| `/api/books/ask/` | POST | RAG query endpoint. Body: `{"question": "...", "book_id": optional}` |

## 🔑 Environment Variables (.env)

```env
ANTHROPIC_API_KEY=your_claude_api_key_here
DJANGO_SECRET_KEY=your_django_secret_key
DB_NAME=ergosphere_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
CHROMA_PERSIST_DIR=./chroma_db
```

## ❓ Sample Questions
- "What is the primary theme of Harry Potter?"
- "Can you suggest a book with a mystery genre?"
- "Is the tone of 'The Alchemist' positive?"

---
Built by Antigravity for Ergosphere Solutions.
