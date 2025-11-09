"""Tests for product search and RAG functionality."""
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.rag.simple_embedder import get_vector_store

client = TestClient(app)


def test_product_search_tumbler():
    """Test searching for tumblers."""
    response = client.post("/products/search", json={
        "query": "tumbler",
        "top_k": 3
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["query"] == "tumbler"
    assert data["total_results"] > 0
    assert len(data["results"]) <= 3
    
    # Check that results have required fields
    first_result = data["results"][0]
    assert "name" in first_result
    assert "price_myr" in first_result
    assert "capacity_ml" in first_result
    assert "similarity_score" in first_result


def test_product_search_large_bottle():
    """Test searching for large bottles."""
    response = client.post("/products/search", json={
        "query": "large water bottle",
        "top_k": 2
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_results"] > 0
    # Should find bottles with larger capacity
    for result in data["results"]:
        assert result["capacity_ml"] >= 500


def test_product_search_glass():
    """Test searching for glass products."""
    response = client.post("/products/search", json={
        "query": "glass cup",
        "top_k": 3
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Should find glass products
    assert any("glass" in result["name"].lower() or "glass" in result["material"].lower() 
               for result in data["results"])


def test_get_all_products():
    """Test getting all products."""
    response = client.get("/products/")
    
    assert response.status_code == 200
    products = response.json()
    
    assert isinstance(products, list)
    assert len(products) == 8  # We have 8 products
    
    # Check structure
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "price_myr" in product


def test_get_product_by_id():
    """Test getting a specific product."""
    response = client.get("/products/DW001")
    
    assert response.status_code == 200
    product = response.json()
    
    assert product["id"] == "DW001"
    assert "name" in product
    assert "price_myr" in product


def test_get_nonexistent_product():
    """Test getting a product that doesn't exist."""
    response = client.get("/products/INVALID")
    
    assert response.status_code == 404


def test_product_search_invalid_top_k():
    """Test product search with invalid top_k."""
    response = client.post("/products/search", json={
        "query": "tumbler",
        "top_k": 20  # Max is 10
    })
    
    # Should be rejected by validation
    assert response.status_code == 422


def test_vector_store_initialization():
    """Test that vector store initializes correctly."""
    vs = get_vector_store()
    
    assert vs is not None
    assert len(vs.products) == 8
    assert len(vs.product_vectors) == 8


def test_vector_store_search():
    """Test vector store search functionality."""
    vs = get_vector_store()
    
    results = vs.search("stainless steel tumbler", top_k=2)
    
    assert len(results) <= 2
    assert all("similarity_score" in r for r in results)
    # Scores should be in descending order
    if len(results) > 1:
        assert results[0]["similarity_score"] >= results[1]["similarity_score"]


def test_chat_with_product_query():
    """Test that chat endpoint works with product queries."""
    response = client.post("/chat/", json={
        "message": "What tumblers do you have?"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "response" in data
    # Should mention products
    assert any(word in data["response"].lower() for word in ["tumbler", "product", "rm"])


def test_chat_mixed_queries():
    """Test chat with mixed calculator and product queries."""
    # First, ask about products
    response1 = client.post("/chat/", json={
        "message": "Show me water bottles"
    })
    
    assert response1.status_code == 200
    
    # Then do a calculation
    response2 = client.post("/chat/", json={
        "message": "what is 79 + 59",
        "session_id": response1.json()["session_id"]
    })
    
    assert response2.status_code == 200
    assert "138" in response2.json()["response"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

