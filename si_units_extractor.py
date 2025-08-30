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

class SIUnitsExtractor:
    """Advanced LLM-powered extraction system using SI units and ratios"""
    
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Add validation per Claude Code recommendation
        if not self.openai_key and not self.anthropic_key:
            print("⚠️ WARNING: No API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
        elif self.openai_key and not self.openai_key.startswith('sk-'):
            print("⚠️ WARNING: OpenAI API key format appears invalid (should start with 'sk-')")
        elif self.anthropic_key and not self.anthropic_key.startswith('sk-ant-'):
            print("⚠️ WARNING: Anthropic API key format appears invalid (should start with 'sk-ant-')")
        
    def extract_goal_and_si_factors(self, goal: str, context: str) -> Optional[Dict]:
        """
        Complete extraction pipeline: Goal + Context -> SI Units + Ratios -> Integers
        
        New architecture per final_plan.md:
        input parser -> lm api -> SI quantification -> int -> monte carlo engine
        """
        print(f"🔬 SI Units Extraction Pipeline")
        print(f"📝 Goal: '{goal}'")
        print(f"📋 Context: '{context}'")
        
        # Try Anthropic first, then OpenAI fallback
        result = self._try_anthropic_si_extraction(goal, context)
        if result:
            return result
            
        result = self._try_openai_si_extraction(goal, context)
        if result:
            return result
            
        print("❌ Both Anthropic and OpenAI SI extraction failed")
        return None
    
    def _try_anthropic_si_extraction(self, goal: str, context: str) -> Optional[Dict]:
        """Try Anthropic Claude for SI units extraction"""
        if not self.anthropic_key:
            print("⚠️ No Anthropic API key available")
            return None
            
        api_url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        prompt = self._build_si_extraction_prompt(goal, context)
        
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 800,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['content'][0]['text'].strip()
            
            # Extract JSON from the response (Claude often adds explanatory text)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                parsed = json.loads(json_content)
                print(f"🎯 Anthropic SI Extraction Success")
                return self._process_si_extraction_result(parsed)
            else:
                raise Exception("No JSON found in response")
            
        except Exception as e:
            print(f"❌ Anthropic SI extraction failed: {e}")
            return None
    
    def _try_openai_si_extraction(self, goal: str, context: str) -> Optional[Dict]:
        """Try OpenAI GPT-4o for SI units extraction"""
        if not self.openai_key:
            print("⚠️ No OpenAI API key available")
            return None
            
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        prompt = self._build_si_extraction_prompt(goal, context)
        
        payload = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Extract JSON from the response (GPT might also add explanatory text)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                parsed = json.loads(json_content)
                print(f"🎯 OpenAI SI Extraction Success")
                return self._process_si_extraction_result(parsed)
            else:
                raise Exception("No JSON found in response")
            
        except Exception as e:
            print(f"❌ OpenAI SI extraction failed: {e}")
            return None
    
    def _build_si_extraction_prompt(self, goal: str, context: str) -> str:
        """Build the revolutionary SI units extraction prompt"""
        return f'''You are an expert natural language processor that converts user goals and context into precise SI units and standardized ratios.

TASK: Analyze the user's goal and context, then extract and quantify ALL relevant factors using SI base units or create appropriate ratios.

USER GOAL: "{goal}"
USER CONTEXT: "{context}"

STEP 1: GOAL ANALYSIS
- What exactly does the user wish to accomplish or know?
- What domain does this belong to? (career, finance, fitness, academic, business, dating, travel)

STEP 2: FACTOR EXTRACTION
- What factors from the context are relevant to achieving this goal?
- Identify ALL quantifiable elements (time, money, effort, experience, demographics, etc.)

STEP 3: SI UNITS QUANTIFICATION
Convert each factor to SI base units or create standardized ratios:

SI BASE UNITS:
- Time: seconds (s) - convert hours/days/months/years to seconds
- Mass: kilograms (kg) - for weight/fitness goals
- Distance: meters (m) - for running/travel distances
- Money: Convert to smallest currency unit (cents for USD)
- Temperature: Kelvin (K) - if relevant

STANDARDIZED RATIOS (when no SI unit exists):
- Education Level: 0.0-1.0 ratio (0.7=bachelor's, 0.8=master's, 0.9=PhD, 0.95=top school)
- Company Competitiveness: 0.0-1.0 ratio (0.95=OpenAI/Google, 0.9=FAANG, 0.8=Fortune 500)
- Experience Level: years as decimal (5.5 years = 5.5)
- Age: years as integer
- Effort Level: hours per day as decimal (4.5 hours/day = 4.5)

CRITICAL REQUIREMENTS (per final_plan.md):
1. Recognize company name variations: "OpenAI", "open ai", "OPENAI" are ALL the same company
2. Extract ALL quantifiable factors from the context  
3. Convert everything to base SI units or standardized ratios
4. DO NOT default to old vector system - extract actual values

COMPANY NAME NORMALIZATION (CRITICAL):
- Treat all variations as identical: "OpenAI"/"open ai"/"OPENAI" = same entity
- "Google"/"google"/"GOOGLE" = same entity
- "Apple"/"apple"/"APPLE" = same entity  
- "Microsoft"/"microsoft"/"MICROSOFT" = same entity
- Normalize to lowercase in the output for consistency
- ALL variations should get same competitiveness_ratio:
  * "OpenAI"/"open ai"/"OPENAI" → competitiveness_ratio: 0.95
  * "Google"/"google"/"GOOGLE" → competitiveness_ratio: 0.95
  * "Apple"/"apple"/"APPLE" → competitiveness_ratio: 0.9
  * "Microsoft"/"microsoft"/"MICROSOFT" → competitiveness_ratio: 0.85

STEP 4: OUTPUT FORMAT
Return JSON with:
{{
    "goal_analysis": {{
        "objective": "clear description of what user wants to achieve",
        "domain": "career/finance/fitness/academic/business/dating/travel",
        "complexity": "low/medium/high"
    }},
    "si_factors": {{
        "time_seconds": null_or_number,
        "effort_hours_per_day": null_or_number,
        "money_cents": null_or_number,
        "distance_meters": null_or_number,
        "mass_kg": null_or_number
    }},
    "ratio_factors": {{
        "education_ratio": null_or_0_to_1,
        "competitiveness_ratio": null_or_0_to_1,
        "experience_years": null_or_number,
        "age_years": null_or_number
    }},
    "target_entity": {{
        "type": "company/school/person/location/other",
        "name": "standardized_name",
        "competitiveness_ratio": null_or_0_to_1
    }},
    "probability_factors": {{
        "positive_factors": ["list of factors that increase success probability"],
        "negative_factors": ["list of factors that decrease success probability"]
    }}
}}

EXAMPLES:
Goal: "I want a job at open ai" | Context: "Northwestern grad, age 23"
→ target_entity: {{"type": "company", "name": "openai", "competitiveness_ratio": 0.95}}
→ education_ratio: 0.9 (Northwestern = top school)
→ age_years: 23

Goal: "Run marathon in 3 hours" | Context: "Currently run 5 miles in 45 minutes"
→ time_seconds: 10800 (3 hours = 10800 seconds)
→ distance_meters: 42195 (marathon = 42,195 meters)
→ Current pace extracted from context

Be extremely precise and consistent with company name recognition!'''

    def _process_si_extraction_result(self, parsed_result: Dict) -> Dict:
        """Process and validate the SI extraction result"""
        
        # Combine SI units and ratios into a unified factors dictionary
        factors = {}
        
        # Add SI units (converted to base units)
        si_factors = parsed_result.get('si_factors', {})
        for key, value in si_factors.items():
            if value is not None:
                factors[key] = value
        
        # Add ratio factors
        ratio_factors = parsed_result.get('ratio_factors', {})
        for key, value in ratio_factors.items():
            if value is not None:
                factors[key] = value
        
        # Add target entity information
        target_entity = parsed_result.get('target_entity', {})
        if target_entity.get('name'):
            factors['target_entity_name'] = target_entity['name']
            factors['target_entity_type'] = target_entity['type']
            if target_entity.get('competitiveness_ratio'):
                factors['competitiveness_ratio'] = target_entity['competitiveness_ratio']
        
        result = {
            'goal_analysis': parsed_result.get('goal_analysis', {}),
            'extracted_factors': factors,
            'probability_factors': parsed_result.get('probability_factors', {}),
            'raw_llm_response': parsed_result
        }
        
        print(f"📊 Processed SI Factors: {factors}")
        return result

def si_extraction_pipeline(goal: str, context: str) -> Optional[Dict]:
    """
    Main entry point for SI units extraction pipeline
    Replaces the old USV system with direct LLM -> SI units -> integers
    """
    extractor = SIUnitsExtractor()
    return extractor.extract_goal_and_si_factors(goal, context)

# Test function
if __name__ == "__main__":
    # Test the new SI units extraction
    test_cases = [
        ("I want a job at OpenAI", "CS grad, 2 years experience"),
        ("I want a job at open ai", "CS grad, 2 years experience"),
        ("Run a marathon under 3 hours", "Currently run 5 miles in 45 minutes"),
        ("Make $100k salary", "Currently making $60k, 3 years experience")
    ]
    
    for goal, context in test_cases:
        print(f"\n{'='*60}")
        result = si_extraction_pipeline(goal, context)
        if result:
            print(f"✅ Success: {result['extracted_factors']}")
        else:
            print("❌ Failed")