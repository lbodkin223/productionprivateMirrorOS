#!/usr/bin/env python3
"""
MirrorOS Monte Carlo Engine with SI Units
Advanced probability calculation using SI factors and standardized ratios

Following final_plan.md architecture:
factor_one (operator) factor_two... = probability_projected
Compare probability_projected to target_baseline from RAG
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import math
from dataclasses import dataclass

@dataclass
class ProbabilityFactors:
    """Container for probability calculation factors"""
    probability_projected: float  # Our calculated probability
    target_baseline: float       # Real-world baseline from RAG
    confidence_interval: Tuple[float, float]
    top_factors: List[str]       # Top 3 factors impacting probability
    reasoning_chain: List[str]   # Chain of thought steps

class MonteCarloSI:
    """Monte Carlo engine optimized for SI units and standardized ratios"""
    
    def __init__(self):
        # Domain-specific baseline probabilities (from historical data/RAG)
        self.domain_baselines = {
            'career': {
                'software_engineer_general': 0.65,
                'faang_company': 0.08,
                'top_tier_company': 0.03,  # OpenAI, Google, etc.
                'startup': 0.45,
                'promotion': 0.25
            },
            'finance': {
                'salary_increase_20pct': 0.35,
                'startup_success': 0.10,
                'investment_double': 0.30,
                'millionaire_by_40': 0.05
            },
            'fitness': {
                'weight_loss_50lbs': 0.20,
                'marathon_sub3': 0.15,
                'muscle_gain_20lbs': 0.40
            },
            'academic': {
                'top_school_admission': 0.12,
                'phd_completion': 0.60,
                'gpa_increase': 0.45
            }
        }
    
    def calculate_probability(self, si_factors: Dict, goal_analysis: Dict, 
                            probability_factors: Dict, num_simulations: int = 10000) -> ProbabilityFactors:
        """
        Main Monte Carlo probability calculation using SI factors
        
        Args:
            si_factors: Dict of SI units and ratios from extraction
            goal_analysis: Goal objective, domain, complexity
            probability_factors: Positive/negative factors
            num_simulations: Number of Monte Carlo simulations
        """
        
        print(f"🎲 Monte Carlo SI Engine Starting")
        print(f"📊 Factors: {si_factors}")
        print(f"🎯 Goal: {goal_analysis}")
        
        # Step 1: Get baseline probability for this domain/goal type
        baseline = self._get_baseline_probability(goal_analysis, si_factors)
        print(f"📈 Baseline probability: {baseline:.1%}")
        
        # Step 2: Calculate factor multipliers
        multipliers, reasoning = self._calculate_factor_multipliers(si_factors)
        print(f"🔢 Multipliers: {multipliers}")
        
        # Step 3: Run Monte Carlo simulation
        probability_projected = self._run_monte_carlo_simulation(
            baseline, multipliers, num_simulations
        )
        
        # Step 4: Calculate confidence interval
        confidence_interval = self._calculate_confidence_interval(
            baseline, multipliers, num_simulations
        )
        
        # Step 5: Extract top 3 factors
        top_factors = self._get_top_factors(multipliers, probability_factors)
        
        # Step 6: Build reasoning chain
        reasoning_chain = self._build_reasoning_chain(
            baseline, multipliers, probability_projected, reasoning
        )
        
        return ProbabilityFactors(
            probability_projected=probability_projected,
            target_baseline=baseline,
            confidence_interval=confidence_interval,
            top_factors=top_factors,
            reasoning_chain=reasoning_chain
        )
    
    def _get_baseline_probability(self, goal_analysis: Dict, si_factors: Dict) -> float:
        """Get baseline probability from domain and goal type"""
        domain = goal_analysis.get('domain', 'career')
        
        # Check for company competitiveness
        if 'competitiveness_ratio' in si_factors:
            comp_ratio = si_factors['competitiveness_ratio']
            if comp_ratio >= 0.95:  # OpenAI, Google level
                return self.domain_baselines.get(domain, {}).get('top_tier_company', 0.03)
            elif comp_ratio >= 0.9:  # FAANG level
                return self.domain_baselines.get(domain, {}).get('faang_company', 0.08)
        
        # Default domain baseline
        domain_defaults = {
            'career': 0.50,
            'finance': 0.40,
            'fitness': 0.35,
            'academic': 0.30,
            'business': 0.25,
            'dating': 0.40,
            'travel': 0.70
        }
        
        return domain_defaults.get(domain, 0.50)
    
    def _calculate_factor_multipliers(self, si_factors: Dict) -> Tuple[Dict[str, float], Dict[str, str]]:
        """Calculate multiplier effects for each factor"""
        multipliers = {}
        reasoning = {}
        
        # Education multiplier (using ratio 0.0-1.0)
        if 'education_ratio' in si_factors:
            edu_ratio = si_factors['education_ratio']
            if edu_ratio >= 0.9:  # Top tier (Harvard, MIT, Stanford)
                multipliers['education'] = 1.8
                reasoning['education'] = f"Top-tier education (ratio: {edu_ratio:.2f}) provides significant advantage"
            elif edu_ratio >= 0.8:  # Graduate degree
                multipliers['education'] = 1.4
                reasoning['education'] = f"Graduate education (ratio: {edu_ratio:.2f}) enhances prospects"
            elif edu_ratio >= 0.7:  # Bachelor's
                multipliers['education'] = 1.2
                reasoning['education'] = f"College education (ratio: {edu_ratio:.2f}) provides good foundation"
            else:
                multipliers['education'] = 0.9
                reasoning['education'] = f"Limited formal education (ratio: {edu_ratio:.2f}) may be challenging"
        
        # Effort level multiplier (hours per day)
        if 'effort_hours_per_day' in si_factors:
            hours = si_factors['effort_hours_per_day']
            if hours >= 8:
                multipliers['effort'] = 2.0
                reasoning['effort'] = f"Exceptional effort ({hours}h/day) significantly increases success probability"
            elif hours >= 4:
                multipliers['effort'] = 1.5
                reasoning['effort'] = f"High effort ({hours}h/day) improves outcomes substantially"
            elif hours >= 2:
                multipliers['effort'] = 1.2
                reasoning['effort'] = f"Good effort ({hours}h/day) provides moderate advantage"
            elif hours >= 1:
                multipliers['effort'] = 1.0
                reasoning['effort'] = f"Minimal effort ({hours}h/day) maintains baseline probability"
            else:
                multipliers['effort'] = 0.7
                reasoning['effort'] = f"Very low effort ({hours}h/day) reduces success probability"
        
        # Experience multiplier (years)
        if 'experience_years' in si_factors:
            years = si_factors['experience_years']
            if years >= 10:
                multipliers['experience'] = 1.8
                reasoning['experience'] = f"Extensive experience ({years} years) provides major advantage"
            elif years >= 5:
                multipliers['experience'] = 1.4
                reasoning['experience'] = f"Solid experience ({years} years) enhances prospects"
            elif years >= 2:
                multipliers['experience'] = 1.1
                reasoning['experience'] = f"Some experience ({years} years) provides slight edge"
            else:
                multipliers['experience'] = 0.9
                reasoning['experience'] = f"Limited experience ({years} years) may be challenging"
        
        # Age factor (sweet spot analysis)
        if 'age_years' in si_factors:
            age = si_factors['age_years']
            if 22 <= age <= 35:  # Prime career building years
                multipliers['age'] = 1.3
                reasoning['age'] = f"Optimal age ({age}) for career advancement and goal achievement"
            elif 18 <= age <= 45:  # Still good range
                multipliers['age'] = 1.1
                reasoning['age'] = f"Good age ({age}) for pursuing goals with energy and time"
            else:
                multipliers['age'] = 1.0
                reasoning['age'] = f"Age ({age}) has neutral impact on probability"
        
        # Competitiveness penalty
        if 'competitiveness_ratio' in si_factors:
            comp_ratio = si_factors['competitiveness_ratio']
            if comp_ratio >= 0.95:  # Extremely competitive (OpenAI)
                multipliers['competition'] = 0.15
                reasoning['competition'] = f"Extremely competitive target (ratio: {comp_ratio:.2f}) - acceptance rate <2%"
            elif comp_ratio >= 0.9:  # Very competitive (FAANG)
                multipliers['competition'] = 0.25
                reasoning['competition'] = f"Highly competitive target (ratio: {comp_ratio:.2f}) - acceptance rate ~5%"
            elif comp_ratio >= 0.8:  # Competitive
                multipliers['competition'] = 0.6
                reasoning['competition'] = f"Competitive target (ratio: {comp_ratio:.2f}) - moderate difficulty"
            else:
                multipliers['competition'] = 1.0
                reasoning['competition'] = f"Standard competitiveness (ratio: {comp_ratio:.2f})"
        
        # Timeline factor (if time pressure exists)
        if 'time_seconds' in si_factors:
            seconds = si_factors['time_seconds']
            months = seconds / (30 * 24 * 3600)  # Convert to months approximation
            if months < 3:
                multipliers['timeline'] = 0.7
                reasoning['timeline'] = f"Very tight timeline ({months:.1f} months) creates pressure"
            elif months > 36:
                multipliers['timeline'] = 0.9
                reasoning['timeline'] = f"Very long timeline ({months:.1f} months) may reduce urgency"
            else:
                multipliers['timeline'] = 1.0
                reasoning['timeline'] = f"Reasonable timeline ({months:.1f} months)"
        
        return multipliers, reasoning
    
    def _run_monte_carlo_simulation(self, baseline: float, multipliers: Dict[str, float], 
                                  num_simulations: int) -> float:
        """Run Monte Carlo simulation with factor variations"""
        
        # Convert baseline probability to logit space for better multiplication
        baseline_logit = math.log(baseline / (1 - baseline))
        
        results = []
        
        for _ in range(num_simulations):
            # Start with baseline logit
            current_logit = baseline_logit
            
            # Apply each multiplier with some random variation
            for factor, multiplier in multipliers.items():
                # Add random variation (±20% of multiplier effect)
                variation = np.random.normal(1.0, 0.2)
                adjusted_multiplier = multiplier * variation
                
                # Convert multiplier to logit adjustment
                if adjusted_multiplier > 1.0:
                    # Positive factor - add to logit
                    logit_adjustment = math.log(adjusted_multiplier)
                else:
                    # Negative factor - subtract from logit
                    # Clamp to prevent math domain errors
                    adjusted_multiplier = max(0.001, adjusted_multiplier)
                    logit_adjustment = -math.log(1.0 / adjusted_multiplier)
                
                current_logit += logit_adjustment
            
            # Convert back to probability space
            probability = 1 / (1 + math.exp(-current_logit))
            
            # Clamp to reasonable bounds
            probability = max(0.001, min(0.999, probability))
            results.append(probability)
        
        # Return median result for stability
        return float(np.median(results))
    
    def _calculate_confidence_interval(self, baseline: float, multipliers: Dict[str, float], 
                                     num_simulations: int) -> Tuple[float, float]:
        """Calculate 90% confidence interval"""
        
        baseline_logit = math.log(baseline / (1 - baseline))
        results = []
        
        for _ in range(num_simulations):
            current_logit = baseline_logit
            
            for factor, multiplier in multipliers.items():
                variation = np.random.normal(1.0, 0.3)  # More variation for CI
                adjusted_multiplier = multiplier * variation
                
                if adjusted_multiplier > 1.0:
                    logit_adjustment = math.log(adjusted_multiplier)
                else:
                    # Clamp to prevent math domain errors
                    adjusted_multiplier = max(0.001, adjusted_multiplier)
                    logit_adjustment = -math.log(1.0 / adjusted_multiplier)
                
                current_logit += logit_adjustment
            
            probability = 1 / (1 + math.exp(-current_logit))
            probability = max(0.001, min(0.999, probability))
            results.append(probability)
        
        # 90% confidence interval (5th and 95th percentiles)
        lower = float(np.percentile(results, 5))
        upper = float(np.percentile(results, 95))
        
        return (lower, upper)
    
    def _get_top_factors(self, multipliers: Dict[str, float], 
                        probability_factors: Dict) -> List[str]:
        """Extract top 3 factors impacting probability"""
        
        # Sort multipliers by absolute impact (distance from 1.0)
        factor_impacts = []
        for factor, multiplier in multipliers.items():
            impact = abs(math.log(multiplier))  # Logarithmic distance from 1.0
            factor_impacts.append((factor, impact, multiplier))
        
        # Sort by impact magnitude
        factor_impacts.sort(key=lambda x: x[1], reverse=True)
        
        # Build descriptive strings for top 3
        top_factors = []
        for factor, impact, multiplier in factor_impacts[:3]:
            if multiplier > 1.0:
                direction = "increases"
            else:
                direction = "decreases" 
            
            top_factors.append(f"{factor.replace('_', ' ').title()} {direction} probability")
        
        return top_factors
    
    def _build_reasoning_chain(self, baseline: float, multipliers: Dict[str, float], 
                             final_probability: float, reasoning: Dict[str, str]) -> List[str]:
        """Build chain of thought reasoning steps"""
        
        chain = [
            f"🎯 **Goal Analysis**: Baseline success rate for this goal type: {baseline:.1%}",
            f"📊 **Factor Analysis**: Identified {len(multipliers)} key factors affecting probability"
        ]
        
        # Add reasoning for each significant factor
        for factor, explanation in reasoning.items():
            if factor in multipliers:
                multiplier = multipliers[factor]
                if abs(math.log(multiplier)) > 0.1:  # Only include significant factors
                    chain.append(f"• {explanation}")
        
        chain.extend([
            f"⚖️ **Monte Carlo Analysis**: Simulated 10,000 scenarios with factor variations",
            f"🎯 **Final Assessment**: {final_probability:.1%} probability based on combined factor analysis"
        ])
        
        return chain

# Test function
if __name__ == "__main__":
    # Test the Monte Carlo SI engine
    monte_carlo = MonteCarloSI()
    
    # Test case: OpenAI job application
    si_factors = {
        'competitiveness_ratio': 0.95,
        'education_ratio': 0.9,
        'experience_years': 2,
        'age_years': 23,
        'effort_hours_per_day': 4
    }
    
    goal_analysis = {
        'domain': 'career',
        'objective': 'get job at openai',
        'complexity': 'high'
    }
    
    probability_factors = {
        'positive_factors': ['strong education', 'relevant experience'],
        'negative_factors': ['extremely competitive', 'limited experience']
    }
    
    result = monte_carlo.calculate_probability(si_factors, goal_analysis, probability_factors)
    
    print(f"\n🎯 MONTE CARLO RESULTS:")
    print(f"Probability Projected: {result.probability_projected:.1%}")
    print(f"Target Baseline: {result.target_baseline:.1%}")
    print(f"Confidence Interval: {result.confidence_interval[0]:.1%} - {result.confidence_interval[1]:.1%}")
    print(f"Top Factors: {result.top_factors}")
    print(f"Reasoning Chain: {len(result.reasoning_chain)} steps")