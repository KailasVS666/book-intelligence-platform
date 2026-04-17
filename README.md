# Document Intelligence Platform

A high-performance, full-stack intelligence platform for book data analysis. It utilizes **Retrieval-Augmented Generation (RAG)** to enable natural language conversations with a library of books, powered by a 100% local and private AI pipeline.

---

## 🖼 Platform Interface

| Dashboard & Discovery | Advanced Filtering |
|:---:|:---:|
| ![Dashboard](./docs/screenshots/dashboard.png) | ![Filtering](./docs/screenshots/filter.png) |

| Deep Intelligence | Contextual Q&A |
|:---:|:---:|
| ![Book Detail](./docs/screenshots/detail.png) | ![AI Response](./docs/screenshots/qa.png) |

---

## 🏗 System Architecture

```mermaid
graph TD
    subgraph "Data Acquisition"
        A[Selenium Scraper] -->|Deep Scrape| B[Raw JSON Data]
        B --> C[Synchronous Database Loader]
    end

    subgraph "Intelligence Core (Local AI)"
        D[Django REST API] <-->|Vector Metadata| E[ChromaDB]
        D <-->|Local Inference| F[Ollama: Deepseek-R1]
        D <-->|Semantic Embeddings| G[Sentence-Transformers]
    end

    subgraph "Storage"
        D <-->|Structured Data| H[MySQL Database]
    end

    subgraph "User Interface"
        I[Next.js 15 Dashboard] <-->|RESTful Calls| D
    end
```

---

## 🚀 Key Features

- **Local-First AI Integration**: Utilizes **Ollama** with the **Deepseek-R1** model for zero-cost, private AI insights and Q&A.
- **Selective Retrieval (RAG)**: Implements semantic search across book descriptions using `all-MiniLM-L6-v2` and **ChromaDB**.
- **Automated Book Forensics**: Generates summaries, genre classification, and sentiment analysis automatically upon book ingestion.
- **Deep Web Scraping**: Advanced Selenium engine that visits industrial catalog pages to harvest high-resolution cover art.
- **Glassmorphism UI**: A premium, responsive dark-mode dashboard built for professional research and analysis.

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL Server
- [Ollama](https://ollama.com/) (Must be installed and running)

### 1. AI Model Setup
Ensure Ollama is running, then pull the required model:
```bash
ollama pull deepseek-r1:latest
```

### 2. Backend Environment
Navigate to `backend/` and initialize the environment:
```bash
# Install dependencies
pip install -r requirements.txt

# Run Database Migrations
python manage.py makemigrations
python manage.py migrate

# Start the API Server
python manage.py runserver
```

### 3. Data Ingestion (Scraping)
To populate the library with 40 intelligence-ready books:
```bash
# Run the scraper
python books/scraper/scrape_books.py

# Load data into the database and initialize RAG index
python books/scraper/load_to_db.py
```

### 4. Frontend Dashboard
Navigate to `frontend/` and start the interface:
```bash
npm install
npm run dev
```

---

## 📄 API Surface

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/books/` | GET | List all books with AI-generated metadata. |
| `/api/books/{id}/` | GET | Retrieve full forensics for a single book. |
| `/api/books/{id}/recommendations/` | GET | Semantic neighbors based on vector similarity. |
| `/api/books/ask/` | POST | Context-aware Q&A against the book library. |

---

## 🔍 Sample Intelligence Response

**Query**: *"Explain David Byrne's core philosophy regarding music as described in this book."*

**AI Response**:
> Based on the provided context, David Byrne's core philosophy regarding music includes:
> 1. **Music as Adaptation and Response**: He views music as part of a "larger, almost Darwinian pattern" of adaptations. Music evolves in response to its surrounding cultural and physical environment.
> 2. **Contextual Shaping**: Byrne emphasizes that music is profoundly shaped by its time and place.
> 3. **Interdisciplinary Approach**: His exploration is described as panoptic, drawing from his roles as an anthropologist, social scientist, and historian.

---

## 🧪 Testing

To verify the stability and data integrity of the platform, run the automated test suite:
```bash
cd backend
python tests/test_stability.py
```

---
**Built for the Ergosphere Solutions Document Intelligence Internship.**

