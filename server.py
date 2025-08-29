"""
MirrorOS Final Private API
Clean server with LLM-powered extraction only
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from lm_extractor import full_extraction_pipeline
from fred_integration import enhance_prediction_with_economic_data, get_economic_indicators

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'system': 'mirroros-final-private'})

@app.route('/economic-data', methods=['GET'])
def economic_data():
    """Get current economic indicators from FRED API."""
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

@app.route('/predict', methods=['POST'])
def predict():
    """LLM-powered prediction endpoint."""
    try:
        data = request.get_json(force=True)
        
        if 'prediction_data' not in data:
            return jsonify({'error': 'prediction_data required'}), 400
            
        prediction_data = data['prediction_data']
        goal_text = prediction_data.get('goal', '')
        context_text = prediction_data.get('context', '')
        
        if not goal_text:
            return jsonify({'error': 'goal required'}), 400
        
        print(f"📝 Goal: {goal_text}")
        print(f"📋 Context: {context_text}")
        
        # Use new LLM extraction pipeline
        result = full_extraction_pipeline(goal_text, context_text)
        
        if not result:
            return jsonify({'error': 'LLM extraction failed'}), 500
        
        # Calculate basic probability from standardized data
        standardized_data = result['standardized_data']
        base_probability = calculate_probability_from_data(standardized_data, result['domain'])
        
        # Enhance with FRED economic data
        probability = enhance_prediction_with_economic_data(base_probability, result['domain'])
        
        response = {
            'probability': round(probability, 2),
            'probability_percent': f'{probability:.1%}',
            'domain': result['domain'],
            'goal_description': result['goal'],
            'extracted_variables': result['raw_variables'],
            'standardized_data': standardized_data,
            'api_version': '3.0-llm',
            'system': 'mirroros-final-private'
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500

def calculate_probability_from_data(data, domain):
    """Calculate probability using standardized integer data."""
    probability = 0.5  # Base 50%
    
    # Company selectivity adjustment
    if 'selectivity_score' in data:
        selectivity = data['selectivity_score']
        if selectivity >= 90:
            probability *= 0.15  # Very competitive (OpenAI, Google)
        elif selectivity >= 80:
            probability *= 0.25  # Competitive
    
    # Timeline adjustment
    if 'timeline_months' in data:
        months = data['timeline_months']
        if months < 3:
            probability *= 0.6  # Too rushed
        elif months > 36:
            probability *= 0.8  # Maybe too long
    
    # Education boost
    if 'education_score' in data:
        edu_score = data['education_score']
        if edu_score >= 90:
            probability *= 1.3  # Top tier education
        elif edu_score >= 80:
            probability *= 1.2  # Good education
    
    # Hours/day effort
    if 'hours_per_day' in data:
        hours = data['hours_per_day']
        if hours >= 6:
            probability *= 1.4  # High effort
        elif hours >= 3:
            probability *= 1.2  # Good effort
        elif hours < 1:
            probability *= 0.7  # Low effort
    
    return max(0.01, min(0.99, probability))

if __name__ == '__main__':
    print("🚀 Starting MirrorOS Final Private API")
    print("🤖 LLM-powered extraction system active")
    
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🌐 Running on {host}:{port}")
    app.run(host=host, port=port, debug=False)