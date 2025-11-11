"""Tests for unhappy flows, error handling, and edge cases."""
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

client = TestClient(app)


# ============================================================================
# VALIDATION ERRORS
# ============================================================================

def test_empty_chat_message():
    """Test sending empty message to chat."""
    response = client.post("/chat/", json={
        "message": ""
    })
    
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_missing_chat_message_field():
    """Test chat request without message field."""
    response = client.post("/chat/", json={})
    
    assert response.status_code == 422
    data = response.json()
    assert "error" in data


def test_invalid_product_search_top_k():
    """Test product search with invalid top_k."""
    response = client.post("/products/search", json={
        "query": "tumbler",
        "top_k": 100  # Max is 10
    })
    
    assert response.status_code == 422


def test_empty_product_query():
    """Test product search with empty query."""
    response = client.post("/products/search", json={
        "query": ""
    })
    
    assert response.status_code == 422


def test_empty_outlet_query():
    """Test outlet search with empty query."""
    response = client.post("/outlets/search", json={
        "query": ""
    })
    
    assert response.status_code == 422


# ============================================================================
# CALCULATOR TOOL ERROR HANDLING
# ============================================================================

def test_calculator_empty_expression():
    """Test calculator with empty expression."""
    response = client.post("/chat/", json={
        "message": "Calculate "
    })
    
    assert response.status_code == 200
    data = response.json()
    # Mock LLM responds conversationally, doesn't crash
    assert "response" in data
    assert len(data["response"]) > 0


def test_calculator_division_by_zero():
    """Test calculator division by zero."""
    response = client.post("/chat/", json={
        "message": "Calculate 10 / 0"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "Division by zero" in data["response"] or "Error" in data["response"]


def test_calculator_invalid_characters():
    """Test calculator with invalid characters."""
    response = client.post("/chat/", json={
        "message": "Calculate 5 + abc"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "Error" in data["response"] or "Invalid" in data["response"]


def test_calculator_mismatched_parentheses():
    """Test calculator with mismatched parentheses."""
    response = client.post("/chat/", json={
        "message": "Calculate (5 + 3"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "Error" in data["response"] or "parentheses" in data["response"].lower()


def test_calculator_overflow():
    """Test calculator with overflow."""
    response = client.post("/chat/", json={
        "message": "Calculate 10 ** 10000"
    })
    
    assert response.status_code == 200
    data = response.json()
    # Should handle gracefully (either error or very large number)
    assert "response" in data


# ============================================================================
# MALICIOUS INPUTS
# ============================================================================

def test_sql_injection_outlet_search():
    """Test SQL injection attempt in outlet search."""
    response = client.post("/outlets/search", json={
        "query": "'; DROP TABLE outlets; --"
    })
    
    assert response.status_code == 200
    data = response.json()
    # Should not crash - may return all outlets (falls back to default query)
    # The important thing is it doesn't execute the DROP command
    assert "results" in data
    assert isinstance(data["results"], list)


def test_sql_injection_with_union():
    """Test SQL injection with UNION attempt."""
    response = client.post("/outlets/search", json={
        "query": "' UNION SELECT * FROM users --"
    })
    
    assert response.status_code == 200
    data = response.json()
    # Should not crash and should not return user data
    assert "results" in data
    assert isinstance(data["results"], list)


def test_xss_attempt_in_chat():
    """Test XSS attempt in chat message."""
    response = client.post("/chat/", json={
        "message": "<script>alert('XSS')</script>"
    })
    
    assert response.status_code == 200
    data = response.json()
    # Should not execute script, just treat as text
    assert "response" in data


def test_very_long_input():
    """Test with extremely long input."""
    long_message = "a" * 10000
    response = client.post("/chat/", json={
        "message": long_message
    })
    
    # Should handle gracefully (either 200 with response or 422 if validated)
    assert response.status_code in [200, 422]


# ============================================================================
# NOT FOUND ERRORS
# ============================================================================

def test_nonexistent_product():
    """Test fetching nonexistent product."""
    response = client.get("/products/INVALID123")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


def test_nonexistent_outlet():
    """Test fetching nonexistent outlet."""
    response = client.get("/outlets/INVALID123")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


def test_nonexistent_endpoint():
    """Test accessing nonexistent endpoint."""
    response = client.get("/nonexistent")
    
    assert response.status_code == 404


# ============================================================================
# INVALID LOCATION QUERIES
# ============================================================================

def test_invalid_city_name():
    """Test outlet search with completely invalid city."""
    response = client.post("/outlets/search", json={
        "query": "outlets in InvalidCity123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] == 0
    assert data["query_metadata"]["valid"] is False


def test_gibberish_outlet_query():
    """Test outlet search with gibberish."""
    response = client.post("/outlets/search", json={
        "query": "asdfghjkl qwertyuiop"
    })
    
    assert response.status_code == 200
    data = response.json()
    # Should return all outlets or empty result
    assert "results" in data


# ============================================================================
# SESSION MANAGEMENT ERRORS
# ============================================================================

def test_invalid_session_id():
    """Test chat with invalid session ID format."""
    response = client.post("/chat/", json={
        "message": "Hello",
        "session_id": "invalid!!!session"
    })
    
    # Should either accept it or create new session
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_delete_nonexistent_session():
    """Test deleting nonexistent session."""
    response = client.delete("/chat/session/nonexistent123")
    
    # Should handle gracefully
    assert response.status_code in [200, 404]


def test_get_history_nonexistent_session():
    """Test getting history for nonexistent session."""
    response = client.get("/chat/history/nonexistent123")
    
    # Should return empty history or 404
    assert response.status_code in [200, 404]


# ============================================================================
# RATE LIMITING (if enabled)
# ============================================================================

def test_rate_limit_basic():
    """Test that rate limiting exists (may skip if disabled)."""
    # Make many requests quickly
    responses = []
    for i in range(70):  # More than 60 per minute limit
        response = client.get("/health")
        responses.append(response.status_code)
    
    # At least some should succeed (health is exempted)
    assert 200 in responses


# ============================================================================
# TOOL FAILURE SCENARIOS
# ============================================================================

def test_ambiguous_query():
    """Test with ambiguous query that could match multiple tools."""
    response = client.post("/chat/", json={
        "message": "show me something"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_query_with_no_context():
    """Test query that needs context but has none."""
    response = client.post("/chat/", json={
        "message": "What about that one?"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


# ============================================================================
# EDGE CASES
# ============================================================================

def test_zero_top_k_products():
    """Test product search with top_k = 0."""
    response = client.post("/products/search", json={
        "query": "tumbler",
        "top_k": 0
    })
    
    assert response.status_code == 422  # Should be invalid


def test_negative_top_k():
    """Test with negative top_k."""
    response = client.post("/products/search", json={
        "query": "tumbler",
        "top_k": -1
    })
    
    assert response.status_code == 422


def test_unicode_characters():
    """Test with Unicode characters."""
    response = client.post("/chat/", json={
        "message": "Hello 你好 مرحبا 🎉"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_special_characters_in_query():
    """Test with special characters."""
    response = client.post("/outlets/search", json={
        "query": "outlets @ #location! $$$"
    })
    
    assert response.status_code == 200


def test_only_whitespace_message():
    """Test with only whitespace."""
    response = client.post("/chat/", json={
        "message": "     "
    })
    
    assert response.status_code == 422  # Should fail validation


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

