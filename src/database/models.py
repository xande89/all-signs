"""
Database models for the Zodiac AI Content System
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Date, 
    ForeignKey, DECIMAL, ARRAY, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class ZodiacSign(Base):
    __tablename__ = "zodiac_signs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    symbol = Column(String(10), nullable=False)
    element = Column(String(20), nullable=False)  # Fire, Earth, Air, Water
    modality = Column(String(20), nullable=False)  # Cardinal, Fixed, Mutable
    ruling_planet = Column(String(50))
    date_range_start = Column(Date, nullable=False)
    date_range_end = Column(Date, nullable=False)
    traits = Column(JSON)  # Personality traits and characteristics
    colors = Column(JSON)  # Brand colors for this sign
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    social_profiles = relationship("SocialProfile", back_populates="zodiac_sign")
    content_templates = relationship("ContentTemplate", back_populates="zodiac_sign")
    generated_content = relationship("GeneratedContent", back_populates="zodiac_sign")


class SocialProfile(Base):
    __tablename__ = "social_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    zodiac_sign_id = Column(Integer, ForeignKey("zodiac_signs.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # instagram, tiktok, twitter, etc.
    username = Column(String(100), nullable=False)
    profile_id = Column(String(100))  # Platform-specific ID
    access_token = Column(Text)  # Encrypted API access token
    refresh_token = Column(Text)  # Encrypted refresh token
    is_active = Column(Boolean, default=True)
    last_post_at = Column(DateTime(timezone=True))
    follower_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    zodiac_sign = relationship("ZodiacSign", back_populates="social_profiles")
    scheduled_posts = relationship("ScheduledPost", back_populates="profile")


class ContentTemplate(Base):
    __tablename__ = "content_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    content_type = Column(String(50), nullable=False)  # daily_horoscope, weekly_forecast, meme, etc.
    template_text = Column(Text, nullable=False)  # Template with placeholders
    platform = Column(String(50), nullable=False)
    zodiac_sign_id = Column(Integer, ForeignKey("zodiac_signs.id"))
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    zodiac_sign = relationship("ZodiacSign", back_populates="content_templates")


class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(Integer, primary_key=True, index=True)
    zodiac_sign_id = Column(Integer, ForeignKey("zodiac_signs.id"), nullable=False)
    content_type = Column(String(50), nullable=False)
    title = Column(String(200))
    text_content = Column(Text, nullable=False)
    image_url = Column(String(500))
    hashtags = Column(ARRAY(String))
    target_date = Column(Date)
    ai_model_used = Column(String(50))
    generation_prompt = Column(Text)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    zodiac_sign = relationship("ZodiacSign", back_populates="generated_content")
    scheduled_posts = relationship("ScheduledPost", back_populates="content")


class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("generated_content.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("social_profiles.id"), nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="pending")  # pending, published, failed, cancelled
    platform_post_id = Column(String(100))  # ID returned by social platform
    error_message = Column(Text)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    content = relationship("GeneratedContent", back_populates="scheduled_posts")
    profile = relationship("SocialProfile", back_populates="scheduled_posts")
    analytics = relationship("AnalyticsData", back_populates="post")


class AnalyticsData(Base):
    __tablename__ = "analytics_data"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("scheduled_posts.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    engagement_rate = Column(DECIMAL(5, 4))
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("ScheduledPost", back_populates="analytics")


# Pydantic models for API
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ZodiacSignBase(BaseModel):
    name: str
    symbol: str
    element: str
    modality: str
    ruling_planet: Optional[str] = None
    date_range_start: date
    date_range_end: date
    traits: Optional[Dict[str, Any]] = None
    colors: Optional[Dict[str, Any]] = None


class ZodiacSignCreate(ZodiacSignBase):
    pass


class ZodiacSignResponse(ZodiacSignBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SocialProfileBase(BaseModel):
    platform: str
    username: str
    profile_id: Optional[str] = None
    is_active: bool = True


class SocialProfileCreate(SocialProfileBase):
    zodiac_sign_id: int
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class SocialProfileResponse(SocialProfileBase):
    id: int
    zodiac_sign_id: int
    last_post_at: Optional[datetime] = None
    follower_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ContentTemplateBase(BaseModel):
    name: str
    content_type: str
    template_text: str
    platform: str
    is_active: bool = True


class ContentTemplateCreate(ContentTemplateBase):
    zodiac_sign_id: Optional[int] = None


class ContentTemplateResponse(ContentTemplateBase):
    id: int
    zodiac_sign_id: Optional[int] = None
    usage_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class GeneratedContentBase(BaseModel):
    content_type: str
    title: Optional[str] = None
    text_content: str
    image_url: Optional[str] = None
    hashtags: Optional[List[str]] = None
    target_date: Optional[date] = None
    ai_model_used: Optional[str] = None
    generation_prompt: Optional[str] = None
    is_approved: bool = False


class GeneratedContentCreate(GeneratedContentBase):
    zodiac_sign_id: int


class GeneratedContentResponse(GeneratedContentBase):
    id: int
    zodiac_sign_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ScheduledPostBase(BaseModel):
    scheduled_time: datetime
    status: str = "pending"


class ScheduledPostCreate(ScheduledPostBase):
    content_id: int
    profile_id: int


class ScheduledPostResponse(ScheduledPostBase):
    id: int
    content_id: int
    profile_id: int
    platform_post_id: Optional[str] = None
    error_message: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalyticsDataBase(BaseModel):
    platform: str
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    views_count: int = 0
    engagement_rate: Optional[float] = None
    reach: int = 0
    impressions: int = 0


class AnalyticsDataCreate(AnalyticsDataBase):
    post_id: int


class AnalyticsDataResponse(AnalyticsDataBase):
    id: int
    post_id: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True


class ContentGenerationRequest(BaseModel):
    zodiac_sign: str
    content_type: str
    target_date: Optional[date] = None
    platform: str = "instagram"
    style_preferences: Optional[Dict[str, Any]] = None


class ContentGenerationResponse(BaseModel):
    content_id: int
    text_content: str
    image_url: Optional[str] = None
    hashtags: List[str]
    generation_time: float
    ai_model_used: str