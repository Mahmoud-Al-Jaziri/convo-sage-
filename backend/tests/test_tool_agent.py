"""Tests for the tool agent with calculator."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.memory_store import memory_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_memory_before_each_test():
    """Clear all sessions before each test."""
    memory_store._sessions.clear()
    memory_store._session_metadata.clear()
    yield
    memory_store._sessions.clear()
    memory_store._session_metadata.clear()


def test_calculator_request():
    """Test that agent uses calculator for math requests."""
    response = client.post("/chat/", json={
        "message": "Calculate 5+3 for me"
    })
    assert response.status_code == 200
    data = response.json()
    assert "8" in data["response"]


def test_calculator_what_is():
    """Test calculator with 'what is' phrasing."""
    response = client.post("/chat/", json={
        "message": "What is 10*2?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "20" in data["response"]


def test_calculator_compute():
    """Test calculator with 'compute' keyword."""
    response = client.post("/chat/", json={
        "message": "Compute 15 + 7"
    })
    assert response.status_code == 200
    data = response.json()
    assert "22" in data["response"]


def test_calculator_complex_expression():
    """Test calculator with complex expression."""
    response = client.post("/chat/", json={
        "message": "Calculate (5+3)*2"
    })
    assert response.status_code == 200
    data = response.json()
    assert "16" in data["response"]


def test_normal_conversation_still_works():
    """Test that normal conversation (non-calculation) still works."""
    response = client.post("/chat/", json={
        "message": "Hello! My name is Bob."
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["response"]) > 0
    # Should not be a calculation result
    assert "result" not in data["response"].lower() or "Bob" in data["response"]


def test_mixed_conversation():
    """Test switching between conversation and calculation."""
    # Start with greeting
    response1 = client.post("/chat/", json={
        "message": "Hi there!"
    })
    session_id = response1.json()["session_id"]
    
    # Ask for calculation
    response2 = client.post("/chat/", json={
        "message": "Can you calculate 7+5?",
        "session_id": session_id
    })
    assert "12" in response2.json()["response"]
    
    # Back to conversation
    response3 = client.post("/chat/", json={
        "message": "Thanks!",
        "session_id": session_id
    })
    assert response3.status_code == 200


def test_calculator_error_handling():
    """Test calculator handles errors gracefully."""
    response = client.post("/chat/", json={
        "message": "Calculate 5/0"
    })
    assert response.status_code == 200
    data = response.json()
    assert "Error" in data["response"] or "zero" in data["response"].lower()


def test_agent_detects_inline_math():
    """Test agent detects math expressions inline."""
    response = client.post("/chat/", json={
        "message": "I need to know 15+20"
    })
    assert response.status_code == 200
    data = response.json()
    # Should calculate
    assert "35" in data["response"]


def test_no_calculation_without_math():
    """Test agent doesn't try to calculate when there's no math."""
    response = client.post("/chat/", json={
        "message": "What products does ZUS Coffee have?"
    })
    assert response.status_code == 200
    data = response.json()
    # Should respond about products, not calculation
    assert "Error" not in data["response"]
    assert len(data["response"]) > 0

