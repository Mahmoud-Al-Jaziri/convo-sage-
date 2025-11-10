"""Pydantic models for outlet-related requests and responses."""
from typing import List, Optional
from pydantic import BaseModel, Field


class OutletSearchRequest(BaseModel):
    """Request model for outlet search using natural language."""
    query: str = Field(..., description="Natural language query for outlets", min_length=1)


class OutletResponse(BaseModel):
    """Response model for a single outlet."""
    outlet_id: str
    outlet_name: str
    address: str
    city: str
    state: str
    postcode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    operating_hours: Optional[str] = None
    has_drive_thru: bool = False
    has_wifi: bool = False
    seating_capacity: Optional[int] = None
    opening_date: Optional[str] = None


class OutletSearchResponse(BaseModel):
    """Response model for outlet search results."""
    query: str
    sql_generated: Optional[str] = None  # For debugging/transparency
    results: List[OutletResponse]
    total_results: int
    query_metadata: Optional[dict] = None

