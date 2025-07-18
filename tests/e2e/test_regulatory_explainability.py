# -*- coding: utf-8 -*-
"""
Test script for Regulatory Explainability Feature
Tests structured inference paths, rationale attachment, STOR-ready exports, and VOI/sensitivity reporting.
"""

import json
import requests
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from core.regulatory_explainability import RegulatoryExplainability, RegulatoryRationale, STORRecord
    from core.alert_generator import AlertGenerator
    from core.bayesian_engine import BayesianEngine
    from core.data_processor import DataProcessor
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the correct directory and the server is started")
    sys.exit(1)

BASE_URL = "http://localhost:5000"

def generate_test_data(scenario_type="high_risk"):
    """Generate test data for regulatory explainability testing"""
    
    base_time = datetime.utcnow()
    
    if scenario_type == "high_risk":
        # High-risk insider dealing scenario
        data = {
            "trades": [
                {
                    "id": "trade_001",
                    "timestamp": (base_time - timedelta(hours=2)).isoformat() + "Z",
                    "instrument": "AAPL",
                    "volume": 50000,
                    "price": 150.0,
                    "side": "buy",
                    "trader_id": "trader_001"
                }
            ],
            "orders": [
                {
                    "id": "order_001",
                    "timestamp": (base_time - timedelta(hours=3)).isoformat() + "Z",
                    "instrument": "AAPL",
                    "volume": 100000,
                    "price": 148.0,
                    "side": "buy",
                    "status": "filled",
                    "trader_id": "trader_001"
                }
            ],
            "trader_info": {
                "id": "trader_001",
                "name": "John Doe",
                "role": "executive",
                "access_level": "high",
                "department": "trading"
            },
            "material_events": [
                {
                    "timestamp": (base_time + timedelta(hours=1)).isoformat() + "Z",
                    "type": "earnings",
                    "description": "Strong quarterly earnings announcement",
                    "expected_impact": 0.15,
                    "materiality_score": 0.9
                }
            ],
            "market_data": {
                "volatility": 0.03,
                "liquidity": 0.7,
                "price_change": 0.12
            },
            "metrics": {
                "volume_ratio": 3.5,
                "pre_event_trading": 1,
                "timing_concentration": 8,
                "price_impact": 0.08,
                "cancellation_ratio": 0.2,
                "order_frequency": 15
            },
            "timeframe": "intraday",
            "instruments": ["AAPL"]
        }
    
    elif scenario_type == "spoofing":
        # Spoofing scenario
        data = {
            "trades": [
                {
                    "id": "trade_001",
                    "timestamp": base_time.isoformat() + "Z",
                    "instrument": "CRUDE_FUTURE",
                    "volume": 1000,
                    "price": 70.0,
                    "side": "buy",
                    "trader_id": "spoof_trader_001"
                }
            ],
            "orders": [
                {
                    "id": "order_001",
                    "timestamp": (base_time - timedelta(minutes=30)).isoformat() + "Z",
                    "instrument": "CRUDE_FUTURE",
                    "volume": 50000,
                    "price": 69.5,
                    "side": "buy",
                    "status": "cancelled",
                    "trader_id": "spoof_trader_001"
                }
            ],
            "trader_info": {
                "id": "spoof_trader_001",
                "name": "Spoof Trader",
                "role": "trader",
                "access_level": "standard"
            },
            "material_events": [],
            "market_data": {
                "volatility": 0.02,
                "liquidity": 0.6
            },
            "metrics": {
                "volume_ratio": 2.0,
                "cancellation_ratio": 0.8,
                "order_frequency": 25,
                "volume_imbalance": 0.7
            },
            "timeframe": "intraday",
            "instruments": ["CRUDE_FUTURE"]
        }
    
    else:
        # Low-risk scenario
        data = {
            "trades": [
                {
                    "id": "trade_001",
                    "timestamp": base_time.isoformat() + "Z",
                    "instrument": "MSFT",
                    "volume": 1000,
                    "price": 300.0,
                    "side": "buy",
                    "trader_id": "trader_002"
                }
            ],
            "orders": [],
            "trader_info": {
                "id": "trader_002",
                "name": "Jane Smith",
                "role": "analyst",
                "access_level": "low"
            },
            "material_events": [],
            "market_data": {
                "volatility": 0.01,
                "liquidity": 0.8
            },
            "metrics": {
                "volume_ratio": 0.5,
                "pre_event_trading": 0,
                "timing_concentration": 1,
                "price_impact": 0.01,
                "cancellation_ratio": 0.1,
                "order_frequency": 2
            },
            "timeframe": "daily",
            "instruments": ["MSFT"]
        }
    
    return data

def test_regulatory_explainability_module():
    """Test the regulatory explainability module directly"""
    print("TESTING REGULATORY EXPLAINABILITY MODULE")
    print("=" * 60)
    
    try:
        # Initialize components
        regulatory_explainability = RegulatoryExplainability()
        alert_generator = AlertGenerator()
        bayesian_engine = BayesianEngine()
        data_processor = DataProcessor()
        
        # Test with high-risk scenario
        test_data = generate_test_data("high_risk")
        processed_data = data_processor.process(test_data)
        
        # Calculate risk scores
        insider_score = bayesian_engine.calculate_insider_dealing_risk(processed_data)
        
        # Generate alerts
        alerts = alert_generator.generate_alerts(
            processed_data, insider_score, 
            {'overall_score': 0.1}, 0.6
        )
        
        if not alerts:
            print("No alerts generated for high-risk scenario")
            return False
        
        # Test regulatory rationale generation
        alert = alerts[0]
        rationale = regulatory_explainability.generate_regulatory_rationale(
            alert, insider_score, processed_data
        )
        
        print(f"Regulatory rationale generated for alert {alert['id']}")
        print(f"   Risk Type: {rationale.risk_type}")
        print(f"   Severity: {rationale.severity}")
        print(f"   Inference Paths: {len(rationale.inference_paths)}")
        print(f"   VOI Analysis: {len(rationale.voi_analysis)} factors")
        print(f"   Regulatory Frameworks: {rationale.regulatory_frameworks}")
        
        # Test STOR export
        stor_record = regulatory_explainability.export_stor_format(rationale, processed_data)
        print(f"STOR record generated: {stor_record.record_id}")
        print(f"   Suspicious Indicators: {len(stor_record.suspicious_indicators)}")
        
        # Test CSV export
        csv_filename = regulatory_explainability.export_csv_report(rationale)
        print(f"CSV report exported: {csv_filename}")
        
        # Test deterministic narrative
        print("\nDETERMINISTIC NARRATIVE:")
        print("-" * 40)
        print(rationale.deterministic_narrative[:500] + "..." if len(rationale.deterministic_narrative) > 500 else rationale.deterministic_narrative)
        
        # Test inference paths
        print(f"\nTOP INFERENCE PATHS:")
        for i, path in enumerate(rationale.inference_paths[:3], 1):
            print(f"{i}. {path.node_name}: {path.rationale}")
            print(f"   Contribution: {path.contribution:.1%} | Confidence: {path.confidence:.2f}")
            print(f"   Regulatory Relevance: {path.regulatory_relevance}")
        
        # Test VOI analysis
        print(f"\nVALUE OF INFORMATION ANALYSIS:")
        for factor, voi_score in rationale.voi_analysis.items():
            print(f"   {factor}: {voi_score:.3f}")
        
        # Test sensitivity report
        print(f"\nSENSITIVITY REPORT:")
        sensitivity = rationale.sensitivity_report
        print(f"   Base Risk Score: {sensitivity.get('base_risk_score', 0):.3f}")
        print(f"   Scenario Analysis: {len(sensitivity.get('scenario_analysis', {}))} scenarios")
        print(f"   Confidence Intervals: {sensitivity.get('confidence_intervals', {})}")
        
        return True
        
    except Exception as e:
        print(f"Error testing regulatory explainability module: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_integration():
    """Test the API integration of regulatory explainability"""
    print("\nTESTING API INTEGRATION")
    print("=" * 60)
    
    try:
        # Test with regulatory explainability enabled
        test_data = generate_test_data("high_risk")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json={
                **test_data,
                "include_regulatory_rationale": True
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        print(f"API analysis completed")
        print(f"   Analysis ID: {result['analysis_id']}")
        print(f"   Alerts Generated: {len(result['alerts'])}")
        print(f"   Regulatory Rationales: {len(result['regulatory_rationales'])}")
        
        if result['regulatory_rationales']:
            rationale = result['regulatory_rationales'][0]
            print(f"   Deterministic Narrative: {len(rationale['deterministic_narrative'])} chars")
            print(f"   Inference Paths: {len(rationale['inference_paths'])}")
            print(f"   VOI Analysis: {len(rationale['voi_analysis'])} factors")
            print(f"   Audit Trail: {len(rationale['audit_trail'])} events")
        
        return True
        
    except Exception as e:
        print(f"Error testing API integration: {str(e)}")
        return False

def main():
    """Main test function"""
    print("REGULATORY EXPLAINABILITY FEATURE TEST")
    print("=" * 80)
    print("Testing structured inference paths, rationale attachment, STOR-ready exports, and VOI/sensitivity reporting")
    print("=" * 80)
    
    # Test module functionality
    module_success = test_regulatory_explainability_module()
    
    # Test API integration
    api_success = test_api_integration()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Module Tests: {'PASSED' if module_success else 'FAILED'}")
    print(f"API Integration: {'PASSED' if api_success else 'FAILED'}")
    
    overall_success = module_success and api_success
    print(f"\nOverall Result: {'ALL TESTS PASSED' if overall_success else 'SOME TESTS FAILED'}")
    
    if overall_success:
        print("\nRegulatory Explainability Feature is working correctly!")
        print("   - Structured inference paths")
        print("   - Deterministic narratives")
        print("   - STOR-ready exports")
        print("   - VOI/sensitivity reporting")
        print("   - Audit trails")
    else:
        print("\nSome tests failed. Please check the implementation.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
