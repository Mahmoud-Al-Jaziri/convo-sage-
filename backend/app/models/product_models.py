"""Pydantic models for product-related requests and responses."""
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductSearchRequest(BaseModel):
    """Request model for product search."""
    query: str = Field(..., description="Search query for products", min_length=1)
    top_k: int = Field(default=3, description="Number of results to return", ge=1, le=10)


class ProductResponse(BaseModel):
    """Response model for a single product."""
    id: str
    name: str
    category: str
    subcategory: str
    description: str
    price_myr: float
    capacity_ml: int
    material: str
    features: List[str]
    colors: List[str]
    in_stock: bool
    similarity_score: Optional[float] = None


class ProductSearchResponse(BaseModel):
    """Response model for product search results."""
    query: str
    results: List[ProductResponse]
    total_results: int

