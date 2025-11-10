"""Outlet search tool using Text2SQL for natural language queries."""
from typing import Any, Dict, List, Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.text2sql.query_generator import get_text2sql_generator
from app.db.database import db


class OutletSearchInput(BaseModel):
    """Input for OutletSearchTool."""
    query: str = Field(description="natural language query for finding outlets (e.g., 'outlets in Petaling Jaya', 'outlets with drive-through')")


class OutletSearchTool(BaseTool):
    """
    A tool that searches for ZUS Coffee outlets using Text2SQL.
    Converts natural language to SQL queries and executes them safely.
    """
    name: str = "outlet_search"
    description: str = (
        "useful for finding ZUS Coffee outlet locations, operating hours, and amenities. "
        "Use this when users ask about outlet locations, cities, states, drive-through availability, WiFi, or operating hours."
    )
    args_schema: Type[BaseModel] = OutletSearchInput

    def _run(self, query: str) -> str:
        """
        Search for outlets using natural language query.
        
        Args:
            query: Natural language query string
            
        Returns:
            Formatted string with outlet information
        """
        try:
            # Generate SQL from natural language
            text2sql = get_text2sql_generator()
            sql, params, metadata = text2sql.generate_sql(query)
            
            # Execute query
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                results = cursor.fetchall()
            
            # Check if location was invalid
            if metadata.get("valid") is False:
                location = metadata.get("location", "that location")
                return f"I couldn't find '{location}' in our database. Please try cities like Kuala Lumpur, Petaling Jaya, Selangor, or Putrajaya."
            
            # Handle no results
            if not results:
                return self._format_no_results(metadata)
            
            # Format results based on query type
            if metadata["query_type"] == "count":
                count = results[0]["count"] if isinstance(results[0], dict) else results[0][0]
                location = metadata.get("location", "")
                return f"There are **{count} outlets** in {location}."
            
            return self._format_results(results, metadata)
            
        except Exception as e:
            print(f"Error in outlet search: {e}")
            return f"I encountered an error while searching for outlets: {str(e)}"

    def _format_no_results(self, metadata: Dict) -> str:
        """Format message for no results."""
        query_type = metadata.get("query_type")
        
        if query_type == "location":
            location = metadata.get("location", "that location")
            return f"I couldn't find any outlets in {location}. Try searching in Kuala Lumpur, Petaling Jaya, or Selangor."
        elif query_type == "drive_thru":
            return "I couldn't find any outlets with drive-through service."
        elif query_type == "wifi":
            return "I couldn't find any outlets with WiFi."
        elif query_type == "operating_hours":
            outlet = metadata.get("outlet_name", "that outlet")
            return f"I couldn't find operating hours for '{outlet}'. Try using the full outlet name or address."
        else:
            return "I couldn't find any outlets matching your query."
    
    def _format_results(self, results: List, metadata: Dict) -> str:
        """Format outlet results into a readable response."""
        query_type = metadata.get("query_type")
        
        # Handle operating hours specially
        if query_type == "operating_hours":
            response_parts = ["Here are the operating hours:\n"]
            for row in results[:3]:  # Limit to top 3 matches
                outlet_name = row["outlet_name"] if isinstance(row, dict) else row[1]
                city = row["city"] if isinstance(row, dict) else row[3]
                hours = row["operating_hours"] if isinstance(row, dict) else row[4]
                
                response_parts.append(f"\n**{outlet_name}** ({city})")
                response_parts.append(f"Hours: {hours}")
            
            return '\n'.join(response_parts)
        
        # Standard outlet listing
        location_info = ""
        if "location" in metadata:
            location_info = f" in {metadata['location']}"
        
        count = len(results)
        response_parts = [f"I found **{count} outlet{'s' if count != 1 else ''}**{location_info}:\n"]
        
        for idx, row in enumerate(results[:10], 1):  # Limit to 10 results
            # Handle both dict and tuple results
            if isinstance(row, dict):
                outlet_name = row["outlet_name"]
                address = row["address"]
                city = row["city"]
                state = row.get("state", "")
                phone = row.get("phone", "")
                hours = row.get("operating_hours", "")
                has_drive_thru = row.get("has_drive_thru", False)
                has_wifi = row.get("has_wifi", False)
            else:
                outlet_name = row[1]
                address = row[2]
                city = row[3]
                state = row[4] if len(row) > 4 else ""
                phone = row[5] if len(row) > 5 else ""
                hours = row[6] if len(row) > 6 else ""
                has_drive_thru = row[7] if len(row) > 7 else False
                has_wifi = row[8] if len(row) > 8 else False
            
            response_parts.append(f"\n{idx}. **{outlet_name}**")
            response_parts.append(f"   Address: {address}, {city}")
            
            if phone:
                response_parts.append(f"   Phone: {phone}")
            
            if hours:
                response_parts.append(f"   Hours: {hours}")
            
            # Add features
            features = []
            if has_drive_thru:
                features.append("Drive-Through")
            if has_wifi:
                features.append("WiFi")
            
            if features:
                response_parts.append(f"   Features: {', '.join(features)}")
        
        if count > 10:
            response_parts.append(f"\n... and {count - 10} more outlets.")
        
        return '\n'.join(response_parts)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)

