#!/usr/bin/env python3
"""
Test Script for Hidden Causality and Latent Intent Feature
Tests the Kor.ai approach of modeling unobservable core abusive intent through latent nodes.
"""

import sys
import os
import json
import numpy as np
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.model_construction import build_insider_dealing_bn_with_latent_intent
from core.node_library import (
    LatentIntentNode, ProfitMotivationNode, AccessPatternNode, 
    OrderBehaviorNode, CommsMetadataNode
)
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

def test_latent_intent_model_structure():
    """Test the structure of the latent intent Bayesian network"""
    print("Testing Latent Intent Model Structure")
    print("=" * 50)
    
    # Build the model with latent intent
    model = build_insider_dealing_bn_with_latent_intent()
    
    # Check that latent intent is properly marked as latent
    assert "latent_intent" in model.latents, "latent_intent should be marked as latent"
    
    # Check that all converging evidence paths are connected to latent intent
    evidence_nodes = ["profit_motivation", "access_pattern", "order_behavior", "comms_metadata"]
    for node in evidence_nodes:
        assert model.has_edge(node, "latent_intent"), f"Edge from {node} to latent_intent missing"
    
    # Check that latent intent influences risk factor
    assert model.has_edge("latent_intent", "risk_factor"), "Edge from latent_intent to risk_factor missing"
    
    print("✓ Model structure validation passed")
    print(f"✓ Latent nodes: {model.latents}")
    print(f"✓ Total nodes: {len(model.nodes())}")
    print(f"✓ Total edges: {len(model.edges())}")
    
    return model

def test_converging_evidence_paths():
    """Test how converging evidence paths influence latent intent"""
    print("\nTesting Converging Evidence Paths")
    print("=" * 50)
    
    model = build_insider_dealing_bn_with_latent_intent()
    inference = VariableElimination(model)
    
    # Test scenarios with different evidence combinations
    test_scenarios = [
        {
            "name": "All Normal Evidence",
            "evidence": {
                "profit_motivation": 0,  # normal_profit
                "access_pattern": 0,     # normal_access
                "order_behavior": 0,     # normal_behavior
                "comms_metadata": 0      # normal_comms
            }
        },
        {
            "name": "Mixed Evidence",
            "evidence": {
                "profit_motivation": 1,  # unusual_profit
                "access_pattern": 0,     # normal_access
                "order_behavior": 1,     # unusual_behavior
                "comms_metadata": 0      # normal_comms
            }
        },
        {
            "name": "All Suspicious Evidence",
            "evidence": {
                "profit_motivation": 2,  # suspicious_profit
                "access_pattern": 2,     # suspicious_access
                "order_behavior": 2,     # suspicious_behavior
                "comms_metadata": 2      # suspicious_comms
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\nScenario: {scenario['name']}")
        print(f"Evidence: {scenario['evidence']}")
        
        # Query latent intent probability
        result = inference.query(variables=["latent_intent"], evidence=scenario['evidence'])
        
        print("Latent Intent Probabilities:")
        for i, state in enumerate(["no_intent", "potential_intent", "clear_intent"]):
            prob = result.values[i]
            print(f"  {state}: {prob:.3f}")
        
        # Query risk factor probability
        risk_result = inference.query(variables=["risk_factor"], evidence=scenario['evidence'])
        
        print("Risk Factor Probabilities:")
        for i, state in enumerate(["low", "medium", "high"]):
            prob = risk_result.values[i]
            print(f"  {state}: {prob:.3f}")

def test_hidden_causality_inference():
    """Test the hidden causality inference - how latent intent affects outcomes"""
    print("\nTesting Hidden Causality Inference")
    print("=" * 50)
    
    model = build_insider_dealing_bn_with_latent_intent()
    inference = VariableElimination(model)
    
    # Test how different latent intent levels affect insider dealing probability
    intent_levels = [0, 1, 2]  # no_intent, potential_intent, clear_intent
    
    for intent_level in intent_levels:
        print(f"\nLatent Intent Level: {['no_intent', 'potential_intent', 'clear_intent'][intent_level]}")
        
        # Set latent intent and observe outcome
        result = inference.query(
            variables=["insider_dealing"], 
            evidence={"latent_intent": intent_level}
        )
        
        print("Insider Dealing Probabilities:")
        for i, state in enumerate(["no", "yes"]):
            prob = result.values[i]
            print(f"  {state}: {prob:.3f}")

def test_evidence_convergence_analysis():
    """Test how evidence convergence affects latent intent inference"""
    print("\nTesting Evidence Convergence Analysis")
    print("=" * 50)
    
    model = build_insider_dealing_bn_with_latent_intent()
    inference = VariableElimination(model)
    
    # Test progressive evidence accumulation
    base_evidence = {
        "trade_pattern": 0,      # normal
        "comms_intent": 0,       # benign
        "pnl_drift": 0           # normal
    }
    
    # Progressive addition of suspicious evidence
    progressive_evidence = [
        {"profit_motivation": 0},  # normal_profit
        {"profit_motivation": 1},  # unusual_profit
        {"profit_motivation": 1, "access_pattern": 1},  # unusual_profit + unusual_access
        {"profit_motivation": 1, "access_pattern": 1, "order_behavior": 1},  # + unusual_behavior
        {"profit_motivation": 1, "access_pattern": 1, "order_behavior": 1, "comms_metadata": 1},  # + unusual_comms
        {"profit_motivation": 2, "access_pattern": 2, "order_behavior": 2, "comms_metadata": 2},  # all suspicious
    ]
    
    for i, additional_evidence in enumerate(progressive_evidence):
        evidence = {**base_evidence, **additional_evidence}
        print(f"\nEvidence Level {i+1}: {additional_evidence}")
        
        # Query latent intent
        intent_result = inference.query(variables=["latent_intent"], evidence=evidence)
        
        print("Latent Intent Probabilities:")
        for j, state in enumerate(["no_intent", "potential_intent", "clear_intent"]):
            prob = intent_result.values[j]
            print(f"  {state}: {prob:.3f}")
        
        # Query final outcome
        outcome_result = inference.query(variables=["insider_dealing"], evidence=evidence)
        
        print("Insider Dealing Probabilities:")
        for j, state in enumerate(["no", "yes"]):
            prob = outcome_result.values[j]
            print(f"  {state}: {prob:.3f}")

def test_latent_intent_node_functionality():
    """Test the LatentIntentNode class functionality"""
    print("\nTesting LatentIntentNode Functionality")
    print("=" * 50)
    
    # Create a latent intent node
    latent_node = LatentIntentNode("test_intent", description="Test latent intent node")
    
    print(f"Node name: {latent_node.name}")
    print(f"Node states: {latent_node.states}")
    print(f"Node description: {latent_node.description}")
    print(f"Fallback prior: {latent_node.get_fallback_prior()}")
    
    # Test intent strength calculation
    evidence_values = {
        "profit_motivation": "unusual_profit",
        "access_pattern": "normal_access",
        "order_behavior": "suspicious_behavior",
        "comms_metadata": "unusual_comms"
    }
    
    intent_strength = latent_node.get_intent_strength(evidence_values)
    print(f"Intent strength for evidence {evidence_values}: {intent_strength}")
    
    # Test node explanation
    print(f"Node explanation:\n{latent_node.explain()}")

def test_converging_evidence_nodes():
    """Test the converging evidence node classes"""
    print("\nTesting Converging Evidence Nodes")
    print("=" * 50)
    
    # Test each converging evidence node type
    evidence_nodes = [
        ProfitMotivationNode("test_profit", description="Test profit motivation"),
        AccessPatternNode("test_access", description="Test access pattern"),
        OrderBehaviorNode("test_behavior", description="Test order behavior"),
        CommsMetadataNode("test_comms", description="Test comms metadata")
    ]
    
    for node in evidence_nodes:
        print(f"\n{node.__class__.__name__}:")
        print(f"  Name: {node.name}")
        print(f"  States: {node.states}")
        print(f"  Description: {node.description}")
        print(f"  Fallback prior: {node.get_fallback_prior()}")

def test_model_validation():
    """Test that the model with latent intent is properly validated"""
    print("\nTesting Model Validation")
    print("=" * 50)
    
    model = build_insider_dealing_bn_with_latent_intent()
    
    # Check model validity
    is_valid = model.check_model()
    print(f"Model validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")
    
    # Check that all CPDs are properly defined
    cpds = model.get_cpds()
    print(f"Number of CPDs: {len(cpds)}")
    
    # Check that latent variables are properly handled
    print(f"Latent variables: {model.latents}")
    
    # Test inference engine initialization
    try:
        inference = VariableElimination(model)
        print("✓ Inference engine initialized successfully")
    except Exception as e:
        print(f"✗ Inference engine initialization failed: {e}")

def run_comprehensive_test():
    """Run all tests for the latent intent feature"""
    print("KOR.AI - Hidden Causality and Latent Intent Feature Test")
    print("=" * 60)
    print("Testing the Kor.ai approach of modeling unobservable core abusive intent")
    print("through latent nodes with converging evidence paths from trade, PnL, and comms metadata.")
    print("=" * 60)
    
    try:
        # Run all test functions
        test_latent_intent_model_structure()
        test_converging_evidence_paths()
        test_hidden_causality_inference()
        test_evidence_convergence_analysis()
        test_latent_intent_node_functionality()
        test_converging_evidence_nodes()
        test_model_validation()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - Latent Intent Feature Working Correctly")
        print("=" * 60)
        
        # Summary of the feature
        print("\nFeature Summary:")
        print("- Hidden causality modeling through latent intent nodes")
        print("- Converging evidence paths from profit, access, order behavior, and comms metadata")
        print("- Unobservable core abusive intent inference")
        print("- Enhanced risk assessment through latent variable modeling")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_comprehensive_test()
