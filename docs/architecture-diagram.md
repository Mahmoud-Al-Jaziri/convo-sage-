# Architecture Overview

ConvoSage system architecture.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│                    (React + Vite)                           │
│                   Port: 5173                                │
│                                                             │
│  - Landing Page ✅                                          │
│  - Chat Interface ✅                                        │
│  - Quick Actions ✅                                         │
│  - localStorage Persistence ✅                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTP/REST
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                        BACKEND                              │
│                      (FastAPI)                              │
│                    Port: 8000                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              API Endpoints                          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  GET  /              - Root ✅                      │   │
│  │  GET  /health        - Health Check ✅              │   │
│  │  GET  /docs          - OpenAPI Docs ✅              │   │
│  │  POST /chat          - Conversation ✅              │   │
│  │  GET  /products      - RAG Search ✅                │   │
│  │  GET  /outlets       - Text2SQL ✅                  │   │
│  │  POST /calculator    - Tool Call ✅                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           LangChain Agents                          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  - Conversation Agent with Memory ✅                │   │
│  │  - Planner/Controller (ReAct) ✅                    │   │
│  │  - Multi-turn State Tracking ✅                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               Custom Tools                          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  - Calculator Tool ✅                               │   │
│  │  - Products Search Tool ✅                          │   │
│  │  - Outlets Query Tool ✅                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Services                           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  - Product Service (RAG) ✅                         │   │
│  │  - Outlets Service (Text2SQL) ✅                    │   │
│  │  - Text2SQL Service ✅                              │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────┬──────────────────┬──────────────────────┘
                   │                  │
        ┌──────────▼─────┐   ┌────────▼──────────┐
        │   Vector Store │   │   SQL Database    │
        │    (FAISS)     │   │    (SQLite)       │
        │                │   │                   │
│  - Products    │   │  - Outlets Table  │
│    Embeddings  │   │  - Location Data  │
│                │   │  - Hours, etc.    │
│  ✅            │   │  ✅               │
        └────────────────┘   └───────────────────┘
                   │                  │
        ┌──────────▼──────────────────▼──────────┐
        │         External Services               │
        ├─────────────────────────────────────────┤
        │  - OpenAI API (GPT-4) ✅                │
        │  - OpenAI Embeddings ✅                 │
        └─────────────────────────────────────────┘
```

---

## Data Flow

### Chat Message Flow
```
1. User sends message via Frontend
   │
   ▼
2. POST /chat with {message, session_id}
   │
   ▼
3. Conversation Agent
   ├─> Retrieve memory for session
   ├─> Send to LLM with context
   └─> Decide: Respond | Ask Follow-up | Call Tool
   │
   ▼
4. Execute action:
   ├─> Direct Response
   ├─> Calculator Tool
   ├─> Products RAG Search
   └─> Outlets Text2SQL Query
   │
   ▼
5. Update conversation memory
   │
   ▼
6. Return response to Frontend
```

### RAG Search Flow
```
1. User query: "best insulated tumbler"
   │
   ▼
2. GET /products?query=...
   │
   ▼
3. Product Service:
   ├─> Embed query (OpenAI)
   ├─> Search FAISS vector store
   ├─> Retrieve top-K products
   └─> Augment LLM prompt with products
   │
   ▼
4. LLM generates summary
   │
   ▼
5. Return formatted response
```

### Text2SQL Flow
```
1. User query: "outlets in Petaling Jaya"
   │
   ▼
2. GET /outlets?query=...
   │
   ▼
3. Text2SQL Service:
   ├─> Send query + schema to LLM
   ├─> LLM generates SQL query
   ├─> Validate & sanitize SQL
   └─> Execute on SQLite DB
   │
   ▼
4. Format results
   │
   ▼
5. Return data to user
```

---

## Technology Stack

### Frontend
- **Framework**: React 19.1
- **Build Tool**: Vite 7.x
- **Styling**: Plain CSS (modern, gradient-based)
- **State**: React Hooks (useState, useEffect)
- **Storage**: localStorage (for persistence)

### Backend
- **Framework**: FastAPI 0.104
- **Server**: Uvicorn with auto-reload
- **Validation**: Pydantic 2.5
- **CORS**: Enabled for localhost:5173

### AI/LLM
- **Agent Framework**: LangChain 0.1.0
- **LLM**: OpenAI GPT-4 (via langchain-openai)
- **Embeddings**: OpenAI text-embedding-ada-002
- **Memory**: ConversationBufferMemory

### Data Storage
- **Vector DB**: FAISS (CPU version 1.7.4)
- **SQL DB**: SQLite (via SQLAlchemy 2.0.23)
- **In-Memory**: Python dicts for session storage

### Testing & Dev
- **Testing**: pytest 7.4.3 + pytest-asyncio
- **HTTP Client**: httpx (for testing)
- **Data Scraping**: BeautifulSoup4 + requests

---

## Directory Structure

```
convo-sage/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py       # App entry, CORS, routes
│   │   ├── config.py     # Settings from env
│   │   ├── api/          # Endpoint handlers
│   │   ├── agents/       # LangChain agents
│   │   ├── tools/        # Custom tools
│   │   ├── services/     # Business logic
│   │   ├── models/       # Pydantic schemas
│   │   └── db/           # DB & vector store
│   ├── tests/            # Test suite
│   ├── requirements.txt  # Dependencies
│   └── .env              # Configuration
│
├── frontend/             # React application
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   ├── main.jsx      # Entry point
│   │   ├── components/   # Chat UI components
│   │   ├── services/     # API clients
│   │   └── hooks/        # Custom hooks
│   └── package.json      # Dependencies
│
├── data/                 # Data storage
│   ├── products_raw.json # ZUS drinkware data
│   ├── outlets_raw.json  # ZUS outlet data
│   ├── app.db            # SQLite database
│   └── vector_store/     # FAISS index files
│
├── scripts/              # Utility scripts
│   ├── scrape_products.py  # Product scraper
│   ├── scrape_outlets.py   # Outlet scraper
│   └── build_vector_store.py # FAISS indexing
│
└── docs/                 # Documentation
    ├── backend-patterns.md    # Code conventions
    ├── api-spec.md            # API documentation
    └── architecture-diagram.md # System architecture
```

---

## API Endpoints

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| GET | `/` | API info | ✅ |
| GET | `/health` | Health check | ✅ |
| GET | `/docs` | OpenAPI docs | ✅ |
| POST | `/chat` | Conversation | ✅ |
| POST | `/calculator` | Arithmetic tool | ✅ |
| GET | `/products` | RAG search | ✅ |
| GET | `/outlets` | Text2SQL query | ✅ |

---

## Security Considerations

- ✅ CORS configured for specific origins
- ✅ Environment variables for secrets
- ✅ .gitignore for sensitive files
- ✅ SQL injection prevention (parameterized queries)
- ✅ Input validation (Pydantic)
- ✅ Rate limiting
- ✅ Error message sanitization

---

## Deployment Architecture

```
┌─────────────────────────────────┐
│         Vercel / Netlify        │
│      (Frontend Deployment)      │
│                                 │
│   - Static React build          │
│   - CDN distribution            │
│   - Environment variables       │
└────────────┬────────────────────┘
             │
             │ HTTPS
             │
┌────────────▼────────────────────┐
│      Render / Railway           │
│     (Backend Deployment)        │
│                                 │
│   - FastAPI server              │
│   - SQLite database             │
│   - FAISS vector store          │
│   - Environment variables       │
│   - Health checks enabled       │
└─────────────────────────────────┘
```


