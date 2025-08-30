import os
import requests
import json

def extract_goal_and_domain(goal_string):
    """
    Phase 1: LLM identifies the target/goal and what domain it belongs to
    FROM THE GOAL INPUT BOX ONLY
    Uses Anthropic Claude first, OpenAI as fallback
    """
    # Try Anthropic first
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_key:
        result = _try_anthropic_goal_analysis(goal_string, anthropic_key)
        if result:
            return result
        print("⚠️ Anthropic failed, trying OpenAI...")
    
    # Fallback to OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        result = _try_openai_goal_analysis(goal_string, openai_key)
        if result:
            return result
    
    print("❌ Both Anthropic and OpenAI failed")
    return None

def _try_anthropic_goal_analysis(goal_string, api_key):
    """Try Anthropic Claude for goal analysis."""
    api_url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": f"""Analyze this goal: "{goal_string}"

Phase 1 Analysis:
1. What specific goal is the user trying to accomplish? (Be precise and specific)
2. What domain does this goal belong to?

Choose domain from: career, finance, fitness, dating, academic, business, travel

Format your response as JSON:
{{
    "goal": "specific goal description",
    "domain": "domain_name"
}}"""
            }
        ]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['content'][0]['text'].strip()
        
        # Extract JSON from the response (Claude often adds explanatory text)
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_content = content[json_start:json_end]
            parsed = json.loads(json_content)
        else:
            raise Exception("No JSON found in response")
        print(f"🎯 Phase 1 (Anthropic) - Goal: {parsed['goal']}, Domain: {parsed['domain']}")
        return parsed
        
    except Exception as e:
        print(f"❌ Anthropic Phase 1 failed: {e}")
        return None

def _try_openai_goal_analysis(goal_string, api_key):
    """Try OpenAI GPT for goal analysis (fallback)."""
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user", 
                "content": f"""Analyze this goal: "{goal_string}"

Phase 1 Analysis:
1. What specific goal is the user trying to accomplish? (Be precise and specific)
2. What domain does this goal belong to?

Choose domain from: career, finance, fitness, dating, academic, business, travel

Format your response as JSON:
{{
    "goal": "specific goal description",
    "domain": "domain_name"
}}"""
            }
        ],
        "max_tokens": 100,
        "temperature": 0
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        # Parse JSON response
        parsed = json.loads(content)
        print(f"🎯 Phase 1 (OpenAI) - Goal: {parsed['goal']}, Domain: {parsed['domain']}")
        return parsed
        
    except Exception as e:
        print(f"❌ OpenAI Phase 1 failed: {e}")
        return None

def extract_variables_and_categories(context_string, goal_info):
    """
    Phase 2: LLM extracts useful variables and categorizes them by type
    FROM THE CONTEXT/TIMELINE INPUT BOX ONLY
    Uses Anthropic first, OpenAI as fallback
    """
    # Try Anthropic first
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_key:
        result = _try_anthropic_variable_extraction(context_string, goal_info, anthropic_key)
        if result:
            return result
        print("⚠️ Anthropic Phase 2 failed, trying OpenAI...")
    
    # Fallback to OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        result = _try_openai_variable_extraction(context_string, goal_info, openai_key)
        if result:
            return result
    
    print("❌ Both Anthropic and OpenAI failed for Phase 2")
    return None

def _try_anthropic_variable_extraction(context_string, goal_info, api_key):
    """Try Anthropic Claude for variable extraction."""
    api_url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    goal = goal_info.get('goal', '') if goal_info else ''
    
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": f"""Given this goal: "{goal}"
And this context/timeline information: "{context_string}"

Phase 2 Analysis:
1. Identify ALL useful variables mentioned (numbers, timeframes, experience, etc.)
2. Categorize each variable by type:
3. CRITICAL: For company names, ALWAYS extract ANY variation as target_entity:
   - "OpenAI" → extract as target_entity
   - "open ai" → extract as target_entity  
   - "OPENAI" → extract as target_entity
   - "google" → extract as target_entity
   - "Google" → extract as target_entity
   - "apple" → extract as target_entity

Variable categories:
- time: examples being durations, frequencies, deadlines (4 hours/day, 6 months, 2 years)
- money: examples being salaries, savings, costs, revenue ($3000/week, $50k salary)  
- distance: examples being physical measurements (miles, km, pace)
- experience:examples being education, job history, skills (Northwestern grad, 5 years experience)
- demographic:examples being  age, location, status (23 years old, San Francisco)
- performance:examples being  metrics, scores, rates (GPA, success rate, weight)
- target_entity:examples being companies, institutions, people (OpenAI, open ai, OPENAI, Google, google, apple, Apple, Harvard, Northwestern)

Format as JSON:
{{
    "variables": {{
        "variable_name": "extracted_value",
        "another_variable": "another_value"
    }},
    "categories": {{
        "time": ["list of time variables"],
        "money": ["list of money variables"], 
        "distance": ["list of distance variables"],
        "experience": ["list of experience variables"],
        "demographic": ["list of demographic variables"],
        "performance": ["list of performance variables"],
        "target_entity": ["list of target entities"]
    }}
}}"""
            }
        ]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['content'][0]['text'].strip()
        
        # Extract JSON from the response (Claude often adds explanatory text)
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_content = content[json_start:json_end]
            parsed = json.loads(json_content)
        else:
            raise Exception("No JSON found in response")
        print(f"🔍 Phase 2 (Anthropic) - Variables: {parsed['variables']}")
        print(f"📂 Categories: {parsed['categories']}")
        return parsed
        
    except Exception as e:
        print(f"❌ Anthropic Phase 2 failed: {e}")
        return None

def _try_openai_variable_extraction(context_string, goal_info, api_key):
    """Try OpenAI GPT for variable extraction (fallback)."""
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    goal = goal_info.get('goal', '') if goal_info else ''
    
    payload = {
        "model": "gpt-4o", 
        "messages": [
            {
                "role": "user",
                "content": f"""Given this goal: "{goal}"
And this context/timeline information: "{context_string}"

Phase 2 Analysis:
1. Identify ALL useful variables mentioned (numbers, timeframes, experience, etc.)
2. Categorize each variable by type:
3. CRITICAL: For company names, ALWAYS extract ANY variation as target_entity:
   - "OpenAI" → extract as target_entity
   - "open ai" → extract as target_entity  
   - "OPENAI" → extract as target_entity
   - "google" → extract as target_entity
   - "Google" → extract as target_entity
   - "apple" → extract as target_entity

Variable categories:
- time: examples being durations, frequencies, deadlines (4 hours/day, 6 months, 2 years)
- money: examples being salaries, savings, costs, revenue ($3000/week, $50k salary)  
- distance: examples being physical measurements (miles, km, pace)
- experience:examples being education, job history, skills (Northwestern grad, 5 years experience)
- demographic:examples being  age, location, status (23 years old, San Francisco)
- performance:examples being  metrics, scores, rates (GPA, success rate, weight)
- target_entity:examples being companies, institutions, people (OpenAI, open ai, OPENAI, Google, google, apple, Apple, Harvard, Northwestern)

Format as JSON:
{{
    "variables": {{
        "variable_name": "extracted_value",
        "another_variable": "another_value"
    }},
    "categories": {{
        "time": ["list of time variables"],
        "money": ["list of money variables"], 
        "distance": ["list of distance variables"],
        "experience": ["list of experience variables"],
        "demographic": ["list of demographic variables"],
        "performance": ["list of performance variables"],
        "target_entity": ["list of target entities"]
    }}
}}"""
            }
        ],
        "max_tokens": 400,
        "temperature": 0
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        # Parse JSON response
        parsed = json.loads(content)
        print(f"🔍 Phase 2 (OpenAI) - Variables: {parsed['variables']}")
        print(f"📂 Categories: {parsed['categories']}")
        return parsed
        
    except Exception as e:
        print(f"❌ OpenAI Phase 2 failed: {e}")
        return None

def standardize_to_integers(variables, categories):
    """
    Phase 3: Convert LLM-extracted variables to standardized integers/data for heuristics
    """
    standardized = {}
    
    # Process time variables
    for time_var in categories.get('time', []):
        if time_var in variables:
            value = variables[time_var]
            standardized.update(parse_time_to_int(time_var, value))
    
    # Process money variables
    for money_var in categories.get('money', []):
        if money_var in variables:
            value = variables[money_var]
            standardized.update(parse_money_to_int(money_var, value))
            
    # Process demographic variables
    for demo_var in categories.get('demographic', []):
        if demo_var in variables:
            value = variables[demo_var]
            standardized.update(parse_demographic_to_int(demo_var, value))
            
    # Process experience variables
    for exp_var in categories.get('experience', []):
        if exp_var in variables:
            value = variables[exp_var]
            standardized.update(parse_experience_to_int(exp_var, value))
            
    # Process target entity - check both variables and categories list
    for target_var in categories.get('target_entity', []):
        if target_var in variables:
            value = variables[target_var]
            standardized.update(parse_target_to_int(target_var, value))
        else:
            # Target entity might be in the category list directly (OpenAI, etc.)
            standardized.update(parse_target_to_int(target_var, target_var))
    
    print(f"📊 Standardized data: {standardized}")
    return standardized

def parse_time_to_int(name, value):
    """Convert time strings to integer months/hours"""
    import re
    result = {}
    value_lower = value.lower()
    
    # Hours per day
    if 'hour' in value_lower and 'day' in value_lower:
        numbers = re.findall(r'\d+', value)
        if numbers:
            result['hours_per_day'] = int(numbers[0])
    
    # Months timeline
    elif 'month' in value_lower:
        numbers = re.findall(r'\d+', value)
        if numbers:
            result['timeline_months'] = int(numbers[0])
    elif 'year' in value_lower:
        numbers = re.findall(r'\d+', value)
        if numbers:
            result['timeline_months'] = int(numbers[0]) * 12
            
    return result

def parse_money_to_int(name, value):
    """Convert money strings to integer dollars"""
    import re
    result = {}
    value_lower = value.lower()
    
    # Extract amount
    amounts = re.findall(r'[\$]?(\d+(?:,\d{3})*(?:\.\d{2})?)', value_lower)
    if amounts:
        amount = float(amounts[0].replace(',', ''))
        
        # Scale for k/m notation
        if 'k' in value_lower:
            amount *= 1000
        elif 'm' in value_lower:
            amount *= 1000000
        
        # Determine type
        if 'week' in value_lower:
            result['income_weekly'] = int(amount)
            result['income_annual'] = int(amount * 52)
        elif 'salary' in value_lower:
            result['target_salary'] = int(amount)
        elif 'save' in value_lower:
            result['savings_target'] = int(amount)
            
    return result

def parse_demographic_to_int(name, value):
    """Convert demographic strings to integers"""
    import re
    result = {}
    value_lower = value.lower()
    
    # Age
    if 'year' in value_lower and 'old' in value_lower:
        numbers = re.findall(r'\d+', value)
        if numbers:
            result['age'] = int(numbers[0])
    elif re.match(r'^\d+$', value_lower):
        result['age'] = int(value)
        
    return result

def parse_experience_to_int(name, value):
    """Convert experience strings to integers/flags"""
    import re
    result = {}
    value_lower = value.lower()
    
    # Extract years of experience
    numbers = re.findall(r'\d+', value)
    if numbers and ('year' in value_lower or 'experience' in value_lower):
        result['experience_years'] = int(numbers[0])
    
    # Education level
    if any(school in value_lower for school in ['northwestern', 'harvard', 'mit', 'stanford']):
        result['education_score'] = 90  # High-tier school
    elif 'graduate' in value_lower or 'grad' in value_lower:
        result['education_score'] = 80  # Graduate degree
    elif 'college' in value_lower or 'university' in value_lower:
        result['education_score'] = 70  # Bachelor's
    
    return result

def parse_target_to_int(name, value):
    """Convert target entity to selectivity score"""
    result = {}
    value_lower = value.lower()
    
    # Company selectivity scores
    company_scores = {
        'openai': 95, 'google': 90, 'apple': 90, 
        'microsoft': 85, 'meta': 90, 'netflix': 80
    }
    
    for company, score in company_scores.items():
        if company in value_lower or company.replace('ai', ' ai') in value_lower:
            result['target_company'] = company
            result['selectivity_score'] = score
            break
            
    return result

def full_extraction_pipeline(goal_string, context_string):
    """
    Complete pipeline: Goal + Context -> LLM Analysis -> Standardized Integers -> Heuristics
    Uses Anthropic Claude first, OpenAI as fallback
    """
    print(f"🚀 Starting extraction")
    print(f"📝 Goal: '{goal_string}'")
    print(f"📋 Context: '{context_string}'")
    
    # Phase 1: Goal and Domain (from goal input box)
    goal_info = extract_goal_and_domain(goal_string)
    if not goal_info:
        return None
    
    # Phase 2: Variables and Categories (from context input box)
    var_info = extract_variables_and_categories(context_string, goal_info)
    if not var_info:
        return None
    
    # Phase 3: Standardize to Integers
    standardized = standardize_to_integers(var_info['variables'], var_info['categories'])
    
    # Combine all results
    final_result = {
        'domain': goal_info['domain'],
        'goal': goal_info['goal'],
        'raw_variables': var_info['variables'],
        'categories': var_info['categories'],
        'standardized_data': standardized  # This goes to your heuristics!
    }
    
    print(f"✅ Final standardized data ready for heuristics: {standardized}")
    return final_result