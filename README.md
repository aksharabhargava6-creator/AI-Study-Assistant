# AI Study Assistant

An AI-powered study assistant that allows users to upload PDF study material and ask questions based on the uploaded documents.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from documents before generating context-grounded answers using a local Large Language Model.

## Features

- Upload PDF study material
- Extract and process PDF text
- Split documents into smaller chunks
- Generate semantic embeddings
- Perform similarity-based document retrieval
- Ask questions about uploaded documents
- Generate answers using a local LLM
- Display source page references
- Persistent chat history
- Create and manage multiple study chats
- Automatic chat titles
- Document management
- Delete documents and chats
- React-based study assistant interface

## Architecture

```text
                    AI Study Assistant
                           |
                           v
                    React Frontend
                           |
                           | REST API
                           v
                    FastAPI Backend
                           |
              +------------+------------+
              |                         |
              v                         v
        PDF Processing             PostgreSQL
              |                  Chat History
              v
       Text Chunking
              |
              v
    Sentence Transformer
        Embeddings
              |
              v
       Vector Retrieval
              |
              v
        Relevant Context
              |
              v
       Local Qwen LLM
              |
              v
        Grounded Answer
              |
              v
       Answer + Sources
Tech Stack
Frontend
React
Vite
JavaScript
HTML
CSS
Backend
Python
FastAPI
REST APIs
AI / Machine Learning
Retrieval-Augmented Generation (RAG)
Sentence Transformers
Semantic embeddings
Cosine similarity search
Large Language Model
Ollama
Qwen 2.5
Database
PostgreSQL
Document Processing
PyPDF
RAG Pipeline

The application follows a basic Retrieval-Augmented Generation pipeline:

PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
Vector Storage
    ↓
User Question
    ↓
Question Embedding
    ↓
Similarity Search
    ↓
Top Relevant Chunks
    ↓
Context + Question
    ↓
Local LLM
    ↓
Answer + Source Pages

This approach allows the application to answer questions using the uploaded study material rather than relying only on the model's general knowledge.

Project Structure
AI-Study-Assistant/
│
├── ai-service/
│   ├── main.py
│   ├── database.py
│   ├── document_processor.py
│   ├── document_registry.py
│   ├── chunker.py
│   ├── embedding_service.py
│   ├── vector_store.py
│   ├── search.py
│   ├── rag.py
│   ├── llm_service.py
│   ├── chat_service.py
│   └── test_*.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
Requirements

Before running the project, install:

Python 3.9+
Node.js
npm
PostgreSQL
Ollama

The application currently uses the local Ollama model:

qwen2.5:1.5b

The embedding model used is:

all-MiniLM-L6-v2
Running the Backend

Navigate to the AI service:

cd ai-service

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install the required Python dependencies.

Then start FastAPI:

uvicorn main:app --reload --port 8001

The backend will be available at:

http://127.0.0.1:8001

Health check:

GET /health
Running the Frontend

Open another terminal:

cd frontend
npm install
npm run dev

The frontend will be available at:

http://localhost:5173
Database

The application uses PostgreSQL for persistent chat sessions and messages.

Create a database named:

ai_study_assistant

Database configuration is read from environment variables:

DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

Example:

DB_NAME=ai_study_assistant
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

Do not commit .env files or database credentials to GitHub.

API Endpoints
Documents
POST   /documents/upload
GET    /documents
GET    /documents/{document_id}
DELETE /documents/{document_id}
Question Answering
POST /ask
Chats
POST   /chats
GET    /chats
GET    /chats/{session_id}
GET    /chats/{session_id}/messages
DELETE /chats/{session_id}
Health
GET /health
Example Workflow
Start PostgreSQL.
Start Ollama.
Start the FastAPI backend.
Start the React frontend.
Upload a PDF.
Select the uploaded document.
Ask a question.
The system retrieves relevant document chunks.
The retrieved context is passed to the local LLM.
The generated answer and source pages are displayed in the UI.
The conversation is stored in PostgreSQL.
Learning Goals

This project was built to understand and apply:

REST API development
React frontend development
Python backend development
PostgreSQL database integration
Document processing
Text chunking
Embeddings
Semantic search
Retrieval-Augmented Generation
LLM integration
Vector-based retrieval
Chat persistence
Full-stack application architecture
Future Improvements

Potential future improvements include:

User authentication
Multiple user accounts
Improved vector database integration
Streaming LLM responses
Conversation-aware RAG
Better document chunking strategies
Hybrid keyword + semantic search
Support for additional document formats
Cloud deployment
More advanced evaluation of RAG retrieval and answer quality
Author

Akshara Bhargava

B.Tech Computer Science Engineering

Built as a full-stack AI/GenAI learning and portfolio project.