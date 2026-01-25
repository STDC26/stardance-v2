"""
StarDance v2 Configuration
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    APP_TITLE: str = "StarDance Platform v2.0"
    APP_DESCRIPTION: str = "Multi-Agent Content Intelligence Platform"
    APP_VERSION: str = "2.0.0-dev"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./stardance_v2.db"
    )
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://stardance-preview.vercel.app",
        "https://stardance-preview-*.vercel.app",
    ]
    
    # Phase 2 Feature Flags
    ENABLE_VIDEO_GENERATION: bool = os.getenv("ENABLE_VIDEO_GENERATION", "false").lower() == "true"
    ENABLE_DISTRIBUTION: bool = os.getenv("ENABLE_DISTRIBUTION", "false").lower() == "true"
    ENABLE_ATTRIBUTION: bool = os.getenv("ENABLE_ATTRIBUTION", "false").lower() == "true"
    ENABLE_LEARNING: bool = os.getenv("ENABLE_LEARNING", "false").lower() == "true"
    ENABLE_REGENERATION: bool = os.getenv("ENABLE_REGENERATION", "false").lower() == "true"
    
    # Agent Configuration
    AGENT_TIMEOUT: int = 300  # seconds
    MAX_CONCURRENT_JOBS: int = 10
    
    # Video Generation
    RUNWAY_API_KEY: str = os.getenv("RUNWAY_API_KEY", "")
    PIKA_API_KEY: str = os.getenv("PIKA_API_KEY", "")
    STABILITY_API_KEY: str = os.getenv("STABILITY_API_KEY", "")
    
    # Platform APIs
    TIKTOK_ACCESS_TOKEN: str = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    INSTAGRAM_ACCESS_TOKEN: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
