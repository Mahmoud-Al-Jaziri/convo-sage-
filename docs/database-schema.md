# Database Schema

Database structure for ConvoSage.

---

## Overview

- **Database**: SQLite
- **Location**: `data/app.db`

---

## Tables

### Outlets Table (Coming Day 4)

```sql
CREATE TABLE outlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    hours TEXT,
    services TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: Store ZUS Coffee outlet information for Text2SQL queries

**Example Data**:
```sql
INSERT INTO outlets (name, location, city, state, hours) VALUES
('ZUS Coffee SS2', 'SS 2, Petaling Jaya', 'Petaling Jaya', 'Selangor', '9:00 AM - 10:00 PM'),
('ZUS Coffee KLCC', 'Suria KLCC', 'Kuala Lumpur', 'KL', '10:00 AM - 10:00 PM');
```

---

## Vector Store

### Products Index (Coming Day 5)

- **Type**: FAISS vector store
- **Location**: `data/vector_store/`
- **Embeddings**: OpenAI text-embedding-ada-002
- **Purpose**: Product search for RAG queries

**Indexed Data**: ZUS drinkware products (tumblers, bottles, mugs)

---

*Schema will be updated as we build*

