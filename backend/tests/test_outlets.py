"""Tests for outlet search and Text2SQL functionality."""
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

client = TestClient(app)


def test_outlet_search_by_city():
    """Test searching for outlets by city."""
    response = client.post("/outlets/search", json={
        "query": "Find outlets in Petaling Jaya"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["query"] == "Find outlets in Petaling Jaya"
    assert data["total_results"] > 0
    assert "sql_generated" in data
    assert "SELECT" in data["sql_generated"]
    
    # Check that results have required fields
    for result in data["results"]:
        assert "outlet_name" in result
        assert "address" in result
        assert "city" in result


def test_outlet_search_drive_thru():
    """Test searching for outlets with drive-through."""
    response = client.post("/outlets/search", json={
        "query": "Which outlets have drive-through?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_results"] > 0
    # All results should have drive_thru
    for result in data["results"]:
        assert result["has_drive_thru"] is True


def test_outlet_search_wifi():
    """Test searching for outlets with WiFi."""
    response = client.post("/outlets/search", json={
        "query": "outlets with WiFi"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # All results should have WiFi
    for result in data["results"]:
        assert result["has_wifi"] is True


def test_outlet_search_combined():
    """Test combined search (location + feature)."""
    response = client.post("/outlets/search", json={
        "query": "outlets in Selangor with WiFi"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have results in Selangor with WiFi
    for result in data["results"]:
        assert result["state"].lower() == "selangor" or result["city"].lower() == "selangor"
        assert result["has_wifi"] is True


def test_outlet_search_count():
    """Test count queries."""
    response = client.post("/outlets/search", json={
        "query": "How many outlets are there in Kuala Lumpur?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Count queries return total in metadata
    assert data["total_results"] >= 0
    assert data["query_metadata"]["query_type"] == "count"


def test_outlet_search_invalid_location():
    """Test searching for outlets in invalid location."""
    response = client.post("/outlets/search", json={
        "query": "outlets in InvalidCity123"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return 0 results for invalid location
    assert data["total_results"] == 0
    assert data["query_metadata"]["valid"] is False


def test_outlet_search_sql_injection():
    """Test that SQL injection is prevented."""
    response = client.post("/outlets/search", json={
        "query": "outlets in '; DROP TABLE outlets; --"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Should safely return 0 results
    assert data["total_results"] == 0


def test_get_all_outlets():
    """Test getting all outlets."""
    response = client.get("/outlets/")
    
    assert response.status_code == 200
    outlets = response.json()
    
    assert isinstance(outlets, list)
    assert len(outlets) == 25  # We have 25 outlets
    
    # Check structure
    for outlet in outlets:
        assert "outlet_id" in outlet
        assert "outlet_name" in outlet
        assert "address" in outlet
        assert "city" in outlet


def test_get_outlet_by_id():
    """Test getting a specific outlet by ID."""
    response = client.get("/outlets/OUT001")
    
    assert response.status_code == 200
    outlet = response.json()
    
    assert outlet["outlet_id"] == "OUT001"
    assert "outlet_name" in outlet
    assert "address" in outlet


def test_get_nonexistent_outlet():
    """Test getting an outlet that doesn't exist."""
    response = client.get("/outlets/INVALID")
    
    assert response.status_code == 404


def test_chat_with_outlet_query():
    """Test that chat endpoint works with outlet queries."""
    response = client.post("/chat/", json={
        "message": "Where are the outlets in Petaling Jaya?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "response" in data
    # Should mention outlets or locations
    response_text = data["response"].lower()
    assert any(word in response_text for word in ["outlet", "address", "petaling jaya", "found"])


def test_chat_mixed_outlet_and_product():
    """Test chat with both outlet and product queries."""
    # First, ask about outlets
    response1 = client.post("/chat/", json={
        "message": "Show me outlets in Kuala Lumpur"
    })
    
    assert response1.status_code == 200
    session_id = response1.json()["session_id"]
    
    # Then ask about products in same session
    response2 = client.post("/chat/", json={
        "message": "What tumblers do you have?",
        "session_id": session_id
    })
    
    assert response2.status_code == 200
    assert "tumbler" in response2.json()["response"].lower()


def test_outlet_tool_integration():
    """Test that OutletSearchTool integrates correctly."""
    from app.tools.outlet_search import OutletSearchTool
    
    tool = OutletSearchTool()
    
    assert tool.name == "outlet_search"
    assert "outlet" in tool.description.lower()
    
    # Test tool execution
    result = tool._run("outlets in Petaling Jaya")
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_outlet_search_operating_hours():
    """Test querying for operating hours."""
    response = client.post("/outlets/search", json={
        "query": "What are the operating hours for SS2 outlet?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return outlets matching SS2
    assert data["total_results"] >= 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

