"""
Main FastAPI application for the Zodiac AI Content System
"""
import os
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn

from .database.models import (
    ZodiacSignCreate, ZodiacSignResponse,
    ContentGenerationRequest, ContentGenerationResponse,
    GeneratedContentCreate, GeneratedContentResponse,
    ScheduledPostCreate, ScheduledPostResponse
)
from .database.database import get_db, init_db
from .content_generation.ai_generator import ZodiacContentGenerator
from .image_generation.image_generator import ZodiacImageGenerator
from .content_generation.content_service import ContentService
from .scheduling.scheduler import ContentScheduler
from .utils.config import get_settings

# Initialize FastAPI app
app = FastAPI(
    title="Zodiac AI Content System",
    description="Automated content generation and publishing for zodiac signs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
os.makedirs("generated_images", exist_ok=True)
app.mount("/images", StaticFiles(directory="generated_images"), name="images")

# Initialize services
settings = get_settings()
content_generator = ZodiacContentGenerator(settings.openai_api_key)
image_generator = ZodiacImageGenerator(settings.openai_api_key)
content_service = ContentService(content_generator, image_generator)
scheduler = ContentScheduler()

@app.on_event("startup")
async def startup_event():
    """Initialize database and start scheduler"""
    init_db()
    await scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await scheduler.stop()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Zodiac AI Content System",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "content_generator": "active",
            "image_generator": "active",
            "scheduler": "active" if scheduler.is_running else "inactive"
        }
    }

# Content Generation Endpoints

@app.post("/api/content/generate", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate content for a zodiac sign"""
    try:
        result = await content_service.generate_content(
            zodiac_sign=request.zodiac_sign,
            content_type=request.content_type,
            target_date=request.target_date or date.today(),
            platform=request.platform,
            style_preferences=request.style_preferences,
            db=db
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/content/generate-batch")
async def generate_batch_content(
    zodiac_signs: List[str],
    content_type: str,
    target_date: Optional[date] = None,
    platform: str = "instagram",
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """Generate content for multiple zodiac signs"""
    try:
        results = []
        target_date = target_date or date.today()
        
        for sign in zodiac_signs:
            # Add to background tasks for async processing
            background_tasks.add_task(
                content_service.generate_content,
                zodiac_sign=sign,
                content_type=content_type,
                target_date=target_date,
                platform=platform,
                db=db
            )
            
        return {
            "message": f"Batch content generation started for {len(zodiac_signs)} signs",
            "zodiac_signs": zodiac_signs,
            "content_type": content_type,
            "target_date": target_date,
            "platform": platform
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/content/{content_id}", response_model=GeneratedContentResponse)
async def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get generated content by ID"""
    content = content_service.get_content_by_id(content_id, db)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@app.get("/api/content/sign/{zodiac_sign}")
async def get_content_by_sign(
    zodiac_sign: str,
    content_type: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get content for a specific zodiac sign"""
    try:
        content = content_service.get_content_by_sign(
            zodiac_sign=zodiac_sign,
            content_type=content_type,
            limit=limit,
            db=db
        )
        return content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scheduling Endpoints

@app.post("/api/schedule/post", response_model=ScheduledPostResponse)
async def schedule_post(
    request: ScheduledPostCreate,
    db: Session = Depends(get_db)
):
    """Schedule a post for publishing"""
    try:
        scheduled_post = await scheduler.schedule_post(
            content_id=request.content_id,
            profile_id=request.profile_id,
            scheduled_time=request.scheduled_time,
            db=db
        )
        
        return scheduled_post
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schedule/daily-batch")
async def schedule_daily_batch(
    target_date: date,
    zodiac_signs: Optional[List[str]] = None,
    platforms: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Schedule daily content for all or specified zodiac signs"""
    try:
        if not zodiac_signs:
            zodiac_signs = [
                "aries", "taurus", "gemini", "cancer", "leo", "virgo",
                "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
            ]
        
        if not platforms:
            platforms = ["instagram", "twitter", "tiktok"]
        
        results = await scheduler.schedule_daily_content(
            target_date=target_date,
            zodiac_signs=zodiac_signs,
            platforms=platforms,
            db=db
        )
        
        return {
            "message": "Daily content scheduled successfully",
            "target_date": target_date,
            "scheduled_posts": len(results),
            "zodiac_signs": zodiac_signs,
            "platforms": platforms
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/schedule/upcoming")
async def get_upcoming_posts(
    days: int = 7,
    zodiac_sign: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get upcoming scheduled posts"""
    try:
        posts = scheduler.get_upcoming_posts(
            days=days,
            zodiac_sign=zodiac_sign,
            platform=platform,
            db=db
        )
        
        return {
            "upcoming_posts": posts,
            "count": len(posts),
            "days": days
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics Endpoints

@app.get("/api/analytics/overview")
async def get_analytics_overview(
    zodiac_sign: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get analytics overview"""
    try:
        # This would be implemented in an analytics service
        return {
            "message": "Analytics overview",
            "zodiac_sign": zodiac_sign,
            "days": days,
            "metrics": {
                "total_posts": 0,
                "total_engagement": 0,
                "avg_engagement_rate": 0.0,
                "top_performing_content": []
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Zodiac Signs Management

@app.get("/api/zodiac-signs", response_model=List[ZodiacSignResponse])
async def get_zodiac_signs(db: Session = Depends(get_db)):
    """Get all zodiac signs"""
    return content_service.get_all_zodiac_signs(db)

@app.post("/api/zodiac-signs", response_model=ZodiacSignResponse)
async def create_zodiac_sign(
    zodiac_sign: ZodiacSignCreate,
    db: Session = Depends(get_db)
):
    """Create a new zodiac sign"""
    return content_service.create_zodiac_sign(zodiac_sign, db)

# Content Templates

@app.get("/api/templates/{zodiac_sign}")
async def get_templates(
    zodiac_sign: str,
    content_type: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get content templates for a zodiac sign"""
    try:
        templates = content_service.get_templates(
            zodiac_sign=zodiac_sign,
            content_type=content_type,
            platform=platform,
            db=db
        )
        
        return {
            "templates": templates,
            "count": len(templates),
            "zodiac_sign": zodiac_sign
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image Generation

@app.post("/api/images/generate")
async def generate_image(
    zodiac_sign: str,
    content_type: str,
    text_content: str,
    platform: str = "instagram",
    target_date: Optional[date] = None
):
    """Generate an image for content"""
    try:
        if content_type == "daily_horoscope":
            image_path = await image_generator.generate_daily_horoscope_image(
                zodiac_sign=zodiac_sign,
                horoscope_text=text_content,
                target_date=target_date or date.today(),
                platform=platform
            )
        elif content_type == "motivational":
            image_path = await image_generator.generate_motivational_image(
                zodiac_sign=zodiac_sign,
                motivational_text=text_content,
                platform=platform
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported content type: {content_type}")
        
        # Return relative path for API access
        relative_path = image_path.replace("generated_images/", "")
        
        return {
            "image_path": f"/images/{relative_path}",
            "full_path": image_path,
            "zodiac_sign": zodiac_sign,
            "content_type": content_type,
            "platform": platform
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System Management

@app.post("/api/system/initialize")
async def initialize_system(db: Session = Depends(get_db)):
    """Initialize the system with default data"""
    try:
        # Initialize zodiac signs
        zodiac_signs_data = [
            {
                "name": "aries",
                "symbol": "♈",
                "element": "Fire",
                "modality": "Cardinal",
                "ruling_planet": "Mars",
                "date_range_start": date(2024, 3, 21),
                "date_range_end": date(2024, 4, 19),
                "traits": {
                    "positive": ["bold", "energetic", "pioneering", "confident"],
                    "challenges": ["impatience", "aggression", "selfishness"]
                },
                "colors": {
                    "primary": "#E74C3C",
                    "secondary": "#FF6B35",
                    "accent": "#FFD700"
                }
            }
            # Add other zodiac signs...
        ]
        
        for sign_data in zodiac_signs_data:
            content_service.create_zodiac_sign(ZodiacSignCreate(**sign_data), db)
        
        return {
            "message": "System initialized successfully",
            "zodiac_signs_created": len(zodiac_signs_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )