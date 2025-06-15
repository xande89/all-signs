# Zodiac AI Content System - Technical Architecture

## System Overview

### Architecture Pattern: Microservices with Event-Driven Design
- **Content Generation Service**: AI-powered content creation
- **Publishing Service**: Multi-platform social media automation
- **Scheduling Service**: Content calendar and timing management
- **Analytics Service**: Performance tracking and optimization
- **User Management Service**: Profile and preference management
- **Image Generation Service**: Automated visual content creation

## Technology Stack

### Backend Services
- **Runtime**: Python 3.11+ with FastAPI framework
- **Database**: PostgreSQL for structured data, Redis for caching
- **Message Queue**: Redis with Celery for background tasks
- **AI Integration**: OpenAI GPT-4, Claude, or local LLM models
- **Image Generation**: DALL-E 3, Midjourney API, or Stable Diffusion
- **Deployment**: Docker containers with Kubernetes orchestration

### Frontend Dashboard
- **Framework**: React.js with TypeScript
- **UI Library**: Material-UI or Tailwind CSS
- **State Management**: Redux Toolkit
- **Charts**: Chart.js or D3.js for analytics
- **Authentication**: JWT with refresh tokens

### External Integrations
- **Social Media APIs**: Instagram Graph API, TikTok API, Twitter API v2
- **Scheduling**: Custom scheduler with timezone support
- **Analytics**: Platform-native analytics + custom tracking
- **Storage**: AWS S3 or Google Cloud Storage for media files

## Database Schema Design

### Core Tables

#### zodiac_signs
```sql
CREATE TABLE zodiac_signs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    element VARCHAR(20) NOT NULL, -- Fire, Earth, Air, Water
    modality VARCHAR(20) NOT NULL, -- Cardinal, Fixed, Mutable
    ruling_planet VARCHAR(50),
    date_range_start DATE NOT NULL,
    date_range_end DATE NOT NULL,
    traits JSONB, -- Personality traits and characteristics
    colors JSONB, -- Brand colors for this sign
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### social_profiles
```sql
CREATE TABLE social_profiles (
    id SERIAL PRIMARY KEY,
    zodiac_sign_id INTEGER REFERENCES zodiac_signs(id),
    platform VARCHAR(50) NOT NULL, -- instagram, tiktok, twitter, etc.
    username VARCHAR(100) NOT NULL,
    profile_id VARCHAR(100), -- Platform-specific ID
    access_token TEXT, -- Encrypted API access token
    refresh_token TEXT, -- Encrypted refresh token
    is_active BOOLEAN DEFAULT true,
    last_post_at TIMESTAMP,
    follower_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### content_templates
```sql
CREATE TABLE content_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- daily_horoscope, weekly_forecast, meme, etc.
    template_text TEXT NOT NULL, -- Template with placeholders
    platform VARCHAR(50) NOT NULL,
    zodiac_sign_id INTEGER REFERENCES zodiac_signs(id),
    is_active BOOLEAN DEFAULT true,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### generated_content
```sql
CREATE TABLE generated_content (
    id SERIAL PRIMARY KEY,
    zodiac_sign_id INTEGER REFERENCES zodiac_signs(id),
    content_type VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    text_content TEXT NOT NULL,
    image_url VARCHAR(500),
    hashtags TEXT[],
    target_date DATE,
    ai_model_used VARCHAR(50),
    generation_prompt TEXT,
    is_approved BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### scheduled_posts
```sql
CREATE TABLE scheduled_posts (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES generated_content(id),
    profile_id INTEGER REFERENCES social_profiles(id),
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, published, failed, cancelled
    platform_post_id VARCHAR(100), -- ID returned by social platform
    error_message TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### analytics_data
```sql
CREATE TABLE analytics_data (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES scheduled_posts(id),
    platform VARCHAR(50) NOT NULL,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4),
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    recorded_at TIMESTAMP DEFAULT NOW()
);
```

## Service Architecture Details

### 1. Content Generation Service

#### Core Components
- **AI Content Generator**: Creates horoscopes, forecasts, and educational content
- **Template Engine**: Manages content templates and personalization
- **Content Validator**: Ensures quality and brand consistency
- **Variation Generator**: Creates multiple versions for A/B testing

#### API Endpoints
```python
# Content Generation API
POST /api/content/generate
{
    "zodiac_sign": "aries",
    "content_type": "daily_horoscope",
    "target_date": "2025-06-13",
    "platform": "instagram",
    "style_preferences": {
        "tone": "motivational",
        "length": "short"
    }
}

GET /api/content/templates/{zodiac_sign}
POST /api/content/templates
PUT /api/content/templates/{template_id}
DELETE /api/content/templates/{template_id}
```

### 2. Image Generation Service

#### Features
- **Template-based Generation**: Consistent visual branding
- **Dynamic Text Overlay**: Horoscope text on branded backgrounds
- **Zodiac Symbol Integration**: Automatic symbol placement
- **Platform Optimization**: Different sizes for each platform

#### Workflow
1. Receive content and zodiac sign information
2. Select appropriate visual template
3. Generate or retrieve background image
4. Add zodiac symbols and branding elements
5. Overlay text with proper typography
6. Optimize for target platform dimensions
7. Return image URL and metadata

### 3. Publishing Service

#### Multi-Platform Support
- **Instagram**: Feed posts, Stories, Reels
- **TikTok**: Video posts with generated visuals
- **Twitter/X**: Text posts with images
- **Pinterest**: Infographic-style pins
- **Facebook**: Cross-posting from Instagram

#### Publishing Workflow
```python
class PublishingService:
    async def publish_content(self, content_id: int, profile_id: int):
        # 1. Retrieve content and profile information
        content = await self.get_content(content_id)
        profile = await self.get_profile(profile_id)
        
        # 2. Adapt content for platform
        adapted_content = await self.adapt_for_platform(content, profile.platform)
        
        # 3. Generate or retrieve images
        if adapted_content.needs_image:
            image_url = await self.generate_image(adapted_content)
            adapted_content.image_url = image_url
        
        # 4. Publish to platform
        result = await self.platform_publisher.publish(profile, adapted_content)
        
        # 5. Update database with results
        await self.update_post_status(content_id, profile_id, result)
        
        return result
```

### 4. Scheduling Service

#### Features
- **Timezone Management**: Post at optimal times for each audience
- **Content Calendar**: Visual planning and management
- **Automatic Rescheduling**: Handle failed posts
- **Batch Operations**: Schedule multiple posts efficiently

#### Scheduling Logic
```python
class SchedulingService:
    def calculate_optimal_posting_times(self, zodiac_sign: str, platform: str):
        # Based on audience analytics and platform best practices
        optimal_times = {
            "instagram": {
                "daily_horoscope": "07:00",
                "motivational": "12:00",
                "evening_reflection": "18:00"
            },
            "tiktok": {
                "daily_horoscope": "08:00",
                "entertainment": "19:00"
            }
        }
        return optimal_times.get(platform, {})
```

### 5. Analytics Service

#### Metrics Tracking
- **Engagement Metrics**: Likes, comments, shares, saves
- **Reach Metrics**: Impressions, reach, profile visits
- **Growth Metrics**: Follower growth, engagement rate trends
- **Content Performance**: Best performing content types and times

#### Analytics Dashboard Features
- Real-time performance monitoring
- Comparative analysis across zodiac signs
- Content optimization recommendations
- Audience insights and demographics
- ROI tracking and reporting

## API Integration Specifications

### Instagram Graph API Integration
```python
class InstagramPublisher:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def create_media_object(self, image_url: str, caption: str):
        endpoint = f"{self.base_url}/{self.page_id}/media"
        data = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        # Implementation details...
    
    async def publish_media(self, creation_id: str):
        endpoint = f"{self.base_url}/{self.page_id}/media_publish"
        data = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        # Implementation details...
```

### TikTok API Integration
```python
class TikTokPublisher:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://open-api.tiktok.com"
    
    async def upload_video(self, video_file: bytes, title: str, description: str):
        # TikTok requires video content, so we'll need to generate
        # short videos from static images with transitions
        endpoint = f"{self.base_url}/share/video/upload/"
        # Implementation details...
```

## Security and Privacy

### Data Protection
- **Encryption**: All API tokens encrypted at rest
- **Access Control**: Role-based permissions
- **Audit Logging**: Track all system actions
- **Data Retention**: Automatic cleanup of old data

### API Security
- **Rate Limiting**: Prevent API abuse
- **Authentication**: JWT tokens with expiration
- **Input Validation**: Sanitize all user inputs
- **HTTPS Only**: Secure communication

## Scalability Considerations

### Horizontal Scaling
- **Microservices**: Independent scaling of components
- **Load Balancing**: Distribute traffic across instances
- **Database Sharding**: Partition data by zodiac sign or date
- **CDN Integration**: Fast image delivery globally

### Performance Optimization
- **Caching Strategy**: Redis for frequently accessed data
- **Background Processing**: Celery for heavy operations
- **Database Indexing**: Optimize query performance
- **Connection Pooling**: Efficient database connections

## Monitoring and Alerting

### System Monitoring
- **Health Checks**: Monitor service availability
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Automatic error reporting
- **Resource Usage**: CPU, memory, and storage monitoring

### Business Metrics
- **Content Generation Success Rate**
- **Publishing Success Rate**
- **Engagement Rate Trends**
- **User Growth Metrics**

## Deployment Strategy

### Development Environment
- **Local Development**: Docker Compose setup
- **Testing**: Automated unit and integration tests
- **Staging**: Production-like environment for testing

### Production Deployment
- **Container Orchestration**: Kubernetes for management
- **CI/CD Pipeline**: Automated testing and deployment
- **Blue-Green Deployment**: Zero-downtime updates
- **Backup Strategy**: Regular database and file backups

## Cost Optimization

### Resource Management
- **Auto-scaling**: Scale based on demand
- **Spot Instances**: Use cheaper compute when possible
- **Storage Optimization**: Compress and archive old data
- **API Cost Management**: Monitor and optimize API usage

### Budget Allocation
- **Infrastructure**: 40% (servers, storage, networking)
- **AI Services**: 30% (content and image generation)
- **Social Media APIs**: 20% (platform access and features)
- **Monitoring/Tools**: 10% (analytics, monitoring, development tools)