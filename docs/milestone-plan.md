# 10-Day Milestone Plan

**Philosophy**: Build the bare minimum that meets requirements. Demo quality, not production quality.

---

## Day 1: Foundation & Setup (3-4 hours)
**Goal**: Project scaffolding, environment setup, understand the assessment deeply

### Deliverables
- [ ] Project structure created
- [ ] Backend FastAPI skeleton running
- [ ] Frontend React app initialized
- [ ] Requirements.txt with core dependencies
- [ ] Environment variables template
- [ ] Basic health check endpoint

### Files to Create
```
backend/
  app/
    main.py              # FastAPI app entry
    config.py            # Settings & env vars
  requirements.txt
  .env.example
frontend/
  package.json
  src/App.tsx
docs/
  backend-patterns.md
  progress.md
```

### Technologies to Understand
- FastAPI basics (routing, dependency injection)
- React project structure
- Environment variable management

### Success Criteria
- `GET /health` returns 200 on backend
- Frontend shows "Hello World" page
- Can run both frontend and backend locally

**Time Breakdown**: Setup (1h) + Coding (2h) + Documentation (1h)

---

## Day 2: Core Agent & Memory System (4-5 hours)
**Goal**: Implement Part 1 (Sequential Conversation) with LangChain

### Deliverables
- [ ] LangChain conversation memory setup
- [ ] Simple chatbot endpoint `/chat` that maintains state
- [ ] Conversation state stored in memory (at least 3 turns)
- [ ] Basic tests for memory persistence

### Files to Create
```
backend/app/
  agents/
    __init__.py
    conversation_agent.py    # Main agent with memory
    memory_store.py          # State management
  api/
    chat.py                  # /chat endpoint
  models/
    chat_models.py           # Pydantic models
tests/
  test_conversation.py       # Memory tests
```

### Technologies to Understand
- **LangChain ConversationBufferMemory** or **ConversationSummaryMemory**
- Agent state management patterns
- Session tracking

### Success Criteria
- Agent remembers context across 3+ turns
- `POST /chat` accepts message and session_id
- Test passes for interrupted conversation flow

**Time Breakdown**: Learning (1.5h) + Implementation (2.5h) + Testing (1h)

---

## Day 3: Agentic Planning & Calculator Tool (4-5 hours)
**Goal**: Implement Part 2 (Agentic Planning) and Part 3 (Tool Calling)

### Deliverables
- [ ] Planner/controller logic using LangChain ReAct agent
- [ ] Calculator tool integration
- [ ] Decision flow: parse intent → choose action → execute
- [ ] Error handling for calculator failures
- [ ] Write-up of decision points

### Files to Create
```
backend/app/
  tools/
    __init__.py
    calculator.py            # Calculator tool wrapper
  agents/
    planner.py               # ReAct agent / controller
  api/
    calculator.py            # Calculator API endpoint (mock)
docs/
  agentic-planning.md        # Decision flow write-up
tests/
  test_planner.py
  test_calculator.py
```

### Technologies to Understand
- **LangChain Tools** and **ReAct agents**
- Function calling with LLMs
- Structured output parsing

### Success Criteria
- Agent can detect "calculate 5+3" and invoke calculator
- Handles calculator errors gracefully
- Can decide between: ask follow-up, call tool, or respond directly

**Time Breakdown**: Learning (1.5h) + Implementation (2.5h) + Testing & Write-up (1h)

---

## Day 4: Data Collection & Database Setup (3-4 hours)
**Goal**: Scrape/collect ZUS data and set up databases

### Deliverables
- [ ] ZUS drinkware product data collected (manually or scraped)
- [ ] ZUS outlet data collected
- [ ] SQLite database schema for outlets
- [ ] Data ingestion scripts
- [ ] Raw data stored in `data/` folder

### Files to Create
```
data/
  products_raw.json         # Scraped drinkware data
  outlets_raw.json          # Scraped outlet data
backend/app/db/
  __init__.py
  database.py               # SQLite connection
  schema.sql                # Outlets table schema
scripts/
  scrape_products.py        # Scraper for drinkware
  scrape_outlets.py         # Scraper for outlets
  ingest_data.py            # Load data into DB
docs/
  database-schema.md        # Document tables
```

### Technologies to Understand
- Web scraping (BeautifulSoup or manual copy-paste)
- SQLite setup and schema design
- Data cleaning basics

### Success Criteria
- At least 10 products in JSON format
- At least 10 outlets with: name, location, hours, services
- SQLite database created with outlets table populated
- Schema documented

**Time Breakdown**: Data collection (2h) + Schema design (0.5h) + Ingestion scripts (1h) + Documentation (0.5h)

---

## Day 5: RAG Pipeline - Products Endpoint (4-5 hours)
**Goal**: Implement Part 4 (Custom API) - `/products` with vector store

### Deliverables
- [ ] Vector store (FAISS) for product embeddings
- [ ] Ingestion script: products → embeddings → FAISS
- [ ] `/products?query=<text>` endpoint with RAG
- [ ] Retrieval + LLM summarization
- [ ] Tests for happy/failure cases

### Files to Create
```
backend/app/
  db/
    vector_store.py          # FAISS wrapper
  services/
    product_service.py       # RAG logic
  api/
    products.py              # /products endpoint
scripts/
  build_vector_store.py      # Embed & index products
tests/
  test_products_api.py
```

### Technologies to Understand
- **OpenAI Embeddings** (text-embedding-ada-002)
- **FAISS** vector store basics
- RAG pattern: retrieve → augment prompt → generate

### Success Criteria
- Vector store built with product data
- Query "best insulated tumbler" returns relevant products
- Returns summary of top-3 products
- Handles empty results gracefully

**Time Breakdown**: Learning RAG (1.5h) + Implementation (2.5h) + Testing (1h)

---

## Day 6: Text2SQL - Outlets Endpoint (4-5 hours)
**Goal**: Implement Part 4 (Custom API) - `/outlets` with Text2SQL

### Deliverables
- [ ] Text2SQL prompt template
- [ ] SQL executor with safety checks
- [ ] `/outlets?query=<nl_text>` endpoint
- [ ] Tests including SQL injection attempts
- [ ] Error handling for malformed SQL

### Files to Create
```
backend/app/
  services/
    text2sql_service.py      # NL → SQL translation
    outlets_service.py       # Query execution
  api/
    outlets.py               # /outlets endpoint
  prompts/
    text2sql_prompt.txt      # Few-shot examples
tests/
  test_outlets_api.py
  test_sql_injection.py
```

### Technologies to Understand
- Text2SQL prompting techniques
- SQL parameterization for security
- SQLite query execution

### Success Criteria
- "outlets in Petaling Jaya" → correct SQL → results
- SQL injection attempts blocked/sanitized
- Returns clear error for ambiguous queries
- Handles "no results found" gracefully

**Time Breakdown**: Learning Text2SQL (1h) + Implementation (2.5h) + Security testing (1h) + Documentation (0.5h)

---

## Day 7: Integration & Unhappy Flows (4-5 hours)
**Goal**: Wire all APIs to agent, implement Part 5 (Unhappy Flows)

### Deliverables
- [ ] Agent can call `/products`, `/outlets`, calculator
- [ ] Handle missing parameters with follow-up questions
- [ ] Handle API downtime (500 errors)
- [ ] Handle malicious inputs
- [ ] Comprehensive test suite for negative cases
- [ ] Update API documentation

### Files to Create
```
backend/app/
  tools/
    products_tool.py         # LangChain tool wrapper
    outlets_tool.py          # LangChain tool wrapper
  middleware/
    error_handler.py         # Global error handling
tests/
  test_unhappy_flows.py
  test_api_downtime.py
  test_malicious_input.py
docs/
  api-spec.md                # OpenAPI documentation
  error-handling.md          # Strategy write-up
```

### Technologies to Understand
- LangChain custom tool creation
- FastAPI error handling and middleware
- Input validation and sanitization

### Success Criteria
- All 3 negative scenarios tested and passing
- Agent asks clarifying questions when params missing
- Clear error messages returned (never crashes)
- Security strategy documented

**Time Breakdown**: Integration (2h) + Unhappy flows (2h) + Testing & docs (1h)

---

## Day 8: Frontend Chat UI - Core Features (5-6 hours)
**Goal**: Build React chat interface (Part 6)

### Deliverables
- [ ] Chat message list with avatars & timestamps
- [ ] Message input with multiline support
- [ ] Send message on Enter (Shift+Enter for newline)
- [ ] Connect to backend `/chat` endpoint
- [ ] Display bot responses in real-time
- [ ] Basic styling (clean, minimal)

### Files to Create
```
frontend/src/
  components/
    ChatContainer.tsx        # Main chat component
    MessageList.tsx          # Message display
    MessageInput.tsx         # Input composer
    Message.tsx              # Single message
  services/
    chatApi.ts               # API client
  types/
    chat.ts                  # TypeScript interfaces
  App.tsx                    # Update with chat UI
  styles/
    chat.css                 # Basic styling
```

### Technologies to Understand
- React hooks (useState, useEffect)
- Async API calls in React
- Controlled form inputs

### Success Criteria
- Can send message and receive response
- Messages display with proper formatting
- UI is responsive and intuitive
- Works with backend memory (maintains context)

**Time Breakdown**: Component structure (2h) + API integration (1.5h) + Styling (1.5h) + Testing (1h)

---

## Day 9: Frontend - Advanced Features & Polish (4-5 hours)
**Goal**: Complete Part 6 requirements (localStorage, quick actions, live updates)

### Deliverables
- [ ] localStorage persistence (survives refresh)
- [ ] Quick actions: /calc, /products, /outlets, /reset
- [ ] Autocomplete for quick actions
- [ ] Multi-turn threading visualization
- [ ] Loading states and error display
- [ ] Mobile-responsive design

### Files to Create
```
frontend/src/
  components/
    QuickActions.tsx         # Action buttons/autocomplete
    LoadingIndicator.tsx     # Loading state
    ErrorMessage.tsx         # Error display
  hooks/
    useLocalStorage.ts       # Persist conversations
    useChat.ts               # Chat logic hook
  utils/
    commands.ts              # Parse quick actions
```

### Technologies to Understand
- localStorage API
- Command parsing patterns
- React loading states

### Success Criteria
- Conversation persists after refresh
- /calc triggers calculator flow
- /products and /outlets trigger respective APIs
- /reset clears conversation
- Loading indicators shown during API calls

**Time Breakdown**: localStorage (1h) + Quick actions (1.5h) + Polish (1.5h) + Testing (1h)

---

## Day 10: Testing, Deployment & Documentation (5-6 hours)
**Goal**: Final testing, deploy, complete documentation

### Deliverables
- [ ] Full end-to-end testing
- [ ] Backend deployed (Render/Railway)
- [ ] Frontend deployed (Vercel/Netlify)
- [ ] README updated with setup instructions
- [ ] Architecture diagrams/screenshots
- [ ] Final review and polish

### Files to Update/Create
```
README.md                    # Complete setup & architecture
docs/
  architecture.md            # System design overview
  deployment.md              # Deployment guide
tests/
  test_e2e.py                # End-to-end tests
.github/workflows/
  test.yml                   # CI pipeline (optional)
```

### Technologies to Understand
- Deployment platforms (Render, Vercel)
- Environment variables in production
- CORS configuration

### Success Criteria
- All tests passing (backend + frontend)
- Public URLs accessible
- README has clear setup instructions
- All 6 parts of assessment completed
- Repository clean (no secrets, well-organized)

**Time Breakdown**: Testing (2h) + Deployment (2h) + Documentation (1.5h) + Buffer (0.5h)

---

## Risk Mitigation

### High-Risk Items
1. **Vector store setup** (Day 5) - Fallback: Use simple keyword search if embedding issues
2. **Text2SQL accuracy** (Day 6) - Fallback: Few-shot prompting + strict schema
3. **Deployment complexity** (Day 10) - Start earlier if possible

### Buffer Strategy
- Days 1-3: Foundation work, should go smoothly
- Days 4-7: Core complexity, may need extra time
- Days 8-9: Frontend is more predictable
- Day 10: Built-in buffer for catching up

### Learning Resources
- **RAG**: LangChain docs on vector stores
- **Text2SQL**: GPT prompting examples, SQL injection patterns
- **Agentic Planning**: ReAct paper, LangChain agent docs
- **FastAPI**: Official tutorial (first 15 minutes)

---

## Daily Workflow

**Morning** (10 min):
1. Review `docs/progress.md` from previous day
2. Read today's milestone goals
3. Set up focus environment

**During Work**:
1. Follow milestone tasks in order
2. Update progress.md as you complete items
3. Ask questions when stuck for >30 min
4. Commit frequently with clear messages

**Evening** (10 min):
1. Update progress.md with:
   - What worked well
   - What was challenging
   - Tomorrow's focus
2. Commit and push changes

---

## Tech Stack Recommendations

### Backend
- **Framework**: FastAPI (fast, modern, great docs)
- **LLM**: OpenAI GPT-4 or GPT-3.5-turbo
- **Agent Framework**: LangChain (comprehensive toolkit)
- **Vector Store**: FAISS (simple, local, no API keys)
- **Database**: SQLite (zero setup, perfect for demo)
- **Testing**: pytest + httpx

### Frontend
- **Framework**: React + TypeScript (type safety)
- **Build Tool**: Vite (fast dev server)
- **Styling**: Plain CSS or Tailwind CSS
- **State**: React hooks (no Redux needed)
- **API Client**: fetch or axios

### Deployment
- **Backend**: Render (free tier, easy setup)
- **Frontend**: Vercel (zero-config React deployment)
- **Alternative**: Railway (both backend + frontend)

### Key Libraries
```txt
# Backend
fastapi==0.104.1
langchain==0.1.0
openai==1.3.0
faiss-cpu==1.7.4
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
beautifulsoup4==4.12.2
pytest==7.4.3

# Frontend
react==18.2.0
typescript==5.2.2
vite==5.0.0
```

---

## Success Metrics

By end of Day 10, you should have:
- ✅ Working chatbot with 3+ turn memory
- ✅ Agentic planning with tool selection
- ✅ Calculator, /products, /outlets APIs working
- ✅ Unhappy flows handled gracefully
- ✅ React UI with all required features
- ✅ Deployed and accessible via public URLs
- ✅ Complete documentation
- ✅ Test suite covering happy + unhappy paths

**This is achievable in 10 days with focused work (3-5 hours/day).**

