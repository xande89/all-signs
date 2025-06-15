"""
Configuration management for the Zodiac AI Content System
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Database
    database_url: str = Field("sqlite:///./zodiac_content.db", env="DATABASE_URL")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # Social Media APIs
    instagram_app_id: Optional[str] = Field(None, env="INSTAGRAM_APP_ID")
    instagram_app_secret: Optional[str] = Field(None, env="INSTAGRAM_APP_SECRET")
    twitter_api_key: Optional[str] = Field(None, env="TWITTER_API_KEY")
    twitter_api_secret: Optional[str] = Field(None, env="TWITTER_API_SECRET")
    tiktok_client_key: Optional[str] = Field(None, env="TIKTOK_CLIENT_KEY")
    tiktok_client_secret: Optional[str] = Field(None, env="TIKTOK_CLIENT_SECRET")
    
    # Application Settings
    app_name: str = "Zodiac AI Content System"
    app_version: str = "1.0.0"
    debug: bool = Field(False, env="DEBUG")
    
    # Content Generation
    default_content_language: str = "en"
    max_content_length: int = 2000
    content_generation_timeout: int = 30  # seconds
    
    # Image Generation
    image_storage_path: str = "generated_images"
    max_image_size: int = 10 * 1024 * 1024  # 10MB
    supported_image_formats: list = ["PNG", "JPEG", "WEBP"]
    
    # Scheduling
    scheduler_timezone: str = "UTC"
    max_scheduled_posts_per_day: int = 50
    
    # Security
    secret_key: str = Field("your-secret-key-here", env="SECRET_KEY")
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(None, env="LOG_FILE")
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    # External Services
    webhook_url: Optional[str] = Field(None, env="WEBHOOK_URL")
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings (useful for testing)"""
    global _settings
    _settings = Settings()
    return _settings


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    database_url: str = "sqlite:///./dev_zodiac_content.db"


class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    log_level: str = "INFO"
    # Production database URL should be set via environment variable


class TestSettings(Settings):
    """Test environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    database_url: str = "sqlite:///./test_zodiac_content.db"
    openai_api_key: str = "test-key"


def get_settings_for_environment(env: str = None) -> Settings:
    """Get settings for specific environment"""
    if env is None:
        env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionSettings()
    elif env == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()


# Configuration validation
def validate_settings(settings: Settings) -> bool:
    """Validate critical settings"""
    required_fields = [
        "openai_api_key",
        "database_url",
        "secret_key"
    ]
    
    for field in required_fields:
        value = getattr(settings, field, None)
        if not value or value == "your-secret-key-here":
            print(f"Warning: {field} is not properly configured")
            return False
    
    return True


# Helper functions for common configurations
def get_database_config() -> dict:
    """Get database configuration"""
    settings = get_settings()
    return {
        "url": settings.database_url,
        "echo": settings.debug
    }


def get_redis_config() -> dict:
    """Get Redis configuration"""
    settings = get_settings()
    return {
        "url": settings.redis_url
    }


def get_ai_config() -> dict:
    """Get AI service configuration"""
    settings = get_settings()
    return {
        "openai_api_key": settings.openai_api_key,
        "anthropic_api_key": settings.anthropic_api_key,
        "timeout": settings.content_generation_timeout,
        "max_length": settings.max_content_length
    }


def get_social_media_config() -> dict:
    """Get social media API configuration"""
    settings = get_settings()
    return {
        "instagram": {
            "app_id": settings.instagram_app_id,
            "app_secret": settings.instagram_app_secret
        },
        "twitter": {
            "api_key": settings.twitter_api_key,
            "api_secret": settings.twitter_api_secret
        },
        "tiktok": {
            "client_key": settings.tiktok_client_key,
            "client_secret": settings.tiktok_client_secret
        }
    }


def get_image_config() -> dict:
    """Get image generation configuration"""
    settings = get_settings()
    return {
        "storage_path": settings.image_storage_path,
        "max_size": settings.max_image_size,
        "supported_formats": settings.supported_image_formats
    }


def get_scheduler_config() -> dict:
    """Get scheduler configuration"""
    settings = get_settings()
    return {
        "timezone": settings.scheduler_timezone,
        "max_posts_per_day": settings.max_scheduled_posts_per_day
    }


# Configuration for different deployment scenarios
DEPLOYMENT_CONFIGS = {
    "local": {
        "database_url": "sqlite:///./zodiac_content.db",
        "redis_url": "redis://localhost:6379",
        "debug": True
    },
    "docker": {
        "database_url": "postgresql://user:password@db:5432/zodiac_content",
        "redis_url": "redis://redis:6379",
        "debug": False
    },
    "kubernetes": {
        "database_url": "postgresql://user:password@postgres-service:5432/zodiac_content",
        "redis_url": "redis://redis-service:6379",
        "debug": False
    },
    "cloud": {
        # These would be set via environment variables in cloud deployment
        "debug": False
    }
}


def get_deployment_config(deployment_type: str) -> dict:
    """Get configuration for specific deployment type"""
    return DEPLOYMENT_CONFIGS.get(deployment_type, DEPLOYMENT_CONFIGS["local"])