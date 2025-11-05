# Setup Guide - ConvoSage

Quick start guide to get the project running locally.

## Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 20.13+** (for frontend)
- **OpenAI API Key** (required for LLM functionality)

## Initial Setup

### 1. Clone and Navigate
```bash
cd convo-sage
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit backend/.env and add your OpenAI API key
```

**Important**: Add your OpenAI API key to `backend/.env`:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Dependencies are already installed from Day 1 setup
# If needed: npm install
```

## Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

Frontend will run on: **http://localhost:5173**

## Verify Installation

1. **Backend Health Check**:
   - Visit http://localhost:8000/health
   - Should see: `{"status": "healthy", "app_name": "ConvoSage", "version": "0.1.0"}`

2. **Frontend**:
   - Visit http://localhost:5173
   - Should see the ConvoSage landing page

3. **Run Tests**:
```bash
cd backend
pytest
```

## Project Structure

```
convo-sage/
├── backend/          # FastAPI server (Port 8000)
│   ├── app/
│   │   ├── main.py   # FastAPI entry point
│   │   └── config.py # Settings
│   ├── tests/        # Backend tests
│   └── .env          # Environment variables (add your API key here!)
├── frontend/         # React app (Port 5173)
│   └── src/
├── data/            # Data files (coming Day 4)
├── docs/            # Documentation
└── scripts/         # Utility scripts (coming Day 4)
```

## Troubleshooting

### Backend Issues

**Import errors?**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Port 8000 already in use?**
- Stop other processes or change port:
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```

**OpenAI API errors?**
- Check your API key in `backend/.env`
- Verify the key is valid at https://platform.openai.com/api-keys

### Frontend Issues

**Port 5173 already in use?**
- Vite will automatically use the next available port (5174, 5175, etc.)

**Module not found?**
- Run `npm install` in the frontend directory

**Node version warnings?**
- Non-blocking. Project should still work fine.

## Next Steps

Once both servers are running:
1. Review the [10-Day Milestone Plan](docs/milestone-plan.md)
2. Check [Backend Patterns](docs/backend-patterns.md) for coding conventions
3. Start Day 2: Implementing conversation memory and chat endpoint

## Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate          # Activate venv (Windows)
uvicorn app.main:app --reload  # Run server
pytest                         # Run tests
pip freeze > requirements.txt  # Update dependencies

# Frontend
cd frontend
npm run dev     # Development server
npm run build   # Production build
npm run preview # Preview production build

# Both
git status      # Check changes
git add .       # Stage changes
git commit -m "message"  # Commit
```

## Environment Variables

Edit `backend/.env`:
```env
OPENAI_API_KEY=sk-your-key-here  # REQUIRED
DATABASE_URL=sqlite:///./data/app.db
VECTOR_STORE_PATH=./data/vector_store
APP_NAME=ConvoSage
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
```

---

**Ready to code?** Start with Day 2 in the milestone plan! 🚀

