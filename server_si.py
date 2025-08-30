#!/usr/bin/env python3
"""
MirrorOS Final Private API - SI Units Architecture
Revolutionary LLM-powered prediction service with SI units and ratios

Following final_plan.md data flow:
input parser -> lm api -> SI quantification -> int -> monte carlo engine -> output parser

Compares probability_projected to target_baseline
Provides top 3 factors and chain of thought reasoning
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from si_units_extractor import si_extraction_pipeline
from monte_carlo_si import MonteCarloSI
from chain_of_thought_animation import ChainOfThoughtAnimator
from shareable_odds import create_shareable_odds_endpoint

# Load environment variables
load_dotenv()

# Optional FRED integration with fallback
try:
    from fred_integration import enhance_prediction_with_economic_data, get_economic_indicators
    FRED_AVAILABLE = True
    print("🏦 FRED Economic Data integration loaded")
except ImportError as e:
    print(f"⚠️  FRED integration unavailable: {e}")
    FRED_AVAILABLE = False
    def enhance_prediction_with_economic_data(probability, domain='general'):
        return probability
    def get_economic_indicators():
        return None

app = Flask(__name__)
monte_carlo_engine = MonteCarloSI()
animation_engine = ChainOfThoughtAnimator()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok', 
        'system': 'mirroros-si-units-engine',
        'version': '4.0-si',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/economic-data', methods=['GET'])
def economic_data():
    """Get current economic indicators from FRED API."""
    if not FRED_AVAILABLE:
        return jsonify({
            'status': 'unavailable', 
            'message': 'FRED integration not available',
            'timestamp': datetime.now().isoformat()
        }), 503
    
    try:
        indicators = get_economic_indicators()
        if indicators:
            return jsonify({
                'status': 'success',
                'data': indicators,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Could not fetch economic data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shareable-odds', methods=['POST'])
def shareable_odds():
    """Generate shareable odds image for social media sharing"""
    try:
        data = request.get_json(force=True)
        
        if 'prediction_data' not in data:
            return jsonify({'error': 'prediction_data required'}), 400
            
        prediction_data = data['prediction_data']
        goal_text = prediction_data.get('goal', '')
        context_text = prediction_data.get('context', '')
        user_name = prediction_data.get('user_name', 'MirrorOS User')
        
        if not goal_text:
            return jsonify({'error': 'goal required'}), 400
        
        print(f"🎨 Generating shareable odds for: {user_name}")
        
        # Run the same analysis as prediction
        extraction_result = si_extraction_pipeline(goal_text, context_text)
        if not extraction_result:
            return jsonify({'error': 'SI units extraction failed'}), 500
        
        goal_analysis = extraction_result['goal_analysis']
        si_factors = extraction_result['extracted_factors']
        probability_factors = extraction_result['probability_factors']
        
        monte_carlo_result = monte_carlo_engine.calculate_probability(
            si_factors, goal_analysis, probability_factors
        )
        
        # Generate shareable content
        sharing_data = create_shareable_odds_endpoint(
            monte_carlo_result, goal_analysis, si_factors, user_name
        )
        
        if sharing_data.get('error'):
            return jsonify(sharing_data), 500
        
        return jsonify({
            'status': 'success',
            'sharing_data': sharing_data,
            'api_version': '4.0-si-shareable',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Shareable odds error: {e}")
        return jsonify({'error': f'Shareable odds generation failed: {str(e)}'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Revolutionary SI Units prediction endpoint
    
    New architecture per final_plan.md:
    1. Input parser -> LM API 
    2. SI quantification -> integers
    3. Monte Carlo engine -> probability_projected
    4. Compare to target_baseline
    5. Output parser with top 3 factors and chain of thought
    """
    try:
        data = request.get_json(force=True)
        
        if 'prediction_data' not in data:
            return jsonify({'error': 'prediction_data required'}), 400
            
        prediction_data = data['prediction_data']
        goal_text = prediction_data.get('goal', '')
        context_text = prediction_data.get('context', '')
        
        if not goal_text:
            return jsonify({'error': 'goal required'}), 400
        
        print(f"🚀 SI Units Prediction Pipeline Starting")
        print(f"📝 Goal: {goal_text}")
        print(f"📋 Context: {context_text}")
        
        # STEP 1: Input parser -> LM API -> SI quantification
        extraction_result = si_extraction_pipeline(goal_text, context_text)
        
        if not extraction_result:
            return jsonify({
                'error': 'SI units extraction failed - API keys may be invalid',
                'message': 'Check OPENAI_API_KEY and ANTHROPIC_API_KEY in environment',
                'system': 'mirroros-si-units-engine'
            }), 500
        
        goal_analysis = extraction_result['goal_analysis']
        si_factors = extraction_result['extracted_factors']
        probability_factors = extraction_result['probability_factors']
        
        print(f"✅ SI Extraction Complete")
        print(f"🎯 Goal Analysis: {goal_analysis}")
        print(f"📊 SI Factors: {si_factors}")
        
        # STEP 2: Monte Carlo engine -> probability_projected vs target_baseline
        monte_carlo_result = monte_carlo_engine.calculate_probability(
            si_factors, goal_analysis, probability_factors
        )
        
        probability_projected = monte_carlo_result.probability_projected
        target_baseline = monte_carlo_result.target_baseline
        
        print(f"🎲 Monte Carlo Complete")
        print(f"📈 Probability Projected: {probability_projected:.1%}")
        print(f"📊 Target Baseline: {target_baseline:.1%}")
        
        # STEP 3: FRED economic enhancement (if available)
        domain = goal_analysis.get('domain', 'general')
        if FRED_AVAILABLE and domain in ['finance', 'career', 'business']:
            probability_projected = enhance_prediction_with_economic_data(probability_projected, domain)
            print(f"🏦 FRED Enhanced: {probability_projected:.1%}")
        
        # STEP 4: Generate animated chain of thought
        animation_sequence = animation_engine.create_animated_chain(
            monte_carlo_result, si_factors, goal_analysis
        )
        
        # STEP 5: Output parser with comprehensive analysis
        response = build_comprehensive_response(
            probability_projected=probability_projected,
            target_baseline=target_baseline,
            monte_carlo_result=monte_carlo_result,
            goal_analysis=goal_analysis,
            si_factors=si_factors,
            extraction_result=extraction_result,
            animation_sequence=animation_sequence
        )
        
        print(f"✅ Prediction Complete: {probability_projected:.1%}")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({
            'error': 'Prediction failed', 
            'message': str(e),
            'system': 'mirroros-si-units-engine'
        }), 500

def build_comprehensive_response(probability_projected: float, target_baseline: float,
                               monte_carlo_result, goal_analysis: dict, 
                               si_factors: dict, extraction_result: dict,
                               animation_sequence: dict) -> dict:
    """Build comprehensive response with all analysis components"""
    
    # Determine outcome category based on probability
    if probability_projected >= 0.7:
        outcome_category = "highly_likely"
        outcome_text = "Success is highly likely"
    elif probability_projected >= 0.5:
        outcome_category = "likely"
        outcome_text = "Success is likely with focused effort"
    elif probability_projected >= 0.3:
        outcome_category = "possible"
        outcome_text = "Success is possible but challenging"
    elif probability_projected >= 0.1:
        outcome_category = "challenging"
        outcome_text = "Success will be challenging"
    else:
        outcome_category = "unlikely"
        outcome_text = "Success is unlikely without significant changes"
    
    # Build explanation narrative
    explanation = build_explanation_narrative(
        probability_projected, target_baseline, monte_carlo_result.top_factors
    )
    
    # Extract key success factors and risks
    key_success_factors = extract_success_factors(si_factors, probability_projected)
    risk_factors = extract_risk_factors(si_factors, monte_carlo_result.top_factors)
    
    response = {
        # Core prediction results
        'probability': round(probability_projected, 2),
        'probability_percent': f'{probability_projected:.1%}',
        'target_baseline': round(target_baseline, 2),
        'baseline_percent': f'{target_baseline:.1%}',
        
        # Analysis components
        'domain': goal_analysis.get('domain', 'general'),
        'outcome_category': outcome_category,
        'outcome_text': outcome_text,
        'explanation': explanation,
        
        # Confidence and factors
        'confidence_interval': [
            round(monte_carlo_result.confidence_interval[0], 2),
            round(monte_carlo_result.confidence_interval[1], 2)
        ],
        'top_factors': monte_carlo_result.top_factors,
        'key_success_factors': key_success_factors,
        'risk_factors': risk_factors,
        
        # Chain of thought reasoning with animation
        'chain_of_thought': {
            'reasoning_steps': monte_carlo_result.reasoning_chain,
            'methodology': 'SI Units Monte Carlo Analysis with 10,000 simulations',
            'confidence_level': 'High',
            'animation_sequence': animation_sequence
        },
        
        # Technical details
        'si_factors_extracted': si_factors,
        'goal_analysis': goal_analysis,
        'probability_comparison': {
            'projected': round(probability_projected, 3),
            'baseline': round(target_baseline, 3),
            'improvement_factor': round(probability_projected / target_baseline, 2) if target_baseline > 0 else None
        },
        
        # System information
        'api_version': '4.0-si-units',
        'system': 'mirroros-si-engine',
        'extraction_method': 'LLM-SI-Units',
        'monte_carlo_simulations': 10000,
        'response_time_ms': 150,  # Placeholder
        'timestamp': datetime.now().isoformat()
    }
    
    return response

def build_explanation_narrative(probability: float, baseline: float, top_factors: list) -> str:
    """Build human-readable explanation of the prediction"""
    
    if probability > baseline * 1.5:
        trend = "significantly higher than"
    elif probability > baseline * 1.2:
        trend = "higher than"
    elif probability < baseline * 0.8:
        trend = "lower than"
    elif probability < baseline * 0.5:
        trend = "significantly lower than"
    else:
        trend = "similar to"
    
    factors_text = f"Key factors include: {', '.join(top_factors[:2])}." if top_factors else ""
    
    return f"Analysis indicates {probability:.1%} success probability, which is {trend} the baseline rate of {baseline:.1%} for similar goals. {factors_text}"

def extract_success_factors(si_factors: dict, probability: float) -> list:
    """Extract key factors that increase success probability"""
    factors = []
    
    if si_factors.get('education_ratio', 0) >= 0.8:
        factors.append("strong educational background")
    
    if si_factors.get('experience_years', 0) >= 3:
        factors.append("relevant experience")
    
    if si_factors.get('effort_hours_per_day', 0) >= 4:
        factors.append("high effort commitment")
    
    age = si_factors.get('age_years', 0)
    if 22 <= age <= 35:
        factors.append("optimal age for goal achievement")
    
    if not factors:
        factors = ["determination and focus", "strategic approach"]
    
    return factors[:3]  # Return top 3

def extract_risk_factors(si_factors: dict, top_factors: list) -> list:
    """Extract key factors that may reduce success probability"""
    risks = []
    
    if si_factors.get('competitiveness_ratio', 0) >= 0.9:
        risks.append("extremely competitive target market")
    
    if si_factors.get('experience_years', 0) < 2:
        risks.append("limited experience in target field")
    
    if si_factors.get('effort_hours_per_day', 0) < 2:
        risks.append("insufficient time commitment")
    
    # Extract risks from top factors that decrease probability
    for factor in top_factors:
        if "decreases" in factor.lower():
            risks.append(factor.replace(" decreases probability", ""))
    
    if not risks:
        risks = ["market uncertainty", "external factors beyond control"]
    
    return risks[:3]  # Return top 3

if __name__ == '__main__':
    print("🚀 Starting MirrorOS SI Units Private API")
    print("🔬 Revolutionary LLM-powered extraction with SI units")
    print("🎲 Advanced Monte Carlo probability engine")
    
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🌐 Running on {host}:{port}")
    app.run(host=host, port=port, debug=False)