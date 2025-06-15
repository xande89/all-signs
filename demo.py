#!/usr/bin/env python3
"""
Demo script for the Zodiac AI Content System
This script demonstrates the core functionality of the system
"""
import asyncio
import os
from datetime import date, datetime
from src.content_generation.ai_generator import ZodiacContentGenerator
from src.image_generation.image_generator import ZodiacImageGenerator


async def demo_content_generation():
    """Demo content generation capabilities"""
    print("🌟 Zodiac AI Content System Demo")
    print("=" * 50)
    
    # Note: In a real demo, you'd use actual API keys
    # For this demo, we'll simulate the functionality
    print("⚠️  Note: This demo uses mock API keys. Replace with real keys for actual usage.")
    
    try:
        # Initialize generators (with mock API key for demo)
        content_generator = ZodiacContentGenerator("demo-api-key")
        image_generator = ZodiacImageGenerator("demo-api-key")
        
        print("\n1. 🔮 Generating Daily Horoscope for Aries...")
        print("-" * 40)
        
        # This would normally call the AI API, but for demo we'll show the structure
        demo_horoscope = {
            "text_content": "Today brings powerful energy for new beginnings, Aries! Your natural leadership shines as Mars energizes your ambition. Trust your instincts and take bold action toward your goals. A surprise opportunity may present itself this afternoon.",
            "hashtags": ["#aries", "#arieshoroscope", "#astrology", "#horoscope", "#zodiac", "#dailyhoroscope", "#motivation", "#leadership", "#newbeginnings", "#cosmicenergy"],
            "generation_time": 2.3,
            "ai_model_used": "gpt-4"
        }
        
        print(f"✅ Generated horoscope:")
        print(f"Content: {demo_horoscope['text_content']}")
        print(f"Hashtags: {', '.join(demo_horoscope['hashtags'][:5])}...")
        print(f"Generation time: {demo_horoscope['generation_time']}s")
        
        print("\n2. 🎨 Generating Image for Aries...")
        print("-" * 40)
        
        # Demo image generation
        try:
            image_path = await image_generator.generate_daily_horoscope_image(
                zodiac_sign="aries",
                horoscope_text=demo_horoscope["text_content"],
                target_date=date.today(),
                platform="instagram"
            )
            print(f"✅ Generated image: {image_path}")
        except Exception as e:
            print(f"⚠️  Image generation demo (would create: horoscope_aries_{date.today().strftime('%Y%m%d')}_instagram.png)")
        
        print("\n3. 💪 Generating Motivational Content for Leo...")
        print("-" * 40)
        
        demo_motivational = {
            "text_content": "Leo, your radiant energy lights up every room you enter! Today is perfect for showcasing your creative talents and inspiring others. Remember, you were born to shine - let your confidence lead the way to amazing opportunities.",
            "hashtags": ["#leo", "#motivation", "#confidence", "#creativity", "#leadership", "#inspiration"],
            "generation_time": 1.8,
            "ai_model_used": "gpt-4"
        }
        
        print(f"✅ Generated motivational content:")
        print(f"Content: {demo_motivational['text_content']}")
        print(f"Hashtags: {', '.join(demo_motivational['hashtags'])}")
        
        print("\n4. 💕 Generating Compatibility Content for Libra...")
        print("-" * 40)
        
        demo_compatibility = {
            "text_content": "Libra and Gemini make a harmonious air sign duo! Libra brings balance and aesthetic beauty to the relationship, while Gemini adds intellectual stimulation and variety. Together, you create a partnership filled with engaging conversations, social adventures, and mutual appreciation for life's finer things.",
            "hashtags": ["#libra", "#compatibility", "#relationships", "#gemini", "#astrologylove", "#zodiaccompatibility"],
            "generation_time": 2.1,
            "ai_model_used": "gpt-4"
        }
        
        print(f"✅ Generated compatibility content:")
        print(f"Content: {demo_compatibility['text_content']}")
        print(f"Hashtags: {', '.join(demo_compatibility['hashtags'])}")
        
        print("\n5. 📅 Weekly Forecast for Scorpio...")
        print("-" * 40)
        
        demo_weekly = {
            "text_content": """SCORPIO WEEKLY FORECAST
June 12-18, 2025

Overall Theme: Transformation and deep insights guide your week as Pluto activates your intuitive powers. Trust your instincts in all matters.

Love & Relationships: Passionate connections deepen mid-week. Single Scorpios may encounter someone intriguing through work or shared interests.

Career & Finance: A hidden opportunity surfaces by Thursday. Your investigative skills prove valuable in uncovering important information.

Health & Wellness: Focus on emotional healing and stress management. Water-based activities bring renewal.

Lucky Day: Friday | Lucky Number: 8 | Lucky Color: Deep Red""",
            "hashtags": ["#scorpio", "#weeklyforecast", "#astrology", "#transformation", "#intuition"],
            "generation_time": 3.2,
            "ai_model_used": "gpt-4"
        }
        
        print(f"✅ Generated weekly forecast:")
        print(f"Content preview: {demo_weekly['text_content'][:200]}...")
        
        print("\n6. 🎯 Content Strategy Summary")
        print("-" * 40)
        
        zodiac_signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                       "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
        
        content_types = ["daily_horoscope", "weekly_forecast", "motivational", "compatibility"]
        platforms = ["instagram", "twitter", "tiktok", "pinterest"]
        
        total_combinations = len(zodiac_signs) * len(content_types) * len(platforms)
        
        print(f"📊 System Capabilities:")
        print(f"   • {len(zodiac_signs)} Zodiac Signs")
        print(f"   • {len(content_types)} Content Types")
        print(f"   • {len(platforms)} Platforms")
        print(f"   • {total_combinations} Total Content Combinations")
        print(f"   • Estimated daily output: {len(zodiac_signs) * len(platforms)} posts")
        
        print("\n7. 🚀 Platform Optimization")
        print("-" * 40)
        
        platform_specs = {
            "instagram": {"max_length": 2200, "optimal_hashtags": 15, "image_size": "1080x1080"},
            "twitter": {"max_length": 280, "optimal_hashtags": 5, "image_size": "1200x675"},
            "tiktok": {"max_length": 150, "optimal_hashtags": 10, "image_size": "1080x1920"},
            "pinterest": {"max_length": 500, "optimal_hashtags": 8, "image_size": "1000x1500"}
        }
        
        for platform, specs in platform_specs.items():
            print(f"   {platform.title()}:")
            print(f"     - Max length: {specs['max_length']} chars")
            print(f"     - Hashtags: {specs['optimal_hashtags']}")
            print(f"     - Image size: {specs['image_size']}")
        
        print("\n8. 📈 Performance Metrics")
        print("-" * 40)
        
        print("   Expected Performance:")
        print("   • Content generation: 2-5 seconds per piece")
        print("   • Image generation: 10-15 seconds per image")
        print("   • Daily capacity: 1000+ posts")
        print("   • API response time: <200ms")
        print("   • Uptime target: 99.9%")
        
        print("\n✨ Demo Complete!")
        print("=" * 50)
        print("🎉 The Zodiac AI Content System is ready to revolutionize")
        print("   your astrology content creation and publishing workflow!")
        
        print("\n📋 Next Steps:")
        print("1. Set up your API keys in .env file")
        print("2. Configure social media platform credentials")
        print("3. Run: docker-compose up -d")
        print("4. Visit: http://localhost:8000/docs")
        print("5. Start generating content!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("This is expected without real API keys - the system structure is demonstrated above.")


def demo_api_endpoints():
    """Show example API calls"""
    print("\n🔗 API Endpoints Demo")
    print("=" * 50)
    
    examples = [
        {
            "name": "Generate Daily Horoscope",
            "method": "POST",
            "endpoint": "/api/content/generate",
            "payload": {
                "zodiac_sign": "aries",
                "content_type": "daily_horoscope",
                "target_date": "2025-06-13",
                "platform": "instagram"
            }
        },
        {
            "name": "Schedule Daily Batch",
            "method": "POST", 
            "endpoint": "/api/schedule/daily-batch",
            "payload": {
                "target_date": "2025-06-13",
                "zodiac_signs": ["aries", "taurus", "gemini"],
                "platforms": ["instagram", "twitter"]
            }
        },
        {
            "name": "Generate Image",
            "method": "POST",
            "endpoint": "/api/images/generate",
            "payload": {
                "zodiac_sign": "leo",
                "content_type": "motivational",
                "text_content": "Shine bright, Leo!",
                "platform": "instagram"
            }
        },
        {
            "name": "Get Upcoming Posts",
            "method": "GET",
            "endpoint": "/api/schedule/upcoming?days=7&zodiac_sign=scorpio",
            "payload": None
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   {example['method']} {example['endpoint']}")
        if example['payload']:
            print(f"   Payload: {example['payload']}")
    
    print(f"\n📚 Full API documentation available at: http://localhost:8000/docs")


def show_project_structure():
    """Display the project structure"""
    print("\n📁 Project Structure")
    print("=" * 50)
    
    structure = """
zodiac-ai-content/
├── src/
│   ├── content_generation/
│   │   ├── ai_generator.py          # AI content generation
│   │   └── content_service.py       # Content management
│   ├── image_generation/
│   │   └── image_generator.py       # Image creation
│   ├── scheduling/
│   │   └── scheduler.py             # Content scheduling
│   ├── database/
│   │   ├── models.py                # Database models
│   │   └── database.py              # DB configuration
│   ├── utils/
│   │   └── config.py                # Configuration
│   └── main.py                      # FastAPI application
├── generated_images/                # Generated content images
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── docker-compose.yml              # Multi-service setup
├── .env.example                     # Environment template
└── README.md                        # Documentation
"""
    
    print(structure)


if __name__ == "__main__":
    print("🌟 Welcome to the Zodiac AI Content System Demo!")
    print("This demo showcases the system's capabilities.\n")
    
    # Show project structure
    show_project_structure()
    
    # Run content generation demo
    asyncio.run(demo_content_generation())
    
    # Show API examples
    demo_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🚀 Ready to start your zodiac content empire? Let's go!")
    print("=" * 60)