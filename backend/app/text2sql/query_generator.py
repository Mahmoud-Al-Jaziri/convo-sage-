"""Pattern-based Text2SQL query generator for outlet queries.

This module converts natural language queries into safe SQL statements
for querying the outlets database.
"""
import re
from typing import Dict, List, Optional, Tuple


class Text2SQLGenerator:
    """
    Converts natural language queries to SQL for the outlets database.
    Uses pattern matching for reliability and safety.
    """
    
    # SQL injection prevention - whitelist of allowed values
    ALLOWED_CITIES = {
        'kuala lumpur', 'kl', 'petaling jaya', 'pj', 'subang jaya', 
        'shah alam', 'putrajaya', 'cyberjaya', 'george town', 'penang',
        'johor bahru', 'jb'
    }
    
    ALLOWED_STATES = {
        'selangor', 'kuala lumpur', 'kl', 'putrajaya', 'penang', 'johor'
    }
    
    CITY_ALIASES = {
        'kl': 'Kuala Lumpur',
        'pj': 'Petaling Jaya',
        'jb': 'Johor Bahru'
    }
    
    def __init__(self):
        """Initialize the Text2SQL generator."""
        self.query_patterns = [
            # Combined queries (must come BEFORE simple location queries)
            (r'outlets?\s+in\s+([a-z0-9\s\'\-;]+?)\s+with\s+drive[\s-]?thro?u?gh?', self._query_location_with_drive_thru),
            (r'outlets?\s+in\s+([a-z0-9\s\'\-;]+?)\s+(?:that\s+)?(?:have|has)\s+wifi', self._query_location_with_wifi),
            
            # Location-based queries (now allows more chars to catch invalid input)
            (r'outlets?\s+in\s+([a-z0-9\s\'\-;]+?)(?:\s*$)', self._query_by_location),
            (r'(?:find|show|list|get)\s+(?:me\s+)?(?:all\s+)?outlets?\s+in\s+([a-z0-9\s\'\-;]+)', self._query_by_location),
            (r'where\s+(?:are|is)\s+(?:the\s+)?outlets?\s+in\s+([a-z0-9\s\'\-;]+)', self._query_by_location),
            
            # Feature-based queries
            (r'(?:which|what)\s+outlets?\s+(?:have|has)\s+drive[\s-]?thro?u?gh?', self._query_with_drive_thru),
            (r'outlets?\s+with\s+drive[\s-]?thro?u?gh?', self._query_with_drive_thru),
            (r'drive[\s-]?thro?u?gh?\s+outlets?', self._query_with_drive_thru),
            (r'(?:which|what)\s+outlets?\s+(?:have|has)\s+wifi', self._query_with_wifi),
            (r'outlets?\s+with\s+wifi', self._query_with_wifi),
            (r'outlets?\s+(?:that\s+)?(?:have|has)\s+wifi', self._query_with_wifi),
            (r'wifi\s+outlets?', self._query_with_wifi),
            
            # Operating hours
            (r'(?:opening|operating)\s+hours?\s+(?:for|of)\s+(.+?)(?:\s+outlet)?$', self._query_operating_hours),
            (r'when\s+(?:does|is)\s+(.+?)\s+(?:outlet\s+)?open', self._query_operating_hours),
            
            # Count queries
            (r'how\s+many\s+outlets?\s+(?:are\s+)?(?:there\s+)?in\s+([a-z\s]+)', self._query_count_by_location),
            (r'count\s+outlets?\s+in\s+([a-z\s]+)', self._query_count_by_location),
            
            # All outlets
            (r'^(?:show|list|get)\s+(?:me\s+)?(?:all\s+)?outlets?$', self._query_all_outlets),
            (r'^all\s+outlets?$', self._query_all_outlets),
        ]
    
    def generate_sql(self, natural_query: str) -> Tuple[str, List[any], Dict[str, any]]:
        """
        Convert natural language query to SQL.
        
        Args:
            natural_query: Natural language query string
            
        Returns:
            Tuple of (sql_query, parameters, metadata)
            - sql_query: Parameterized SQL query string
            - parameters: List of parameters for the query
            - metadata: Additional info (query_type, location, etc.)
        """
        # Normalize query
        query = natural_query.lower().strip()
        
        # Try each pattern
        for pattern, handler in self.query_patterns:
            match = re.search(pattern, query)
            if match:
                sql, params, metadata = handler(match, query)
                # Ensure valid key exists (only if not explicitly set to False)
                if "valid" not in metadata:
                    metadata["valid"] = True
                return sql, params, metadata
        
        # Default: return all outlets (no pattern matched)
        return self._query_all_outlets(None, query)
    
    def _normalize_location(self, location: str) -> str:
        """Normalize location name (handle aliases, clean whitespace)."""
        location = location.strip().lower()
        
        # Check aliases
        if location in self.CITY_ALIASES:
            return self.CITY_ALIASES[location]
        
        # Title case for display
        return location.title()
    
    def _validate_location(self, location: str) -> bool:
        """Validate that location is in allowed list."""
        location_lower = location.lower().strip()
        return (location_lower in self.ALLOWED_CITIES or 
                location_lower in self.ALLOWED_STATES)
    
    def _query_by_location(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for location-based queries."""
        location = self._normalize_location(match.group(1))
        
        # Validate to prevent injection
        if not self._validate_location(location):
            # Return empty result for invalid locations
            return "SELECT * FROM outlets WHERE 1=0", [], {
                "query_type": "location",
                "location": location,
                "valid": False
            }
        
        sql = """
            SELECT outlet_id, outlet_name, address, city, state, phone, 
                   operating_hours, has_drive_thru, has_wifi
            FROM outlets 
            WHERE LOWER(city) = LOWER(?) OR LOWER(state) = LOWER(?)
            ORDER BY outlet_name
        """
        
        return sql, [location, location], {
            "query_type": "location",
            "location": location,
            "valid": True
        }
    
    def _query_with_drive_thru(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for drive-through queries."""
        sql = """
            SELECT outlet_id, outlet_name, address, city, state, phone, 
                   operating_hours, has_drive_thru, has_wifi
            FROM outlets 
            WHERE has_drive_thru = TRUE
            ORDER BY city, outlet_name
        """
        
        return sql, [], {"query_type": "drive_thru"}
    
    def _query_with_wifi(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for WiFi queries."""
        sql = """
            SELECT outlet_id, outlet_name, address, city, state, phone, 
                   operating_hours, has_drive_thru, has_wifi
            FROM outlets 
            WHERE has_wifi = TRUE
            ORDER BY city, outlet_name
        """
        
        return sql, [], {"query_type": "wifi"}
    
    def _query_location_with_drive_thru(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for location + drive-through queries."""
        location = self._normalize_location(match.group(1))
        
        if not self._validate_location(location):
            return "SELECT * FROM outlets WHERE 1=0", [], {
                "query_type": "location_drive_thru",
                "location": location,
                "valid": False
            }
        
        sql = """
            SELECT outlet_id, outlet_name, address, city, state, phone, 
                   operating_hours, has_drive_thru, has_wifi
            FROM outlets 
            WHERE (LOWER(city) = LOWER(?) OR LOWER(state) = LOWER(?))
              AND has_drive_thru = TRUE
            ORDER BY outlet_name
        """
        
        return sql, [location, location], {
            "query_type": "location_drive_thru",
            "location": location,
            "valid": True
        }
    
    def _query_location_with_wifi(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for location + WiFi queries."""
        location = self._normalize_location(match.group(1))
        
        if not self._validate_location(location):
            return "SELECT * FROM outlets WHERE 1=0", [], {
                "query_type": "location_wifi",
                "location": location,
                "valid": False
            }
        
        sql = """
            SELECT outlet_id, outlet_name, address, city, state, phone, 
                   operating_hours, has_drive_thru, has_wifi
            FROM outlets 
            WHERE (LOWER(city) = LOWER(?) OR LOWER(state) = LOWER(?))
              AND has_wifi = TRUE
            ORDER BY outlet_name
        """
        
        return sql, [location, location], {
            "query_type": "location_wifi",
            "location": location,
            "valid": True
        }
    
    def _query_operating_hours(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for operating hours queries."""
        outlet_name = match.group(1).strip()
        
        sql = """
            SELECT outlet_id, outlet_name, address, city, operating_hours
            FROM outlets 
            WHERE LOWER(outlet_name) LIKE LOWER(?)
               OR LOWER(address) LIKE LOWER(?)
            ORDER BY outlet_name
            LIMIT 5
        """
        
        search_pattern = f"%{outlet_name}%"
        
        return sql, [search_pattern, search_pattern], {
            "query_type": "operating_hours",
            "outlet_name": outlet_name
        }
    
    def _query_count_by_location(self, match: re.Match, query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for count queries."""
        location = self._normalize_location(match.group(1))
        
        if not self._validate_location(location):
            return "SELECT 0 as count", [], {
                "query_type": "count",
                "location": location,
                "valid": False
            }
        
        sql = """
            SELECT COUNT(*) as count
            FROM outlets 
            WHERE LOWER(city) = LOWER(?) OR LOWER(state) = LOWER(?)
        """
        
        return sql, [location, location], {
            "query_type": "count",
            "location": location,
            "valid": True
        }
    
    def _query_all_outlets(self, match: Optional[re.Match], query: str) -> Tuple[str, List, Dict]:
        """Generate SQL for listing all outlets."""
        sql = """
            SELECT outlet_id, outlet_name, address, city, state, phone, 
                   operating_hours, has_drive_thru, has_wifi
            FROM outlets 
            ORDER BY state, city, outlet_name
        """
        
        return sql, [], {"query_type": "all", "valid": True}


# Global instance
_generator = None

def get_text2sql_generator() -> Text2SQLGenerator:
    """Get the singleton Text2SQL generator instance."""
    global _generator
    if _generator is None:
        _generator = Text2SQLGenerator()
    return _generator


if __name__ == "__main__":
    # Test examples
    generator = Text2SQLGenerator()
    
    test_queries = [
        "Find outlets in Petaling Jaya",
        "Which outlets have drive-through?",
        "Show me outlets in Selangor with WiFi",
        "How many outlets are there in KL?",
        "What are the operating hours for SS2 outlet?",
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        sql, params, metadata = generator.generate_sql(query)
        print(f"SQL: {sql.strip()}")
        print(f"Params: {params}")
        print(f"Metadata: {metadata}")

