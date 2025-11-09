"""API endpoints for product search using RAG."""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.product_models import ProductSearchRequest, ProductSearchResponse, ProductResponse
from app.rag.simple_embedder import get_vector_store

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/search", response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest):
    """
    Search for products using natural language queries.
    
    This endpoint uses RAG (Retrieval Augmented Generation) to find
    relevant products based on semantic similarity.
    
    Example queries:
    - "stainless steel tumbler"
    - "large water bottle"
    - "glass cup for latte"
    - "travel mug with good insulation"
    """
    try:
        vector_store = get_vector_store()
        results = vector_store.search(request.query, top_k=request.top_k)
        
        # Convert to Pydantic models
        product_responses = [ProductResponse(**product) for product in results]
        
        return ProductSearchResponse(
            query=request.query,
            results=product_responses,
            total_results=len(product_responses)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")


@router.get("/", response_model=List[ProductResponse])
async def get_all_products():
    """
    Get all available products.
    
    Returns the complete product catalog.
    """
    try:
        vector_store = get_vector_store()
        products = vector_store.get_all_products()
        
        return [ProductResponse(**product, similarity_score=None) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: str):
    """
    Get a specific product by ID.
    
    Args:
        product_id: Product ID (e.g., 'DW001')
    """
    try:
        vector_store = get_vector_store()
        product = vector_store.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found")
        
        return ProductResponse(**product, similarity_score=None)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

