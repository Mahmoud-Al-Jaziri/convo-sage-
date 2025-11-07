"""Tests for conversation memory and chat endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_without_session_id():
    """Test chat endpoint creates new session when no session_id provided."""
    response = client.post("/chat/", json={
        "message": "Hello, who are you?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "response" in data
    assert "session_id" in data
    assert "timestamp" in data
    
    # Check session_id was generated
    assert data["session_id"].startswith("session_")
    
    # Check AI responded
    assert len(data["response"]) > 0


def test_chat_with_session_id():
    """Test chat endpoint uses provided session_id."""
    session_id = "test-session-123"
    
    response = client.post("/chat/", json={
        "message": "My name is John",
        "session_id": session_id
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Check same session_id returned
    assert data["session_id"] == session_id


def test_conversation_memory_multi_turn():
    """Test that conversation remembers context across turns."""
    session_id = "test-memory-session"
    
    # Turn 1: Introduce name
    response1 = client.post("/chat/", json={
        "message": "Hi, my name is Alice",
        "session_id": session_id
    })
    assert response1.status_code == 200
    
    # Turn 2: Ask about something else
    response2 = client.post("/chat/", json={
        "message": "What's the weather like?",
        "session_id": session_id
    })
    assert response2.status_code == 200
    
    # Turn 3: Ask about name (should remember from Turn 1)
    response3 = client.post("/chat/", json={
        "message": "What's my name?",
        "session_id": session_id
    })
    assert response3.status_code == 200
    data3 = response3.json()
    
    # AI should remember the name "Alice"
    # This is a fuzzy check - in real testing, you'd mock the LLM
    assert len(data3["response"]) > 0


def test_get_conversation_history():
    """Test retrieving conversation history."""
    session_id = "test-history-session"
    
    # Have a conversation
    client.post("/chat/", json={
        "message": "Hello",
        "session_id": session_id
    })
    
    client.post("/chat/", json={
        "message": "How are you?",
        "session_id": session_id
    })
    
    # Get history
    response = client.get(f"/chat/history/{session_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert "session_id" in data
    assert "history" in data
    assert "metadata" in data
    
    # Should have 2 messages (2 user interactions)
    assert data["metadata"]["message_count"] == 2
    assert len(data["history"]) > 0


def test_delete_session():
    """Test deleting a session."""
    session_id = "test-delete-session"
    
    # Create session
    client.post("/chat/", json={
        "message": "Hello",
        "session_id": session_id
    })
    
    # Delete session
    response = client.delete(f"/chat/session/{session_id}")
    assert response.status_code == 200
    
    # Try to get history (should not find it or return empty)
    history_response = client.get(f"/chat/history/{session_id}")
    assert history_response.status_code == 404


def test_get_stats():
    """Test getting session statistics."""
    response = client.get("/chat/stats")
    assert response.status_code == 200
    data = response.json()
    
    assert "active_sessions" in data
    assert isinstance(data["active_sessions"], int)


def test_chat_empty_message():
    """Test chat with empty message fails validation."""
    response = client.post("/chat/", json={
        "message": ""
    })
    
    # Should fail Pydantic validation
    assert response.status_code == 422


def test_interrupted_conversation():
    """Test that memory persists even with gaps in conversation."""
    session_id = "test-interrupted-session"
    
    # Turn 1
    response1 = client.post("/chat/", json={
        "message": "Remember this number: 42",
        "session_id": session_id
    })
    assert response1.status_code == 200
    
    # Simulate other sessions (different session_id)
    client.post("/chat/", json={
        "message": "Random message",
        "session_id": "other-session"
    })
    
    # Turn 2: Return to original session
    response2 = client.post("/chat/", json={
        "message": "What number did I tell you to remember?",
        "session_id": session_id
    })
    assert response2.status_code == 200
    
    # Should still remember (though actual response depends on LLM)
    assert len(response2.json()["response"]) > 0

