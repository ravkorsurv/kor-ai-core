# Enhanced Test Infrastructure - Phase 3

This document describes the comprehensive test infrastructure improvements implemented in Phase 3 of the codebase structure enhancements.

## Overview

The enhanced test infrastructure provides a robust, scalable foundation for testing the Korinsic Surveillance Platform with:

- **Comprehensive fixtures** for all test scenarios
- **Mock factories** for consistent test data generation
- **Custom assertions** for domain-specific validation
- **Test utilities** for common operations
- **Organized test structure** with clear categorization
- **Configuration integration** with environment-specific settings
- **Performance testing** capabilities
- **Automated test runners** with multiple execution modes

## Directory Structure

```
tests/
├── conftest.py                    # Comprehensive fixtures and test configuration
├── utils/                         # Test utilities and helpers
│   ├── __init__.py               # Utility exports
│   ├── test_helpers.py           # Common test operations
│   ├── mock_factories.py         # Mock object factories
│   ├── data_generators.py        # Realistic test data generators
│   └── assertions.py             # Custom assertion functions
├── fixtures/                      # Static test data files
│   └── sample_data.json          # Sample test scenarios
├── unit/                          # Unit tests
├── integration/                   # Integration tests
├── e2e/                          # End-to-end tests
├── performance/                   # Performance tests
└── README.md                     # This documentation
```

## Key Features

### 1. Comprehensive Fixtures (conftest.py)

**Session-level fixtures** for shared test configuration:
- `test_config`: Global test settings
- `app_config`: Application configuration for testing
- `test_logger`: Minimal logging for tests

**Data fixtures** for consistent test scenarios:
- `sample_trade_data`: Basic trade data
- `sample_trader_info`: Trader information
- `sample_material_events`: Material events
- `sample_market_data`: Market data
- `complete_analysis_data`: Full analysis dataset

**Scenario fixtures** for specific test cases:
- `high_risk_scenario`: High-risk insider dealing scenario
- `spoofing_scenario`: Spoofing detection scenario
- `large_dataset`: Performance testing dataset

**Mock fixtures** for isolated testing:
- `mock_data_processor`: Mock data processor
- `mock_bayesian_engine`: Mock Bayesian engine
- `mock_alert_generator`: Mock alert generator

### 2. Test Utilities (tests/utils/)

**Test Helpers** (`test_helpers.py`):
- `create_test_scenario()`: Generate standardized test scenarios
- `validate_api_response()`: Validate API response structure
- `compare_risk_scores()`: Compare risk scores with tolerance
- `assert_alert_generated()`: Assert alert generation
- `wait_for_condition()`: Wait for asynchronous conditions

**Mock Factories** (`mock_factories.py`):
- `MockDataFactory`: Generate mock data objects
- `MockEngineFactory`: Generate mock engine components
- `MockResponseFactory`: Generate mock API responses
- `MockDatabaseFactory`: Generate mock database objects

**Data Generators** (`data_generators.py`):
- `generate_trade_data()`: Realistic trade data
- `generate_order_data()`: Realistic order data
- `generate_material_events()`: Realistic material events
- `generate_market_data()`: Realistic market data
- `generate_news_data()`: Realistic news data

**Custom Assertions** (`assertions.py`):
- `assert_risk_score_valid()`: Validate risk score structure
- `assert_alert_fields_present()`: Validate alert fields
- `assert_regulatory_rationale_complete()`: Validate regulatory rationale
- `assert_performance_metrics()`: Validate performance metrics

### 3. Test Organization and Markers

Tests are organized with pytest markers for flexible execution:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.e2e`: End-to-end tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.slow`: Slow running tests
- `@pytest.mark.api`: API tests requiring server
- `@pytest.mark.mock`: Tests using mocks

### 4. Configuration Integration

Tests integrate with the enhanced configuration system from Phase 2:
- Environment-specific test configuration
- Test-optimized settings (minimal logging, fast execution)
- Automatic environment detection
- Configuration fixture for easy access

## Usage Examples

### Basic Test with Fixtures

```python
import pytest
from tests.utils import assert_risk_score_valid

@pytest.mark.unit
def test_risk_calculation(sample_trade_data, sample_trader_info):
    """Test risk calculation with fixtures."""
    # Use fixtures directly
    assert len(sample_trade_data["trades"]) > 0
    assert sample_trader_info["id"] is not None
    
    # Test business logic here
    # ...
```

### Test with Mock Factories

```python
from tests.utils import MockDataFactory, MockEngineFactory

@pytest.mark.unit
def test_with_mocks():
    """Test using mock factories."""
    # Generate mock data
    mock_trade = MockDataFactory.create_mock_trade(
        volume=100000,
        price=50.0
    )
    
    # Generate mock engine
    mock_engine = MockEngineFactory.create_mock_bayesian_engine()
    result = mock_engine.calculate_insider_dealing_risk(mock_trade)
    
    # Validate result
    assert_risk_score_valid(result)
```

### Test with Scenario Creation

```python
from tests.utils import create_test_scenario

@pytest.mark.unit
def test_insider_dealing_scenario():
    """Test insider dealing scenario."""
    # Create scenario
    scenario = create_test_scenario(
        "insider_dealing",
        instrument="TEST_STOCK",
        volume=500000,
        trader_id="exec_001"
    )
    
    # Test scenario
    assert scenario["trader_info"]["role"] == "executive"
    assert scenario["trader_info"]["access_level"] == "high"
```

### Integration Test with Configuration

```python
@pytest.mark.integration
def test_with_configuration(app_config):
    """Test with application configuration."""
    assert app_config.environment == "testing"
    
    # Use configuration
    risk_thresholds = app_config.get_risk_thresholds()
    assert "insider_dealing" in risk_thresholds
```

## Running Tests

### Test Runner Script

Use the comprehensive test runner:

```bash
# Run all tests
python scripts/development/run_tests.py

# Run specific test types
python scripts/development/run_tests.py --unit
python scripts/development/run_tests.py --integration
python scripts/development/run_tests.py --e2e
python scripts/development/run_tests.py --performance

# Run with coverage
python scripts/development/run_tests.py --coverage

# Quick test for fast feedback
python scripts/development/run_tests.py --quick

# Check dependencies
python scripts/development/run_tests.py --check-deps
```

### Direct pytest Commands

```bash
# Run all tests
pytest

# Run unit tests only
pytest -m unit

# Run integration tests
pytest -m integration

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_example_enhanced.py

# Run with verbose output
pytest -v

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

### Test Filtering

```bash
# Run only mock tests
pytest -m mock

# Run only slow tests
pytest -m slow

# Run API tests
pytest -m api

# Exclude slow tests
pytest -m "not slow"

# Run unit and integration tests
pytest -m "unit or integration"
```

## Test Data Management

### Static Test Data

Static test data is stored in `tests/fixtures/sample_data.json`:
- **Scenarios**: Predefined test scenarios for different abuse types
- **Expected Responses**: Expected risk calculation results
- **Trader Profiles**: Sample trader information
- **Market Conditions**: Different market scenarios

### Dynamic Test Data

Dynamic test data is generated using data generators:
- **Realistic Data**: Generated with proper relationships and constraints
- **Configurable**: Customizable parameters for different test needs
- **Diverse**: Multiple instruments, traders, and market conditions
- **Temporal**: Proper timestamp sequences and relationships

## Performance Testing

### Large Dataset Testing

```python
@pytest.mark.performance
def test_large_dataset_performance(large_dataset):
    """Test performance with large datasets."""
    assert len(large_dataset["trades"]) >= 1000
    
    # Measure performance
    start_time = time.time()
    result = process_large_dataset(large_dataset)
    duration = time.time() - start_time
    
    # Assert performance requirements
    assert duration < 5.0  # Max 5 seconds
    assert_performance_metrics({"response_time": duration})
```

### Memory and Resource Testing

```python
@pytest.mark.performance
def test_memory_usage():
    """Test memory usage constraints."""
    initial_memory = get_memory_usage()
    
    # Run memory-intensive operation
    result = process_intensive_operation()
    
    final_memory = get_memory_usage()
    memory_delta = final_memory - initial_memory
    
    # Assert memory constraints
    assert memory_delta < 100  # Max 100MB increase
```

## Best Practices

### 1. Test Organization

- **Use markers** for test categorization
- **Group related tests** in test classes
- **Use descriptive test names** that explain what is being tested
- **Write docstrings** for complex test methods

### 2. Fixture Usage

- **Use appropriate fixture scopes** (session, function, class)
- **Prefer fixtures over setup/teardown** methods
- **Create specialized fixtures** for specific test scenarios
- **Use fixture parametrization** for testing multiple scenarios

### 3. Mock Usage

- **Use mocks for external dependencies** (databases, APIs, file systems)
- **Mock at the right level** (don't mock too much or too little)
- **Use mock factories** for consistent mock objects
- **Validate mock interactions** when necessary

### 4. Assertions

- **Use custom assertions** for domain-specific validation
- **Provide descriptive error messages** in assertions
- **Assert on multiple aspects** of the result
- **Use appropriate assertion methods** (assertEqual, assertIn, etc.)

### 5. Test Data

- **Use realistic test data** that represents actual scenarios
- **Avoid hardcoded values** in tests
- **Use data generators** for varied test inputs
- **Keep test data focused** on what's being tested

## Debugging Tests

### Running Individual Tests

```bash
# Run single test method
pytest tests/unit/test_example_enhanced.py::TestEnhancedTestInfrastructure::test_basic_fixture_usage

# Run single test class
pytest tests/unit/test_example_enhanced.py::TestEnhancedTestInfrastructure

# Run with debugger
pytest --pdb tests/unit/test_example_enhanced.py

# Run with traceback
pytest --tb=long tests/unit/test_example_enhanced.py
```

### Test Output and Logging

```bash
# Show print statements
pytest -s

# Show warnings
pytest --disable-warnings

# Show test durations
pytest --durations=10

# Generate JUnit XML report
pytest --junitxml=reports/junit.xml
```

## Integration with CI/CD

The test infrastructure is designed to integrate with CI/CD pipelines:

- **Multiple test execution modes** for different pipeline stages
- **Comprehensive reporting** with JUnit XML and coverage reports
- **Dependency checking** for environment validation
- **Performance benchmarking** for regression detection
- **Parallel execution** support for faster feedback

## Migration from Existing Tests

When migrating existing tests to the enhanced infrastructure:

1. **Update imports** to use test utilities and fixtures
2. **Replace hardcoded data** with fixtures and generators
3. **Add appropriate markers** for test categorization
4. **Use custom assertions** for better validation
5. **Refactor test setup** to use fixtures instead of setup methods

## Conclusion

The enhanced test infrastructure provides a comprehensive foundation for testing the Korinsic Surveillance Platform. It offers:

- **Consistency** through standardized fixtures and utilities
- **Maintainability** through organized structure and clear patterns
- **Scalability** through performance testing capabilities
- **Reliability** through comprehensive validation and assertions
- **Flexibility** through configurable test execution

This infrastructure supports both current testing needs and future expansion as the platform grows.