"""Application configuration and settings."""
from pydantic_settings import BaseSettings
from typing import List


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
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

