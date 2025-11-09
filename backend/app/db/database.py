"""Database connection and setup for SQLite."""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from app.config import settings


class Database:
    """
    SQLite database manager for ZUS Coffee outlets.
    Handles connection pooling and provides context managers for transactions.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file. Defaults to config setting.
        """
        self.db_path = db_path or settings.DATABASE_URL.replace("sqlite:///", "")
        # Ensure the database directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Automatically commits on success and rolls back on error.
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM outlets")
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_db(self):
        """
        Initialize database schema.
        Creates tables if they don't exist.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create outlets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS outlets (
                    outlet_id TEXT PRIMARY KEY,
                    outlet_name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    postcode TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    phone TEXT,
                    operating_hours TEXT,
                    has_drive_thru BOOLEAN DEFAULT FALSE,
                    has_wifi BOOLEAN DEFAULT FALSE,
                    seating_capacity INTEGER,
                    opening_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create index on city and state for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_outlets_city 
                ON outlets(city)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_outlets_state 
                ON outlets(state)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_outlets_drive_thru 
                ON outlets(has_drive_thru)
            """)

            print("✅ Database schema initialized successfully")

    def drop_all_tables(self):
        """
        Drop all tables. Use with caution!
        Useful for testing and development.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS outlets")
            print("⚠️  All tables dropped")

    def get_table_count(self, table_name: str) -> int:
        """
        Get the number of records in a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of records
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]


# Singleton instance
db = Database()

