#!/usr/bin/env python3
"""
MirrorOS USV Test Runner
Executes all 100 test cases and analyzes extraction consistency
"""

import json
import requests
import time
from datetime import datetime
import csv

# API Configuration
API_URL = "https://yyk4197cr6.execute-api.us-east-2.amazonaws.com/prod/api/predict"
HEADERS = {"Content-Type": "application/json"}

# Test cases from USV_TEST_CASES.md
TEST_CASES = [
    # Career Domain (25 tests)
    {"id": 1, "domain": "career", "goal": "I want a job at OpenAI", "context": "CS grad, 2 years experience", "expected_company": "openai"},
    {"id": 2, "domain": "career", "goal": "I want a job at open ai", "context": "CS grad, 2 years experience", "expected_company": "openai"},
    {"id": 3, "domain": "career", "goal": "I want a job at OPENAI", "context": "CS grad, 2 years experience", "expected_company": "openai"},
    {"id": 4, "domain": "career", "goal": "I want a job at Google", "context": "Northwestern grad, age 24", "expected_company": "google"},
    {"id": 5, "domain": "career", "goal": "I want a job at google", "context": "Northwestern grad, age 24", "expected_company": "google"},
    {"id": 6, "domain": "career", "goal": "I want a job at GOOGLE", "context": "Northwestern grad, age 24", "expected_company": "google"},
    {"id": 7, "domain": "career", "goal": "I want a job at Apple", "context": "Stanford CS degree", "expected_company": "apple"},
    {"id": 8, "domain": "career", "goal": "I want a job at apple", "context": "Stanford CS degree", "expected_company": "apple"},
    {"id": 9, "domain": "career", "goal": "I want a job at Microsoft", "context": "5 years coding experience", "expected_company": "microsoft"},
    {"id": 10, "domain": "career", "goal": "I want a job at microsoft", "context": "5 years coding experience", "expected_company": "microsoft"},
    {"id": 11, "domain": "career", "goal": "I want a job at Meta", "context": "React specialist, 3 years", "expected_company": "meta"},
    {"id": 12, "domain": "career", "goal": "I want a job at meta", "context": "React specialist, 3 years", "expected_company": "meta"},
    {"id": 13, "domain": "career", "goal": "I want a job at Netflix", "context": "Streaming platform experience", "expected_company": "netflix"},
    {"id": 14, "domain": "career", "goal": "I want a job at netflix", "context": "Streaming platform experience", "expected_company": "netflix"},
    {"id": 15, "domain": "career", "goal": "Get a software engineering role", "context": "Northwestern grad, 10 years experience, Python expert", "expected_education": 90},
    {"id": 16, "domain": "career", "goal": "Get a software engineering role", "context": "Harvard CS PhD, published researcher", "expected_education": 90},
    {"id": 17, "domain": "career", "goal": "Get a software engineering role", "context": "MIT grad, startup founder, 15 years experience", "expected_education": 90},
    {"id": 18, "domain": "career", "goal": "Get a software engineering role", "context": "Bootcamp grad, 6 months experience", "expected_education": 70},
    {"id": 19, "domain": "career", "goal": "Get a software engineering role", "context": "Self-taught, no degree, 2 years experience", "expected_education": None},
    {"id": 20, "domain": "career", "goal": "Get a software engineering role", "context": "Community college, working 20 hours/week studying", "expected_hours": 20},
    {"id": 21, "domain": "career", "goal": "Get promoted to senior engineer", "context": "Working 8 hours/day, 2 years at current company", "expected_hours": 8},
    {"id": 22, "domain": "career", "goal": "Switch to data science career", "context": "Studying 4 hours/day for 6 months", "expected_hours": 4, "expected_timeline": 6},
    {"id": 23, "domain": "career", "goal": "Become a technical lead", "context": "10 hours/day effort, 18-month timeline", "expected_hours": 10, "expected_timeline": 18},
    {"id": 24, "domain": "career", "goal": "Get into FAANG company", "context": "Practicing 6 hours/day leetcode for 8 months", "expected_hours": 6, "expected_timeline": 8},
    {"id": 25, "domain": "career", "goal": "Land remote software job", "context": "Available immediately, 40 hours/week commitment", "expected_hours": 40},
    
    # Finance Domain (20 tests)
    {"id": 26, "domain": "finance", "goal": "Make $1 million in the stock market", "context": "$50k starting capital, 5 years timeline", "expected_timeline": 60},
    {"id": 27, "domain": "finance", "goal": "Double my investment portfolio", "context": "$100k current portfolio, 3 years", "expected_timeline": 36},
    {"id": 28, "domain": "finance", "goal": "Earn $5k/month passive income", "context": "$200k to invest, real estate focus", "expected_income": 60000},
    {"id": 29, "domain": "finance", "goal": "Build $500k retirement fund", "context": "Age 35, saving $2k/month", "expected_age": 35},
    {"id": 30, "domain": "finance", "goal": "Pay off $80k student loans", "context": "$60k salary, $1k/month payment capacity", "expected_salary": 60000},
    {"id": 31, "domain": "finance", "goal": "Increase salary to $150k", "context": "Currently $90k, software engineer, 4 years experience", "expected_salary": 150000},
    {"id": 32, "domain": "finance", "goal": "Earn $300k total compensation", "context": "Senior engineer at startup, equity included", "expected_salary": 300000},
    {"id": 33, "domain": "finance", "goal": "Make $10k/month freelancing", "context": "Web developer, working 30 hours/week", "expected_hours": 30},
    {"id": 34, "domain": "finance", "goal": "Generate $2k/week side income", "context": "Full-time job, 15 hours/week available", "expected_hours": 15},
    {"id": 35, "domain": "finance", "goal": "Reach $500k annual income", "context": "Starting consulting business, 10 years experience", "expected_salary": 500000},
    {"id": 36, "domain": "finance", "goal": "Raise $2M Series A funding", "context": "SaaS startup, $50k MRR, 2 co-founders"},
    {"id": 37, "domain": "finance", "goal": "Sell business for $5M", "context": "E-commerce business, $100k/month revenue"},
    {"id": 38, "domain": "finance", "goal": "Launch profitable app", "context": "$20k development budget, 8 months timeline", "expected_timeline": 8},
    {"id": 39, "domain": "finance", "goal": "Build $1M ARR SaaS", "context": "Technical founder, working full-time"},
    {"id": 40, "domain": "finance", "goal": "Exit startup for $50M", "context": "Series B funded, 50 employees"},
    {"id": 41, "domain": "finance", "goal": "Save $100k for house down payment", "context": "Age 28, $80k salary, saving $1.5k/month", "expected_age": 28},
    {"id": 42, "domain": "finance", "goal": "Accumulate $2M net worth", "context": "Age 40, $200k household income", "expected_age": 40},
    {"id": 43, "domain": "finance", "goal": "Retire by age 45", "context": "$500k current assets, $150k income", "expected_age": 45},
    {"id": 44, "domain": "finance", "goal": "Build emergency fund of $50k", "context": "$5k/month expenses, saving $2k/month"},
    {"id": 45, "domain": "finance", "goal": "Pay off mortgage early", "context": "$300k remaining, 15 years left, extra $1k/month"},
    
    # Fitness Domain (15 tests) - Sample subset for performance
    {"id": 46, "domain": "fitness", "goal": "Lose 50 pounds", "context": "Age 32, working out 5 hours/week, 6-month timeline", "expected_age": 32, "expected_hours": 5, "expected_timeline": 6},
    {"id": 47, "domain": "fitness", "goal": "Gain 20 pounds muscle", "context": "Lifting 6 hours/week, protein diet, 1 year timeline", "expected_hours": 6, "expected_timeline": 12},
    {"id": 48, "domain": "fitness", "goal": "Get to 10% body fat", "context": "Currently 18%, training 8 hours/week", "expected_hours": 8},
    {"id": 49, "domain": "fitness", "goal": "Run sub-3-hour marathon", "context": "Current PR 3:30, running 8 hours/week", "expected_hours": 8},
    {"id": 50, "domain": "fitness", "goal": "Complete Ironman triathlon", "context": "Training 12 hours/week, 18-month timeline", "expected_hours": 12, "expected_timeline": 18},
]

def run_single_test(test_case):
    """Run a single test case and return results"""
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
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data,
                "error": None
            }
        else:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }

def analyze_extraction(test_case, result_data):
    """Analyze extraction quality for a test case"""
    analysis = {
        "test_id": test_case["id"],
        "domain": test_case["domain"], 
        "goal": test_case["goal"],
        "context": test_case["context"],
        "success": True,
        "issues": [],
        "extracted_data": {}
    }
    
    if not result_data:
        analysis["success"] = False
        analysis["issues"].append("No result data")
        return analysis
    
    # Extract key data points
    probability = result_data.get("probability", 0)
    extracted_vars = result_data.get("extracted_variables", {})
    standardized = result_data.get("standardized_data", {})
    
    analysis["extracted_data"] = {
        "probability": probability,
        "extracted_variables": extracted_vars,
        "standardized_data": standardized
    }
    
    # Check company extraction
    if "expected_company" in test_case:
        expected = test_case["expected_company"]
        found_company = standardized.get("target_company")
        selectivity = standardized.get("selectivity_score")
        
        if found_company == expected:
            analysis["company_extraction"] = "✅ PASS"
        else:
            analysis["company_extraction"] = f"❌ FAIL - Expected: {expected}, Got: {found_company}"
            analysis["issues"].append(f"Company mismatch: expected {expected}, got {found_company}")
            analysis["success"] = False
            
        if selectivity and selectivity >= 80:
            analysis["selectivity_detection"] = "✅ PASS"
        else:
            analysis["selectivity_detection"] = f"❌ FAIL - Selectivity: {selectivity}"
            analysis["issues"].append(f"Low/missing selectivity score: {selectivity}")
    
    # Check other expected variables
    for key in ["expected_age", "expected_hours", "expected_timeline", "expected_education", "expected_salary"]:
        if key in test_case:
            expected_val = test_case[key]
            actual_key = key.replace("expected_", "")
            if actual_key == "hours":
                actual_key = "hours_per_day"
            elif actual_key == "timeline":
                actual_key = "timeline_months"
            elif actual_key == "salary":
                actual_key = "target_salary"
            
            actual_val = standardized.get(actual_key)
            
            if actual_val == expected_val or (expected_val is None and actual_val is None):
                analysis[f"{actual_key}_extraction"] = "✅ PASS"
            else:
                analysis[f"{actual_key}_extraction"] = f"❌ FAIL - Expected: {expected_val}, Got: {actual_val}"
                analysis["issues"].append(f"{actual_key} mismatch: expected {expected_val}, got {actual_val}")
    
    return analysis

def main():
    """Run all test cases and generate analysis"""
    print("🚀 Starting MirrorOS USV Test Suite")
    print(f"📊 Running {len(TEST_CASES)} test cases...")
    print(f"🎯 API Endpoint: {API_URL}")
    print("=" * 80)
    
    results = []
    failed_tests = []
    company_extraction_stats = {}
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n[{i:3d}/{len(TEST_CASES)}] Test {test_case['id']:2d}: {test_case['domain']}")
        print(f"Goal: {test_case['goal'][:50]}...")
        
        # Run the test
        result = run_single_test(test_case)
        
        if result["success"]:
            # Analyze extraction
            analysis = analyze_extraction(test_case, result["data"])
            results.append(analysis)
            
            # Track company extraction stats
            if "expected_company" in test_case:
                company = test_case["expected_company"]
                variation = test_case["goal"].lower()
                
                if company not in company_extraction_stats:
                    company_extraction_stats[company] = {"total": 0, "passed": 0, "variations": {}}
                
                company_extraction_stats[company]["total"] += 1
                if analysis["success"]:
                    company_extraction_stats[company]["passed"] += 1
                
                # Track by variation
                key_variation = "lowercase" if variation != test_case["goal"] else "normal"
                if key_variation not in company_extraction_stats[company]["variations"]:
                    company_extraction_stats[company]["variations"][key_variation] = {"total": 0, "passed": 0}
                
                company_extraction_stats[company]["variations"][key_variation]["total"] += 1
                if analysis["success"]:
                    company_extraction_stats[company]["variations"][key_variation]["passed"] += 1
            
            # Print quick status
            status = "✅ PASS" if analysis["success"] else "❌ FAIL"
            prob = result["data"].get("probability", 0)
            print(f"Result: {status} | Probability: {prob:.1%}")
            
            if not analysis["success"]:
                failed_tests.append(analysis)
                print(f"Issues: {', '.join(analysis['issues'][:2])}")
                
        else:
            print(f"❌ API ERROR: {result['error']}")
            failed_tests.append({
                "test_id": test_case["id"],
                "error": result["error"]
            })
        
        # Rate limiting
        time.sleep(0.5)
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY REPORT")
    print("=" * 80)
    
    total_tests = len(TEST_CASES)
    passed_tests = len([r for r in results if r["success"]])
    failed_count = len(failed_tests)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ({passed_tests/total_tests:.1%})")
    print(f"Failed: {failed_count} ({failed_count/total_tests:.1%})")
    
    # Company extraction analysis
    print(f"\n🏢 COMPANY EXTRACTION ANALYSIS")
    print("-" * 50)
    
    for company, stats in company_extraction_stats.items():
        success_rate = stats["passed"] / stats["total"] * 100
        print(f"{company.upper()}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        for variation, var_stats in stats["variations"].items():
            var_rate = var_stats["passed"] / var_stats["total"] * 100
            print(f"  └── {variation}: {var_stats['passed']}/{var_stats['total']} ({var_rate:.1f}%)")
    
    # Failed test details
    if failed_tests:
        print(f"\n❌ FAILED TESTS DETAILS")
        print("-" * 50)
        
        for failure in failed_tests[:10]:  # Show first 10 failures
            if "error" in failure:
                print(f"Test {failure['test_id']}: API Error - {failure['error']}")
            else:
                print(f"Test {failure['test_id']}: {', '.join(failure['issues'][:2])}")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"usv_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_count,
                "success_rate": passed_tests/total_tests
            },
            "company_stats": company_extraction_stats,
            "detailed_results": results,
            "failed_tests": failed_tests
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    print("🎯 Test suite completed!")

if __name__ == "__main__":
    main()