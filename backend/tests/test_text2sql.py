"""Tests for Text2SQL query generation."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.text2sql.query_generator import Text2SQLGenerator


def test_query_outlets_by_city():
    """Test generating SQL for city-based queries."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("Find outlets in Petaling Jaya")
    
    assert "SELECT" in sql
    assert "FROM outlets" in sql
    assert "WHERE" in sql.upper()
    assert "LOWER(city)" in sql or "city" in sql.lower()
    assert params == ['Petaling Jaya', 'Petaling Jaya']
    assert metadata["query_type"] == "location"
    assert metadata["location"] == "Petaling Jaya"
    assert metadata["valid"] is True


def test_query_outlets_by_state():
    """Test generating SQL for state-based queries."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("Show me outlets in Selangor")
    
    assert "SELECT" in sql
    assert params == ['Selangor', 'Selangor']
    assert metadata["query_type"] == "location"
    assert metadata["location"] == "Selangor"


def test_query_with_drive_thru():
    """Test generating SQL for drive-through queries."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("Which outlets have drive-through?")
    
    assert "SELECT" in sql
    assert "has_drive_thru" in sql
    assert "TRUE" in sql
    assert params == []
    assert metadata["query_type"] == "drive_thru"


def test_query_with_wifi():
    """Test generating SQL for WiFi queries."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets with WiFi")
    
    assert "SELECT" in sql
    assert "has_wifi" in sql
    assert "TRUE" in sql
    assert params == []
    assert metadata["query_type"] == "wifi"


def test_query_location_with_drive_thru():
    """Test combined location and drive-through query."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets in Selangor with drive-through")
    
    assert "SELECT" in sql
    assert "has_drive_thru" in sql
    assert "TRUE" in sql
    assert params == ['Selangor', 'Selangor']
    assert metadata["query_type"] == "location_drive_thru"


def test_query_location_with_wifi():
    """Test combined location and WiFi query."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets in Kuala Lumpur that have WiFi")
    
    assert "SELECT" in sql
    assert "has_wifi" in sql
    assert params == ['Kuala Lumpur', 'Kuala Lumpur']
    assert metadata["query_type"] == "location_wifi"


def test_query_count():
    """Test count queries."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("How many outlets are there in KL?")
    
    assert "COUNT" in sql.upper()
    assert params == ['Kuala Lumpur', 'Kuala Lumpur']  # KL alias
    assert metadata["query_type"] == "count"
    assert metadata["location"] == "Kuala Lumpur"


def test_query_operating_hours():
    """Test operating hours queries."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("What are the operating hours for SS2 outlet?")
    
    assert "SELECT" in sql
    assert "operating_hours" in sql
    assert "LIKE" in sql.upper()
    assert metadata["query_type"] == "operating_hours"
    assert "ss2" in metadata["outlet_name"].lower()


def test_query_all_outlets():
    """Test listing all outlets."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("show all outlets")
    
    assert "SELECT" in sql
    assert "FROM outlets" in sql
    assert params == []
    assert metadata["query_type"] == "all"


def test_city_alias_kl():
    """Test that 'KL' is recognized as Kuala Lumpur."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets in KL")
    
    assert params == ['Kuala Lumpur', 'Kuala Lumpur']
    assert metadata["location"] == "Kuala Lumpur"


def test_city_alias_pj():
    """Test that 'PJ' is recognized as Petaling Jaya."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets in PJ")
    
    assert params == ['Petaling Jaya', 'Petaling Jaya']
    assert metadata["location"] == "Petaling Jaya"


def test_sql_injection_prevention():
    """Test that SQL injection attempts are blocked."""
    generator = Text2SQLGenerator()
    
    # Try SQL injection
    sql, params, metadata = generator.generate_sql("outlets in '; DROP TABLE outlets; --")
    
    # Should return empty results due to validation
    assert metadata["valid"] is False
    assert "WHERE 1=0" in sql  # Returns no results


def test_invalid_location():
    """Test handling of invalid/unknown locations."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets in InvalidCity123")
    
    assert metadata["valid"] is False
    assert "WHERE 1=0" in sql  # Returns no results


def test_case_insensitive_matching():
    """Test that location matching is case-insensitive."""
    generator = Text2SQLGenerator()
    
    # Try different cases
    sql1, params1, meta1 = generator.generate_sql("outlets in KUALA LUMPUR")
    sql2, params2, meta2 = generator.generate_sql("outlets in kuala lumpur")
    sql3, params3, meta3 = generator.generate_sql("outlets in Kuala Lumpur")
    
    # All should be valid
    assert meta1["valid"] is True
    assert meta2["valid"] is True
    assert meta3["valid"] is True


def test_parameterized_queries():
    """Test that queries use parameters (not string interpolation)."""
    generator = Text2SQLGenerator()
    
    sql, params, metadata = generator.generate_sql("outlets in Petaling Jaya")
    
    # Should have ? placeholders
    assert "?" in sql
    # Should not have direct string interpolation
    assert "Petaling Jaya" not in sql
    # Parameters should be separate
    assert len(params) > 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

