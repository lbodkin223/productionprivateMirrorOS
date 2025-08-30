#!/usr/bin/env python3
"""
MirrorOS SI Units LLM Extractor
Revolutionary natural language to SI units conversion system

Following final_plan.md:
1. Find goal: "What does the user wish to accomplish or know?"
2. Extract factors: "What factors from context are relevant to this query?"
3. Quantify in SI units or create appropriate ratios
4. Convert to base metric units
5. Remove need for USV library - direct LLM to int conversion
"""

import os
import json
import requests
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# REMOVED: SIUnitsExtractor class - no longer needed
# The sequential pipeline now uses lm_extractor.py → convert_llm_to_si() → Monte Carlo

def si_extraction_pipeline(goal: str, context: str) -> Optional[Dict]:
    """
    Sequential pipeline: Natural Language → LM Extractor → SI Units Converter → Monte Carlo → Result
    
    Fixed to use existing lm_extractor.py then convert to SI units
    """
    # Step 1: Use the EXISTING lm_extractor to get integers
    from lm_extractor import full_extraction_pipeline
    llm_result = full_extraction_pipeline(goal, context)
    
    if not llm_result:
        return None
    
    # Step 2: Convert LLM integers to SI units/ratios
    si_factors = convert_llm_to_si(llm_result['standardized_data'])
    
    # Step 3: Package for Monte Carlo
    return {
        'goal_analysis': {
            'domain': llm_result['domain'],
            'objective': llm_result['goal'],
            'complexity': 'high' if llm_result.get('standardized_data', {}).get('selectivity_score', 0) > 90 else 'medium'
        },
        'extracted_factors': si_factors,
        'probability_factors': {
            'positive_factors': [],
            'negative_factors': []
        }
    }

def convert_llm_to_si(standardized_data: dict) -> dict:
    """
    Convert LLM extractor output to SI units and standardized ratios
    
    This bridges the gap between lm_extractor.py output and Monte Carlo input
    """
    si_factors = {}
    
    # Direct mappings
    if 'age' in standardized_data:
        si_factors['age_years'] = standardized_data['age']
    
    if 'hours_per_day' in standardized_data:
        si_factors['effort_hours_per_day'] = standardized_data['hours_per_day']
    
    if 'timeline_months' in standardized_data:
        si_factors['time_seconds'] = standardized_data['timeline_months'] * 30 * 24 * 3600
    
    # Convert selectivity score (0-100) to ratio (0-1)
    if 'selectivity_score' in standardized_data:
        si_factors['competitiveness_ratio'] = standardized_data['selectivity_score'] / 100.0
    
    # Convert education score (0-100) to ratio (0-1)
    if 'education_score' in standardized_data:
        si_factors['education_ratio'] = standardized_data['education_score'] / 100.0
    
    # Years of experience
    if 'experience_years' in standardized_data:
        si_factors['experience_years'] = standardized_data['experience_years']
    
    # Target company information
    if 'target_company' in standardized_data:
        si_factors['target_entity_name'] = standardized_data['target_company']
        si_factors['target_entity_type'] = 'company'
    
    print(f"📊 LLM → SI Conversion: {standardized_data} → {si_factors}")
    return si_factors

# Test function
if __name__ == "__main__":
    # Test the sequential pipeline
    print("🧪 Testing Sequential Pipeline")
    print("Natural Language → LM Extractor → SI Units Converter → Monte Carlo")
    
    result = si_extraction_pipeline(
        "I want a job at OpenAI",
        "CS grad, 2 years experience"
    )
    print(f"\n✅ Result: {result}")