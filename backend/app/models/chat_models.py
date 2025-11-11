"""Pydantic models for chat endpoints."""
from dataclasses import field
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User message"
    )
    
    @field_validator('message')
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        """Validate that message is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or contain only whitespace")
        return v.strip()
    session_id: Optional[str] = Field(
        None,
        description="Session ID for conversation tracking. If not provided, a new session will be created."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you?",
                "session_id": "user-123-session"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    response: str = Field(..., description="AI assistant response")
    session_id: str = Field(..., description="Session ID for this conversation")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
                "session_id": "user-123-session",
                "timestamp": "2025-11-04T10:30:00Z"
            }
        }


class ConversationHistory(BaseModel):
    """Model for conversation history."""
    
    session_id: str
    messages: list[dict]
    created_at: datetime
    updated_at: datetime

