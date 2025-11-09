"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A conversational AI chatbot with agentic planning, RAG, and Text2SQL capabilities",
    version="0.1.0",
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to ConvoSage API",
        "docs": "/docs",
        "health": "/health"
    }

# Import and include routers
from app.api import chat, products
app.include_router(chat.router)
app.include_router(products.router)

# Coming soon
# from app.api import outlets
# app.include_router(outlets.router)
# app.include_router(calculator.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

