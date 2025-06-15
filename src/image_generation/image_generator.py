"""
Image generation service for zodiac content
"""
import asyncio
import time
from datetime import date
from typing import Dict, List, Optional, Any, Tuple
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
import os
import random


class ZodiacImageGenerator:
    """Generate images for zodiac content"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.zodiac_colors = self._load_zodiac_colors()
        self.zodiac_symbols = self._load_zodiac_symbols()
        
    def _load_zodiac_colors(self) -> Dict[str, Dict[str, str]]:
        """Load color schemes for each zodiac sign"""
        return {
            "aries": {
                "primary": "#E74C3C",
                "secondary": "#FF6B35", 
                "accent": "#FFD700",
                "background": "#2C3E50",
                "text": "#FFFFFF"
            },
            "taurus": {
                "primary": "#27AE60",
                "secondary": "#8B4513",
                "accent": "#E8B4B8",
                "background": "#F5F5DC",
                "text": "#2C3E50"
            },
            "gemini": {
                "primary": "#F1C40F",
                "secondary": "#3498DB",
                "accent": "#9B59B6",
                "background": "#FFFFFF",
                "text": "#2C3E50"
            },
            "cancer": {
                "primary": "#2980B9",
                "secondary": "#20B2AA",
                "accent": "#FFB6C1",
                "background": "#F8F8FF",
                "text": "#2C3E50"
            },
            "leo": {
                "primary": "#FFD700",
                "secondary": "#FF8C00",
                "accent": "#4B0082",
                "background": "#000000",
                "text": "#FFFFFF"
            },
            "virgo": {
                "primary": "#9CAF88",
                "secondary": "#8B4513",
                "accent": "#D3D3D3",
                "background": "#F5F5DC",
                "text": "#2C3E50"
            },
            "libra": {
                "primary": "#FFB6C1",
                "secondary": "#B0E0E6",
                "accent": "#E8B4B8",
                "background": "#FFFFFF",
                "text": "#2C3E50"
            },
            "scorpio": {
                "primary": "#8B0000",
                "secondary": "#4B0082",
                "accent": "#C0C0C0",
                "background": "#000000",
                "text": "#FFFFFF"
            },
            "sagittarius": {
                "primary": "#9B59B6",
                "secondary": "#40E0D0",
                "accent": "#FFD700",
                "background": "#FFFFFF",
                "text": "#2C3E50"
            },
            "capricorn": {
                "primary": "#006400",
                "secondary": "#36454F",
                "accent": "#FFD700",
                "background": "#F5F5DC",
                "text": "#FFFFFF"
            },
            "aquarius": {
                "primary": "#00BFFF",
                "secondary": "#39FF14",
                "accent": "#C0C0C0",
                "background": "#000000",
                "text": "#FFFFFF"
            },
            "pisces": {
                "primary": "#006994",
                "secondary": "#20B2AA",
                "accent": "#F8F8FF",
                "background": "#E6E6FA",
                "text": "#2C3E50"
            }
        }
    
    def _load_zodiac_symbols(self) -> Dict[str, str]:
        """Load Unicode symbols for each zodiac sign"""
        return {
            "aries": "♈",
            "taurus": "♉", 
            "gemini": "♊",
            "cancer": "♋",
            "leo": "♌",
            "virgo": "♍",
            "libra": "♎",
            "scorpio": "♏",
            "sagittarius": "♐",
            "capricorn": "♑",
            "aquarius": "♒",
            "pisces": "♓"
        }
    
    async def generate_daily_horoscope_image(
        self,
        zodiac_sign: str,
        horoscope_text: str,
        target_date: date,
        platform: str = "instagram"
    ) -> str:
        """Generate a daily horoscope image"""
        
        # Get platform dimensions
        dimensions = self._get_platform_dimensions(platform)
        colors = self.zodiac_colors.get(zodiac_sign.lower())
        symbol = self.zodiac_symbols.get(zodiac_sign.lower(), "⭐")
        
        if not colors:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        # Create the image
        image = self._create_daily_horoscope_template(
            dimensions, colors, symbol, zodiac_sign, horoscope_text, target_date
        )
        
        # Save the image
        filename = f"horoscope_{zodiac_sign}_{target_date.strftime('%Y%m%d')}_{platform}.png"
        filepath = f"generated_images/{filename}"
        
        # Ensure directory exists
        os.makedirs("generated_images", exist_ok=True)
        
        image.save(filepath, "PNG", quality=95)
        
        return filepath
    
    async def generate_weekly_forecast_image(
        self,
        zodiac_sign: str,
        forecast_text: str,
        start_date: date,
        platform: str = "instagram"
    ) -> str:
        """Generate a weekly forecast image"""
        
        dimensions = self._get_platform_dimensions(platform)
        colors = self.zodiac_colors.get(zodiac_sign.lower())
        symbol = self.zodiac_symbols.get(zodiac_sign.lower(), "⭐")
        
        if not colors:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        # Create the image
        image = self._create_weekly_forecast_template(
            dimensions, colors, symbol, zodiac_sign, forecast_text, start_date
        )
        
        # Save the image
        filename = f"weekly_{zodiac_sign}_{start_date.strftime('%Y%m%d')}_{platform}.png"
        filepath = f"generated_images/{filename}"
        
        os.makedirs("generated_images", exist_ok=True)
        image.save(filepath, "PNG", quality=95)
        
        return filepath
    
    async def generate_motivational_image(
        self,
        zodiac_sign: str,
        motivational_text: str,
        platform: str = "instagram"
    ) -> str:
        """Generate a motivational image"""
        
        dimensions = self._get_platform_dimensions(platform)
        colors = self.zodiac_colors.get(zodiac_sign.lower())
        symbol = self.zodiac_symbols.get(zodiac_sign.lower(), "⭐")
        
        if not colors:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")
        
        # Create the image
        image = self._create_motivational_template(
            dimensions, colors, symbol, zodiac_sign, motivational_text
        )
        
        # Save the image
        filename = f"motivational_{zodiac_sign}_{int(time.time())}_{platform}.png"
        filepath = f"generated_images/{filename}"
        
        os.makedirs("generated_images", exist_ok=True)
        image.save(filepath, "PNG", quality=95)
        
        return filepath
    
    async def generate_ai_background_image(
        self,
        zodiac_sign: str,
        content_type: str = "daily_horoscope"
    ) -> Optional[str]:
        """Generate AI background image using DALL-E"""
        
        if not self.openai_api_key:
            return None
        
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_api_key)
            
            prompt = self._create_background_prompt(zodiac_sign, content_type)
            
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Download the image
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                filename = f"ai_bg_{zodiac_sign}_{content_type}_{int(time.time())}.png"
                filepath = f"generated_images/{filename}"
                
                os.makedirs("generated_images", exist_ok=True)
                
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                
                return filepath
            
        except Exception as e:
            print(f"Failed to generate AI background: {e}")
            return None
    
    def _get_platform_dimensions(self, platform: str) -> Tuple[int, int]:
        """Get image dimensions for different platforms"""
        dimensions = {
            "instagram": (1080, 1080),  # Square post
            "instagram_story": (1080, 1920),  # Story format
            "twitter": (1200, 675),  # Twitter post
            "tiktok": (1080, 1920),  # Vertical video format
            "pinterest": (1000, 1500),  # Pinterest pin
            "facebook": (1200, 630)  # Facebook post
        }
        
        return dimensions.get(platform, (1080, 1080))
    
    def _create_daily_horoscope_template(
        self,
        dimensions: Tuple[int, int],
        colors: Dict[str, str],
        symbol: str,
        zodiac_sign: str,
        horoscope_text: str,
        target_date: date
    ) -> Image.Image:
        """Create a daily horoscope image template"""
        
        width, height = dimensions
        
        # Create base image with gradient background
        image = self._create_gradient_background(width, height, colors["primary"], colors["secondary"])
        draw = ImageDraw.Draw(image)
        
        # Load fonts (fallback to default if custom fonts not available)
        try:
            title_font = ImageFont.truetype("arial.ttf", size=int(height * 0.08))
            date_font = ImageFont.truetype("arial.ttf", size=int(height * 0.04))
            text_font = ImageFont.truetype("arial.ttf", size=int(height * 0.035))
            symbol_font = ImageFont.truetype("arial.ttf", size=int(height * 0.12))
        except:
            title_font = ImageFont.load_default()
            date_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            symbol_font = ImageFont.load_default()
        
        # Draw zodiac symbol at the top
        symbol_bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_x = (width - symbol_width) // 2
        symbol_y = int(height * 0.05)
        
        draw.text((symbol_x, symbol_y), symbol, fill=colors["accent"], font=symbol_font)
        
        # Draw zodiac sign name
        title_text = zodiac_sign.upper()
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = symbol_y + int(height * 0.15)
        
        draw.text((title_x, title_y), title_text, fill=colors["text"], font=title_font)
        
        # Draw date
        date_text = target_date.strftime("%B %d, %Y")
        date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_x = (width - date_width) // 2
        date_y = title_y + int(height * 0.08)
        
        draw.text((date_x, date_y), date_text, fill=colors["accent"], font=date_font)
        
        # Draw horoscope text (wrapped)
        text_y = date_y + int(height * 0.1)
        text_margin = int(width * 0.1)
        text_width = width - (2 * text_margin)
        
        wrapped_text = self._wrap_text(horoscope_text, text_font, text_width, draw)
        
        for line in wrapped_text:
            line_bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (width - line_width) // 2
            
            draw.text((line_x, text_y), line, fill=colors["text"], font=text_font)
            text_y += int(height * 0.05)
        
        # Add decorative elements
        self._add_decorative_elements(draw, width, height, colors)
        
        return image
    
    def _create_weekly_forecast_template(
        self,
        dimensions: Tuple[int, int],
        colors: Dict[str, str],
        symbol: str,
        zodiac_sign: str,
        forecast_text: str,
        start_date: date
    ) -> Image.Image:
        """Create a weekly forecast image template"""
        
        width, height = dimensions
        
        # Create base image
        image = self._create_gradient_background(width, height, colors["background"], colors["primary"])
        draw = ImageDraw.Draw(image)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", size=int(height * 0.06))
            subtitle_font = ImageFont.truetype("arial.ttf", size=int(height * 0.04))
            text_font = ImageFont.truetype("arial.ttf", size=int(height * 0.03))
            symbol_font = ImageFont.truetype("arial.ttf", size=int(height * 0.1))
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            symbol_font = ImageFont.load_default()
        
        # Draw header
        header_y = int(height * 0.05)
        
        # Symbol
        symbol_bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_x = (width - symbol_width) // 2
        draw.text((symbol_x, header_y), symbol, fill=colors["accent"], font=symbol_font)
        
        # Title
        title_text = f"{zodiac_sign.upper()} WEEKLY FORECAST"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = header_y + int(height * 0.12)
        draw.text((title_x, title_y), title_text, fill=colors["text"], font=title_font)
        
        # Date range
        end_date = date(start_date.year, start_date.month, start_date.day + 6)
        date_text = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
        date_bbox = draw.textbbox((0, 0), date_text, font=subtitle_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_x = (width - date_width) // 2
        date_y = title_y + int(height * 0.06)
        draw.text((date_x, date_y), date_text, fill=colors["accent"], font=subtitle_font)
        
        # Forecast text
        text_y = date_y + int(height * 0.08)
        text_margin = int(width * 0.08)
        text_width = width - (2 * text_margin)
        
        wrapped_text = self._wrap_text(forecast_text, text_font, text_width, draw)
        
        for line in wrapped_text:
            if text_y > height - int(height * 0.1):  # Stop if we're near the bottom
                break
                
            draw.text((text_margin, text_y), line, fill=colors["text"], font=text_font)
            text_y += int(height * 0.04)
        
        return image
    
    def _create_motivational_template(
        self,
        dimensions: Tuple[int, int],
        colors: Dict[str, str],
        symbol: str,
        zodiac_sign: str,
        motivational_text: str
    ) -> Image.Image:
        """Create a motivational image template"""
        
        width, height = dimensions
        
        # Create base image with solid background
        image = Image.new('RGB', (width, height), colors["primary"])
        draw = ImageDraw.Draw(image)
        
        # Add overlay pattern
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Create subtle pattern
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                if (i + j) % 100 == 0:
                    overlay_draw.ellipse([i, j, i+20, j+20], fill=(255, 255, 255, 20))
        
        image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(image)
        
        # Load fonts
        try:
            quote_font = ImageFont.truetype("arial.ttf", size=int(height * 0.05))
            sign_font = ImageFont.truetype("arial.ttf", size=int(height * 0.04))
            symbol_font = ImageFont.truetype("arial.ttf", size=int(height * 0.15))
        except:
            quote_font = ImageFont.load_default()
            sign_font = ImageFont.load_default()
            symbol_font = ImageFont.load_default()
        
        # Draw large symbol in background (watermark style)
        symbol_bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_height = symbol_bbox[3] - symbol_bbox[1]
        symbol_x = (width - symbol_width) // 2
        symbol_y = (height - symbol_height) // 2
        
        # Draw symbol with low opacity effect
        symbol_color = tuple(int(colors["accent"].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        symbol_color = (*symbol_color, 100)  # Add alpha
        
        symbol_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        symbol_draw = ImageDraw.Draw(symbol_img)
        symbol_draw.text((symbol_x, symbol_y), symbol, fill=symbol_color, font=symbol_font)
        
        image = Image.alpha_composite(image.convert('RGBA'), symbol_img).convert('RGB')
        draw = ImageDraw.Draw(image)
        
        # Draw motivational text
        text_margin = int(width * 0.1)
        text_width = width - (2 * text_margin)
        text_y = int(height * 0.3)
        
        wrapped_text = self._wrap_text(motivational_text, quote_font, text_width, draw)
        
        for line in wrapped_text:
            line_bbox = draw.textbbox((0, 0), line, font=quote_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (width - line_width) // 2
            
            draw.text((line_x, text_y), line, fill=colors["text"], font=quote_font)
            text_y += int(height * 0.06)
        
        # Draw zodiac sign name at bottom
        sign_text = f"- {zodiac_sign.upper()} -"
        sign_bbox = draw.textbbox((0, 0), sign_text, font=sign_font)
        sign_width = sign_bbox[2] - sign_bbox[0]
        sign_x = (width - sign_width) // 2
        sign_y = int(height * 0.8)
        
        draw.text((sign_x, sign_y), sign_text, fill=colors["accent"], font=sign_font)
        
        return image
    
    def _create_gradient_background(self, width: int, height: int, color1: str, color2: str) -> Image.Image:
        """Create a gradient background"""
        
        # Convert hex colors to RGB
        color1_rgb = tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        color2_rgb = tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        # Create gradient
        image = Image.new('RGB', (width, height))
        
        for y in range(height):
            # Calculate interpolation factor
            factor = y / height
            
            # Interpolate between colors
            r = int(color1_rgb[0] * (1 - factor) + color2_rgb[0] * factor)
            g = int(color1_rgb[1] * (1 - factor) + color2_rgb[1] * factor)
            b = int(color1_rgb[2] * (1 - factor) + color2_rgb[2] * factor)
            
            # Draw horizontal line
            for x in range(width):
                image.putpixel((x, y), (r, g, b))
        
        return image
    
    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """Wrap text to fit within specified width"""
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, add it anyway
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _add_decorative_elements(self, draw: ImageDraw.Draw, width: int, height: int, colors: Dict[str, str]):
        """Add decorative elements to the image"""
        
        # Add corner decorations
        corner_size = min(width, height) // 20
        
        # Top corners
        draw.ellipse([10, 10, 10 + corner_size, 10 + corner_size], fill=colors["accent"])
        draw.ellipse([width - 10 - corner_size, 10, width - 10, 10 + corner_size], fill=colors["accent"])
        
        # Bottom corners
        draw.ellipse([10, height - 10 - corner_size, 10 + corner_size, height - 10], fill=colors["accent"])
        draw.ellipse([width - 10 - corner_size, height - 10 - corner_size, width - 10, height - 10], fill=colors["accent"])
        
        # Add subtle border
        border_width = 3
        draw.rectangle([border_width, border_width, width - border_width, height - border_width], 
                      outline=colors["accent"], width=border_width)
    
    def _create_background_prompt(self, zodiac_sign: str, content_type: str) -> str:
        """Create a prompt for AI background generation"""
        
        sign_themes = {
            "aries": "fiery energy, ram symbolism, red and orange colors, dynamic movement",
            "taurus": "earth elements, bull symbolism, green and brown colors, stability and luxury",
            "gemini": "air elements, twin symbolism, yellow and blue colors, communication and duality",
            "cancer": "water elements, crab and moon symbolism, blue and silver colors, nurturing energy",
            "leo": "fire elements, lion symbolism, gold and orange colors, royal and dramatic",
            "virgo": "earth elements, maiden symbolism, green and brown colors, precision and nature",
            "libra": "air elements, scales symbolism, pink and blue colors, balance and harmony",
            "scorpio": "water elements, scorpion symbolism, deep red and black colors, mystery and transformation",
            "sagittarius": "fire elements, archer symbolism, purple and turquoise colors, adventure and freedom",
            "capricorn": "earth elements, goat symbolism, dark green and gray colors, ambition and mountains",
            "aquarius": "air elements, water bearer symbolism, blue and silver colors, innovation and technology",
            "pisces": "water elements, fish symbolism, sea green and purple colors, dreams and spirituality"
        }
        
        theme = sign_themes.get(zodiac_sign.lower(), "cosmic and mystical elements")
        
        prompt = f"""
        Create a beautiful, mystical background image for {zodiac_sign} {content_type}.
        
        Style: Modern, ethereal, cosmic, spiritual
        Elements: {theme}
        Mood: Inspiring, peaceful, magical
        
        The image should be suitable as a background for text overlay, so avoid busy central areas.
        Include subtle constellation patterns, cosmic elements, and astrological symbols.
        Use a dreamy, gradient style with soft lighting effects.
        
        Avoid: Text, words, overly busy patterns in the center, harsh contrasts
        """
        
        return prompt.strip()


# Example usage
async def test_image_generator():
    """Test the image generator"""
    generator = ZodiacImageGenerator()
    
    try:
        # Test daily horoscope image
        image_path = await generator.generate_daily_horoscope_image(
            zodiac_sign="aries",
            horoscope_text="Today brings powerful energy for new beginnings. Trust your instincts and take bold action toward your goals.",
            target_date=date.today(),
            platform="instagram"
        )
        
        print(f"Generated image: {image_path}")
        
    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_image_generator())