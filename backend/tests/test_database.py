"""Tests for database operations."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import db


def test_database_connection():
    """Test database connection."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1


def test_outlets_table_exists():
    """Test that outlets table exists."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='outlets'
        """)
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == "outlets"


def test_outlets_data_loaded():
    """Test that outlets data is loaded."""
    count = db.get_table_count("outlets")
    assert count > 0, "Outlets table should have data"
    print(f"✅ Found {count} outlets in database")


def test_query_outlets_by_city():
    """Test querying outlets by city."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT outlet_id, outlet_name, city 
            FROM outlets 
            WHERE city = 'Kuala Lumpur'
        """)
        results = cursor.fetchall()
        assert len(results) > 0, "Should find outlets in Kuala Lumpur"
        print(f"✅ Found {len(results)} outlets in Kuala Lumpur")


def test_query_drive_thru_outlets():
    """Test querying drive-through outlets."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT outlet_id, outlet_name 
            FROM outlets 
            WHERE has_drive_thru = TRUE
        """)
        results = cursor.fetchall()
        print(f"✅ Found {len(results)} drive-through outlets")
        # Should have at least one drive-through
        assert len(results) > 0


def test_outlets_schema():
    """Test that outlets table has correct columns."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(outlets)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        required_columns = [
            'outlet_id', 'outlet_name', 'address', 'city', 'state',
            'postcode', 'latitude', 'longitude', 'phone', 'operating_hours',
            'has_drive_thru', 'has_wifi', 'seating_capacity', 'opening_date'
        ]
        
        for col in required_columns:
            assert col in column_names, f"Column '{col}' should exist in outlets table"
        
        print(f"✅ All {len(required_columns)} required columns present")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

