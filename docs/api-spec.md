# API Specification

Complete API documentation for ConvoSage chatbot.

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: TBD

## Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "status": 400,
    "details": {
      // Optional additional information
    }
  }
}
```

### HTTP Status Codes
- `200 OK` - Success
- `422 Unprocessable Entity` - Validation error
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Unexpected error

### Error Codes
- `VALIDATION_ERROR` - Invalid input data
- `HTTP_404` - Resource not found
- `HTTP_429` - Rate limit exceeded
- `INTERNAL_ERROR` - Server error

---

## Rate Limiting

- **Limit**: 60 requests/minute, 1000 requests/hour per IP
- **Headers**: `X-RateLimit-Limit-Minute`, `X-RateLimit-Limit-Hour`
- **Exempt**: `/health` and `/` endpoints

---

## Endpoints

### 1. Health Check
```
GET /health
```

**Description**: Verify API is running

**Response** (200 OK):
```json
{
  "status": "healthy",
  "app_name": "ConvoSage",
  "version": "0.1.0"
}
```

---

### 2. Chat Endpoint
```
POST /chat/
```

**Description**: Send a message to the chatbot with conversation memory

**Request Body**:
```json
{
  "message": "Where are the outlets in KL?",
  "session_id": "optional-session-id"
}
```

**Parameters**:
- `message` (required, 1-2000 chars): User message
- `session_id` (optional): Session ID for conversation continuity

**Response** (200 OK):
```json
{
  "response": "I found 8 outlets in Kuala Lumpur...",
  "session_id": "abc123",
  "timestamp": "2025-11-10T10:30:00Z"
}
```

**Errors**:
- `422` - Empty or invalid message
- `500` - Internal error

---

### 3. Get Conversation History
```
GET /chat/history/{session_id}
```

**Description**: Retrieve conversation history for a session

**Response** (200 OK):
```json
{
  "history": [
    {"type": "human", "content": "Hello"},
    {"type": "ai", "content": "Hi! How can I help?"}
  ],
  "metadata": {
    "message_count": 2,
    "created_at": "2025-11-10T10:00:00Z"
  }
}
```

**Errors**:
- `404` - Session not found

---

### 4. Delete Session
```
DELETE /chat/session/{session_id}
```

**Description**: Delete a conversation session

**Response** (200 OK):
```json
{
  "message": "Session deleted successfully"
}
```

---

### 5. Product Search
```
POST /products/search
```

**Description**: Search for products using RAG

**Request Body**:
```json
{
  "query": "stainless steel tumbler",
  "top_k": 3
}
```

**Parameters**:
- `query` (required, min 1 char): Search query
- `top_k` (optional, default 3, max 10): Number of results

**Response** (200 OK):
```json
{
  "query": "stainless steel tumbler",
  "results": [
    {
      "id": "DRINK001",
      "name": "ZUS Classic Tumbler 350ml",
      "category": "Drinkware",
      "subcategory": "Tumbler",
      "price_myr": 59.00,
      "capacity_ml": 350,
      "material": "Stainless Steel",
      "description": "...",
      "features": ["Insulated", "Leak-proof"],
      "colors": ["Black", "White"],
      "in_stock": true
    }
  ],
  "total_results": 3
}
```

**Errors**:
- `422` - Invalid query or top_k

---

### 6. Get All Products
```
GET /products/
```

**Description**: Get complete product catalog

**Response** (200 OK):
```json
[
  {
    "id": "DRINK001",
    "name": "ZUS Classic Tumbler 350ml",
    // ... full product details
  }
]
```

---

### 7. Get Product by ID
```
GET /products/{product_id}
```

**Description**: Get a specific product

**Response** (200 OK):
```json
{
  "id": "DRINK001",
  "name": "ZUS Classic Tumbler 350ml",
  // ... full product details
}
```

**Errors**:
- `404` - Product not found

---

### 8. Outlet Search (Text2SQL)
```
POST /outlets/search
```

**Description**: Search for outlets using natural language

**Request Body**:
```json
{
  "query": "outlets in Kuala Lumpur with drive-through"
}
```

**Parameters**:
- `query` (required, min 1 char): Natural language query

**Supported Queries**:
- "Find outlets in [city]"
- "Which outlets have drive-through?"
- "Outlets in [state] with WiFi"
- "How many outlets are there in [city]?"
- "Operating hours for [outlet name]"

**Response** (200 OK):
```json
{
  "query": "outlets in Kuala Lumpur",
  "sql_generated": "SELECT ... FROM outlets WHERE city = ?",
  "results": [
    {
      "outlet_id": "OUT001",
      "outlet_name": "ZUS Coffee KLCC",
      "address": "...",
      "city": "Kuala Lumpur",
      "state": "KL",
      "postcode": "50088",
      "phone": "+60321819876",
      "operating_hours": "Mon-Sun: 10:00 AM - 10:00 PM",
      "has_drive_thru": false,
      "has_wifi": true,
      "seating_capacity": 50
    }
  ],
  "total_results": 8,
  "query_metadata": {
    "query_type": "location",
    "valid": true
  }
}
```

**Errors**:
- `422` - Invalid query

---

### 9. Get All Outlets
```
GET /outlets/
```

**Description**: Get complete outlet list

**Response** (200 OK):
```json
[
  {
    "outlet_id": "OUT001",
    "outlet_name": "ZUS Coffee KLCC",
    // ... full outlet details
  }
]
```

---

### 10. Get Outlet by ID
```
GET /outlets/{outlet_id}
```

**Description**: Get a specific outlet

**Response** (200 OK):
```json
{
  "outlet_id": "OUT001",
  "outlet_name": "ZUS Coffee KLCC",
  // ... full outlet details
}
```

**Errors**:
- `404` - Outlet not found

---

## Agent Capabilities

The chatbot intelligently routes queries to appropriate tools:

### Calculator
- Detects: "Calculate", "What is", math expressions
- Example: "Calculate 25 * 4" → "The result is 100"

### Product Search (RAG)
- Detects: "tumbler", "bottle", "cup", "product", "buy"
- Example: "Show me tumblers" → Returns product list

### Outlet Search (Text2SQL)
- Detects: "outlet", "location", "where", "city", "drive-through"
- Example: "Outlets in PJ" → Returns Petaling Jaya outlets

### Conversation
- Handles: Greetings, questions, general conversation
- Maintains: Memory across turns

---

## Examples

### Multi-Turn Conversation
```
User: "Hi, my name is Sarah"
Bot: "Hello Sarah! Nice to meet you..."

User: "What's my name?"
Bot: "Your name is Sarah!"
```

### Tool Chaining
```
User: "Show me outlets in KL"
Bot: "I found 8 outlets in Kuala Lumpur..."

User: "What tumblers do you have?"
Bot: "I found 3 tumblers..."

User: "Calculate the total if I buy 2 tumblers at RM59 each"
Bot: "The result of 2*59 is 118"
```

---

*Last updated: Day 7*
*106 tests passing | All features operational*
