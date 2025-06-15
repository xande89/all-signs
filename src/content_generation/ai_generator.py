"""
AI-powered content generation for zodiac signs
"""
import asyncio
import time
from datetime import date, datetime
from typing import Dict, List, Optional, Any
from openai import AsyncOpenAI
import json
import random

from ..database.models import ZodiacSign


class ZodiacContentGenerator:
    """AI-powered content generator for zodiac signs"""
    
    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.zodiac_traits = self._load_zodiac_traits()
        
    def _load_zodiac_traits(self) -> Dict[str, Dict[str, Any]]:
        """Load zodiac sign traits and characteristics"""
        return {
            "aries": {
                "element": "Fire",
                "modality": "Cardinal",
                "ruling_planet": "Mars",
                "traits": ["bold", "energetic", "pioneering", "confident", "impulsive", "leadership"],
                "keywords": ["action", "courage", "initiative", "competition", "independence"],
                "challenges": ["impatience", "aggression", "selfishness"],
                "strengths": ["leadership", "courage", "determination", "enthusiasm"],
                "lucky_numbers": [1, 8, 17],
                "colors": ["red", "orange", "gold"]
            },
            "taurus": {
                "element": "Earth",
                "modality": "Fixed",
                "ruling_planet": "Venus",
                "traits": ["reliable", "practical", "devoted", "stable", "stubborn", "sensual"],
                "keywords": ["stability", "luxury", "comfort", "persistence", "beauty"],
                "challenges": ["stubbornness", "materialism", "resistance to change"],
                "strengths": ["reliability", "patience", "practical", "devoted"],
                "lucky_numbers": [2, 6, 9, 12, 24],
                "colors": ["green", "pink", "earth tones"]
            },
            "gemini": {
                "element": "Air",
                "modality": "Mutable",
                "ruling_planet": "Mercury",
                "traits": ["adaptable", "curious", "witty", "communicative", "inconsistent", "intellectual"],
                "keywords": ["communication", "versatility", "learning", "social", "variety"],
                "challenges": ["inconsistency", "superficiality", "restlessness"],
                "strengths": ["adaptability", "communication", "intelligence", "wit"],
                "lucky_numbers": [5, 7, 14, 23],
                "colors": ["yellow", "blue", "silver"]
            },
            "cancer": {
                "element": "Water",
                "modality": "Cardinal",
                "ruling_planet": "Moon",
                "traits": ["nurturing", "emotional", "intuitive", "protective", "moody", "caring"],
                "keywords": ["home", "family", "emotions", "intuition", "protection"],
                "challenges": ["moodiness", "over-sensitivity", "clinginess"],
                "strengths": ["empathy", "intuition", "loyalty", "nurturing"],
                "lucky_numbers": [2, 7, 11, 16, 20, 25],
                "colors": ["silver", "sea green", "blue"]
            },
            "leo": {
                "element": "Fire",
                "modality": "Fixed",
                "ruling_planet": "Sun",
                "traits": ["dramatic", "confident", "generous", "creative", "proud", "warm-hearted"],
                "keywords": ["creativity", "leadership", "drama", "generosity", "pride"],
                "challenges": ["arrogance", "stubbornness", "self-centeredness"],
                "strengths": ["confidence", "generosity", "loyalty", "creativity"],
                "lucky_numbers": [1, 3, 10, 19],
                "colors": ["gold", "orange", "red"]
            },
            "virgo": {
                "element": "Earth",
                "modality": "Mutable",
                "ruling_planet": "Mercury",
                "traits": ["analytical", "practical", "perfectionist", "helpful", "critical", "organized"],
                "keywords": ["service", "health", "perfection", "analysis", "efficiency"],
                "challenges": ["perfectionism", "criticism", "worry"],
                "strengths": ["analytical", "helpful", "reliable", "precise"],
                "lucky_numbers": [6, 14, 18, 29, 35],
                "colors": ["navy blue", "grey", "brown"]
            },
            "libra": {
                "element": "Air",
                "modality": "Cardinal",
                "ruling_planet": "Venus",
                "traits": ["diplomatic", "balanced", "social", "indecisive", "charming", "fair"],
                "keywords": ["balance", "harmony", "relationships", "justice", "beauty"],
                "challenges": ["indecisiveness", "superficiality", "avoidance"],
                "strengths": ["diplomacy", "fairness", "social skills", "aesthetic sense"],
                "lucky_numbers": [4, 6, 13, 15, 24],
                "colors": ["blue", "green", "pink"]
            },
            "scorpio": {
                "element": "Water",
                "modality": "Fixed",
                "ruling_planet": "Pluto",
                "traits": ["intense", "passionate", "mysterious", "transformative", "jealous", "powerful"],
                "keywords": ["transformation", "mystery", "intensity", "power", "regeneration"],
                "challenges": ["jealousy", "resentment", "secrecy"],
                "strengths": ["determination", "passion", "intuition", "resourcefulness"],
                "lucky_numbers": [8, 11, 18, 22],
                "colors": ["deep red", "black", "maroon"]
            },
            "sagittarius": {
                "element": "Fire",
                "modality": "Mutable",
                "ruling_planet": "Jupiter",
                "traits": ["adventurous", "optimistic", "philosophical", "freedom-loving", "blunt", "enthusiastic"],
                "keywords": ["adventure", "philosophy", "freedom", "travel", "wisdom"],
                "challenges": ["restlessness", "tactlessness", "over-confidence"],
                "strengths": ["optimism", "honesty", "generosity", "idealism"],
                "lucky_numbers": [3, 9, 15, 21, 33],
                "colors": ["turquoise", "purple", "red"]
            },
            "capricorn": {
                "element": "Earth",
                "modality": "Cardinal",
                "ruling_planet": "Saturn",
                "traits": ["ambitious", "disciplined", "practical", "responsible", "pessimistic", "traditional"],
                "keywords": ["ambition", "discipline", "responsibility", "achievement", "tradition"],
                "challenges": ["pessimism", "rigidity", "materialism"],
                "strengths": ["discipline", "responsibility", "ambition", "patience"],
                "lucky_numbers": [6, 8, 26, 35],
                "colors": ["brown", "black", "dark green"]
            },
            "aquarius": {
                "element": "Air",
                "modality": "Fixed",
                "ruling_planet": "Uranus",
                "traits": ["independent", "innovative", "humanitarian", "eccentric", "detached", "progressive"],
                "keywords": ["innovation", "independence", "humanity", "progress", "friendship"],
                "challenges": ["detachment", "rebelliousness", "unpredictability"],
                "strengths": ["originality", "independence", "humanitarian", "intellectual"],
                "lucky_numbers": [4, 7, 11, 22, 29],
                "colors": ["blue", "silver", "aqua"]
            },
            "pisces": {
                "element": "Water",
                "modality": "Mutable",
                "ruling_planet": "Neptune",
                "traits": ["compassionate", "artistic", "intuitive", "gentle", "escapist", "dreamy"],
                "keywords": ["compassion", "intuition", "spirituality", "creativity", "dreams"],
                "challenges": ["escapism", "over-sensitivity", "indecisiveness"],
                "strengths": ["compassion", "intuition", "creativity", "gentleness"],
                "lucky_numbers": [3, 9, 12, 15, 18, 24],
                "colors": ["sea green", "lavender", "purple"]
            }
        }
    
    async def generate_daily_horoscope(
        self, 
        zodiac_sign: str, 
        target_date: date,
        platform: str = "instagram",
        style_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a daily horoscope for a specific zodiac sign"""
        start_time = time.time()
        
        sign_data = self.zodiac_traits.get(zodiac_sign.lower())
        if not sign_data:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        # Create the prompt
        prompt = self._create_daily_horoscope_prompt(
            zodiac_sign, sign_data, target_date, platform, style_preferences
        )
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional astrologer who creates engaging, positive, and insightful horoscopes. Your writing is warm, encouraging, and specific to each zodiac sign's characteristics."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            hashtags = self._generate_hashtags(zodiac_sign, "daily_horoscope", platform)
            
            generation_time = time.time() - start_time
            
            return {
                "text_content": content,
                "hashtags": hashtags,
                "generation_time": generation_time,
                "ai_model_used": "gpt-4",
                "generation_prompt": prompt
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate horoscope: {str(e)}")
    
    async def generate_weekly_forecast(
        self,
        zodiac_sign: str,
        start_date: date,
        platform: str = "instagram",
        style_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a weekly forecast for a specific zodiac sign"""
        start_time = time.time()
        
        sign_data = self.zodiac_traits.get(zodiac_sign.lower())
        if not sign_data:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        prompt = self._create_weekly_forecast_prompt(
            zodiac_sign, sign_data, start_date, platform, style_preferences
        )
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional astrologer creating detailed weekly forecasts. Focus on different life areas: love, career, health, finances, and personal growth. Be specific and actionable."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            hashtags = self._generate_hashtags(zodiac_sign, "weekly_forecast", platform)
            
            generation_time = time.time() - start_time
            
            return {
                "text_content": content,
                "hashtags": hashtags,
                "generation_time": generation_time,
                "ai_model_used": "gpt-4",
                "generation_prompt": prompt
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate weekly forecast: {str(e)}")
    
    async def generate_motivational_content(
        self,
        zodiac_sign: str,
        platform: str = "instagram",
        style_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate motivational content for a specific zodiac sign"""
        start_time = time.time()
        
        sign_data = self.zodiac_traits.get(zodiac_sign.lower())
        if not sign_data:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        prompt = self._create_motivational_prompt(
            zodiac_sign, sign_data, platform, style_preferences
        )
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a motivational coach who understands astrology. Create inspiring, empowering content that speaks to each zodiac sign's unique strengths and potential."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=250
            )
            
            content = response.choices[0].message.content.strip()
            hashtags = self._generate_hashtags(zodiac_sign, "motivational", platform)
            
            generation_time = time.time() - start_time
            
            return {
                "text_content": content,
                "hashtags": hashtags,
                "generation_time": generation_time,
                "ai_model_used": "gpt-4",
                "generation_prompt": prompt
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate motivational content: {str(e)}")
    
    async def generate_compatibility_content(
        self,
        zodiac_sign: str,
        platform: str = "instagram",
        style_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate compatibility content for a specific zodiac sign"""
        start_time = time.time()
        
        sign_data = self.zodiac_traits.get(zodiac_sign.lower())
        if not sign_data:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        # Select a random compatible sign for this content
        compatible_signs = self._get_compatible_signs(zodiac_sign)
        featured_sign = random.choice(compatible_signs)
        
        prompt = self._create_compatibility_prompt(
            zodiac_sign, featured_sign, sign_data, platform, style_preferences
        )
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a relationship astrologer who creates engaging content about zodiac compatibility. Focus on positive aspects and practical relationship advice."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            hashtags = self._generate_hashtags(zodiac_sign, "compatibility", platform)
            
            generation_time = time.time() - start_time
            
            return {
                "text_content": content,
                "hashtags": hashtags,
                "generation_time": generation_time,
                "ai_model_used": "gpt-4",
                "generation_prompt": prompt
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate compatibility content: {str(e)}")
    
    def _create_daily_horoscope_prompt(
        self, 
        zodiac_sign: str, 
        sign_data: Dict[str, Any], 
        target_date: date,
        platform: str,
        style_preferences: Optional[Dict[str, Any]]
    ) -> str:
        """Create a prompt for daily horoscope generation"""
        
        day_of_week = target_date.strftime("%A")
        date_str = target_date.strftime("%B %d, %Y")
        
        # Platform-specific length requirements
        length_guide = {
            "instagram": "2-3 sentences, engaging and visual",
            "twitter": "1-2 sentences, concise and impactful",
            "tiktok": "1-2 sentences, trendy and relatable"
        }.get(platform, "2-3 sentences")
        
        tone = "motivational and positive"
        if style_preferences:
            tone = style_preferences.get("tone", tone)
        
        prompt = f"""
        Create a daily horoscope for {zodiac_sign.title()} for {day_of_week}, {date_str}.
        
        Zodiac Sign Details:
        - Element: {sign_data['element']}
        - Ruling Planet: {sign_data['ruling_planet']}
        - Key Traits: {', '.join(sign_data['traits'][:4])}
        - Strengths: {', '.join(sign_data['strengths'])}
        
        Requirements:
        - Length: {length_guide}
        - Tone: {tone}
        - Platform: {platform}
        - Include specific, actionable advice
        - Reference the day of the week naturally
        - Be encouraging and empowering
        - Avoid generic statements
        
        Focus areas to potentially include:
        - Career/work opportunities
        - Relationships and social connections
        - Personal growth and self-care
        - Financial matters
        - Health and wellness
        
        Write the horoscope now:
        """
        
        return prompt.strip()
    
    def _create_weekly_forecast_prompt(
        self,
        zodiac_sign: str,
        sign_data: Dict[str, Any],
        start_date: date,
        platform: str,
        style_preferences: Optional[Dict[str, Any]]
    ) -> str:
        """Create a prompt for weekly forecast generation"""
        
        end_date = date(start_date.year, start_date.month, start_date.day + 6)
        date_range = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
        
        prompt = f"""
        Create a comprehensive weekly forecast for {zodiac_sign.title()} for the week of {date_range}.
        
        Zodiac Sign Details:
        - Element: {sign_data['element']}
        - Ruling Planet: {sign_data['ruling_planet']}
        - Key Traits: {', '.join(sign_data['traits'])}
        - Keywords: {', '.join(sign_data['keywords'])}
        
        Structure the forecast with these sections:
        1. Overall Week Theme (2-3 sentences)
        2. Love & Relationships (2-3 sentences)
        3. Career & Finance (2-3 sentences)
        4. Health & Wellness (1-2 sentences)
        5. Lucky Day/Number/Color (1 sentence)
        
        Requirements:
        - Be specific and actionable
        - Include timing (early week, mid-week, weekend)
        - Reference the sign's natural tendencies
        - Provide practical advice
        - Maintain an encouraging tone
        - Platform: {platform}
        
        Write the weekly forecast now:
        """
        
        return prompt.strip()
    
    def _create_motivational_prompt(
        self,
        zodiac_sign: str,
        sign_data: Dict[str, Any],
        platform: str,
        style_preferences: Optional[Dict[str, Any]]
    ) -> str:
        """Create a prompt for motivational content generation"""
        
        prompt = f"""
        Create inspiring motivational content for {zodiac_sign.title()}.
        
        Zodiac Sign Details:
        - Element: {sign_data['element']}
        - Key Strengths: {', '.join(sign_data['strengths'])}
        - Natural Traits: {', '.join(sign_data['traits'][:3])}
        - Keywords: {', '.join(sign_data['keywords'][:3])}
        
        Requirements:
        - 2-3 sentences maximum
        - Speak directly to {zodiac_sign.title()}'s unique strengths
        - Include a call to action or empowering statement
        - Be authentic to the sign's personality
        - Platform: {platform}
        - Tone: Uplifting and empowering
        
        Focus on:
        - Their natural abilities and talents
        - How they can overcome challenges
        - Their potential for growth and success
        - Specific actions they can take today
        
        Write the motivational content now:
        """
        
        return prompt.strip()
    
    def _create_compatibility_prompt(
        self,
        zodiac_sign: str,
        featured_sign: str,
        sign_data: Dict[str, Any],
        platform: str,
        style_preferences: Optional[Dict[str, Any]]
    ) -> str:
        """Create a prompt for compatibility content generation"""
        
        prompt = f"""
        Create engaging compatibility content about {zodiac_sign.title()} and {featured_sign.title()}.
        
        {zodiac_sign.title()} Details:
        - Element: {sign_data['element']}
        - Key Traits: {', '.join(sign_data['traits'][:3])}
        
        Requirements:
        - 3-4 sentences
        - Focus on positive compatibility aspects
        - Include specific relationship dynamics
        - Mention what each sign brings to the relationship
        - Be engaging and relatable
        - Platform: {platform}
        
        Structure:
        1. Opening statement about the pairing
        2. What {zodiac_sign.title()} brings to the relationship
        3. What {featured_sign.title()} offers in return
        4. Why this combination works well
        
        Write the compatibility content now:
        """
        
        return prompt.strip()
    
    def _get_compatible_signs(self, zodiac_sign: str) -> List[str]:
        """Get compatible zodiac signs for the given sign"""
        compatibility_map = {
            "aries": ["leo", "sagittarius", "gemini", "aquarius"],
            "taurus": ["virgo", "capricorn", "cancer", "pisces"],
            "gemini": ["libra", "aquarius", "aries", "leo"],
            "cancer": ["scorpio", "pisces", "taurus", "virgo"],
            "leo": ["aries", "sagittarius", "gemini", "libra"],
            "virgo": ["taurus", "capricorn", "cancer", "scorpio"],
            "libra": ["gemini", "aquarius", "leo", "sagittarius"],
            "scorpio": ["cancer", "pisces", "virgo", "capricorn"],
            "sagittarius": ["aries", "leo", "libra", "aquarius"],
            "capricorn": ["taurus", "virgo", "scorpio", "pisces"],
            "aquarius": ["gemini", "libra", "sagittarius", "aries"],
            "pisces": ["cancer", "scorpio", "capricorn", "taurus"]
        }
        
        return compatibility_map.get(zodiac_sign.lower(), ["leo", "libra", "sagittarius"])
    
    def _generate_hashtags(self, zodiac_sign: str, content_type: str, platform: str) -> List[str]:
        """Generate relevant hashtags for the content"""
        
        # Base hashtags
        base_hashtags = [
            f"#{zodiac_sign.lower()}",
            f"#{zodiac_sign.lower()}horoscope",
            "#astrology",
            "#horoscope",
            "#zodiac",
            "#starsigns"
        ]
        
        # Content type specific hashtags
        content_hashtags = {
            "daily_horoscope": [
                "#dailyhoroscope",
                "#horoscopedaily",
                "#astrologypost",
                "#cosmicenergy",
                "#starsguidance"
            ],
            "weekly_forecast": [
                "#weeklyhoroscope",
                "#weeklyforecast",
                "#astrologyweek",
                "#cosmicweek",
                "#starweek"
            ],
            "motivational": [
                "#motivation",
                "#inspiration",
                "#empowerment",
                "#selfgrowth",
                "#positivevibes"
            ],
            "compatibility": [
                "#compatibility",
                "#lovehoroscope",
                "#relationships",
                "#zodiaccompatibility",
                "#astrologylove"
            ]
        }
        
        # Platform specific hashtags
        platform_hashtags = {
            "instagram": [
                "#spirituality",
                "#manifestation",
                "#mindfulness",
                "#selfcare",
                "#wellness"
            ],
            "tiktok": [
                "#fyp",
                "#viral",
                "#astrologytok",
                "#spiritualtok",
                "#zodiacfacts"
            ],
            "twitter": [
                "#astrologycommunity",
                "#cosmicvibes",
                "#starpower",
                "#astrologytwitter"
            ]
        }
        
        # Combine hashtags
        all_hashtags = (
            base_hashtags + 
            content_hashtags.get(content_type, []) + 
            platform_hashtags.get(platform, [])
        )
        
        # Return a selection of hashtags (limit based on platform)
        hashtag_limits = {
            "instagram": 15,
            "twitter": 5,
            "tiktok": 10
        }
        
        limit = hashtag_limits.get(platform, 10)
        return all_hashtags[:limit]


# Example usage and testing
async def test_content_generator():
    """Test the content generator"""
    # This would use a real API key in production
    generator = ZodiacContentGenerator("test-api-key")
    
    try:
        # Test daily horoscope generation
        horoscope = await generator.generate_daily_horoscope(
            zodiac_sign="aries",
            target_date=date.today(),
            platform="instagram"
        )
        
        print("Generated Horoscope:")
        print(f"Content: {horoscope['text_content']}")
        print(f"Hashtags: {', '.join(horoscope['hashtags'])}")
        print(f"Generation time: {horoscope['generation_time']:.2f}s")
        
    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_content_generator())