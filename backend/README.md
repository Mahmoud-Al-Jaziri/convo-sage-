# ConvoSage Backend

FastAPI backend for the ConvoSage chatbot.

## Setup

1. **Create virtual environment**:
```bash
python -m venv venv
```

2. **Activate virtual environment**:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
- Edit `.env` file
- Add your OpenAI API key to `OPENAI_API_KEY`

5. **Run the server**:
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Or using Python directly
python -m app.main
```

6. **Verify it's running**:
- Open http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry
│   ├── config.py        # Settings & env vars
│   ├── api/             # API endpoints (coming soon)
│   ├── services/        # Business logic (coming soon)
│   ├── agents/          # LangChain agents (coming soon)
│   ├── tools/           # Custom tools (coming soon)
│   ├── models/          # Pydantic models (coming soon)
│   └── db/              # Database & vector store (coming soon)
├── tests/               # Tests (coming soon)
├── requirements.txt
└── .env
```

## Development

- API runs on http://localhost:8000
- Auto-reload enabled in DEBUG mode
- Interactive docs at `/docs`
- Alternative docs at `/redoc`

