# Database Schema

Database structure for ConvoSage.

---

## Overview

- **Database**: SQLite
- **Location**: `data/app.db`

---

## Tables

### Outlets Table ✅

```sql
CREATE TABLE outlets (
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
);

-- Indexes for faster queries
CREATE INDEX idx_outlets_city ON outlets(city);
CREATE INDEX idx_outlets_state ON outlets(state);
CREATE INDEX idx_outlets_drive_thru ON outlets(has_drive_thru);
```

**Purpose**: Store ZUS Coffee outlet information for Text2SQL queries

**Fields**:
- `outlet_id`: Unique identifier (e.g., OUT001)
- `outlet_name`: Full outlet name (e.g., "ZUS Coffee KLCC")
- `address`: Complete street address
- `city`: City name
- `state`: State/territory name
- `postcode`: Postal code
- `latitude`, `longitude`: GPS coordinates for mapping
- `phone`: Contact phone number
- `operating_hours`: Business hours (e.g., "Mon-Sun: 8:00 AM - 10:00 PM")
- `has_drive_thru`: Boolean flag for drive-through availability
- `has_wifi`: Boolean flag for WiFi availability
- `seating_capacity`: Number of seats available
- `opening_date`: Date outlet opened

**Current Data**: 25 ZUS Coffee outlets across Kuala Lumpur, Selangor, and Putrajaya

**Example Queries**:
```sql
-- Find outlets in Kuala Lumpur
SELECT * FROM outlets WHERE city = 'Kuala Lumpur';

-- Find drive-through outlets
SELECT outlet_name, address, city FROM outlets WHERE has_drive_thru = TRUE;

-- Find outlets by state with WiFi
SELECT outlet_name, address FROM outlets 
WHERE state = 'Selangor' AND has_wifi = TRUE;

-- Count outlets per city
SELECT city, COUNT(*) as total FROM outlets GROUP BY city;
```

---

## Vector Store

### Products Index

- **Type**: FAISS vector store
- **Location**: `data/vector_store/`
- **Embeddings**: TF-IDF based custom embedder
- **Purpose**: Product search for RAG queries

**Indexed Data**: ZUS drinkware products (tumblers, bottles, mugs)

