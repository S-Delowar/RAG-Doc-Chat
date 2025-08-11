# 📄 AI-Powered Document Chat Application
_Chat with documents using advanced retrieval-augmented AI agents_

## 🚀 Overview
This is a **production-ready backend** for AI-powered document chat platform where authenticated users can:
- Upload documents (stored **AWS S3**).
- Ingest vectorized data to **Weaviate**.
- Chat with an **AI agent** about uploaded documents or general queries.
- Get **web search-augmented answers** when the knowledge base is insufficient.

It combines **retrieval-augmented generation (RAG)**, **agent routing, memory-aware summarization**, and **continuous deployment**.

## 🎯 Problem Statement
Searching through large documents manually is inefficient.
This system enables **natural-language document** interaction powered by:
- **Vector database search** (Weaviate)
- **Multi-tool AI agent**
- **Web search integration**
- **Memory-based context management**

## ✨ Features
- 🔐 **JWT Authentication** & **Authorization**

- 📤 **Document Upload** to AWS S3 bucket

- 🔍 **Semantic Search** & **RAG** with Weaviate

- 🧠 **Conversation Memory**:

  - Stores last 10 messages

  - Summarizes older chat logs via Celery tasks

- ⚙️ **Agent Routing** using LangGraph:

  - **QA Tool** – Document-based answers

  - **Direct Tool** – Simple Q&A without retrieval

  - **Web Search Tool** – Tavily-powered answers

- 📡 **Background Processing** – Celery + Redis

- 🧪 **Automated Testing** with Pytest

- 🐳 **Dockerized Application** with `start.sh`

- 🔄 **docker-compose** for local multi-service orchestration

- 🚀 **CI/CD Pipeline** with GitHub Actions deploying to AWS EC2
- 🗄 **Relational + Vector Databases**: PostgreSQL + Weaviate.

  
## 🛠 Tech Stack
- **Backend**: Django REST Framework, Celery, Redis, PostgreSQL, LangChain, LangGraph, LangSmith, Tavily
- **Vector DB**: Weaviate
- **Cloud**: AWS S3, EC2
- **Auth**: SimpleJWT
- **Deployment**: Docker, docker-compose, GitHub Actions CI/CD to AWS EC2
- **Testing**: Pytest


  
## 🏗 Architecture
(Replace placeholder with your diagram)

**Flow Summary**:

1. **User uploads document** → Stored in AWS S3.
2. **Django signal** → Triggers ingestion:
    - Load from S3.
    - Split into chunks.
    - Store embeddings in Weaviate.
3. **User sends message**:
    - Query Rewriter cleans/optimizes query.
    - Router Node picks tool.
    - Result returned with memory context.
4. **Celery background job**:
  - Summarizes chat history every 10 messages.

## ⚙️ Installation & Setup
### 1. Prerequisites
- Python 3.11+
- An OpenAI API key
- An AWS account, S3 bucket; IAM user
- A Weaviate cluster(cloud or self-hosted)
- A PostgreSQL database(local or containerized)
- Docker & Docker Compose

### 2. Clone the Repository
```bash
git clone https://github.com/S-Delowar/RAG-Doc-Chat.git
cd RAG-Doc-Chat
```

### 3. Create .env file 
Add the following environmental variables with your values.
```bash
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-api-key
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_TRACING=true
LANGCHAIN_PROJECT=RAG-Doc-Chat-Project

ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SECRET_KEY=your-django-secret-key

DB_NAME=your-db-name
DB_USER=db-username
DB_PASSWORD=db-password
DB_HOST=db-host
DB_PORT=db-port

SUPERUSER_USERNAME=super
SUPERUSER_EMAIL=super@mail.com
SUPERUSER_PASSWORD=super1234

WEAVIATE_URL=your-weviate-cluster-url
WEAVIATE_API_KEY=your-weaviate-api-key

AWS_ACCESS_KEY_ID=your-aws-iam-user-access-key
AWS_SECRET_ACCESS_KEY=your-aws-iam-user-secret-access-key
AWS_S3_BUCKET_NAME=your-aws-s3-bucket
AWS_REGION=your-aws-region
USE_S3=TRUE

DOCKER_IMAGE=
sdelowar2/rag-doc-api
```

### 3. Run Locally (Virtual Environment)
```
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
python manage.py collecstatic --noinput
python manage.py migrate
python manage.py runserver
```
Application will be available at: http://localhost:8000

### 4. Run with Docker
```
docker-compose up --build
```
Application will be available at: http://localhost:8000

**docker-compose.yml** orchestrates:
- **web** → Django + Gunicorn app
- **redis** → task broker for Celery
- **celery** → background worker

**Dockerization**
- `start.sh` ensures migrations, superuser creation and staticfiles collection before starting the app.
- **Dockerfile** copies code, installs dependencies, and runs `start.sh`.


## 🔄 CI/CD Pipeline
This project includes a **GitHub Actions CI/CD** workflow:
1. **Tests** – Runs Pytest against a PostgreSQL service
2. **Docker Build & Push** – Builds image and pushes to Docker Hub
3. **Deploy to AWS EC2** – Pulls latest image, updates .env, restarts services with docker-compose

*(Workflow file in `.github/workflows/ci-cd.yml`)*


## 📚 API Endpoints

| API Endpoint | Use Case | Input | Output |
|--------------|----------|-------|--------|
| **POST** `/api/auth/login/` | Authenticate user and retrieve JWT tokens | `{ "email": "string", "password": "string" }` | `{ "refresh": "string", "access": "string" }` |
| **POST** `/api/auth/refresh/` | Refresh expired access token | `{ "refresh": "string" }` | `{ "access": "string" }` |
| **POST** `/api/auth/register/` | Register a new user and get authentication tokens | `{ "email": "string", "username": "string", "password": "string" }` | `{ "user": { "id": "uuid", "email": "string", "username": "string", "first_name": "string/null", "last_name": "string/null", "is_active": true, "is_staff": false, "date_joined": "datetime" }, "refresh": "string", "token": "string" }` |
| **PATCH** `/api/documents/{id}/` | Update a specific document | `{ "file": "string" }` | `{ "id": "uuid", "file": "string", "uploaded_at": "datetime" }` |
| **DELETE** `/api/documents/{id}/` | Delete a specific document | Path param: `id` | `204 No Content` |
| **PATCH** `/api/messages/{id}/` | Update a specific message | `{ "content": "string" }` | `{ "id": "uuid", "sender": "user", "content": "string", "timestamp": "datetime" }` |
| **DELETE** `/api/messages/{id}/` | Delete a specific message | Path param: `id` | `204 No Content` |
| **GET** `/api/sessions/` | List all chat sessions of the authenticated user | None | `[ { "id": "uuid", "user": "uuid", "title": "string", "created_at": "datetime", "documents": [ { "id": "uuid", "file": "string", "uploaded_at": "datetime" } ], "chat_messages": [ { "id": "uuid", "sender": "user", "content": "string", "timestamp": "datetime" } ] } ]` |
| **POST** `/api/sessions/` | Create a new chat session | `{ "title": "string" }` | `{ "id": "uuid", "user": "uuid", "title": "string", "created_at": "datetime", "documents": [], "chat_messages": [] }` |
| **GET** `/api/sessions/{id}/` | Retrieve details of a specific chat session | Path param: `id` | `{ "id": "uuid", "user": "uuid", "title": "string", "created_at": "datetime", "documents": [...], "chat_messages": [...] }` |
| **PATCH** `/api/sessions/{id}/` | Update a specific chat session | `{ "title": "string" }` | `{ "id": "uuid", "user": "uuid", "title": "string", "created_at": "datetime", "documents": [...], "chat_messages": [...] }` |
| **DELETE** `/api/sessions/{id}/` | Delete a specific chat session | Path param: `id` | `204 No Content` |
| **POST** `/api/sessions/{id}/documents/` | Upload a document to a chat session | File upload (multipart/form-data) | Updated session object with documents list |
| **POST** `/api/sessions/{id}/messages/` | Send a message and get AI response for a session | `{ "content": "string" }` | `{ "ai_response": "string" }` |
| **GET** `/api/user/me/` | Get current authenticated user's profile | None | `{ "id": "uuid", "email": "string", "username": "string", "first_name": "string/null", "last_name": "string/null", "is_active": true, "is_staff": false, "date_joined": "datetime" }` |
| **PATCH** `/api/user/me/` | Update current authenticated user's profile (username/email cannot be updated) | `{ "first_name": "string", "last_name": "string" }` | Updated user profile object |













