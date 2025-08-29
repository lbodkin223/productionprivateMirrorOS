"""
FRED API Integration for Economic Data
Provides real-time economic indicators for financial predictions
"""

import os
from fredapi import Fred
from datetime import datetime, timedelta
import requests

def get_fred_client():
    """Initialize FRED API client with API key."""
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        raise ValueError("FRED_API_KEY environment variable not set")
    return Fred(api_key=api_key)

def get_economic_indicators():
    """Fetch key economic indicators from FRED API."""
    try:
        fred = get_fred_client()
        
        # Key economic indicators
        indicators = {
            'unemployment_rate': 'UNRATE',
            'gdp_growth': 'GDP',
            'inflation_rate': 'CPIAUCSL',
            'interest_rate': 'FEDFUNDS',
            'stock_market': 'SP500',
            'consumer_confidence': 'UMCSENT'
        }
        
        data = {}
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        for key, series_id in indicators.items():
            try:
                series_data = fred.get_series(series_id, start=start_date, end=end_date)
                if not series_data.empty:
                    # Get most recent value
                    data[key] = {
                        'value': float(series_data.iloc[-1]),
                        'date': series_data.index[-1].strftime('%Y-%m-%d'),
                        'trend': calculate_trend(series_data)
                    }
            except Exception as e:
                print(f"Warning: Could not fetch {key}: {e}")
                data[key] = {'value': None, 'date': None, 'trend': 'unknown'}
        
        return data
    
    except Exception as e:
        print(f"FRED API Error: {e}")
        return None

def calculate_trend(series_data):
    """Calculate trend direction from recent data points."""
    if len(series_data) < 2:
        return 'unknown'
    
    recent = series_data.tail(3).values
    if recent[-1] > recent[0]:
        return 'increasing'
    elif recent[-1] < recent[0]:
        return 'decreasing'
    else:
        return 'stable'

def get_economic_context_score():
    """Calculate overall economic context score (0-100)."""
    indicators = get_economic_indicators()
    if not indicators:
        return 50  # Neutral if no data
    
    score = 50  # Base score
    
    # Unemployment rate (lower is better)
    if indicators['unemployment_rate']['value']:
        unemployment = indicators['unemployment_rate']['value']
        if unemployment < 4.0:
            score += 15
        elif unemployment < 6.0:
            score += 5
        elif unemployment > 8.0:
            score -= 15
        elif unemployment > 6.0:
            score -= 5
    
    # GDP growth trend
    if indicators['gdp_growth']['trend'] == 'increasing':
        score += 10
    elif indicators['gdp_growth']['trend'] == 'decreasing':
        score -= 10
    
    # Interest rates (moderate levels preferred)
    if indicators['interest_rate']['value']:
        rate = indicators['interest_rate']['value']
        if 2.0 <= rate <= 5.0:
            score += 10
        elif rate > 7.0 or rate < 1.0:
            score -= 10
    
    # Consumer confidence trend
    if indicators['consumer_confidence']['trend'] == 'increasing':
        score += 10
    elif indicators['consumer_confidence']['trend'] == 'decreasing':
        score -= 10
    
    return max(0, min(100, score))

def enhance_prediction_with_economic_data(base_probability, domain='general'):
    """Enhance prediction probability with economic indicators."""
    try:
        economic_score = get_economic_context_score()
        
        # Economic adjustment factor (0.8 - 1.2)
        economic_factor = 0.8 + (economic_score / 100.0) * 0.4
        
        # Domain-specific adjustments
        if domain in ['career', 'finance', 'business']:
            # Career/finance goals more sensitive to economic conditions
            enhanced_probability = base_probability * economic_factor
        else:
            # Other domains less affected by economics
            enhanced_probability = base_probability * (0.9 + economic_factor * 0.1)
        
        return max(0.01, min(0.99, enhanced_probability))
    
    except Exception as e:
        print(f"Economic enhancement error: {e}")
        return base_probability  # Return original if enhancement fails