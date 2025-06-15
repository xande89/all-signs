"""
Content service for managing content generation and storage
"""
import time
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database.models import (
    ZodiacSign, GeneratedContent, ContentTemplate,
    ZodiacSignCreate, ZodiacSignResponse,
    GeneratedContentCreate, GeneratedContentResponse,
    ContentGenerationResponse
)
from .ai_generator import ZodiacContentGenerator
from ..image_generation.image_generator import ZodiacImageGenerator


class ContentService:
    """Service for managing content generation and storage"""
    
    def __init__(self, content_generator: ZodiacContentGenerator, image_generator: ZodiacImageGenerator):
        self.content_generator = content_generator
        self.image_generator = image_generator
    
    async def generate_content(
        self,
        zodiac_sign: str,
        content_type: str,
        target_date: date,
        platform: str = "instagram",
        style_preferences: Optional[Dict[str, Any]] = None,
        db: Session = None
    ) -> ContentGenerationResponse:
        """Generate content and save to database"""
        
        start_time = time.time()
        
        # Get zodiac sign from database
        zodiac_sign_obj = db.query(ZodiacSign).filter(
            ZodiacSign.name == zodiac_sign.lower()
        ).first()
        
        if not zodiac_sign_obj:
            raise ValueError(f"Zodiac sign '{zodiac_sign}' not found in database")
        
        # Generate text content based on type
        if content_type == "daily_horoscope":
            content_result = await self.content_generator.generate_daily_horoscope(
                zodiac_sign=zodiac_sign,
                target_date=target_date,
                platform=platform,
                style_preferences=style_preferences
            )
        elif content_type == "weekly_forecast":
            content_result = await self.content_generator.generate_weekly_forecast(
                zodiac_sign=zodiac_sign,
                start_date=target_date,
                platform=platform,
                style_preferences=style_preferences
            )
        elif content_type == "motivational":
            content_result = await self.content_generator.generate_motivational_content(
                zodiac_sign=zodiac_sign,
                platform=platform,
                style_preferences=style_preferences
            )
        elif content_type == "compatibility":
            content_result = await self.content_generator.generate_compatibility_content(
                zodiac_sign=zodiac_sign,
                platform=platform,
                style_preferences=style_preferences
            )
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        # Generate image
        image_url = None
        try:
            if content_type == "daily_horoscope":
                image_path = await self.image_generator.generate_daily_horoscope_image(
                    zodiac_sign=zodiac_sign,
                    horoscope_text=content_result["text_content"],
                    target_date=target_date,
                    platform=platform
                )
            elif content_type == "weekly_forecast":
                image_path = await self.image_generator.generate_weekly_forecast_image(
                    zodiac_sign=zodiac_sign,
                    forecast_text=content_result["text_content"],
                    start_date=target_date,
                    platform=platform
                )
            elif content_type == "motivational":
                image_path = await self.image_generator.generate_motivational_image(
                    zodiac_sign=zodiac_sign,
                    motivational_text=content_result["text_content"],
                    platform=platform
                )
            else:
                image_path = None
            
            if image_path:
                # Convert to relative URL
                image_url = f"/images/{image_path.replace('generated_images/', '')}"
                
        except Exception as e:
            print(f"Failed to generate image: {e}")
            # Continue without image
        
        # Save to database
        generated_content = GeneratedContent(
            zodiac_sign_id=zodiac_sign_obj.id,
            content_type=content_type,
            text_content=content_result["text_content"],
            image_url=image_url,
            hashtags=content_result["hashtags"],
            target_date=target_date,
            ai_model_used=content_result["ai_model_used"],
            generation_prompt=content_result["generation_prompt"],
            is_approved=True  # Auto-approve for now
        )
        
        db.add(generated_content)
        db.commit()
        db.refresh(generated_content)
        
        total_time = time.time() - start_time
        
        return ContentGenerationResponse(
            content_id=generated_content.id,
            text_content=content_result["text_content"],
            image_url=image_url,
            hashtags=content_result["hashtags"],
            generation_time=total_time,
            ai_model_used=content_result["ai_model_used"]
        )
    
    def get_content_by_id(self, content_id: int, db: Session) -> Optional[GeneratedContentResponse]:
        """Get content by ID"""
        content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if content:
            return GeneratedContentResponse.from_orm(content)
        return None
    
    def get_content_by_sign(
        self,
        zodiac_sign: str,
        content_type: Optional[str] = None,
        limit: int = 10,
        db: Session = None
    ) -> List[GeneratedContentResponse]:
        """Get content for a specific zodiac sign"""
        
        # Get zodiac sign ID
        zodiac_sign_obj = db.query(ZodiacSign).filter(
            ZodiacSign.name == zodiac_sign.lower()
        ).first()
        
        if not zodiac_sign_obj:
            return []
        
        query = db.query(GeneratedContent).filter(
            GeneratedContent.zodiac_sign_id == zodiac_sign_obj.id
        )
        
        if content_type:
            query = query.filter(GeneratedContent.content_type == content_type)
        
        content_list = query.order_by(GeneratedContent.created_at.desc()).limit(limit).all()
        
        return [GeneratedContentResponse.from_orm(content) for content in content_list]
    
    def get_all_zodiac_signs(self, db: Session) -> List[ZodiacSignResponse]:
        """Get all zodiac signs"""
        signs = db.query(ZodiacSign).all()
        return [ZodiacSignResponse.from_orm(sign) for sign in signs]
    
    def create_zodiac_sign(self, zodiac_sign: ZodiacSignCreate, db: Session) -> ZodiacSignResponse:
        """Create a new zodiac sign"""
        
        # Check if sign already exists
        existing_sign = db.query(ZodiacSign).filter(
            ZodiacSign.name == zodiac_sign.name.lower()
        ).first()
        
        if existing_sign:
            return ZodiacSignResponse.from_orm(existing_sign)
        
        db_sign = ZodiacSign(**zodiac_sign.dict())
        db.add(db_sign)
        db.commit()
        db.refresh(db_sign)
        
        return ZodiacSignResponse.from_orm(db_sign)
    
    def get_templates(
        self,
        zodiac_sign: str,
        content_type: Optional[str] = None,
        platform: Optional[str] = None,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """Get content templates"""
        
        # Get zodiac sign ID
        zodiac_sign_obj = db.query(ZodiacSign).filter(
            ZodiacSign.name == zodiac_sign.lower()
        ).first()
        
        query = db.query(ContentTemplate)
        
        if zodiac_sign_obj:
            query = query.filter(
                or_(
                    ContentTemplate.zodiac_sign_id == zodiac_sign_obj.id,
                    ContentTemplate.zodiac_sign_id.is_(None)  # Generic templates
                )
            )
        
        if content_type:
            query = query.filter(ContentTemplate.content_type == content_type)
        
        if platform:
            query = query.filter(ContentTemplate.platform == platform)
        
        query = query.filter(ContentTemplate.is_active == True)
        
        templates = query.all()
        
        return [
            {
                "id": template.id,
                "name": template.name,
                "content_type": template.content_type,
                "template_text": template.template_text,
                "platform": template.platform,
                "usage_count": template.usage_count
            }
            for template in templates
        ]
    
    def get_content_stats(self, db: Session, days: int = 30) -> Dict[str, Any]:
        """Get content generation statistics"""
        
        from datetime import datetime, timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total content generated
        total_content = db.query(GeneratedContent).filter(
            GeneratedContent.created_at >= start_date
        ).count()
        
        # Content by type
        content_by_type = db.query(
            GeneratedContent.content_type,
            db.func.count(GeneratedContent.id).label('count')
        ).filter(
            GeneratedContent.created_at >= start_date
        ).group_by(GeneratedContent.content_type).all()
        
        # Content by zodiac sign
        content_by_sign = db.query(
            ZodiacSign.name,
            db.func.count(GeneratedContent.id).label('count')
        ).join(GeneratedContent).filter(
            GeneratedContent.created_at >= start_date
        ).group_by(ZodiacSign.name).all()
        
        return {
            "total_content": total_content,
            "content_by_type": {item.content_type: item.count for item in content_by_type},
            "content_by_sign": {item.name: item.count for item in content_by_sign},
            "period_days": days
        }
    
    def approve_content(self, content_id: int, db: Session) -> bool:
        """Approve content for publishing"""
        content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if content:
            content.is_approved = True
            db.commit()
            return True
        return False
    
    def reject_content(self, content_id: int, db: Session) -> bool:
        """Reject content"""
        content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if content:
            content.is_approved = False
            db.commit()
            return True
        return False
    
    def delete_content(self, content_id: int, db: Session) -> bool:
        """Delete content"""
        content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if content:
            db.delete(content)
            db.commit()
            return True
        return False
    
    def search_content(
        self,
        query: str,
        zodiac_sign: Optional[str] = None,
        content_type: Optional[str] = None,
        limit: int = 20,
        db: Session = None
    ) -> List[GeneratedContentResponse]:
        """Search content by text"""
        
        search_query = db.query(GeneratedContent).filter(
            GeneratedContent.text_content.contains(query)
        )
        
        if zodiac_sign:
            zodiac_sign_obj = db.query(ZodiacSign).filter(
                ZodiacSign.name == zodiac_sign.lower()
            ).first()
            if zodiac_sign_obj:
                search_query = search_query.filter(
                    GeneratedContent.zodiac_sign_id == zodiac_sign_obj.id
                )
        
        if content_type:
            search_query = search_query.filter(
                GeneratedContent.content_type == content_type
            )
        
        results = search_query.order_by(
            GeneratedContent.created_at.desc()
        ).limit(limit).all()
        
        return [GeneratedContentResponse.from_orm(content) for content in results]