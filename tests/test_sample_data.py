import json
import sys
import os
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.data_processor import DataProcessor
from core.bayesian_engine import BayesianEngine

def generate_sample_insider_data():
    """Generate sample data for insider dealing scenario"""
    base_time = datetime.utcnow() - timedelta(days=7)
    
    return {
        "trades": [
            {
                "id": "trade_001",
                "timestamp": (base_time + timedelta(days=1)).isoformat() + "Z",
                "instrument": "ENERGY_STOCK_A",
                "volume": 50000,
                "price": 45.50,
                "side": "buy",
                "trader_id": "trader_insider_001"
            },
            {
                "id": "trade_002", 
                "timestamp": (base_time + timedelta(days=2)).isoformat() + "Z",
                "instrument": "ENERGY_STOCK_A",
                "volume": 75000,
                "price": 46.20,
                "side": "buy", 
                "trader_id": "trader_insider_001"
            },
            {
                "id": "trade_003",
                "timestamp": (base_time + timedelta(days=3)).isoformat() + "Z",
                "instrument": "ENERGY_STOCK_A",
                "volume": 100000,
                "price": 47.10,
                "side": "buy",
                "trader_id": "trader_insider_001"
            }
        ],
        "orders": [],
        "trader_info": {
            "id": "trader_insider_001",
            "name": "John Executive",
            "role": "senior_trader",
            "department": "energy_trading",
            "access_level": "high",
            "start_date": "2020-01-01"
        },
        "market_data": {
            "volatility": 0.025,
            "volume": 1000000,
            "price_movement": 0.08,
            "liquidity": 0.7,
            "market_hours": True
        },
        "material_events": [
            {
                "id": "event_001",
                "timestamp": (base_time + timedelta(days=5)).isoformat() + "Z",
                "type": "earnings_announcement",
                "description": "Quarterly earnings beat expectations by 15%",
                "instruments_affected": ["ENERGY_STOCK_A"],
                "materiality_score": 0.9
            }
        ],
        "historical_data": {
            "avg_volume": 20000,
            "avg_frequency": 5,
            "avg_price_impact": 0.005
        }
    }

def generate_sample_spoofing_data():
    """Generate sample data for spoofing scenario"""
    base_time = datetime.utcnow() - timedelta(hours=2)
    
    orders = []
    trades = []
    
    # Generate pattern of large orders that get cancelled and small trades that execute
    for i in range(50):
        order_time = base_time + timedelta(minutes=i*2)
        
        if i % 10 == 0:  # Every 10th order becomes a trade
            order = {
                "id": f"order_{i:03d}",
                "timestamp": order_time.isoformat() + "Z",
                "instrument": "CRUDE_OIL_FUTURE",
                "size": 1000,
                "price": 75.50 + (i * 0.01),
                "side": "buy",
                "status": "filled",
                "trader_id": "trader_spoofer_001"
            }
            
            trade = {
                "id": f"trade_{i//10:03d}",
                "timestamp": order_time.isoformat() + "Z",
                "instrument": "CRUDE_OIL_FUTURE",
                "volume": 1000,
                "price": 75.50 + (i * 0.01),
                "side": "buy",
                "trader_id": "trader_spoofer_001"
            }
            trades.append(trade)
        else:
            # Large orders that get cancelled
            order = {
                "id": f"order_{i:03d}",
                "timestamp": order_time.isoformat() + "Z",
                "instrument": "CRUDE_OIL_FUTURE",
                "size": 10000,  # Much larger
                "price": 75.50 + (i * 0.01),
                "side": "sell",
                "status": "cancelled",
                "trader_id": "trader_spoofer_001",
                "cancellation_time": (order_time + timedelta(seconds=30)).isoformat() + "Z"
            }
        
        orders.append(order)
    
    return {
        "trades": trades,
        "orders": orders,
        "trader_info": {
            "id": "trader_spoofer_001",
            "name": "Mike Spoofer",
            "role": "trader",
            "department": "commodities",
            "access_level": "standard",
            "start_date": "2019-06-01"
        },
        "market_data": {
            "volatility": 0.018,
            "volume": 500000,
            "price_movement": 0.025,
            "liquidity": 0.6,
            "market_hours": True
        },
        "material_events": [],
        "historical_data": {
            "avg_volume": 5000,
            "avg_frequency": 20,
            "avg_price_impact": 0.002
        }
    }

def test_sample_data():
    """Test the surveillance system with sample data"""
    print("Testing Korinsic Surveillance Platform with Sample Data")
    print("=" * 60)
    
    # Initialize components
    data_processor = DataProcessor()
    bayesian_engine = BayesianEngine()
    
    # Test insider dealing scenario
    print("\n1. Testing Insider Dealing Scenario:")
    print("-" * 40)
    
    insider_data = generate_sample_insider_data()
    processed_insider = data_processor.process(insider_data)
    insider_risk = bayesian_engine.calculate_insider_dealing_risk(processed_insider)
    
    print(f"Processed {len(processed_insider['trades'])} trades")
    print(f"Insider Dealing Risk Score: {insider_risk.get('overall_score', 0):.3f}")
    print(f"Risk Level: {insider_risk.get('high_risk', 0):.3f} (High)")
    
    # Test spoofing scenario
    print("\n2. Testing Spoofing Scenario:")
    print("-" * 40)
    
    spoofing_data = generate_sample_spoofing_data()
    processed_spoofing = data_processor.process(spoofing_data)
    spoofing_risk = bayesian_engine.calculate_spoofing_risk(processed_spoofing)
    
    print(f"Processed {len(processed_spoofing['orders'])} orders")
    print(f"Spoofing Risk Score: {spoofing_risk.get('overall_score', 0):.3f}")
    print(f"Risk Level: {spoofing_risk.get('high_risk', 0):.3f} (High)")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_sample_data()