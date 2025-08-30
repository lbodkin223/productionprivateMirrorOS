#!/usr/bin/env python3
"""
MirrorOS Shareable Odds Feature
Generate beautiful JPG images with user-specific odds and factors

Following final_plan.md point 17: "See how feasible shareable odds feature would be: 
JPG with factors user specific odds"
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Optional
import io
import base64
from datetime import datetime
import os

class ShareableOddsGenerator:
    """Generate shareable odds images for social media"""
    
    def __init__(self):
        # Image dimensions optimized for social media
        self.width = 1080  # Instagram/Twitter optimal
        self.height = 1080
        self.margin = 60
        
        # Color themes based on probability
        self.color_themes = {
            'high': {
                'primary': '#4CAF50',
                'secondary': '#81C784', 
                'background': '#E8F5E8',
                'accent': '#2E7D32'
            },
            'medium': {
                'primary': '#FF9800',
                'secondary': '#FFB74D',
                'background': '#FFF3E0', 
                'accent': '#F57C00'
            },
            'low': {
                'primary': '#F44336',
                'secondary': '#E57373',
                'background': '#FFEBEE',
                'accent': '#C62828'
            },
            'challenging': {
                'primary': '#9C27B0',
                'secondary': '#BA68C8',
                'background': '#F3E5F5',
                'accent': '#7B1FA2'
            }
        }
    
    def generate_odds_image(self, monte_carlo_result, goal_analysis: Dict, 
                          si_factors: Dict, user_name: str = "Anonymous") -> bytes:
        """
        Generate shareable odds image with personalized factors
        
        Returns: Image bytes for saving as JPG
        """
        
        probability = monte_carlo_result.probability_projected
        
        # Determine theme based on probability
        if probability >= 0.7:
            theme = self.color_themes['high']
            emoji = "🚀"
        elif probability >= 0.5:
            theme = self.color_themes['medium']
            emoji = "💪"
        elif probability >= 0.2:
            theme = self.color_themes['challenging']
            emoji = "🎯"
        else:
            theme = self.color_themes['low']
            emoji = "⚡"
        
        # Create image
        img = Image.new('RGB', (self.width, self.height), theme['background'])
        draw = ImageDraw.Draw(img)
        
        # Load fonts (with fallbacks)
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            body_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw header section
        self._draw_header(draw, theme, emoji, title_font, subtitle_font)
        
        # Draw main probability
        self._draw_main_probability(draw, probability, theme, title_font, subtitle_font)
        
        # Draw goal description
        self._draw_goal_description(draw, goal_analysis, theme, body_font, 380)
        
        # Draw key factors
        y_pos = self._draw_key_factors(draw, monte_carlo_result.top_factors, theme, body_font, 460)
        
        # Draw confidence interval
        y_pos = self._draw_confidence_interval(draw, monte_carlo_result.confidence_interval, theme, body_font, y_pos + 40)
        
        # Draw user attribution
        self._draw_user_attribution(draw, user_name, theme, small_font)
        
        # Draw MirrorOS branding
        self._draw_branding(draw, theme, small_font)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
    
    def _draw_header(self, draw, theme: Dict, emoji: str, title_font, subtitle_font):
        """Draw header section with emoji and title"""
        
        # Draw background accent bar
        draw.rectangle([0, 0, self.width, 120], fill=theme['primary'])
        
        # Draw emoji and title
        header_text = f"{emoji} MirrorOS Prediction"
        
        # Center the text
        bbox = draw.textbbox((0, 0), header_text, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        
        draw.text((x, 45), header_text, fill='white', font=subtitle_font)
    
    def _draw_main_probability(self, draw, probability: float, theme: Dict, title_font, subtitle_font):
        """Draw the main probability percentage"""
        
        # Main percentage
        prob_text = f"{probability:.0%}"
        bbox = draw.textbbox((0, 0), prob_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        
        draw.text((x, 180), prob_text, fill=theme['primary'], font=title_font)
        
        # Subtitle
        subtitle_text = "Success Probability"
        bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        
        draw.text((x, 260), subtitle_text, fill=theme['accent'], font=subtitle_font)
    
    def _draw_goal_description(self, draw, goal_analysis: Dict, theme: Dict, font, y_pos: int):
        """Draw goal description"""
        
        goal_text = f"Goal: {goal_analysis.get('objective', 'Personal Goal')}"
        domain_text = f"Domain: {goal_analysis.get('domain', 'general').title()}"
        
        # Center goal text
        bbox = draw.textbbox((0, 0), goal_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, y_pos), goal_text, fill=theme['accent'], font=font)
        
        # Center domain text
        bbox = draw.textbbox((0, 0), domain_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, y_pos + 35), domain_text, fill=theme['secondary'], font=font)
    
    def _draw_key_factors(self, draw, top_factors: List[str], theme: Dict, font, y_pos: int) -> int:
        """Draw key factors affecting probability"""
        
        # Section title
        title_text = "🔑 Key Factors"
        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, y_pos), title_text, fill=theme['primary'], font=font)
        
        current_y = y_pos + 45
        
        # Draw top 3 factors
        for i, factor in enumerate(top_factors[:3]):
            # Clean up factor text
            clean_factor = factor.replace("increases probability", "✅").replace("decreases probability", "⚠️")
            clean_factor = clean_factor.replace("_", " ").title()
            
            # Bullet point
            bullet_text = f"• {clean_factor}"
            
            # Center the text
            bbox = draw.textbbox((0, 0), bullet_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            
            draw.text((x, current_y), bullet_text, fill=theme['accent'], font=font)
            current_y += 35
        
        return current_y
    
    def _draw_confidence_interval(self, draw, confidence_interval, theme: Dict, font, y_pos: int) -> int:
        """Draw confidence interval"""
        
        ci_text = f"📊 Confidence: {confidence_interval[0]:.0%} - {confidence_interval[1]:.0%}"
        
        # Center the text
        bbox = draw.textbbox((0, 0), ci_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        
        draw.text((x, y_pos), ci_text, fill=theme['secondary'], font=font)
        
        return y_pos + 35
    
    def _draw_user_attribution(self, draw, user_name: str, theme: Dict, font):
        """Draw user attribution"""
        
        user_text = f"Generated for {user_name}"
        timestamp = datetime.now().strftime("%B %d, %Y")
        
        # User name
        bbox = draw.textbbox((0, 0), user_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, self.height - 120), user_text, fill=theme['accent'], font=font)
        
        # Timestamp
        bbox = draw.textbbox((0, 0), timestamp, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, self.height - 90), timestamp, fill=theme['secondary'], font=font)
    
    def _draw_branding(self, draw, theme: Dict, font):
        """Draw MirrorOS branding"""
        
        brand_text = "MirrorOS • AI-Powered Future Prediction"
        
        # Center the branding
        bbox = draw.textbbox((0, 0), brand_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        
        draw.text((x, self.height - 40), brand_text, fill=theme['primary'], font=font)
    
    def generate_base64_image(self, monte_carlo_result, goal_analysis: Dict, 
                            si_factors: Dict, user_name: str = "Anonymous") -> str:
        """Generate base64 encoded image for web/mobile use"""
        
        image_bytes = self.generate_odds_image(
            monte_carlo_result, goal_analysis, si_factors, user_name
        )
        
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_string}"
    
    def save_odds_image(self, monte_carlo_result, goal_analysis: Dict, 
                       si_factors: Dict, filename: str, user_name: str = "Anonymous") -> bool:
        """Save odds image to file"""
        
        try:
            image_bytes = self.generate_odds_image(
                monte_carlo_result, goal_analysis, si_factors, user_name
            )
            
            with open(filename, 'wb') as f:
                f.write(image_bytes)
            
            print(f"✅ Shareable odds image saved: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save odds image: {e}")
            return False

def create_shareable_odds_endpoint(monte_carlo_result, goal_analysis: Dict, 
                                 si_factors: Dict, user_name: str = "User") -> Dict:
    """
    Create shareable odds data for API endpoint
    Returns both base64 image and metadata
    """
    
    generator = ShareableOddsGenerator()
    
    try:
        # Generate base64 image
        base64_image = generator.generate_base64_image(
            monte_carlo_result, goal_analysis, si_factors, user_name
        )
        
        # Create sharing metadata
        probability = monte_carlo_result.probability_projected
        
        sharing_data = {
            "shareable_image": {
                "base64_data": base64_image,
                "format": "jpeg",
                "dimensions": {"width": 1080, "height": 1080},
                "size_estimate_kb": len(base64_image) * 3 // 4 // 1024  # Base64 size estimate
            },
            "sharing_text": {
                "short": f"My {goal_analysis.get('domain', 'goal')} success probability: {probability:.0%} 🎯",
                "medium": f"MirrorOS predicts {probability:.0%} success probability for my goal: {goal_analysis.get('objective', 'personal goal')} 📊",
                "long": f"Just got my personalized prediction from MirrorOS! {probability:.0%} success probability for: {goal_analysis.get('objective', 'my goal')}. Key factors: {', '.join(monte_carlo_result.top_factors[:2])} 🚀 #MirrorOS #AI #Goals"
            },
            "social_media_tags": [
                "#MirrorOS", "#AI", "#Goals", "#Prediction", "#Success",
                f"#{goal_analysis.get('domain', 'goal').title()}"
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "user_name": user_name,
                "goal_domain": goal_analysis.get('domain', 'general'),
                "probability": probability,
                "confidence_interval": monte_carlo_result.confidence_interval
            }
        }
        
        return sharing_data
        
    except Exception as e:
        return {
            "error": f"Failed to generate shareable odds: {e}",
            "shareable_image": None,
            "sharing_text": None
        }

# Test function
if __name__ == "__main__":
    # Test the shareable odds generator
    from monte_carlo_si import ProbabilityFactors
    
    # Mock data for testing
    mock_result = ProbabilityFactors(
        probability_projected=0.18,
        target_baseline=0.03,
        confidence_interval=(0.10, 0.25),
        top_factors=[
            "Education increases probability", 
            "Competition decreases probability",
            "Experience increases probability"
        ],
        reasoning_chain=["Analysis complete"]
    )
    
    mock_goal_analysis = {
        'domain': 'career',
        'objective': 'get job at OpenAI',
        'complexity': 'high'
    }
    
    mock_si_factors = {
        'competitiveness_ratio': 0.95,
        'education_ratio': 0.9,
        'experience_years': 2,
        'effort_hours_per_day': 4
    }
    
    # Test image generation
    generator = ShareableOddsGenerator()
    
    # Save test image
    success = generator.save_odds_image(
        mock_result, mock_goal_analysis, mock_si_factors, 
        "test_shareable_odds.jpg", "Test User"
    )
    
    if success:
        print("🎨 Shareable odds image generated successfully!")
        
        # Test API endpoint data
        sharing_data = create_shareable_odds_endpoint(
            mock_result, mock_goal_analysis, mock_si_factors, "Test User"
        )
        
        print(f"📱 Sharing data created:")
        print(f"  Image size: ~{sharing_data['shareable_image']['size_estimate_kb']}KB")
        print(f"  Short text: {sharing_data['sharing_text']['short']}")
        print(f"  Tags: {sharing_data['social_media_tags']}")
    else:
        print("❌ Failed to generate shareable odds image")