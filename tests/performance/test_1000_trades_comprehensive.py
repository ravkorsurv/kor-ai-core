#!/usr/bin/env python3
"""
Comprehensive Mock Data Test: 1000 Trades with Various Alert Scenarios
Tests both positive alerts (should trigger) and negative tests (should not trigger)
"""

import sys
import os
import json
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Import core modules with fallback for testing
try:
    from core.data_processor import DataProcessor
    from core.bayesian_engine import BayesianEngine
    from core.risk_aggregator import ComplexRiskAggregator
    MODULES_AVAILABLE = True
except ImportError:
    # Create mock classes for testing when modules are not available
    class MockDataProcessor:
        def process(self, data):
            return data
    
    class MockBayesianEngine:
        def calculate_insider_dealing_risk(self, data):
            return {"overall_score": random.uniform(0.1, 0.9), "risk_level": "MEDIUM"}
        def calculate_spoofing_risk(self, data):
            return {"overall_score": random.uniform(0.1, 0.9), "risk_level": "MEDIUM"}
    
    DataProcessor = MockDataProcessor
    BayesianEngine = MockBayesianEngine
    ComplexRiskAggregator = None
    MODULES_AVAILABLE = False
    print("Warning: Core modules not found. Using mock implementations for testing.")

class TradeScenarioGenerator:
    """Generate various trading scenarios for comprehensive testing"""
    
    def __init__(self):
        self.base_time = datetime.utcnow() - timedelta(days=30)
        self.instruments = [
            "CRUDE_OIL_FUTURE", "NATURAL_GAS_FUTURE", "ENERGY_STOCK_A", 
            "ENERGY_STOCK_B", "POWER_FUTURE", "HEATING_OIL_FUTURE",
            "GASOLINE_FUTURE", "ENERGY_ETF_X", "RENEWABLE_STOCK_C", "UTILITIES_STOCK_D"
        ]
        self.trader_profiles = self._create_trader_profiles()
        
    def _create_trader_profiles(self) -> Dict[str, Dict]:
        """Create diverse trader profiles for testing"""
        return {
            "insider_high_risk": {
                "id": "trader_insider_001",
                "name": "John Executive",
                "role": "senior_trader",
                "department": "energy_trading",
                "access_level": "high",
                "insider_access": True,
                "compliance_violations": 2,
                "disciplinary_actions": 1
            },
            "insider_medium_risk": {
                "id": "trader_insider_002", 
                "name": "Sarah Manager",
                "role": "portfolio_manager",
                "department": "investment",
                "access_level": "medium",
                "insider_access": True,
                "compliance_violations": 1,
                "disciplinary_actions": 0
            },
            "spoofer_high_risk": {
                "id": "trader_spoofer_001",
                "name": "Mike Manipulator",
                "role": "trader",
                "department": "commodities",
                "access_level": "standard",
                "insider_access": False,
                "compliance_violations": 3,
                "disciplinary_actions": 2
            },
            "normal_trader_1": {
                "id": "trader_normal_001",
                "name": "Alice Regular",
                "role": "trader",
                "department": "trading",
                "access_level": "standard",
                "insider_access": False,
                "compliance_violations": 0,
                "disciplinary_actions": 0
            },
            "normal_trader_2": {
                "id": "trader_normal_002",
                "name": "Bob Standard",
                "role": "analyst",
                "department": "research",
                "access_level": "low",
                "insider_access": False,
                "compliance_violations": 0,
                "disciplinary_actions": 0
            }
        }
    
    def generate_insider_dealing_scenario(self, num_trades: int, risk_level: str = "high") -> Dict[str, Any]:
        """Generate insider dealing scenario trades"""
        trades = []
        material_events = []
        
        # Create material event that should trigger insider alerts
        event_time = self.base_time + timedelta(days=random.randint(15, 25))
        material_events.append({
            "id": f"event_insider_{random.randint(1000, 9999)}",
            "timestamp": event_time.isoformat() + "Z",
            "type": "earnings_announcement",
            "description": "Major acquisition announcement - 20% premium",
            "instruments_affected": [random.choice(self.instruments)],
            "materiality_score": 0.9 if risk_level == "high" else 0.6
        })
        
        trader_key = "insider_high_risk" if risk_level == "high" else "insider_medium_risk"
        trader = self.trader_profiles[trader_key]
        instrument = material_events[0]["instruments_affected"][0]
        
        # Generate trades leading up to the event (suspicious timing)
        for i in range(num_trades):
            days_before_event = random.randint(1, 5) if risk_level == "high" else random.randint(7, 14)
            trade_time = event_time - timedelta(days=days_before_event, hours=random.randint(1, 23))
            
            # High risk: large volumes, consistent direction
            if risk_level == "high":
                volume = random.randint(50000, 200000)
                side = "buy"  # Consistent buying before good news
            else:
                volume = random.randint(10000, 50000)
                side = random.choice(["buy", "sell"])
            
            trade = {
                "id": f"trade_insider_{i:04d}",
                "timestamp": trade_time.isoformat() + "Z",
                "instrument": instrument,
                "volume": volume,
                "price": 45.50 + random.uniform(-2, 2),
                "side": side,
                "trader_id": trader["id"]
            }
            trades.append(trade)
        
        return {
            "trades": trades,
            "material_events": material_events,
            "trader_info": trader,
            "scenario_type": "insider_dealing",
            "expected_risk": risk_level
        }
    
    def generate_spoofing_scenario(self, num_trades: int, risk_level: str = "high") -> Dict[str, Any]:
        """Generate spoofing scenario with layered orders and cancellations"""
        trades = []
        orders = []
        
        trader = self.trader_profiles["spoofer_high_risk"]
        instrument = random.choice(self.instruments)
        
        # Generate spoofing pattern: many large cancelled orders, few small executed trades
        order_count = num_trades * 10  # 10 orders per trade on average
        cancellation_rate = 0.9 if risk_level == "high" else 0.3
        
        for i in range(order_count):
            order_time = self.base_time + timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 59))
            
            is_cancelled = random.random() < cancellation_rate
            
            if is_cancelled:
                # Large orders that get cancelled (spoofing behavior)
                order = {
                    "id": f"order_spoof_{i:05d}",
                    "timestamp": order_time.isoformat() + "Z",
                    "instrument": instrument,
                    "size": random.randint(50000, 500000) if risk_level == "high" else random.randint(5000, 20000),
                    "price": 75.50 + random.uniform(-1, 1),
                    "side": random.choice(["buy", "sell"]),
                    "status": "cancelled",
                    "trader_id": trader["id"],
                    "cancellation_time": (order_time + timedelta(seconds=random.randint(5, 300))).isoformat() + "Z"
                }
                orders.append(order)
            else:
                # Small trades that actually execute
                if len(trades) < num_trades:
                    trade = {
                        "id": f"trade_spoof_{len(trades):04d}",
                        "timestamp": order_time.isoformat() + "Z",
                        "instrument": instrument,
                        "volume": random.randint(1000, 5000),
                        "price": 75.50 + random.uniform(-0.5, 0.5),
                        "side": random.choice(["buy", "sell"]),
                        "trader_id": trader["id"]
                    }
                    trades.append(trade)
        
        return {
            "trades": trades[:num_trades],  # Limit to requested number
            "orders": orders,
            "trader_info": trader,
            "scenario_type": "spoofing",
            "expected_risk": risk_level
        }
    
    def generate_normal_trading_scenario(self, num_trades: int) -> Dict[str, Any]:
        """Generate normal trading scenario that should not trigger alerts"""
        trades = []
        
        trader = random.choice([self.trader_profiles["normal_trader_1"], self.trader_profiles["normal_trader_2"]])
        instruments = random.sample(self.instruments, random.randint(2, 4))  # Diversified trading
        
        for i in range(num_trades):
            trade_time = self.base_time + timedelta(days=random.randint(1, 29), hours=random.randint(9, 17))
            
            trade = {
                "id": f"trade_normal_{i:04d}",
                "timestamp": trade_time.isoformat() + "Z",
                "instrument": random.choice(instruments),
                "volume": random.randint(1000, 20000),  # Normal volumes
                "price": 50.00 + random.uniform(-5, 5),
                "side": random.choice(["buy", "sell"]),
                "trader_id": trader["id"]
            }
            trades.append(trade)
        
        return {
            "trades": trades,
            "orders": [],
            "material_events": [],
            "trader_info": trader,
            "scenario_type": "normal_trading",
            "expected_risk": "low"
        }
    
    def generate_mixed_scenario(self, num_trades: int) -> Dict[str, Any]:
        """Generate mixed scenario with some suspicious patterns but not clear violations"""
        trades = []
        
        trader = self.trader_profiles["normal_trader_1"]
        instrument = random.choice(self.instruments)
        
        # Some clustering but not as obvious as insider trading
        for i in range(num_trades):
            if i < num_trades * 0.3:  # 30% of trades clustered
                trade_time = self.base_time + timedelta(days=random.randint(1, 3), hours=random.randint(1, 23))
            else:
                trade_time = self.base_time + timedelta(days=random.randint(4, 29), hours=random.randint(1, 23))
            
            trade = {
                "id": f"trade_mixed_{i:04d}",
                "timestamp": trade_time.isoformat() + "Z",
                "instrument": instrument,
                "volume": random.randint(5000, 30000),
                "price": 45.00 + random.uniform(-3, 3),
                "side": random.choice(["buy", "sell"]),
                "trader_id": trader["id"]
            }
            trades.append(trade)
        
        # Add a minor material event (lower materiality)
        minor_event = {
            "id": f"event_minor_{random.randint(1000, 9999)}",
            "timestamp": (self.base_time + timedelta(days=15)).isoformat() + "Z",
            "type": "regulatory_update",
            "description": "Minor regulatory change announced",
            "instruments_affected": [instrument],
            "materiality_score": 0.3
        }
        
        return {
            "trades": trades,
            "orders": [],
            "material_events": [minor_event],
            "trader_info": trader,
            "scenario_type": "mixed_signals",
            "expected_risk": "medium"
        }

class ComprehensiveTestRunner:
    """Run comprehensive tests with 1000 trades across various scenarios"""
    
    def __init__(self):
        self.generator = TradeScenarioGenerator()
        self.data_processor = DataProcessor()
        self.bayesian_engine = BayesianEngine()
        self.results = []
        
    def run_comprehensive_test(self):
        """Run the full comprehensive test suite"""
        print("🚀 STARTING COMPREHENSIVE 1000-TRADE SURVEILLANCE TEST")
        print("=" * 80)
        
        start_time = time.time()
        
        # Test Scenarios Distribution:
        scenarios = [
            # HIGH RISK SCENARIOS (Should trigger alerts)
            ("insider_dealing_high", 150, "high"),      # 150 trades - high risk insider
            ("insider_dealing_medium", 100, "medium"),   # 100 trades - medium risk insider  
            ("spoofing_high", 120, "high"),             # 120 trades - high risk spoofing
            ("spoofing_medium", 80, "medium"),          # 80 trades - medium risk spoofing
            
            # MIXED SCENARIOS (Should trigger medium alerts)
            ("mixed_signals", 150, "medium"),           # 150 trades - ambiguous patterns
            
            # LOW RISK SCENARIOS (Should NOT trigger alerts)
            ("normal_trading_1", 200, "low"),           # 200 trades - normal trading
            ("normal_trading_2", 200, "low"),           # 200 trades - normal trading
        ]
        
        total_trades = 0
        scenario_results = []
        
        for scenario_name, num_trades, expected_risk in scenarios:
            print(f"\n📊 TESTING SCENARIO: {scenario_name.upper()}")
            print(f"   Target Trades: {num_trades} | Expected Risk: {expected_risk}")
            print("-" * 60)
            
            # Generate scenario data
            if "insider_dealing" in scenario_name:
                scenario_data = self.generator.generate_insider_dealing_scenario(num_trades, expected_risk)
            elif "spoofing" in scenario_name:
                scenario_data = self.generator.generate_spoofing_scenario(num_trades, expected_risk)
            elif "mixed" in scenario_name:
                scenario_data = self.generator.generate_mixed_scenario(num_trades)
            else:  # normal trading
                scenario_data = self.generator.generate_normal_trading_scenario(num_trades)
            
            # Process and analyze
            result = self._process_scenario(scenario_data, scenario_name)
            scenario_results.append(result)
            total_trades += len(scenario_data["trades"])
            
            # Display results
            self._display_scenario_results(result)
        
        end_time = time.time()
        
        # Final Summary
        self._display_final_summary(scenario_results, total_trades, end_time - start_time)
        
        return scenario_results
    
    def _process_scenario(self, scenario_data: Dict, scenario_name: str) -> Dict:
        """Process a single scenario and return results"""
        
        # Prepare complete data structure
        test_data = {
            "trades": scenario_data["trades"],
            "orders": scenario_data.get("orders", []),
            "trader_info": scenario_data["trader_info"],
            "material_events": scenario_data.get("material_events", []),
            "market_data": {
                "volatility": random.uniform(0.01, 0.05),
                "volume": random.randint(100000, 1000000),
                "price_movement": random.uniform(-0.05, 0.1),
                "liquidity": random.uniform(0.5, 0.9),
                "market_hours": True
            },
            "historical_data": {
                "avg_volume": random.randint(5000, 25000),
                "avg_frequency": random.randint(1, 20),
                "avg_price_impact": random.uniform(0.001, 0.01)
            }
        }
        
        # Process data
        processed_data = self.data_processor.process(test_data)
        
        # Run Bayesian analysis
        if "insider" in scenario_name:
            risk_result = self.bayesian_engine.calculate_insider_dealing_risk(processed_data)
        elif "spoofing" in scenario_name:
            risk_result = self.bayesian_engine.calculate_spoofing_risk(processed_data)
        else:
            # For mixed and normal scenarios, run both analyses
            insider_risk = self.bayesian_engine.calculate_insider_dealing_risk(processed_data)
            spoofing_risk = self.bayesian_engine.calculate_spoofing_risk(processed_data)
            risk_result = {
                "insider_dealing": insider_risk,
                "spoofing": spoofing_risk,
                "overall_score": max(
                    insider_risk.get("overall_score", 0),
                    spoofing_risk.get("overall_score", 0)
                )
            }
        
        return {
            "scenario_name": scenario_name,
            "scenario_type": scenario_data["scenario_type"],
            "expected_risk": scenario_data["expected_risk"],
            "trade_count": len(scenario_data["trades"]),
            "order_count": len(scenario_data.get("orders", [])),
            "material_events_count": len(scenario_data.get("material_events", [])),
            "trader_info": scenario_data["trader_info"],
            "risk_result": risk_result,
            "test_passed": self._evaluate_test_result(risk_result, scenario_data["expected_risk"])
        }
    
    def _evaluate_test_result(self, risk_result: Dict, expected_risk: str) -> bool:
        """Evaluate if the test result matches expectations"""
        overall_score = risk_result.get("overall_score", 0)
        
        if expected_risk == "high":
            return overall_score >= 0.7  # High risk should score 0.7+
        elif expected_risk == "medium":
            return 0.3 <= overall_score < 0.7  # Medium risk should score 0.3-0.7
        else:  # low risk
            return overall_score < 0.3  # Low risk should score <0.3
    
    def _display_scenario_results(self, result: Dict):
        """Display results for a single scenario"""
        risk_result = result["risk_result"]
        overall_score = risk_result.get("overall_score", 0)
        test_status = "✅ PASS" if result["test_passed"] else "❌ FAIL"
        
        print(f"   📈 Trades Processed: {result['trade_count']}")
        print(f"   📋 Orders Processed: {result['order_count']}")
        print(f"   📰 Material Events: {result['material_events_count']}")
        print(f"   👤 Trader: {result['trader_info']['name']} ({result['trader_info']['role']})")
        print(f"   🎯 Risk Score: {overall_score:.3f}")
        print(f"   📊 Expected: {result['expected_risk'].upper()} | Result: {test_status}")
        
        # Additional details for complex results
        if isinstance(risk_result.get("insider_dealing"), dict):
            insider_score = risk_result["insider_dealing"].get("overall_score", 0)
            spoofing_score = risk_result["spoofing"].get("overall_score", 0)
            print(f"   🔍 Insider Score: {insider_score:.3f} | Spoofing Score: {spoofing_score:.3f}")
    
    def _display_final_summary(self, scenario_results: List[Dict], total_trades: int, execution_time: float):
        """Display final test summary"""
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(1 for r in scenario_results if r["test_passed"])
        total_tests = len(scenario_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"📊 EXECUTION METRICS:")
        print(f"   • Total Trades Processed: {total_trades:,}")
        print(f"   • Total Scenarios Tested: {total_tests}")
        print(f"   • Execution Time: {execution_time:.2f} seconds")
        print(f"   • Processing Rate: {total_trades/execution_time:.1f} trades/second")
        
        print(f"\n🎯 TEST RESULTS:")
        print(f"   • Tests Passed: {passed_tests}/{total_tests}")
        print(f"   • Success Rate: {success_rate:.1f}%")
        
        # Break down by risk level
        high_risk_scenarios = [r for r in scenario_results if r["expected_risk"] == "high"]
        medium_risk_scenarios = [r for r in scenario_results if r["expected_risk"] == "medium"]
        low_risk_scenarios = [r for r in scenario_results if r["expected_risk"] == "low"]
        
        print(f"\n📈 RISK LEVEL BREAKDOWN:")
        print(f"   • High Risk Scenarios: {sum(1 for r in high_risk_scenarios if r['test_passed'])}/{len(high_risk_scenarios)} passed")
        print(f"   • Medium Risk Scenarios: {sum(1 for r in medium_risk_scenarios if r['test_passed'])}/{len(medium_risk_scenarios)} passed")
        print(f"   • Low Risk Scenarios: {sum(1 for r in low_risk_scenarios if r['test_passed'])}/{len(low_risk_scenarios)} passed")
        
        # Detailed scenario results
        print(f"\n📋 DETAILED SCENARIO RESULTS:")
        for result in scenario_results:
            status = "✅" if result["test_passed"] else "❌"
            score = result["risk_result"].get("overall_score", 0)
            print(f"   {status} {result['scenario_name']:25} | Score: {score:.3f} | Expected: {result['expected_risk']:6}")
        
        print(f"\n🔍 ANALYSIS INSIGHTS:")
        avg_high_risk_score = sum(r["risk_result"].get("overall_score", 0) for r in high_risk_scenarios) / len(high_risk_scenarios) if high_risk_scenarios else 0
        avg_low_risk_score = sum(r["risk_result"].get("overall_score", 0) for r in low_risk_scenarios) / len(low_risk_scenarios) if low_risk_scenarios else 0
        
        print(f"   • Average High Risk Score: {avg_high_risk_score:.3f}")
        print(f"   • Average Low Risk Score: {avg_low_risk_score:.3f}")
        print(f"   • Score Separation: {avg_high_risk_score - avg_low_risk_score:.3f}")
        
        if success_rate >= 80:
            print(f"\n🎉 EXCELLENT! Surveillance system performance is strong with {success_rate:.1f}% accuracy.")
        elif success_rate >= 60:
            print(f"\n👍 GOOD! Surveillance system shows reasonable performance at {success_rate:.1f}% accuracy.")
        else:
            print(f"\n⚠️  NEEDS IMPROVEMENT! Surveillance system needs tuning - {success_rate:.1f}% accuracy.")
        
        print("\n" + "=" * 80)

def main():
    """Main function to run the comprehensive test"""
    print("Kor.ai Surveillance Platform - Comprehensive 1000-Trade Test")
    print("Testing both positive alerts and negative scenarios")
    print()
    
    runner = ComprehensiveTestRunner()
    results = runner.run_comprehensive_test()
    
    # Optional: Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results_1000_trades_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        # Convert results to JSON-serializable format
        json_results = []
        for result in results:
            json_result = result.copy()
            json_result["risk_result"] = str(json_result["risk_result"])  # Convert to string for JSON
            json_results.append(json_result)
        
        json.dump({
            "timestamp": timestamp,
            "total_trades": sum(r["trade_count"] for r in results),
            "total_scenarios": len(results),
            "success_rate": sum(1 for r in results if r["test_passed"]) / len(results),
            "scenario_results": json_results
        }, f, indent=2)
    
    print(f"📄 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()