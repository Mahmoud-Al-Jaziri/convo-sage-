# ConvoSage - AI Chatbot

A conversational AI chatbot with agentic planning, RAG, and Text2SQL capabilities for the Mindhive AI Software Engineer assessment.

## Features

- 🤖 **Multi-turn Conversations** - Maintains context across 3+ turns
- 🧠 **Agentic Planning** - Intent parsing and action selection
- 🔧 **Tool Calling** - Integrated calculator and custom APIs
- 📚 **RAG Pipeline** - Product search using vector embeddings
- 🗄️ **Text2SQL** - Natural language to database queries
- 🛡️ **Error Handling** - Graceful degradation and security measures

## Documentation

- [API Specification](docs/api-spec.md)
- [Database Schema](docs/database-schema.md)
- [Architecture Overview](docs/architecture-diagram.md)

## Tech Stack
- **Backend**: Python, FastAPI, LangChain
- **Frontend**: React
- **Vector Store**: FAISS
- **Database**: SQLite
- **LLM**: OpenAI GPT-4

## Project Structure
```
convo-sage/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── agents/      # LangChain agents & memory
│   │   ├── tools/       # Custom tools (calculator, etc)
│   │   ├── models/      # Pydantic models
│   │   └── db/          # Database & vector store
│   └── tests/           # Backend tests
├── frontend/            # React app
│   └── src/
│       ├── components/  # UI components
│       ├── services/    # API clients
│       └── hooks/       # Custom React hooks
├── data/               # Raw data (products, outlets)
├── docs/               # Documentation
└── scripts/            # Setup & ingestion scripts
```

## Setup

### Prerequisites
- Python 3.10+
- Node.js 20+
- OpenAI API key

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Add your OpenAI API key to .env
# OPENAI_API_KEY=sk-your-key-here

uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
cd backend
pytest
```

## API Endpoints

- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `POST /chat` - Chat with AI (coming soon)
- `GET /products` - Search products (coming soon)
- `GET /outlets` - Query outlets (coming soon)

## Architecture

Full-stack application with:
- **Frontend**: React with Vite for fast development
- **Backend**: FastAPI with LangChain for AI capabilities
- **Data Layer**: SQLite database + FAISS vector store

---
**Assessment Timeline**: 10 days  
**Start Date**: November 4, 2025  
**Target Completion**: November 13, 2025

