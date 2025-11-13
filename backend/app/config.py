"""Application configuration and settings."""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/app.db"
    
    # Vector Store
    VECTOR_STORE_PATH: str = "./data/vector_store"
    
    # Application
    APP_NAME: str = "ConvoSage"
    DEBUG: bool = True
    
    # CORS - Parse comma-separated origins
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,https://convo-sage.vercel.app"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Development - Use mock LLM instead of OpenAI
    USE_MOCK_LLM: bool = True  # Set to False when you have OpenAI credits
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        # Look for .env in backend directory
        env_file = Path(__file__).parent.parent / ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

