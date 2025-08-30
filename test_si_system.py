#!/usr/bin/env python3
"""
Test Suite for MirrorOS SI Units System
Comprehensive testing of the revolutionary new architecture

Tests the complete final_plan.md implementation:
- SI units extraction
- Monte Carlo analysis  
- Chain of thought animation
- Shareable odds generation
"""

import requests
import json
from datetime import datetime

# Test configuration
LOCAL_URL = "http://localhost:8080"
PRODUCTION_URL = "https://yyk4197cr6.execute-api.us-east-2.amazonaws.com/prod/api"

def test_si_units_system(base_url=LOCAL_URL):
    """Test the complete SI units system"""
    
    print("🧪 Testing MirrorOS SI Units System")
    print(f"🌐 Target URL: {base_url}")
    print("=" * 60)
    
    # Test cases that should work once API keys are fixed
    test_cases = [
        {
            "name": "OpenAI Career Goal",
            "goal": "I want a job at OpenAI", 
            "context": "Northwestern grad, age 23, 2 years CS experience",
            "expected_domain": "career",
            "expected_company": "openai"
        },
        {
            "name": "Fitness Goal",
            "goal": "Lose 30 pounds in 6 months",
            "context": "Age 32, currently 180lbs, workout 3 times/week", 
            "expected_domain": "fitness"
        },
        {
            "name": "Finance Goal", 
            "goal": "Make $150k salary",
            "context": "Currently $90k, software engineer, 4 years experience",
            "expected_domain": "finance"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[TEST {i}] {test_case['name']}")
        print(f"Goal: {test_case['goal']}")
        print(f"Context: {test_case['context']}")
        
        # Test prediction endpoint
        prediction_result = test_prediction_endpoint(base_url, test_case)
        results.append(prediction_result)
        
        if prediction_result.get('success'):
            # Test shareable odds endpoint
            shareable_result = test_shareable_odds_endpoint(base_url, test_case)
            prediction_result['shareable_test'] = shareable_result
        
        print("-" * 40)
    
    # Generate test report
    generate_test_report(results)

def test_prediction_endpoint(base_url, test_case):
    """Test the main prediction endpoint"""
    
    payload = {
        "prediction_data": {
            "goal": test_case["goal"],
            "context": test_case["context"],
            "domain": "auto",
            "confidence_level": "standard",
            "enhanced_grounding": True,
            "use_llm_domain_detection": True
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate SI units response structure
            validation_results = validate_si_response(data, test_case)
            
            print(f"✅ Prediction Success")
            print(f"   Probability: {data.get('probability_percent', 'N/A')}")
            print(f"   Domain: {data.get('domain', 'N/A')}")
            print(f"   API Version: {data.get('api_version', 'N/A')}")
            
            if validation_results['animation_present']:
                print(f"   Animation Steps: {validation_results['animation_steps']}")
            
            if validation_results['si_factors_present']:
                print(f"   SI Factors: {len(data.get('si_factors_extracted', {}))}")
            
            return {
                'success': True,
                'test_case': test_case['name'],
                'data': data,
                'validation': validation_results
            }
            
        else:
            error_msg = response.text
            print(f"❌ Prediction Failed: HTTP {response.status_code}")
            print(f"   Error: {error_msg}")
            
            return {
                'success': False,
                'test_case': test_case['name'],
                'error': f"HTTP {response.status_code}: {error_msg}"
            }
            
    except Exception as e:
        print(f"❌ Prediction Exception: {e}")
        return {
            'success': False,
            'test_case': test_case['name'],
            'error': f"Exception: {str(e)}"
        }

def test_shareable_odds_endpoint(base_url, test_case):
    """Test the shareable odds endpoint"""
    
    payload = {
        "prediction_data": {
            "goal": test_case["goal"],
            "context": test_case["context"],
            "user_name": "Test User"
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/shareable-odds",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            sharing_data = data.get('sharing_data', {})
            
            print(f"🎨 Shareable Odds Success")
            
            if 'shareable_image' in sharing_data:
                image_data = sharing_data['shareable_image']
                print(f"   Image Size: ~{image_data.get('size_estimate_kb', 0)}KB")
                print(f"   Format: {image_data.get('format', 'N/A')}")
            
            if 'sharing_text' in sharing_data:
                text_data = sharing_data['sharing_text']
                print(f"   Short Text: {text_data.get('short', 'N/A')[:50]}...")
            
            return {'success': True, 'data': data}
            
        else:
            print(f"❌ Shareable Odds Failed: HTTP {response.status_code}")
            return {'success': False, 'error': response.text}
            
    except Exception as e:
        print(f"❌ Shareable Odds Exception: {e}")
        return {'success': False, 'error': str(e)}

def validate_si_response(data, test_case):
    """Validate the SI units response structure"""
    
    validation = {
        'si_factors_present': 'si_factors_extracted' in data,
        'animation_present': False,
        'animation_steps': 0,
        'monte_carlo_present': 'probability_comparison' in data,
        'chain_of_thought_present': 'chain_of_thought' in data,
        'domain_correct': data.get('domain') == test_case.get('expected_domain')
    }
    
    # Check animation sequence
    chain_of_thought = data.get('chain_of_thought', {})
    if 'animation_sequence' in chain_of_thought:
        animation = chain_of_thought['animation_sequence']
        validation['animation_present'] = True
        validation['animation_steps'] = animation.get('total_steps', 0)
    
    # Check for company extraction (if expected)
    if test_case.get('expected_company'):
        si_factors = data.get('si_factors_extracted', {})
        extracted_company = si_factors.get('target_entity_name', '').lower()
        validation['company_extraction_correct'] = extracted_company == test_case['expected_company']
    
    return validation

def generate_test_report(results):
    """Generate comprehensive test report"""
    
    print("\n" + "=" * 60)
    print("📊 SI UNITS SYSTEM TEST REPORT")
    print("=" * 60)
    
    total_tests = len(results)
    successful_tests = len([r for r in results if r.get('success')])
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {successful_tests/total_tests:.1%}")
    
    print(f"\n🔬 SI UNITS FEATURES VALIDATION:")
    
    # Check feature implementation
    features_tested = 0
    features_working = 0
    
    for result in results:
        if result.get('success') and 'validation' in result:
            validation = result['validation']
            features_tested += 1
            
            print(f"\n[{result['test_case']}]")
            
            if validation.get('si_factors_present'):
                print("   ✅ SI Factors Extraction")
                features_working += 1
            else:
                print("   ❌ SI Factors Extraction")
            
            if validation.get('animation_present'):
                print(f"   ✅ Chain of Thought Animation ({validation.get('animation_steps', 0)} steps)")
                features_working += 1
            else:
                print("   ❌ Chain of Thought Animation")
            
            if validation.get('monte_carlo_present'):
                print("   ✅ Monte Carlo Analysis")
                features_working += 1
            else:
                print("   ❌ Monte Carlo Analysis")
            
            if validation.get('domain_correct'):
                print("   ✅ Domain Classification")
                features_working += 1
            else:
                print("   ❌ Domain Classification")
            
            if result.get('shareable_test', {}).get('success'):
                print("   ✅ Shareable Odds Generation")
                features_working += 1
            else:
                print("   ❌ Shareable Odds Generation")
    
    if features_tested > 0:
        feature_success_rate = features_working / (features_tested * 5) * 100  # 5 features per test
        print(f"\nFeature Implementation Rate: {feature_success_rate:.1f}%")
    
    # Failure analysis
    failed_tests = [r for r in results if not r.get('success')]
    if failed_tests:
        print(f"\n❌ FAILURE ANALYSIS:")
        for failure in failed_tests:
            print(f"   {failure['test_case']}: {failure.get('error', 'Unknown error')}")
    
    # Next steps based on results
    print(f"\n🎯 NEXT STEPS:")
    if successful_tests == 0:
        print("   1. ⚠️ Fix API authentication (OPENAI_API_KEY, ANTHROPIC_API_KEY)")
        print("   2. 🧪 Re-run tests after API keys are configured")
        print("   3. 🚀 Deploy to production once working locally")
    elif successful_tests < total_tests:
        print("   1. 🔍 Investigate partial failures")
        print("   2. 🧪 Add more comprehensive test cases")
        print("   3. 🚀 Deploy working features to production")
    else:
        print("   1. ✅ All tests passing - ready for production!")
        print("   2. 🧪 Add performance benchmarks")
        print("   3. 📱 Update mobile app to use new API features")
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"si_system_test_report_{timestamp}.json"
    
    with open(report_filename, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total_tests': total_tests,
                'successful': successful_tests,
                'failed': total_tests - successful_tests,
                'success_rate': successful_tests/total_tests if total_tests > 0 else 0
            },
            'detailed_results': results,
            'features_tested': {
                'si_factors_extraction': True,
                'monte_carlo_analysis': True,
                'chain_of_thought_animation': True,
                'shareable_odds_generation': True,
                'domain_classification': True
            }
        }, f, indent=2)
    
    print(f"\n💾 Detailed report saved: {report_filename}")

if __name__ == "__main__":
    # Test against local server first, then production
    print("🧪 MirrorOS SI Units System - Comprehensive Test Suite")
    print("Following final_plan.md implementation validation")
    print()
    
    # Try local server first
    try:
        response = requests.get(f"{LOCAL_URL}/health", timeout=5)
        if response.status_code == 200:
            print("🟢 Local server detected - testing locally")
            test_si_units_system(LOCAL_URL)
        else:
            raise Exception("Local server not responding")
    except:
        print("🔴 Local server unavailable - testing production")
        test_si_units_system(PRODUCTION_URL)