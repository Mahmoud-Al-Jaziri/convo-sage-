# ConvoSage ☕🤖

A conversational AI chatbot for ZUS Coffee with agentic planning, RAG, Text2SQL, and modern UX features.

[![Tests](https://img.shields.io/badge/tests-106%2F106%20passing-success)]() 
[![Frontend](https://img.shields.io/badge/frontend-React%2019-blue)]() 
[![Backend](https://img.shields.io/badge/backend-FastAPI-green)]()

---

## Features

### Core Capabilities
- 🤖 **Sequential Conversation** - Multi-turn memory with LangChain
- 🧠 **Agentic Planning** - Intelligent tool routing and action selection
- 🧮 **Calculator Tool** - Safe mathematical expression evaluation
- ☕ **Product Search (RAG)** - Custom TF-IDF vector search
- 📍 **Outlet Finder (Text2SQL)** - Natural language to SQL queries
- 🛡️ **Error Handling** - Comprehensive validation and security

### Advanced UX
- ⚡ **Quick Actions** - Slash commands with autocomplete
- 🎨 **Tool Badges** - Visual indicators for tool usage
- 📋 **Copy Messages** - One-click clipboard copy
- 💾 **Dual Persistence** - localStorage + backend sessions
- ✨ **Smooth Animations** - 60fps transitions
- 📱 **Mobile Responsive** - Touch-optimized interface

---

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **AI/ML**: LangChain 0.1.0
- **Database**: SQLite3
- **Vector Store**: Custom TF-IDF
- **Testing**: Pytest (106 tests passing)

### Frontend
- **Framework**: React 19.1.1
- **Build Tool**: Vite 7.1.7
- **Styling**: CSS3
- **State**: React Hooks

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/Mahmoud-Al-Jaziri/convo-sage-.git
cd convo-sage
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Ingest data
python scripts/ingest_outlets.py

# Start server
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## Usage Examples

### Basic Conversation
```
User: Hi, my name is Sarah
Bot: Hello Sarah! Nice to meet you.
User: What is my name?
Bot: Your name is Sarah.
```

### Calculator
```
User: Calculate 25 * 4
Bot: The result of 25*4 is 100
[Badge: 🧮 Calculator]
```

### Product Search
```
User: Show me tumblers
Bot: Here are the tumblers I found:
     1. Large Tumbler - RM 45.00
     2. ZUS Tumbler - RM 55.00
[Badge: ☕ Product Search]
```

### Outlet Search
```
User: Find outlets in Kuala Lumpur with drive-through
Bot: Here are the ZUS Coffee outlets...
[Badge: 📍 Outlet Finder]
```

### Slash Commands
```
/calc 5 + 3         → Quick calculation
/products tumbler   → Search products
/outlets KL         → Find outlets
/help               → Show commands
/reset              → Clear conversation
```

---

## Architecture

```
Frontend (React) → FastAPI Backend → ToolAgent
                                       ├─ Calculator
                                       ├─ Product Search (RAG)
                                       └─ Outlet Search (Text2SQL)
```

### Project Structure

```
convo-sage/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── api/         # Endpoints
│   │   ├── agents/      # LangChain agents
│   │   ├── tools/       # Calculator, RAG, Text2SQL
│   │   ├── models/      # Pydantic models
│   │   ├── rag/         # Vector search
│   │   ├── text2sql/    # SQL generation
│   │   ├── db/          # Database
│   │   └── middleware/  # Error handling, rate limiting
│   ├── tests/           # 106 tests
│   ├── scripts/         # Data ingestion
│   └── data/            # Products, outlets
│
├── frontend/            # React app
│   ├── src/
│   │   ├── components/  # Chat UI
│   │   └── utils/       # Command parser
│   └── package.json
│
└── docs/               # Documentation
```

---

## Testing

### Backend Tests

```bash
cd backend
.\venv\Scripts\activate
pytest tests/ -v
```

**Results:** 106/106 tests passing ✅

---

## API Endpoints

- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `POST /chat/` - Chat with AI
- `GET /chat/history/{session_id}` - Get conversation history
- `DELETE /chat/session/{session_id}` - Clear session
- `GET /chat/stats` - Get statistics
- `GET /products/` - List all products
- `GET /products/search` - Search products
- `GET /outlets/` - List all outlets
- `GET /outlets/search` - Search outlets

---

## Security Features

- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Rate limiting (60/min, 1000/hour)
- ✅ Input validation
- ✅ Error sanitization
- ✅ CORS configuration

---

## Performance

- **Backend Response**: < 500ms average
- **Frontend Load**: < 1s
- **Animations**: 60fps
- **localStorage Restore**: Instant

---

## Documentation

- **[API Specification](docs/api-spec.md)** - API endpoints
- **[Database Schema](docs/database-schema.md)** - Database structure
- **[Frontend Architecture](docs/frontend-architecture.md)** - Component design
- **[Agentic Planning](docs/agentic-planning.md)** - Tool routing

---

## Contributing

This is a portfolio project. For questions or suggestions, please open an issue.

---

## License

MIT License - see LICENSE file for details.

---

**Developer:** Mahmoud Al-Jaziri  
**GitHub:** https://github.com/Mahmoud-Al-Jaziri/convo-sage-
