"""API endpoints for outlet search using Text2SQL."""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.outlet_models import OutletSearchRequest, OutletSearchResponse, OutletResponse
from app.text2sql.query_generator import get_text2sql_generator
from app.db.database import db

router = APIRouter(prefix="/outlets", tags=["Outlets"])


@router.post("/search", response_model=OutletSearchResponse)
async def search_outlets(request: OutletSearchRequest):
    """
    Search for outlets using natural language queries.
    
    This endpoint uses Text2SQL to convert natural language to SQL,
    then safely executes the query and returns formatted results.
    
    Example queries:
    - "Find outlets in Petaling Jaya"
    - "Which outlets have drive-through?"
    - "Show me outlets in Selangor with WiFi"
    - "How many outlets are there in KL?"
    - "What are the operating hours for SS2 outlet?"
    """
    try:
        # Generate SQL from natural language
        text2sql = get_text2sql_generator()
        sql, params, metadata = text2sql.generate_sql(request.query)
        
        # Execute query
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
        
        # Convert to Pydantic models
        outlet_responses = []
        for row in results:
            # Handle both dict and tuple results
            if isinstance(row, dict):
                outlet_responses.append(OutletResponse(**row))
            else:
                # For count queries, handle differently
                if metadata.get("query_type") == "count":
                    # Return empty list with metadata
                    count = row[0]
                    return OutletSearchResponse(
                        query=request.query,
                        sql_generated=sql.strip(),
                        results=[],
                        total_results=count,
                        query_metadata=metadata
                    )
                
                # For other queries, map tuple to OutletResponse
                outlet_responses.append(OutletResponse(
                    outlet_id=row[0] if len(row) > 0 else "",
                    outlet_name=row[1] if len(row) > 1 else "",
                    address=row[2] if len(row) > 2 else "",
                    city=row[3] if len(row) > 3 else "",
                    state=row[4] if len(row) > 4 else "",
                    postcode="",  # Not in select
                    phone=row[5] if len(row) > 5 else None,
                    operating_hours=row[6] if len(row) > 6 else None,
                    has_drive_thru=bool(row[7]) if len(row) > 7 else False,
                    has_wifi=bool(row[8]) if len(row) > 8 else False,
                ))
        
        return OutletSearchResponse(
            query=request.query,
            sql_generated=sql.strip(),
            results=outlet_responses,
            total_results=len(outlet_responses),
            query_metadata=metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching outlets: {str(e)}")


@router.get("/", response_model=List[OutletResponse])
async def get_all_outlets():
    """
    Get all available outlets.
    
    Returns the complete outlet catalog with all details.
    """
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT outlet_id, outlet_name, address, city, state, postcode,
                       latitude, longitude, phone, operating_hours,
                       has_drive_thru, has_wifi, seating_capacity, opening_date
                FROM outlets
                ORDER BY state, city, outlet_name
            """)
            results = cursor.fetchall()
        
        outlets = []
        for row in results:
            if isinstance(row, dict):
                outlets.append(OutletResponse(**row))
            else:
                outlets.append(OutletResponse(
                    outlet_id=row[0],
                    outlet_name=row[1],
                    address=row[2],
                    city=row[3],
                    state=row[4],
                    postcode=row[5],
                    latitude=row[6],
                    longitude=row[7],
                    phone=row[8],
                    operating_hours=row[9],
                    has_drive_thru=bool(row[10]),
                    has_wifi=bool(row[11]),
                    seating_capacity=row[12],
                    opening_date=row[13]
                ))
        
        return outlets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching outlets: {str(e)}")


@router.get("/{outlet_id}", response_model=OutletResponse)
async def get_outlet_by_id(outlet_id: str):
    """
    Get a specific outlet by ID.
    
    Args:
        outlet_id: Outlet ID (e.g., 'OUT001')
    """
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT outlet_id, outlet_name, address, city, state, postcode,
                       latitude, longitude, phone, operating_hours,
                       has_drive_thru, has_wifi, seating_capacity, opening_date
                FROM outlets
                WHERE outlet_id = ?
            """, (outlet_id,))
            row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Outlet with ID '{outlet_id}' not found")
        
        if isinstance(row, dict):
            return OutletResponse(**row)
        else:
            return OutletResponse(
                outlet_id=row[0],
                outlet_name=row[1],
                address=row[2],
                city=row[3],
                state=row[4],
                postcode=row[5],
                latitude=row[6],
                longitude=row[7],
                phone=row[8],
                operating_hours=row[9],
                has_drive_thru=bool(row[10]),
                has_wifi=bool(row[11]),
                seating_capacity=row[12],
                opening_date=row[13]
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching outlet: {str(e)}")

