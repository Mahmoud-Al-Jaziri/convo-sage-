# Architecture Overview

Current system architecture as of Day 1.

---

## System Architecture (Day 1)

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│                    (React + Vite)                           │
│                   Port: 5173                                │
│                                                             │
│  - Landing Page (Day 1) ✅                                  │
│  - Chat Interface (Days 8-9) ⏳                             │
│  - Quick Actions ⏳                                          │
│  - localStorage Persistence ⏳                               │
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
│  │  POST /chat          - Conversation (Day 2) ⏳      │   │
│  │  GET  /products      - RAG Search (Day 5) ⏳        │   │
│  │  GET  /outlets       - Text2SQL (Day 6) ⏳          │   │
│  │  POST /calculator    - Tool Call (Day 3) ⏳         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           LangChain Agents (Day 2+)                 │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  - Conversation Agent with Memory ⏳                 │   │
│  │  - Planner/Controller (ReAct) ⏳                     │   │
│  │  - Multi-turn State Tracking ⏳                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               Custom Tools (Day 3+)                 │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  - Calculator Tool ⏳                                │   │
│  │  - Products Search Tool ⏳                           │   │
│  │  - Outlets Query Tool ⏳                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Services                           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  - Product Service (RAG) ⏳                          │   │
│  │  - Outlets Service (Text2SQL) ⏳                     │   │
│  │  - Text2SQL Service ⏳                               │   │
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
        │  (Day 5) ⏳    │   │  (Day 4) ⏳       │
        └────────────────┘   └───────────────────┘
                   │                  │
        ┌──────────▼──────────────────▼──────────┐
        │         External Services               │
        ├─────────────────────────────────────────┤
        │  - OpenAI API (GPT-4) ⏳                │
        │  - OpenAI Embeddings ⏳                 │
        └─────────────────────────────────────────┘
```

---

## Data Flow (Planned for Day 2+)

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

### RAG Search Flow (Day 5)
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

### Text2SQL Flow (Day 6)
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
│   │   ├── main.py       # ✅ App entry, CORS, routes
│   │   ├── config.py     # ✅ Settings from env
│   │   ├── api/          # ⏳ Endpoint handlers
│   │   ├── agents/       # ⏳ LangChain agents
│   │   ├── tools/        # ⏳ Custom tools
│   │   ├── services/     # ⏳ Business logic
│   │   ├── models/       # ⏳ Pydantic schemas
│   │   └── db/           # ⏳ DB & vector store
│   ├── tests/            # ✅ Test suite
│   ├── requirements.txt  # ✅ Dependencies
│   └── .env              # ⏠ Config (add API key!)
│
├── frontend/             # React application
│   ├── src/
│   │   ├── App.jsx       # ✅ Main component
│   │   ├── main.jsx      # ✅ Entry point
│   │   ├── components/   # ⏳ Chat UI components
│   │   ├── services/     # ⏳ API clients
│   │   └── hooks/        # ⏳ Custom hooks
│   └── package.json      # ✅ Dependencies
│
├── data/                 # Data storage
│   ├── products_raw.json # ⏳ ZUS drinkware data
│   ├── outlets_raw.json  # ⏳ ZUS outlet data
│   ├── app.db            # ⏳ SQLite database
│   └── vector_store/     # ⏳ FAISS index files
│
├── scripts/              # Utility scripts
│   ├── scrape_products.py  # ⏳ Product scraper
│   ├── scrape_outlets.py   # ⏳ Outlet scraper
│   └── build_vector_store.py # ⏳ FAISS indexing
│
└── docs/                 # Documentation
    ├── milestone-plan.md      # ✅ 10-day plan
    ├── backend-patterns.md    # ✅ Code conventions
    ├── learning-resources.md  # ✅ Learning guides
    ├── progress.md            # ✅ Daily progress
    ├── day1-summary.md        # ✅ Day 1 recap
    └── architecture-diagram.md # ✅ This file

Legend:
  ✅ Complete
  ⏳ Planned/In Progress
  ⏠ Action Required
```

---

## API Endpoints (Final State)

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| GET | `/` | API info | ✅ Day 1 |
| GET | `/health` | Health check | ✅ Day 1 |
| GET | `/docs` | OpenAPI docs | ✅ Day 1 |
| POST | `/chat` | Conversation | ⏳ Day 2 |
| POST | `/calculator` | Arithmetic tool | ⏳ Day 3 |
| GET | `/products` | RAG search | ⏳ Day 5 |
| GET | `/outlets` | Text2SQL query | ⏳ Day 6 |

---

## Security Considerations

### Implemented (Day 1)
- ✅ CORS configured for specific origins
- ✅ Environment variables for secrets
- ✅ .gitignore for sensitive files

### Planned
- ⏳ SQL injection prevention (parameterized queries)
- ⏳ Input validation (Pydantic)
- ⏳ Rate limiting (if time permits)
- ⏳ Error message sanitization

---

## Deployment Architecture (Day 10)

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

---

## Next Evolution (Day 2)

The next major update to this architecture will be:

1. **Conversation Agent** - LangChain agent with memory
2. **Memory Store** - Session-based state management
3. **Chat Endpoint** - POST /chat handler
4. **Multi-turn Testing** - Verify 3+ turn conversations

**See**: `docs/milestone-plan.md` (Day 2 section) for details.

---

*Last Updated: Day 1 - November 4, 2025*

