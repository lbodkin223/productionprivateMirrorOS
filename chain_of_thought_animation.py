#!/usr/bin/env python3
"""
MirrorOS Chain of Thought with Dynamic Animation
Enhanced reasoning display with step-by-step animated explanations

Following final_plan.md point 13: "Re add chain of thought with dynamic animation"
"""

from typing import List, Dict, Optional
from datetime import datetime
import json

class ChainOfThoughtAnimator:
    """Dynamic animated chain of thought reasoning display"""
    
    def __init__(self):
        self.animation_steps = []
        self.reasoning_timeline = []
    
    def create_animated_chain(self, monte_carlo_result, si_factors: Dict, 
                            goal_analysis: Dict) -> Dict:
        """
        Create animated chain of thought with dynamic step reveals
        
        Returns a structured animation sequence for the mobile app
        """
        
        animation_sequence = {
            "total_steps": 0,
            "animation_duration_ms": 8000,  # 8 seconds total
            "steps": [],
            "final_summary": {},
            "interactive_elements": []
        }
        
        # Step 1: Goal Analysis Animation (1.5 seconds)
        step1 = self._create_goal_analysis_step(goal_analysis, 0, 1500)
        animation_sequence["steps"].append(step1)
        
        # Step 2: Factor Discovery Animation (2 seconds)  
        step2 = self._create_factor_discovery_step(si_factors, 1500, 3500)
        animation_sequence["steps"].append(step2)
        
        # Step 3: SI Units Conversion Animation (2 seconds)
        step3 = self._create_si_conversion_step(si_factors, 3500, 5500)
        animation_sequence["steps"].append(step3)
        
        # Step 4: Monte Carlo Simulation Animation (1.5 seconds)
        step4 = self._create_monte_carlo_step(monte_carlo_result, 5500, 7000)
        animation_sequence["steps"].append(step4)
        
        # Step 5: Final Results Reveal (1 second)
        step5 = self._create_results_reveal_step(monte_carlo_result, 7000, 8000)
        animation_sequence["steps"].append(step5)
        
        animation_sequence["total_steps"] = len(animation_sequence["steps"])
        
        # Create interactive elements for user exploration
        animation_sequence["interactive_elements"] = self._create_interactive_elements(
            monte_carlo_result, si_factors, goal_analysis
        )
        
        # Final summary for quick reference
        animation_sequence["final_summary"] = self._create_final_summary(
            monte_carlo_result, si_factors
        )
        
        return animation_sequence
    
    def _create_goal_analysis_step(self, goal_analysis: Dict, start_ms: int, end_ms: int) -> Dict:
        """Animated goal analysis step"""
        return {
            "step_number": 1,
            "title": "🎯 Goal Analysis",
            "start_time_ms": start_ms,
            "end_time_ms": end_ms,
            "animation_type": "typewriter",
            "content": {
                "primary_text": f"Analyzing: {goal_analysis.get('objective', 'Unknown goal')}",
                "secondary_text": f"Domain: {goal_analysis.get('domain', 'general').title()}",
                "complexity_indicator": goal_analysis.get('complexity', 'medium'),
                "progress_bar": True
            },
            "visual_effects": {
                "icon_animation": "pulse",
                "background_color": "#E3F2FD",
                "text_color": "#1976D2"
            }
        }
    
    def _create_factor_discovery_step(self, si_factors: Dict, start_ms: int, end_ms: int) -> Dict:
        """Animated factor discovery step"""
        
        # Count different types of factors
        factor_types = []
        if any(k in si_factors for k in ['education_ratio', 'experience_years']):
            factor_types.append("📚 Background")
        if any(k in si_factors for k in ['effort_hours_per_day', 'time_seconds']):
            factor_types.append("⏰ Commitment")  
        if any(k in si_factors for k in ['competitiveness_ratio', 'target_entity_name']):
            factor_types.append("🎯 Target")
        if any(k in si_factors for k in ['age_years']):
            factor_types.append("👤 Demographics")
        
        return {
            "step_number": 2,
            "title": "🔍 Factor Discovery",
            "start_time_ms": start_ms,
            "end_time_ms": end_ms,
            "animation_type": "cascade_reveal",
            "content": {
                "primary_text": f"Identified {len(si_factors)} key factors",
                "factor_categories": factor_types,
                "discovery_sequence": [
                    {"factor": cat, "delay_ms": i * 400} 
                    for i, cat in enumerate(factor_types)
                ]
            },
            "visual_effects": {
                "icon_animation": "bounce_in",
                "background_color": "#F3E5F5",
                "text_color": "#7B1FA2",
                "particle_effect": "discovery_sparkles"
            }
        }
    
    def _create_si_conversion_step(self, si_factors: Dict, start_ms: int, end_ms: int) -> Dict:
        """Animated SI units conversion step"""
        
        conversions = []
        
        # Show key conversions with animation
        if 'competitiveness_ratio' in si_factors:
            comp = si_factors['competitiveness_ratio']
            if comp >= 0.95:
                conversions.append({
                    "from": "Target Company", 
                    "to": f"Competitiveness: {comp:.0%}",
                    "animation": "scale_up"
                })
        
        if 'effort_hours_per_day' in si_factors:
            hours = si_factors['effort_hours_per_day']
            conversions.append({
                "from": f"{hours} hours/day",
                "to": f"Effort Index: {hours:.1f}",
                "animation": "slide_transform"
            })
        
        if 'education_ratio' in si_factors:
            edu = si_factors['education_ratio'] 
            conversions.append({
                "from": "Educational Background",
                "to": f"Education Score: {edu:.0%}",
                "animation": "fade_morph"
            })
        
        return {
            "step_number": 3,
            "title": "🔬 Quantification",
            "start_time_ms": start_ms,
            "end_time_ms": end_ms,
            "animation_type": "transformation",
            "content": {
                "primary_text": "Converting to standardized metrics",
                "conversions": conversions,
                "transformation_sequence": [
                    {"conversion": conv, "delay_ms": i * 500}
                    for i, conv in enumerate(conversions)
                ]
            },
            "visual_effects": {
                "icon_animation": "rotate_transform",
                "background_color": "#E8F5E8", 
                "text_color": "#2E7D32",
                "particle_effect": "conversion_glow"
            }
        }
    
    def _create_monte_carlo_step(self, monte_carlo_result, start_ms: int, end_ms: int) -> Dict:
        """Animated Monte Carlo simulation step"""
        return {
            "step_number": 4,
            "title": "🎲 Simulation",
            "start_time_ms": start_ms,
            "end_time_ms": end_ms,
            "animation_type": "progress_simulation",
            "content": {
                "primary_text": "Running 10,000 scenarios...",
                "simulation_progress": {
                    "total_scenarios": 10000,
                    "animation_speed": "fast",
                    "progress_indicators": ["⚡", "📊", "🔄", "✅"]
                },
                "convergence_display": {
                    "show_probability_convergence": True,
                    "final_value": monte_carlo_result.probability_projected
                }
            },
            "visual_effects": {
                "icon_animation": "spinning_dice",
                "background_color": "#FFF3E0",
                "text_color": "#F57C00", 
                "particle_effect": "simulation_particles"
            }
        }
    
    def _create_results_reveal_step(self, monte_carlo_result, start_ms: int, end_ms: int) -> Dict:
        """Animated results reveal step"""
        
        probability = monte_carlo_result.probability_projected
        
        # Determine reveal style based on probability
        if probability >= 0.7:
            reveal_style = "celebration"
            color_theme = "#4CAF50"
        elif probability >= 0.3:
            reveal_style = "confident"
            color_theme = "#FF9800"
        else:
            reveal_style = "realistic"
            color_theme = "#F44336"
        
        return {
            "step_number": 5,
            "title": "🎯 Final Assessment",
            "start_time_ms": start_ms, 
            "end_time_ms": end_ms,
            "animation_type": "dramatic_reveal",
            "content": {
                "primary_text": f"{probability:.1%}",
                "secondary_text": "Success Probability",
                "confidence_interval": monte_carlo_result.confidence_interval,
                "reveal_style": reveal_style
            },
            "visual_effects": {
                "icon_animation": reveal_style,
                "background_color": f"{color_theme}20",  # 20% opacity
                "text_color": color_theme,
                "particle_effect": f"{reveal_style}_burst"
            }
        }
    
    def _create_interactive_elements(self, monte_carlo_result, si_factors: Dict, 
                                   goal_analysis: Dict) -> List[Dict]:
        """Create interactive elements for user exploration"""
        
        interactive_elements = []
        
        # Factor Impact Explorer
        interactive_elements.append({
            "type": "factor_impact_slider",
            "title": "🔧 Factor Impact Explorer",
            "description": "Adjust factors to see how they impact your probability",
            "factors": [
                {
                    "name": "Effort Level",
                    "current_value": si_factors.get('effort_hours_per_day', 2),
                    "min_value": 0,
                    "max_value": 12,
                    "unit": "hours/day",
                    "impact_weight": "high"
                },
                {
                    "name": "Experience",
                    "current_value": si_factors.get('experience_years', 2),
                    "min_value": 0,
                    "max_value": 20,
                    "unit": "years",
                    "impact_weight": "medium"
                }
            ]
        })
        
        # Comparison Tool
        interactive_elements.append({
            "type": "baseline_comparison",
            "title": "📊 Baseline Comparison",
            "description": "See how your probability compares to others",
            "comparisons": [
                {
                    "category": "Average Person",
                    "probability": monte_carlo_result.target_baseline,
                    "your_advantage": monte_carlo_result.probability_projected - monte_carlo_result.target_baseline
                },
                {
                    "category": "Your Profile",
                    "probability": monte_carlo_result.probability_projected,
                    "factors": monte_carlo_result.top_factors[:2]
                }
            ]
        })
        
        # Success Timeline
        interactive_elements.append({
            "type": "success_timeline", 
            "title": "📅 Success Timeline",
            "description": "Key milestones for achieving your goal",
            "milestones": self._generate_success_milestones(goal_analysis, si_factors)
        })
        
        return interactive_elements
    
    def _create_final_summary(self, monte_carlo_result, si_factors: Dict) -> Dict:
        """Create final summary for quick reference"""
        return {
            "probability": f"{monte_carlo_result.probability_projected:.1%}",
            "confidence_range": f"{monte_carlo_result.confidence_interval[0]:.1%} - {monte_carlo_result.confidence_interval[1]:.1%}",
            "key_strengths": [factor for factor in monte_carlo_result.top_factors if "increase" in factor.lower()][:2],
            "key_challenges": [factor for factor in monte_carlo_result.top_factors if "decrease" in factor.lower()][:2],
            "next_steps": self._generate_next_steps(monte_carlo_result, si_factors)
        }
    
    def _generate_success_milestones(self, goal_analysis: Dict, si_factors: Dict) -> List[Dict]:
        """Generate success timeline milestones"""
        domain = goal_analysis.get('domain', 'general')
        
        if domain == 'career':
            return [
                {"milestone": "Skill Development", "timeframe": "1-3 months", "priority": "high"},
                {"milestone": "Application Preparation", "timeframe": "2-4 weeks", "priority": "high"},
                {"milestone": "Interview Process", "timeframe": "1-2 months", "priority": "medium"},
                {"milestone": "Goal Achievement", "timeframe": "3-6 months", "priority": "high"}
            ]
        elif domain == 'fitness':
            return [
                {"milestone": "Training Plan Setup", "timeframe": "1 week", "priority": "high"},
                {"milestone": "Initial Progress", "timeframe": "1 month", "priority": "medium"},
                {"milestone": "Midpoint Assessment", "timeframe": "2-3 months", "priority": "medium"},
                {"milestone": "Goal Achievement", "timeframe": "4-6 months", "priority": "high"}
            ]
        else:
            return [
                {"milestone": "Planning Phase", "timeframe": "2 weeks", "priority": "high"},
                {"milestone": "Implementation", "timeframe": "1-3 months", "priority": "high"},
                {"milestone": "Progress Review", "timeframe": "3-4 months", "priority": "medium"},
                {"milestone": "Goal Achievement", "timeframe": "6 months", "priority": "high"}
            ]
    
    def _generate_next_steps(self, monte_carlo_result, si_factors: Dict) -> List[str]:
        """Generate actionable next steps"""
        steps = []
        
        # Based on weakest factors
        if si_factors.get('effort_hours_per_day', 0) < 2:
            steps.append("Increase daily time commitment")
        
        if si_factors.get('experience_years', 0) < 2:
            steps.append("Build relevant experience through projects")
        
        if si_factors.get('education_ratio', 0) < 0.8:
            steps.append("Consider additional training or certification")
        
        # Default steps if no specific weaknesses
        if not steps:
            steps = [
                "Maintain current momentum",
                "Monitor progress regularly", 
                "Adjust strategy based on results"
            ]
        
        return steps[:3]  # Return top 3

# Test function
if __name__ == "__main__":
    # Test the chain of thought animator
    from monte_carlo_si import MonteCarloSI, ProbabilityFactors
    
    # Mock monte carlo result for testing
    mock_result = ProbabilityFactors(
        probability_projected=0.18,
        target_baseline=0.03,
        confidence_interval=(0.10, 0.25),
        top_factors=["Education increases probability", "Competition decreases probability"],
        reasoning_chain=["Goal analysis complete", "Factors identified", "Simulation complete"]
    )
    
    mock_si_factors = {
        'competitiveness_ratio': 0.95,
        'education_ratio': 0.9,
        'experience_years': 2,
        'effort_hours_per_day': 4
    }
    
    mock_goal_analysis = {
        'domain': 'career',
        'objective': 'get job at openai',
        'complexity': 'high'
    }
    
    animator = ChainOfThoughtAnimator()
    animation_sequence = animator.create_animated_chain(
        mock_result, mock_si_factors, mock_goal_analysis
    )
    
    print("🎬 Chain of Thought Animation Created:")
    print(f"Total Steps: {animation_sequence['total_steps']}")
    print(f"Duration: {animation_sequence['animation_duration_ms']}ms")
    print(f"Interactive Elements: {len(animation_sequence['interactive_elements'])}")
    
    for step in animation_sequence['steps']:
        print(f"  Step {step['step_number']}: {step['title']} ({step['end_time_ms'] - step['start_time_ms']}ms)")