# Korinsic – AI-Powered Surveillance Platform

Korinsic is a professional-grade AI surveillance platform designed to detect market abuse risks including insider dealing and spoofing. This repository contains the core analytical engine, Bayesian inference system, and service orchestration components.

---

## 📁 Repository Structure

The codebase follows enterprise-grade architecture with clear separation of concerns:

```
kor-ai-core/
├── src/                          # Core application source code
│   ├── app.py                   # Main Flask application entry point
│   ├── api/                     # API layer with versioning
│   │   └── v1/                  # API version 1
│   │       ├── routes/          # REST endpoints by domain
│   │       ├── middleware/      # Request/response middleware
│   │       └── schemas/         # Input/output validation schemas
│   ├── core/                    # Core business logic
│   │   ├── engines/            # Bayesian inference engines
│   │   ├── processors/         # Data processing pipeline
│   │   └── services/           # Business service coordination
│   ├── models/                  # Data models and ML components
│   │   ├── bayesian/           # Bayesian inference models
│   │   ├── data/               # Data structure definitions
│   │   └── shared/             # Shared model utilities
│   └── utils/                  # Common utilities and helpers
├── tests/                       # Comprehensive test suite
│   ├── unit/                   # Unit tests with mocking
│   ├── integration/            # Component integration tests
│   ├── e2e/                    # End-to-end workflow tests
│   ├── performance/            # Load and performance tests
│   ├── fixtures/               # Test data and scenarios
│   └── utils/                  # Test utilities and helpers
├── config/                     # Configuration management
│   ├── *.json                  # Environment-specific configs
│   ├── models/                 # Model configuration files
│   └── deployment/             # Deployment configurations
├── docs/                       # Documentation
│   ├── development/            # Development guides
│   └── models/                 # Model documentation
├── scripts/                    # Automation scripts
│   ├── development/            # Development utilities
│   ├── deployment/             # Deployment automation
│   ├── data/                   # Data management scripts
│   └── maintenance/            # System maintenance
├── deployment/                 # Container and cloud configs
├── archive/                    # Archived/legacy components
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── .gitignore                  # Git ignore patterns
└── pytest.ini                 # Test configuration
```

---

## 🧭 Navigating the Codebase

### Understanding the Architecture

**🚀 Application Entry Point**
- **`src/app.py`** - Flask application initialization, CORS setup, route registration

**🌐 API Layer** (`src/api/v1/`)
- **`routes/`** - RESTful endpoints organized by business domain
- **`middleware/`** - Request validation, error handling, authentication
- **`schemas/`** - Request/response validation using marshmallow

**⚙️ Core Business Logic** (`src/core/`)
- **`engines/`** - Bayesian inference engine, risk calculation algorithms
- **`processors/`** - Data transformation and evidence mapping
- **`services/`** - High-level business logic coordination

**🧠 Models** (`src/models/`)
- **`bayesian/`** - Probabilistic models for risk detection
- **`data/`** - Data structure definitions and validators
- **`shared/`** - Common components and utilities

### Key Navigation Points

1. **Start Here:** `src/app.py` - Main application entry
2. **API Contracts:** `src/api/v1/routes/analysis.py` - Primary endpoints
3. **Core Engine:** `src/core/engines/bayesian_engine.py` - Inference logic
4. **Model Implementation:** `src/models/bayesian/insider_dealing/model.py`
5. **Configuration:** `config/base.json` - System settings
6. **Test Setup:** `tests/conftest.py` - Test configuration

### Development Workflow

```bash
# 1. Environment Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 2. Configuration
cp .env.example .env
# Edit .env with your settings

# 3. Pre-commit Setup (MANDATORY)
pre-commit install

# 4. Development Server
python scripts/development/run_server.py

# 5. Testing (MANDATORY before PR)
python scripts/development/run_tests.py --fast

# 6. Quality Checks (MANDATORY before PR)
python scripts/development/run_quality_checks.py

# 7. API Testing
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d @tests/fixtures/sample_request.json
```

### 🚨 MANDATORY: Feature Development Process

**Before starting any new feature or enhancement, you MUST follow the Feature Development Checklist:**

1. **Read the checklist:** `FEATURE_DEVELOPMENT_CHECKLIST.md`
2. **Follow the process:** Complete all pre-development requirements
3. **Use the PR template:** Follow `.github/PULL_REQUEST_TEMPLATE.md`
4. **Run all checks:** Use automation scripts provided

**Key Requirements:**
- ✅ 80% minimum test coverage
- ✅ All quality checks must pass
- ✅ Security scans must pass
- ✅ Documentation must be updated
- ✅ Regulatory compliance addressed
- ✅ API documentation updated

---

## 🐳 Containerization & Deployment

### Docker Configuration

**Dockerfile** optimized for production deployment:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "src/app.py"]
```

### Container Operations

```bash
# Build container
docker build -t kor-ai-core .

# Development mode
docker run -p 5000:5000 \
  -e ENVIRONMENT=development \
  -e DEBUG=true \
  kor-ai-core

# Production mode
docker run -p 5000:5000 \
  -e ENVIRONMENT=production \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  kor-ai-core
```

### Environment Configuration

**Required Environment Variables:**
- `ENVIRONMENT` - deployment environment (development/production/testing)
- `PORT` - server port (default: 5000)
- `HOST` - server host (default: 0.0.0.0)

**Optional Environment Variables:**
- `DATABASE_URL` - database connection string
- `REDIS_URL` - Redis connection string
- `LOG_LEVEL` - logging verbosity (DEBUG/INFO/WARNING/ERROR)
- `DEBUG` - enable debug mode (development only)
- `INSIDER_HIGH_THRESHOLD` - risk threshold for insider dealing
- `SPOOFING_HIGH_THRESHOLD` - risk threshold for spoofing

### Docker Compose for Local Development

```yaml
version: '3.8'
services:
  kor-ai-core:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    depends_on:
      - redis
      - postgres
    volumes:
      - .:/app
      - /app/venv
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=korai
      - POSTGRES_USER=korai
      - POSTGRES_PASSWORD=korai
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Production Deployment

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kor-ai-core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kor-ai-core
  template:
    metadata:
      labels:
        app: kor-ai-core
    spec:
      containers:
      - name: kor-ai-core
        image: kor-ai-core:latest
        ports:
        - containerPort: 5000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: kor-ai-secrets
              key: database-url
```

---

## 🌿 Branch Strategy & Git Workflow

### Branch Structure

**Primary Branches:**
- `main` - Production-ready code, protected branch
- `develop` - Integration branch (if using GitFlow)

**Working Branches:**
- `feature/[description]` - New features and enhancements
- `bugfix/[description]` - Bug fixes and patches
- `hotfix/[description]` - Critical production fixes
- `refactor/[description]` - Code refactoring
- `docs/[description]` - Documentation updates
- `test/[description]` - Test improvements

### Development Workflow

**Feature Development:**
```bash
git checkout main
git pull origin main
git checkout -b feature/new-spoofing-detection
# ... implement feature ...
git add .
git commit -m "feat: Add spoofing pattern detection"
git push origin feature/new-spoofing-detection
# Create Pull Request
```

**Bug Fixes:**
```bash
git checkout -b bugfix/fix-bayesian-inference
# ... fix issue ...
git commit -m "fix: Correct probability calculation in Bayesian engine"
git push origin bugfix/fix-bayesian-inference
# Create Pull Request
```

**Hotfixes:**
```bash
git checkout main
git checkout -b hotfix/critical-security-patch
# ... apply fix ...
git commit -m "hotfix: Patch security vulnerability in auth"
git push origin hotfix/critical-security-patch
# Create urgent Pull Request
```

### Pull Request Process

1. **Create descriptive PR** with clear title and description
2. **Automated checks** - CI/CD pipeline runs tests
3. **Code review** - Team member review required
4. **Documentation** - Update docs if API/behavior changes
5. **Merge strategy** - Squash commits for clean history

### Current Branch Status

**Active Branches:**
- `main` - ✅ Keep (production baseline)
- `cursor/update-readme-and-clean-up-branches-9f08` - 🔄 Current work

**Branches for Cleanup:**
- `cursor/write-complete-code-f9b6` - ❌ Delete (work merged)
- `init/github-pr-bot-service` - 📦 Archive (historical reference)

---

## 🚀 Quick Start Guide

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-org/kor-ai-core.git
cd kor-ai-core

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

### 3. Run Application

```bash
# Using development script (recommended)
python scripts/development/run_server.py

# Or run directly
python src/app.py

# Or using Docker
docker build -t kor-ai-core .
docker run -p 5000:5000 kor-ai-core
```

### 4. Verify Installation

```bash
# Health check
curl http://localhost:5000/health

# Run tests
python scripts/development/run_tests.py
```

---

## 📖 API Reference

### Core Endpoints

**Health Check**
```http
GET /health
```

**Risk Analysis**
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "trades": [...],
  "orders": [...],
  "trader_info": {...},
  "material_events": [...],
  "market_data": {...}
}
```

**Batch Processing**
```http
POST /api/v1/analyze/batch
Content-Type: application/json

{
  "datasets": [
    {
      "id": "dataset_1",
      "trades": [...],
      "orders": [...],
      ...
    }
  ]
}
```

**Real-time Analysis**
```http
POST /api/v1/analyze/realtime
Content-Type: application/json

{
  "stream_data": {...},
  "analysis_config": {...}
}
```

### Response Format

```json
{
  "status": "success",
  "data": {
    "analysis_id": "uuid",
    "risk_scores": {
      "insider_dealing": {
        "overall_score": 0.73,
        "confidence": "High",
        "contributing_factors": [...]
      }
    },
    "evidence_sufficiency_index": 0.84,
    "alerts": [...]
  }
}
```

---

## ⚙️ Configuration System

### Configuration Files

```
config/
├── base.json              # Base configuration
├── development.json       # Development overrides
├── production.json        # Production overrides
├── testing.json          # Test configuration
├── models/                # Model configurations
│   └── bayesian_models.json
└── deployment/            # Deployment settings
```

### Environment Variables

Configuration can be overridden via environment variables:

```bash
# Core settings
ENVIRONMENT=production
DEBUG=false
PORT=5000
HOST=0.0.0.0

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# Model thresholds
INSIDER_HIGH_THRESHOLD=0.7
SPOOFING_HIGH_THRESHOLD=0.8
```

### Configuration Usage

```python
from src.utils.config import ConfigManager

config = ConfigManager()
db_host = config.get('database.host')
threshold = config.get('models.insider_dealing.high_threshold')
```

---

## � Testing Framework

### Test Structure

```
tests/
├── unit/                   # Fast, isolated tests
├── integration/            # Component interaction tests
├── e2e/                    # Full workflow tests
├── performance/            # Load and stress tests
├── fixtures/               # Test data and scenarios
└── utils/                  # Test utilities
```

### Running Tests

```bash
# All tests
python scripts/development/run_tests.py

# Specific test types
python scripts/development/run_tests.py --mode unit
python scripts/development/run_tests.py --mode integration
python scripts/development/run_tests.py --mode e2e

# With coverage
python scripts/development/run_tests.py --mode coverage

# Performance tests
python scripts/development/run_tests.py --mode performance
```

### Test Fixtures

Located in `tests/fixtures/`:
- `sample_request.json` - Example API request
- `trader_profiles.json` - Test trader data
- `market_events.json` - Sample market events
- `expected_responses.json` - Expected analysis outputs

---

## 🔧 Development Tools

### Code Quality

```bash
# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/

# Dependency checking
safety check
```

### Development Scripts

```bash
# Start development server
python scripts/development/run_server.py

# Run test suite
python scripts/development/run_tests.py

# Generate test data
python scripts/development/generate_test_data.py

# Database migrations
python scripts/development/migrate_db.py
```

---

## 📊 Monitoring & Observability

### Logging

The application uses structured logging with JSON format in production:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Analysis completed", extra={
    "analysis_id": "123",
    "risk_score": 0.85,
    "duration_ms": 250
})
```

### Metrics

Key metrics to monitor:
- Request latency and throughput
- Analysis success/failure rates
- Risk score distributions
- Model performance metrics

### Health Checks

```bash
# Application health
curl http://localhost:5000/health

# Database connectivity
curl http://localhost:5000/health/db

# Model status
curl http://localhost:5000/health/models
```

---

## 🤝 Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Code Standards

- Follow PEP 8 for Python code
- Add type hints for new functions
- Include docstrings for public APIs
- Write tests for new functionality
- Update documentation as needed

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run quality checks
python scripts/development/quality_check.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For questions and support:
- 📧 Create an issue on GitHub
- 📖 Check the documentation in `docs/`
- 💬 Contact the development team

---

*This README serves as your primary navigation guide for the Korinsic surveillance platform. For detailed technical documentation, see the `docs/` directory.*
