# API Specification

API endpoints for ConvoSage chatbot.

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: TBD

---

## Endpoints

### Health Check
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

### Root
```
GET /
```

**Description**: API information

**Response** (200 OK):
```json
{
  "message": "Welcome to ConvoSage API",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Coming Soon

- `POST /chat` - Chat endpoint with conversation memory
- `POST /calculator` - Calculator tool for arithmetic
- `GET /products` - Product search with RAG
- `GET /outlets` - Outlet queries with Text2SQL

---

*Last updated: Day 1*

