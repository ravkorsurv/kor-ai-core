#!/usr/bin/env python3
"""
Simple Test Script for Hidden Causality and Latent Intent Feature
Demonstrates the Korinsic approach of modeling unobservable core abusive intent.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_latent_intent_nodes():
    """Test the new latent intent node classes"""
    print("Testing Latent Intent Node Classes")
    print("=" * 50)
    
    try:
        from core.node_library import (
            LatentIntentNode, ProfitMotivationNode, AccessPatternNode, 
            OrderBehaviorNode, CommsMetadataNode
        )
        
        # Test LatentIntentNode
        print("\n1. Testing LatentIntentNode:")
        latent_node = LatentIntentNode("test_intent", description="Test latent intent")
        print(f"   Name: {latent_node.name}")
        print(f"   States: {latent_node.states}")
        print(f"   Description: {latent_node.description}")
        
        # Test converging evidence nodes
        print("\n2. Testing Converging Evidence Nodes:")
        evidence_nodes = [
            ("ProfitMotivationNode", ProfitMotivationNode("test_profit", "Test profit motivation")),
            ("AccessPatternNode", AccessPatternNode("test_access", "Test access pattern")),
            ("OrderBehaviorNode", OrderBehaviorNode("test_behavior", "Test order behavior")),
            ("CommsMetadataNode", CommsMetadataNode("test_comms", "Test comms metadata"))
        ]
        
        for name, node in evidence_nodes:
            print(f"   {name}: {node.states}")
        
        print("\n✓ All latent intent node classes working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Error testing latent intent nodes: {e}")
        return False

def test_model_construction():
    """Test the model construction with latent intent"""
    print("\nTesting Model Construction with Latent Intent")
    print("=" * 50)
    
    try:
        from core.model_construction import build_insider_dealing_bn_with_latent_intent
        
        # Build the model
        model = build_insider_dealing_bn_with_latent_intent()
        
        print(f"✓ Model built successfully")
        print(f"   Total nodes: {len(model.nodes())}")
        print(f"   Total edges: {len(model.edges())}")
        print(f"   Latent nodes: {model.latents}")
        
        # Check for key nodes
        expected_nodes = [
            "latent_intent", "profit_motivation", "access_pattern", 
            "order_behavior", "comms_metadata", "risk_factor", "insider_dealing"
        ]
        
        for node in expected_nodes:
            if node in model.nodes():
                print(f"   ✓ Found node: {node}")
            else:
                print(f"   ✗ Missing node: {node}")
                return False
        
        # Check model validity
        if model.check_model():
            print("   ✓ Model validation passed")
        else:
            print("   ✗ Model validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing model construction: {e}")
        return False

def test_bayesian_engine_integration():
    """Test the Bayesian engine integration with latent intent"""
    print("\nTesting Bayesian Engine Integration")
    print("=" * 50)
    
    try:
        from core.bayesian_engine import BayesianEngine
        
        # Initialize engine
        engine = BayesianEngine()
        
        print(f"✓ Bayesian engine initialized")
        print(f"   Models loaded: {engine.models_loaded}")
        
        # Check if latent intent model is available
        if hasattr(engine, 'insider_dealing_model_with_latent'):
            print("   ✓ Latent intent model available")
        else:
            print("   ✗ Latent intent model not available")
            return False
        
        # Test with sample data
        sample_data = {
            'trades': [{'volume': 1000, 'price': 50.0}],
            'orders': [{'size': 1000, 'status': 'filled'}],
            'trader_info': {'role': 'trader'},
            'historical_data': {'avg_volume': 500},
            'pnl_metrics': {'drift_score': 0.05, 'profit_ratio': 0.1},
            'access_logs': [],
            'comms_data': {'unusual_patterns': 0},
            'comms_indicators': []
        }
        
        # Test latent intent risk calculation
        result = engine.calculate_insider_dealing_risk_with_latent_intent(sample_data)
        
        if 'error' not in result:
            print("   ✓ Latent intent risk calculation successful")
            print(f"   Insider dealing probability: {result.get('insider_dealing_probability', 0):.3f}")
            print(f"   Latent intent (clear): {result.get('latent_intent_clear', 0):.3f}")
        else:
            print(f"   ✗ Latent intent risk calculation failed: {result['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing Bayesian engine integration: {e}")
        return False

def run_simple_test():
    """Run the simple test suite"""
    print("KORINSIC - Hidden Causality and Latent Intent Feature Test")
    print("=" * 60)
    print("Testing the Korinsic approach of modeling unobservable core abusive intent")
    print("through latent nodes with converging evidence paths.")
    print("=" * 60)
    
    tests = [
        ("Latent Intent Nodes", test_latent_intent_nodes),
        ("Model Construction", test_model_construction),
        ("Bayesian Engine Integration", test_bayesian_engine_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print(f"\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ ALL TESTS PASSED - Latent Intent Feature Working Correctly")
        print("\nFeature Summary:")
        print("- Hidden causality modeling through latent intent nodes")
        print("- Converging evidence paths from profit, access, order behavior, and comms metadata")
        print("- Unobservable core abusive intent inference")
        print("- Enhanced risk assessment through latent variable modeling")
    else:
        print("✗ SOME TESTS FAILED - Please check implementation")
    
    print("=" * 60)

if __name__ == "__main__":
    run_simple_test() 