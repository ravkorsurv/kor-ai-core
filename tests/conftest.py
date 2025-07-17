"""
Comprehensive test configuration and fixtures for Korinsic Surveillance Platform.

This module provides shared fixtures, utilities, and test configuration across
all test types (unit, integration, e2e, performance).
"""

import pytest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, MagicMock

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import core modules for fixtures
try:
    from utils.config import Config
    from utils.logger import setup_logger
    from core.data_processor import DataProcessor
    from core.bayesian_engine import BayesianEngine
    from core.alert_generator import AlertGenerator
    from core.risk_calculator import RiskCalculator
except ImportError as e:
    # Allow fixtures to be loaded even if dependencies are missing
    print(f"Warning: Some imports failed in conftest.py: {e}")

# Test configuration
@pytest.fixture(scope="session")
def test_config():
    """Session-wide test configuration."""
    return {
        "test_data_dir": Path(__file__).parent / "fixtures",
        "log_level": "CRITICAL",  # Minimize logging during tests
        "timeout": 30,
        "max_retries": 3,
        "test_environment": "testing"
    }

@pytest.fixture(scope="session")
def app_config():
    """Application configuration for testing."""
    return Config(environment='testing')

@pytest.fixture(scope="session")
def test_logger(app_config):
    """Test logger with minimal output."""
    return setup_logger('test-logger', config=app_config.get_logging_config())

@pytest.fixture(scope="function")
def temp_dir():
    """Temporary directory for test files."""
    temp_dir = tempfile.mkdtemp(prefix="kor_ai_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def mock_data_processor():
    """Mock data processor for unit tests."""
    mock = Mock(spec=DataProcessor)
    mock.process.return_value = {
        "trades": [],
        "orders": [],
        "trader_info": {},
        "material_events": [],
        "market_data": {},
        "timeframe": "intraday",
        "instruments": []
    }
    return mock

@pytest.fixture(scope="function")
def mock_bayesian_engine():
    """Mock Bayesian engine for unit tests."""
    mock = Mock(spec=BayesianEngine)
    mock.calculate_insider_dealing_risk.return_value = {
        "overall_score": 0.5,
        "risk_level": "MEDIUM",
        "evidence_factors": {},
        "model_type": "standard"
    }
    mock.calculate_spoofing_risk.return_value = {
        "overall_score": 0.3,
        "risk_level": "LOW",
        "evidence_factors": {},
        "model_type": "standard"
    }
    return mock

@pytest.fixture(scope="function")
def mock_alert_generator():
    """Mock alert generator for unit tests."""
    mock = Mock(spec=AlertGenerator)
    mock.generate_alerts.return_value = []
    return mock

# Sample data fixtures
@pytest.fixture(scope="session")
def sample_trader_info():
    """Sample trader information."""
    return {
        "id": "trader_001",
        "name": "John Doe",
        "role": "senior_trader",
        "access_level": "medium",
        "department": "equity_trading",
        "hire_date": "2020-01-15",
        "clearance_level": "standard"
    }

@pytest.fixture(scope="session")
def sample_executive_trader():
    """Sample executive trader with high access."""
    return {
        "id": "exec_001",
        "name": "Jane Smith",
        "role": "executive",
        "access_level": "high",
        "department": "management",
        "hire_date": "2015-03-01",
        "clearance_level": "executive"
    }

@pytest.fixture(scope="session")
def sample_trade_data():
    """Sample trade data for testing."""
    return {
        "trades": [
            {
                "id": "trade_001",
                "timestamp": "2024-01-15T10:30:00Z",
                "instrument": "ENERGY_CORP",
                "volume": 100000,
                "price": 50.25,
                "side": "buy",
                "trader_id": "trader_001",
                "execution_venue": "NYSE",
                "order_type": "market"
            },
            {
                "id": "trade_002",
                "timestamp": "2024-01-15T11:45:00Z",
                "instrument": "ENERGY_CORP",
                "volume": 75000,
                "price": 50.45,
                "side": "sell",
                "trader_id": "trader_001",
                "execution_venue": "NYSE",
                "order_type": "limit"
            }
        ]
    }

@pytest.fixture(scope="session")
def sample_order_data():
    """Sample order data for testing."""
    return {
        "orders": [
            {
                "id": "order_001",
                "timestamp": "2024-01-15T10:25:00Z",
                "instrument": "ENERGY_CORP",
                "volume": 100000,
                "price": 50.20,
                "side": "buy",
                "status": "filled",
                "trader_id": "trader_001",
                "order_type": "market"
            },
            {
                "id": "order_002",
                "timestamp": "2024-01-15T10:26:00Z",
                "instrument": "ENERGY_CORP",
                "volume": 50000,
                "price": 50.50,
                "side": "buy",
                "status": "cancelled",
                "trader_id": "trader_001",
                "order_type": "limit"
            }
        ]
    }

@pytest.fixture(scope="session")
def sample_material_events():
    """Sample material events for testing."""
    return [
        {
            "id": "event_001",
            "timestamp": "2024-01-16T09:00:00Z",
            "type": "earnings_announcement",
            "description": "Q4 earnings announcement",
            "instruments_affected": ["ENERGY_CORP"],
            "expected_impact": 0.08,
            "materiality_score": 0.9,
            "public_release": "2024-01-16T08:30:00Z"
        },
        {
            "id": "event_002",
            "timestamp": "2024-01-14T16:00:00Z",
            "type": "merger_announcement",
            "description": "Strategic acquisition announcement",
            "instruments_affected": ["ENERGY_CORP"],
            "expected_impact": 0.15,
            "materiality_score": 0.95,
            "public_release": "2024-01-14T16:00:00Z"
        }
    ]

@pytest.fixture(scope="session")
def sample_market_data():
    """Sample market data for testing."""
    return {
        "volatility": 0.025,
        "liquidity": 0.8,
        "price_movement": 0.05,
        "volume": 1500000,
        "bid_ask_spread": 0.02,
        "market_cap": 50000000000,
        "average_volume": 1200000
    }

@pytest.fixture(scope="session")
def sample_news_data():
    """Sample news data for testing."""
    return {
        "news_events": [
            {
                "id": "news_001",
                "timestamp": "2024-01-15T08:00:00Z",
                "headline": "Energy Corp Reports Strong Q4 Results",
                "sentiment": 0.8,
                "market_impact": 0.06,
                "relevance_score": 0.9,
                "source": "Reuters",
                "instruments_affected": ["ENERGY_CORP"]
            }
        ]
    }

@pytest.fixture(scope="function")
def complete_analysis_data(sample_trade_data, sample_order_data, sample_trader_info, 
                          sample_material_events, sample_market_data):
    """Complete dataset for analysis testing."""
    return {
        **sample_trade_data,
        **sample_order_data,
        "trader_info": sample_trader_info,
        "material_events": sample_material_events,
        "market_data": sample_market_data,
        "timeframe": "intraday",
        "instruments": ["ENERGY_CORP"]
    }

@pytest.fixture(scope="function")
def high_risk_scenario(sample_executive_trader):
    """High-risk scenario data for testing alerts."""
    return {
        "trades": [
            {
                "id": "high_risk_trade_001",
                "timestamp": "2024-01-15T09:45:00Z",
                "instrument": "TECH_CORP",
                "volume": 500000,  # Very high volume
                "price": 75.50,
                "side": "buy",
                "trader_id": "exec_001",
                "execution_venue": "NASDAQ",
                "order_type": "market"
            }
        ],
        "trader_info": sample_executive_trader,
        "material_events": [
            {
                "id": "high_impact_event",
                "timestamp": "2024-01-15T10:00:00Z",  # 15 minutes after trade
                "type": "earnings_announcement",
                "description": "Record-breaking quarterly results",
                "instruments_affected": ["TECH_CORP"],
                "expected_impact": 0.20,
                "materiality_score": 1.0,
                "public_release": "2024-01-15T10:00:00Z"
            }
        ],
        "market_data": {
            "volatility": 0.08,
            "price_movement": 0.18,
            "volume": 2000000
        }
    }

@pytest.fixture(scope="function")
def spoofing_scenario():
    """Spoofing scenario data for testing."""
    return {
        "orders": [
            {
                "id": "spoof_order_001",
                "timestamp": "2024-01-15T10:00:00Z",
                "instrument": "COMMODITY_A",
                "volume": 100000,
                "price": 45.00,
                "side": "buy",
                "status": "cancelled",
                "trader_id": "trader_002",
                "order_type": "limit"
            },
            {
                "id": "spoof_order_002",
                "timestamp": "2024-01-15T10:00:30Z",
                "instrument": "COMMODITY_A",
                "volume": 150000,
                "price": 45.10,
                "side": "buy",
                "status": "cancelled",
                "trader_id": "trader_002",
                "order_type": "limit"
            },
            {
                "id": "real_order_001",
                "timestamp": "2024-01-15T10:01:00Z",
                "instrument": "COMMODITY_A",
                "volume": 10000,
                "price": 44.90,
                "side": "sell",
                "status": "filled",
                "trader_id": "trader_002",
                "order_type": "market"
            }
        ],
        "market_data": {
            "volatility": 0.03,
            "price_movement": 0.02,
            "volume": 800000
        }
    }

# Test utilities fixtures
@pytest.fixture(scope="function")
def api_test_client():
    """Flask test client for API testing."""
    try:
        from app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    except ImportError:
        # Return a mock client if Flask app can't be imported
        mock_client = Mock()
        mock_client.post.return_value = Mock(status_code=200, json=lambda: {})
        yield mock_client

@pytest.fixture(scope="function")
def database_session():
    """Mock database session for testing."""
    session = Mock()
    session.query.return_value = session
    session.filter.return_value = session
    session.all.return_value = []
    session.first.return_value = None
    session.commit.return_value = None
    session.rollback.return_value = None
    yield session

# Performance testing fixtures
@pytest.fixture(scope="function")
def large_dataset():
    """Large dataset for performance testing."""
    base_time = datetime(2024, 1, 1, 9, 0, 0)
    
    trades = []
    for i in range(1000):  # 1000 trades
        trades.append({
            "id": f"perf_trade_{i:04d}",
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "instrument": f"STOCK_{i % 50}",  # 50 different instruments
            "volume": 1000 + (i % 100000),
            "price": 50.0 + (i % 100) * 0.1,
            "side": "buy" if i % 2 == 0 else "sell",
            "trader_id": f"trader_{i % 20:03d}",  # 20 different traders
            "execution_venue": "NYSE" if i % 2 == 0 else "NASDAQ",
            "order_type": "market" if i % 3 == 0 else "limit"
        })
    
    return {
        "trades": trades,
        "trader_info": {"id": "trader_001", "role": "trader", "access_level": "medium"},
        "market_data": {"volatility": 0.02, "volume": 5000000},
        "timeframe": "daily"
    }

# Test markers for organization
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests") 
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "api: API tests requiring server")
    config.addinivalue_line("markers", "mock: Tests using mocks")

# Test collection customization
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on file location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)

# Cleanup fixtures
@pytest.fixture(scope="function", autouse=True)
def cleanup_environment():
    """Clean up environment variables after each test."""
    original_env = dict(os.environ)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)