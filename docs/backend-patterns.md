# Backend Patterns & Conventions

This document defines how we structure our FastAPI backend. Follow these patterns for consistency.

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry, CORS, middleware
│   ├── config.py            # Settings, env vars (using pydantic BaseSettings)
│   ├── api/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── chat.py          # /chat endpoint
│   │   ├── products.py      # /products endpoint
│   │   ├── outlets.py       # /outlets endpoint
│   │   └── calculator.py    # /calculator endpoint
│   ├── services/            # Business logic (reusable)
│   │   ├── __init__.py
│   │   ├── product_service.py
│   │   ├── outlets_service.py
│   │   └── text2sql_service.py
│   ├── agents/              # LangChain agents & memory
│   │   ├── __init__.py
│   │   ├── conversation_agent.py
│   │   ├── planner.py
│   │   └── memory_store.py
│   ├── tools/               # LangChain custom tools
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   ├── products_tool.py
│   │   └── outlets_tool.py
│   ├── models/              # Pydantic models (request/response)
│   │   ├── __init__.py
│   │   └── chat_models.py
│   ├── db/                  # Database & vector store
│   │   ├── __init__.py
│   │   ├── database.py      # SQLite connection
│   │   └── vector_store.py  # FAISS wrapper
│   └── prompts/             # Prompt templates
│       └── text2sql_prompt.txt
├── tests/                   # All tests
│   ├── __init__.py
│   └── test_*.py
├── requirements.txt
└── .env.example
```

---

## Pattern 1: API Endpoint Structure

**Location**: `app/api/<feature>.py`

**Template**:
```python
from fastapi import APIRouter, HTTPException, Depends
from app.models.chat_models import RequestModel, ResponseModel
from app.services.feature_service import FeatureService

router = APIRouter(prefix="/feature", tags=["Feature"])

@router.post("/", response_model=ResponseModel)
async def feature_endpoint(request: RequestModel):
    """
    Brief description of what this endpoint does.
    
    Args:
        request: Description of input
        
    Returns:
        ResponseModel with expected data
        
    Raises:
        HTTPException: When something goes wrong
    """
    try:
        # 1. Validate input (Pydantic does this automatically)
        
        # 2. Call service layer
        service = FeatureService()
        result = await service.process(request.data)
        
        # 3. Return response
        return ResponseModel(result=result)
        
    except ValueError as e:
        # Handle expected errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Key Points**:
- Use `APIRouter` for modularity
- Type all inputs/outputs with Pydantic models
- Service layer handles business logic
- Endpoint handles HTTP concerns (status codes, errors)
- Always include docstrings

---

## Pattern 2: Service Layer

**Location**: `app/services/<feature>_service.py`

**Template**:
```python
from typing import Optional
from app.db.database import get_db_connection
from app.config import settings

class FeatureService:
    """Service for handling feature business logic."""
    
    def __init__(self):
        self.config = settings
    
    async def process(self, data: str) -> dict:
        """
        Main processing logic.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed result as dict
            
        Raises:
            ValueError: If input is invalid
        """
        # 1. Validate input (business rules)
        if not data:
            raise ValueError("Data cannot be empty")
        
        # 2. Perform core logic
        result = self._do_work(data)
        
        # 3. Return structured result
        return {"output": result}
    
    def _do_work(self, data: str) -> str:
        """Private helper method."""
        return data.upper()
```

**Key Points**:
- Pure business logic, no HTTP concerns
- Easy to test in isolation
- Can be reused by multiple endpoints or agents
- Private methods use `_` prefix

---

## Pattern 3: Pydantic Models

**Location**: `app/models/<feature>_models.py`

**Template**:
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Bot response")
    session_id: str = Field(..., description="Session ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Hello! How can I help?",
                "session_id": "abc123",
                "timestamp": "2025-11-04T10:00:00Z"
            }
        }
```

**Key Points**:
- Use `Field()` for validation and documentation
- Add examples for OpenAPI docs
- Validators for complex rules
- Clear descriptions for every field

---

## Pattern 4: LangChain Agent Setup

**Location**: `app/agents/<agent_name>.py`

**Template**:
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.tools.calculator import calculator_tool
from app.config import settings

class ConversationAgent:
    """Main conversation agent with memory."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = [calculator_tool]
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the ReAct agent with tools."""
        prompt = PromptTemplate.from_template(
            "You are a helpful assistant...\n{chat_history}\nUser: {input}\nAssistant:"
        )
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    
    async def process_message(self, message: str) -> str:
        """Process user message and return response."""
        result = await self.agent.ainvoke({"input": message})
        return result["output"]
```

**Key Points**:
- Session-based memory
- Tools list is easily extensible
- Use async methods for FastAPI compatibility
- Verbose mode for debugging

---

## Pattern 5: Custom LangChain Tools

**Location**: `app/tools/<tool_name>.py`

**Template**:
```python
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""
    expression: str = Field(..., description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    """Tool for performing calculations."""
    
    name: str = "calculator"
    description: str = "Useful for performing arithmetic calculations. Input should be a mathematical expression."
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """Execute the tool."""
        try:
            # Sanitize and evaluate
            result = eval(expression, {"__builtins__": {}}, {})
            return f"The result is {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """Async version."""
        return self._run(expression)

# Export instance
calculator_tool = CalculatorTool()
```

**Key Points**:
- Clear input schema with Pydantic
- Descriptive name and description (helps LLM choose tool)
- Error handling in tool itself
- Export instance for easy import

---

## Pattern 6: Configuration Management

**Location**: `app/config.py`

**Template**:
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API Keys
    OPENAI_API_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/app.db"
    
    # Vector Store
    VECTOR_STORE_PATH: str = "./data/vector_store"
    
    # App Config
    APP_NAME: str = "ConvoSage"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
```

**Key Points**:
- Use `pydantic-settings` for type-safe env vars
- Sensible defaults for development
- Single source of truth
- Import as `from app.config import settings`

---

## Pattern 7: Error Handling

**Global Error Handler** (in `main.py`):
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid input", "detail": str(exc)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the error (add logging later)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "Something went wrong"}
    )
```

**In Services**:
```python
# Raise specific exceptions
if not valid_input:
    raise ValueError("Input must be non-empty")

# Let unexpected errors bubble up
```

---

## Pattern 8: Testing

**Location**: `tests/test_<feature>.py`

**Template**:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoint_success():
    """Test successful case."""
    response = client.post("/chat", json={
        "message": "Hello",
        "session_id": "test-123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == "test-123"

def test_endpoint_missing_param():
    """Test missing required parameter."""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_service_logic():
    """Test service layer in isolation."""
    from app.services.feature_service import FeatureService
    
    service = FeatureService()
    result = await service.process("test")
    assert result["output"] == "TEST"
```

**Key Points**:
- Test both endpoints and services
- Cover happy and unhappy paths
- Use `TestClient` for API tests
- Mock external dependencies (LLM calls) when needed

---

## Quick Reference

### Adding a New API Endpoint
1. Create Pydantic models in `app/models/`
2. Create service in `app/services/`
3. Create endpoint in `app/api/`
4. Register router in `app/main.py`
5. Write tests in `tests/`

### Adding a New LangChain Tool
1. Create tool class in `app/tools/`
2. Define input schema with Pydantic
3. Implement `_run()` and `_arun()`
4. Add to agent's tools list
5. Test with agent

### Common Imports
```python
# FastAPI
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

# LangChain
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory

# Config
from app.config import settings
```

---

## Anti-Patterns (Avoid These)

❌ **Don't** put business logic in endpoints  
✅ **Do** put it in services

❌ **Don't** use raw strings for validation  
✅ **Do** use Pydantic models

❌ **Don't** hardcode API keys  
✅ **Do** use environment variables

❌ **Don't** return raw exceptions to users  
✅ **Do** convert to HTTPException with appropriate status codes

❌ **Don't** create circular imports  
✅ **Do** use proper layering (api → services → db)

---

*This document will be updated as we discover new patterns during development.*

