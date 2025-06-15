"""
Content scheduling service
"""
import asyncio
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import pytz

from ..database.models import (
    ScheduledPost, GeneratedContent, SocialProfile, ZodiacSign,
    ScheduledPostCreate, ScheduledPostResponse
)
from ..database.database import get_db_session, close_db_session


class ContentScheduler:
    """Service for scheduling and managing content publishing"""
    
    def __init__(self):
        self.is_running = False
        self.scheduler_task = None
        self.timezone = pytz.UTC
    
    async def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self.is_running = True
            self.scheduler_task = asyncio.create_task(self._scheduler_loop())
    
    async def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass
    
    async def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                await self._process_scheduled_posts()
                await asyncio.sleep(60)  # Check every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def _process_scheduled_posts(self):
        """Process posts that are ready to be published"""
        db = get_db_session()
        try:
            now = datetime.utcnow()
            
            # Get posts that are ready to publish
            ready_posts = db.query(ScheduledPost).filter(
                and_(
                    ScheduledPost.scheduled_time <= now,
                    ScheduledPost.status == "pending"
                )
            ).all()
            
            for post in ready_posts:
                try:
                    await self._publish_post(post, db)
                except Exception as e:
                    print(f"Failed to publish post {post.id}: {e}")
                    post.status = "failed"
                    post.error_message = str(e)
                    db.commit()
        
        finally:
            close_db_session(db)
    
    async def _publish_post(self, scheduled_post: ScheduledPost, db: Session):
        """Publish a single post"""
        # This would integrate with actual social media APIs
        # For now, we'll just mark it as published
        
        scheduled_post.status = "published"
        scheduled_post.published_at = datetime.utcnow()
        scheduled_post.platform_post_id = f"mock_post_{scheduled_post.id}"
        
        db.commit()
        
        print(f"Published post {scheduled_post.id} to platform")
    
    async def schedule_post(
        self,
        content_id: int,
        profile_id: int,
        scheduled_time: datetime,
        db: Session
    ) -> ScheduledPostResponse:
        """Schedule a single post"""
        
        # Verify content and profile exist
        content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if not content:
            raise ValueError(f"Content with ID {content_id} not found")
        
        profile = db.query(SocialProfile).filter(SocialProfile.id == profile_id).first()
        if not profile:
            raise ValueError(f"Profile with ID {profile_id} not found")
        
        # Create scheduled post
        scheduled_post = ScheduledPost(
            content_id=content_id,
            profile_id=profile_id,
            scheduled_time=scheduled_time,
            status="pending"
        )
        
        db.add(scheduled_post)
        db.commit()
        db.refresh(scheduled_post)
        
        return ScheduledPostResponse.from_orm(scheduled_post)
    
    async def schedule_daily_content(
        self,
        target_date: date,
        zodiac_signs: List[str],
        platforms: List[str],
        db: Session
    ) -> List[ScheduledPostResponse]:
        """Schedule daily content for multiple signs and platforms"""
        
        scheduled_posts = []
        
        for sign in zodiac_signs:
            for platform in platforms:
                try:
                    # Get the most recent content for this sign and type
                    zodiac_sign_obj = db.query(ZodiacSign).filter(
                        ZodiacSign.name == sign.lower()
                    ).first()
                    
                    if not zodiac_sign_obj:
                        continue
                    
                    # Find content for this date
                    content = db.query(GeneratedContent).filter(
                        and_(
                            GeneratedContent.zodiac_sign_id == zodiac_sign_obj.id,
                            GeneratedContent.content_type == "daily_horoscope",
                            GeneratedContent.target_date == target_date,
                            GeneratedContent.is_approved == True
                        )
                    ).first()
                    
                    if not content:
                        continue
                    
                    # Find profile for this sign and platform
                    profile = db.query(SocialProfile).filter(
                        and_(
                            SocialProfile.zodiac_sign_id == zodiac_sign_obj.id,
                            SocialProfile.platform == platform,
                            SocialProfile.is_active == True
                        )
                    ).first()
                    
                    if not profile:
                        continue
                    
                    # Calculate posting time based on platform and sign
                    posting_time = self._calculate_optimal_posting_time(
                        target_date, platform, sign
                    )
                    
                    # Check if already scheduled
                    existing_post = db.query(ScheduledPost).filter(
                        and_(
                            ScheduledPost.content_id == content.id,
                            ScheduledPost.profile_id == profile.id,
                            ScheduledPost.scheduled_time.cast(date) == target_date
                        )
                    ).first()
                    
                    if existing_post:
                        continue
                    
                    # Schedule the post
                    scheduled_post = await self.schedule_post(
                        content_id=content.id,
                        profile_id=profile.id,
                        scheduled_time=posting_time,
                        db=db
                    )
                    
                    scheduled_posts.append(scheduled_post)
                    
                except Exception as e:
                    print(f"Failed to schedule content for {sign} on {platform}: {e}")
                    continue
        
        return scheduled_posts
    
    def _calculate_optimal_posting_time(
        self,
        target_date: date,
        platform: str,
        zodiac_sign: str
    ) -> datetime:
        """Calculate optimal posting time based on platform and audience"""
        
        # Platform-specific optimal times (in UTC)
        platform_times = {
            "instagram": {
                "daily_horoscope": 7,  # 7 AM
                "motivational": 12,    # 12 PM
                "evening": 18          # 6 PM
            },
            "twitter": {
                "daily_horoscope": 8,  # 8 AM
                "motivational": 13,    # 1 PM
                "evening": 19          # 7 PM
            },
            "tiktok": {
                "daily_horoscope": 9,  # 9 AM
                "motivational": 15,    # 3 PM
                "evening": 20          # 8 PM
            }
        }
        
        # Get base hour for platform
        base_hour = platform_times.get(platform, {}).get("daily_horoscope", 8)
        
        # Add some variation based on zodiac sign (to spread out posting times)
        sign_offset = {
            "aries": 0, "taurus": 1, "gemini": 2, "cancer": 3,
            "leo": 4, "virgo": 5, "libra": 6, "scorpio": 7,
            "sagittarius": 8, "capricorn": 9, "aquarius": 10, "pisces": 11
        }
        
        offset_minutes = sign_offset.get(zodiac_sign.lower(), 0) * 5  # 5-minute intervals
        
        posting_datetime = datetime.combine(target_date, datetime.min.time()) + timedelta(
            hours=base_hour,
            minutes=offset_minutes
        )
        
        return posting_datetime
    
    def get_upcoming_posts(
        self,
        days: int = 7,
        zodiac_sign: Optional[str] = None,
        platform: Optional[str] = None,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """Get upcoming scheduled posts"""
        
        end_date = datetime.utcnow() + timedelta(days=days)
        
        query = db.query(ScheduledPost).filter(
            and_(
                ScheduledPost.scheduled_time >= datetime.utcnow(),
                ScheduledPost.scheduled_time <= end_date,
                ScheduledPost.status == "pending"
            )
        )
        
        # Join with related tables for filtering
        query = query.join(GeneratedContent).join(SocialProfile).join(ZodiacSign)
        
        if zodiac_sign:
            query = query.filter(ZodiacSign.name == zodiac_sign.lower())
        
        if platform:
            query = query.filter(SocialProfile.platform == platform)
        
        posts = query.order_by(ScheduledPost.scheduled_time).all()
        
        result = []
        for post in posts:
            result.append({
                "id": post.id,
                "scheduled_time": post.scheduled_time,
                "zodiac_sign": post.content.zodiac_sign.name,
                "platform": post.profile.platform,
                "content_type": post.content.content_type,
                "content_preview": post.content.text_content[:100] + "..." if len(post.content.text_content) > 100 else post.content.text_content,
                "status": post.status
            })
        
        return result
    
    def cancel_scheduled_post(self, post_id: int, db: Session) -> bool:
        """Cancel a scheduled post"""
        post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()
        if post and post.status == "pending":
            post.status = "cancelled"
            db.commit()
            return True
        return False
    
    def reschedule_post(
        self,
        post_id: int,
        new_time: datetime,
        db: Session
    ) -> Optional[ScheduledPostResponse]:
        """Reschedule a post to a new time"""
        post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()
        if post and post.status == "pending":
            post.scheduled_time = new_time
            db.commit()
            db.refresh(post)
            return ScheduledPostResponse.from_orm(post)
        return None
    
    def get_posting_schedule(
        self,
        start_date: date,
        end_date: date,
        zodiac_sign: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get posting schedule for a date range"""
        
        query = db.query(ScheduledPost).filter(
            and_(
                ScheduledPost.scheduled_time >= datetime.combine(start_date, datetime.min.time()),
                ScheduledPost.scheduled_time <= datetime.combine(end_date, datetime.max.time())
            )
        )
        
        query = query.join(GeneratedContent).join(SocialProfile).join(ZodiacSign)
        
        if zodiac_sign:
            query = query.filter(ZodiacSign.name == zodiac_sign.lower())
        
        posts = query.order_by(ScheduledPost.scheduled_time).all()
        
        # Group by date
        schedule = {}
        for post in posts:
            post_date = post.scheduled_time.date().isoformat()
            if post_date not in schedule:
                schedule[post_date] = []
            
            schedule[post_date].append({
                "id": post.id,
                "time": post.scheduled_time.strftime("%H:%M"),
                "zodiac_sign": post.content.zodiac_sign.name,
                "platform": post.profile.platform,
                "content_type": post.content.content_type,
                "status": post.status
            })
        
        return schedule
    
    def get_scheduler_stats(self, db: Session) -> Dict[str, Any]:
        """Get scheduler statistics"""
        
        now = datetime.utcnow()
        today = now.date()
        
        # Posts scheduled for today
        today_posts = db.query(ScheduledPost).filter(
            and_(
                ScheduledPost.scheduled_time >= datetime.combine(today, datetime.min.time()),
                ScheduledPost.scheduled_time <= datetime.combine(today, datetime.max.time())
            )
        ).count()
        
        # Posts published today
        published_today = db.query(ScheduledPost).filter(
            and_(
                ScheduledPost.published_at >= datetime.combine(today, datetime.min.time()),
                ScheduledPost.published_at <= datetime.combine(today, datetime.max.time()),
                ScheduledPost.status == "published"
            )
        ).count()
        
        # Failed posts today
        failed_today = db.query(ScheduledPost).filter(
            and_(
                ScheduledPost.scheduled_time >= datetime.combine(today, datetime.min.time()),
                ScheduledPost.scheduled_time <= datetime.combine(today, datetime.max.time()),
                ScheduledPost.status == "failed"
            )
        ).count()
        
        # Pending posts
        pending_posts = db.query(ScheduledPost).filter(
            and_(
                ScheduledPost.scheduled_time >= now,
                ScheduledPost.status == "pending"
            )
        ).count()
        
        return {
            "today_scheduled": today_posts,
            "today_published": published_today,
            "today_failed": failed_today,
            "pending_posts": pending_posts,
            "scheduler_running": self.is_running
        }