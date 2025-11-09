"""Script to ingest outlet data from CSV file into SQLite database."""
import csv
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import db


def ingest_outlets(csv_path: str):
    """
    Ingest outlets data from CSV file into database.
    
    Args:
        csv_path: Path to the CSV file containing outlet data
    """
    print(f"📥 Ingesting outlets from: {csv_path}")
    
    # Initialize database schema
    db.init_db()
    
    # Read and insert data
    inserted_count = 0
    updated_count = 0
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Convert string booleans to actual booleans
                row['has_drive_thru'] = row['has_drive_thru'].upper() == 'TRUE'
                row['has_wifi'] = row['has_wifi'].upper() == 'TRUE'
                
                # Check if outlet already exists
                cursor.execute(
                    "SELECT outlet_id FROM outlets WHERE outlet_id = ?",
                    (row['outlet_id'],)
                )
                exists = cursor.fetchone()
                
                if exists:
                    # Update existing record
                    cursor.execute("""
                        UPDATE outlets SET
                            outlet_name = ?,
                            address = ?,
                            city = ?,
                            state = ?,
                            postcode = ?,
                            latitude = ?,
                            longitude = ?,
                            phone = ?,
                            operating_hours = ?,
                            has_drive_thru = ?,
                            has_wifi = ?,
                            seating_capacity = ?,
                            opening_date = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE outlet_id = ?
                    """, (
                        row['outlet_name'],
                        row['address'],
                        row['city'],
                        row['state'],
                        row['postcode'],
                        row['latitude'],
                        row['longitude'],
                        row['phone'],
                        row['operating_hours'],
                        row['has_drive_thru'],
                        row['has_wifi'],
                        row['seating_capacity'],
                        row['opening_date'],
                        row['outlet_id']
                    ))
                    updated_count += 1
                else:
                    # Insert new record
                    cursor.execute("""
                        INSERT INTO outlets (
                            outlet_id, outlet_name, address, city, state, postcode,
                            latitude, longitude, phone, operating_hours,
                            has_drive_thru, has_wifi, seating_capacity, opening_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['outlet_id'],
                        row['outlet_name'],
                        row['address'],
                        row['city'],
                        row['state'],
                        row['postcode'],
                        row['latitude'],
                        row['longitude'],
                        row['phone'],
                        row['operating_hours'],
                        row['has_drive_thru'],
                        row['has_wifi'],
                        row['seating_capacity'],
                        row['opening_date']
                    ))
                    inserted_count += 1
    
    print(f"✅ Ingestion complete!")
    print(f"   - Inserted: {inserted_count} new outlets")
    print(f"   - Updated: {updated_count} existing outlets")
    print(f"   - Total in database: {db.get_table_count('outlets')}")


def main():
    """Main entry point for the script."""
    # Default path to CSV file
    csv_path = Path(__file__).parent.parent.parent / "data" / "outlets.csv"
    
    if not csv_path.exists():
        print(f"❌ Error: CSV file not found at {csv_path}")
        sys.exit(1)
    
    try:
        ingest_outlets(str(csv_path))
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

