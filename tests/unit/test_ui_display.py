#!/usr/bin/env python3
"""
UI-style display for risk analysis results
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.risk_aggregator import ComplexRiskAggregator
from core.evidence_mapper import map_evidence
from datetime import datetime

def display_ui_results():
    print("=" * 80)
    print("🚨 KORINSIC RISK SURVEILLANCE DASHBOARD")
    print("=" * 80)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Trader ID: TRADER_INSIDER_001")
    print(f"📊 Analysis Period: Last 7 days")
    print()
    
    # Test data
    test_data = {
        "trades": [
            {"id": "trade_001", "volume": 50000, "side": "buy", "timestamp": "2024-01-01T10:00:00Z"},
            {"id": "trade_002", "volume": 75000, "side": "buy", "timestamp": "2024-01-02T10:00:00Z"},
            {"id": "trade_003", "volume": 100000, "side": "buy", "timestamp": "2024-01-03T10:00:00Z"}
        ],
        "orders": [
            {"id": "order_001", "size": 10000, "status": "cancelled"},
            {"id": "order_002", "size": 15000, "status": "cancelled"},
            {"id": "order_003", "size": 5000, "status": "filled"}
        ],
        "hr": {
            "access_level": "high",
            "role": "senior_trader",
            "insider_indicators": ["board_meeting_access", "earnings_call_access"],
            "disciplinary_actions": 1,
            "compliance_violations": 2
        },
        "pnl": {
            "drift": 5000,
            "threshold": 10000,
            "recent_pnl": [
                {"value": -50000, "timestamp": "2024-01-01T10:00:00Z"},
                {"value": -30000, "timestamp": "2024-01-02T10:00:00Z"},
                {"value": -20000, "timestamp": "2024-01-03T10:00:00Z"},
                {"value": 10000, "timestamp": "2024-01-04T10:00:00Z"}
            ]
        },
        "sales": {
            "client_activity": {
                "unusual_count": 5,
                "volume_change": 0.6
            }
        },
        "comms": {
            "intent": "suspicious",
            "messages": [
                {"text": "suspicious message 1", "sentiment": "negative"},
                {"text": "suspicious message 2", "sentiment": "negative"}
            ]
        },
        "trade": {
            "suspicious_flag": True
        },
        "market": {
            "price_movement": 0.08,
            "material_events": [
                {
                    "timestamp": "2024-01-05T10:00:00Z", 
                    "type": "earnings",
                    "expected_impact": 0.06,
                    "materiality_score": 0.8,
                    "description": "Strong quarterly earnings"
                }
            ]
        },
        "news": {
            "news_events": [
                {
                    "sentiment": 0.7,
                    "market_impact": 0.04,
                    "relevance_score": 0.8,
                    "headline": "Company beats earnings expectations"
                }
            ]
        },
        "historical": {
            "alert_count": 3,
            "avg_volume": 20000
        }
    }
    
    # Process data using enhanced Bayesian engine
    from core.bayesian_engine import BayesianEngine
    from core.data_processor import DataProcessor
    
    data_processor = DataProcessor()
    bayesian_engine = BayesianEngine()
    
    processed_data = data_processor.process(test_data)
    result = bayesian_engine.calculate_insider_dealing_risk(processed_data)
    
    # RISK OVERVIEW SECTION
    print("🎯 RISK OVERVIEW")
    print("-" * 40)
    risk_level = result['risk_level']
    risk_color = {
        'CRITICAL': '🔴',
        'HIGH': '🟠', 
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }
    
    print(f"{risk_color.get(risk_level, '⚪')} Overall Risk Level: {risk_level}")
    print(f"📊 Risk Score: {result['overall_score']:.1%}")
    print(f"⚠️  High-Risk Indicators: {len(result.get('high_nodes', []))}")
    print(f"🚨 Critical Indicators: {len(result.get('critical_nodes', []))}")
    print(f"📰 News Context: {result.get('news_context', 'N/A')}")
    print()
    
    # DATA SUMMARY SECTION
    print("📈 DATA SUMMARY")
    print("-" * 40)
    print(f"💼 Trades Analyzed: {len(test_data['trades'])}")
    print(f"📋 Orders Processed: {len(test_data['orders'])}")
    print(f"💰 PnL Records: {len(test_data['pnl']['recent_pnl'])}")
    print(f"💬 Communications: {len(test_data['comms']['messages'])}")
    print(f"📅 Material Events: {len(test_data['market']['material_events'])}")
    print(f"📰 News Events: {len(test_data.get('news', {}).get('news_events', []))}")
    print()
    
    # ALERT TRIGGERS SECTION
    print("🚨 ALERT TRIGGERS")
    print("-" * 40)
    high_nodes = result.get('high_nodes', [])
    critical_nodes = result.get('critical_nodes', [])
    
    if len(critical_nodes) > 0:
        print("🔴 CRITICAL NODE ALERT: Critical risk factors present")
    if len(high_nodes) > 2:
        print("🔴 MULTI-NODE ALERT: Multiple high-risk indicators detected")
    if len(high_nodes) == 0 and len(critical_nodes) == 0:
        print("🟢 No critical alerts triggered")
    print()
    
    # TOP RISK FACTORS SECTION
    print("🔥 TOP RISK FACTORS")
    print("-" * 40)
    if 'node_scores' in result:
        top_contributors = sorted(result['node_scores'].items(), 
                                key=lambda x: x[1].get('weighted_score', 0), reverse=True)[:5]
        
        for i, (node_name, score_info) in enumerate(top_contributors, 1):
            risk_icon = "🔴" if score_info.get('state_index', 0) >= 2 else "🟠" if score_info.get('state_index', 0) >= 1 else "🟢"
            print(f"{i}. {risk_icon} {score_info.get('description', node_name)}")
            print(f"   Score: {score_info.get('weighted_score', 0):.2f} | State: {score_info.get('state_index', 0)}")
    else:
        print("📊 Risk factors analysis available in detailed results")
    print()
    
    # PNL ANALYSIS SECTION
    print("💰 PNL ANALYSIS")
    print("-" * 40)
    pnl_values = [p['value'] for p in test_data['pnl']['recent_pnl']]
    total_loss = sum([v for v in pnl_values if v < 0])
    total_gain = sum([v for v in pnl_values if v > 0])
    
    print(f"📉 Total Losses: ${abs(total_loss):,}")
    print(f"📈 Total Gains: ${total_gain:,}")
    print(f"📊 Net PnL: ${total_gain + total_loss:,}")
    
    if total_loss > abs(total_gain):
        print("⚠️  WARNING: Net negative PnL detected")
    print()
    
    # RECOMMENDED ACTIONS SECTION
    print("🎯 RECOMMENDED ACTIONS")
    print("-" * 40)
    
    risk_level = result.get('risk_level', 'UNKNOWN')
    if risk_level == 'CRITICAL':
        print("🔴 IMMEDIATE ACTION REQUIRED:")
        print("   • Suspend trading privileges")
        print("   • Initiate compliance investigation")
        print("   • Notify senior management")
        print("   • Review all recent trades")
    elif risk_level == 'HIGH':
        print("🟠 URGENT REVIEW REQUIRED:")
        print("   • Enhanced monitoring")
        print("   • Compliance review")
        print("   • Manager notification")
    elif risk_level == 'MEDIUM':
        print("🟡 MONITORING REQUIRED:")
        print("   • Regular review")
        print("   • Watch for escalation")
    else:
        print("🟢 STANDARD MONITORING:")
        print("   • Continue normal surveillance")
    
    print()
    print("=" * 80)
    print("📋 Analysis Complete | Generated by Korinsic Risk Engine")
    print("=" * 80)

if __name__ == "__main__":
    display_ui_results() 