# 🚀 Nadi Dosha Calculator - Server-Side Architecture

## Architecture Overview

This project has been refactored to follow **SOLID principles** with a clean, maintainable server-side architecture.

## 📁 Project Structure

```
nadi-dosha-calculator/
├── server/                      # Server package
│   ├── __init__.py
│   ├── main.py                 # FastAPI app (standalone)
│   ├── domain/                 # Domain layer
│   │   ├── models.py          # Domain models (NadiResult, BirthDetails)
│   │   └── constants.py       # Astronomical constants
│   ├── services/               # Service layer (business logic)
│   │   ├── julian_date_calculator.py
│   │   ├── moon_position_calculator.py
│   │   ├── ayanamsa_calculator.py
│   │   ├── nakshatra_mapper.py
│   │   ├── nadi_mapper.py
│   │   └── nadi_calculation_service.py  # Orchestrator
│   ├── api/                    # API layer
│   │   ├── routes.py          # API endpoints
│   │   ├── schemas.py         # Request/Response models
│   │   └── middleware.py      # Rate limiting
│   └── utils/                  # Utilities
│       └── logger.py          # Logging
├── server.py                   # Unified server (proxy + API + static)
├── requirements.txt            # Python dependencies
├── index.html                  # Client UI
├── script.js                   # Client code (calls API)
└── styles.css                  # Styles
```

## 🏗️ SOLID Principles Applied

### Single Responsibility Principle (SRP)
- **JulianDateCalculator**: Only converts dates to Julian dates
- **MoonPositionCalculator**: Only calculates Moon's position
- **AyanamsaCalculator**: Only calculates Ayanamsa
- **NakshatraMapper**: Only maps longitude to Nakshatra
- **NadiMapper**: Only maps Nakshatra to Nadi
- **NadiCalculationService**: Orchestrates the calculation workflow

### Open/Closed Principle (OCP)
- Services can be extended without modification (e.g., add new Ayanamsa methods)
- Middleware can be added/removed without changing core logic
- New calculation strategies can be implemented as alternatives

### Liskov Substitution Principle (LSP)
- All calculators follow consistent interfaces
- Can substitute implementations for testing (dependency injection)

### Interface Segregation Principle (ISP)
- Focused, minimal interfaces
- No client depends on methods it doesn't use

### Dependency Inversion Principle (DIP)
- High-level modules (API routes) depend on abstractions (services)
- Services use dependency injection for testability
- Dependencies flow inward: API → Service → Calculators

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python server.py
```

The server will start at `http://localhost:8000`

### 3. Access the Application

- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Calculate Nadi Dosha

**POST** `/api/calculate-nadi`

```json
{
  "birth_date": "1998-12-20",
  "birth_time": "14:30",
  "timezone": "5.5",
  "latitude": 19.0760,
  "longitude": 72.8777
}
```

**Response:**
```json
{
  "nakshatra": "Ashwini",
  "nakshatraIndex": 0,
  "pada": 1,
  "nadi": "Aadi",
  "siderealLongitude": 12.345678,
  "tropicalLongitude": 36.789012,
  "accuracy": "Enhanced (±0.5 arc-minutes)"
}
```

### Proxy Endpoints

- **GET** `/api/nominatim` - Nominatim geocoding proxy
- **GET** `/api/photon` - Photon geocoding proxy
- **GET** `/api/timeapi` - TimeAPI timezone proxy

## 🔒 Security Features

### Rate Limiting
- **100 requests per hour** per IP address
- Sliding window algorithm
- Headers: `X-RateLimit-Remaining`, `X-RateLimit-Limit`

### Input Validation
- Pydantic schemas validate all inputs
- Type checking and range validation
- Clear error messages

### Error Handling
- Comprehensive error logging
- User-friendly error messages
- No sensitive data in responses

## 🧪 Testing

### Manual Testing

```bash
# Start server
python server.py

# Test API endpoint
curl -X POST http://localhost:8000/api/calculate-nadi \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1998-12-20",
    "birth_time": "14:30",
    "timezone": "5.5",
    "latitude": 19.0760,
    "longitude": 72.8777
  }'
```

### Unit Testing (Future)

Each service can be tested independently:

```python
from server.services.julian_date_calculator import JulianDateCalculator
from datetime import datetime

calculator = JulianDateCalculator()
jd = calculator.from_ut_datetime(datetime(2000, 1, 1, 12, 0, 0))
assert jd == 2451545.0  # J2000.0
```

## 📊 Performance

- **Calculation Speed**: < 50ms (server-side)
- **API Response Time**: < 100ms (excluding network)
- **Rate Limiting**: In-memory (fast)
- **Concurrent Requests**: Limited by uvicorn workers

## 🔧 Configuration

### Rate Limiting

Edit `server/api/middleware.py`:

```python
rate_limiter = RateLimiter(
    max_requests=100,      # Requests per window
    window_minutes=60      # Time window
)
```

### Logging

Edit `server/utils/logger.py`:

```python
logger = setup_logger(
    name="nadi_calculator",
    level=logging.INFO  # DEBUG, INFO, WARNING, ERROR
)
```

## 🚢 Deployment

### Option 1: Railway/Render/Fly.io

1. Push code to repository
2. Connect to platform
3. Set Python version: `3.9+`
4. Install command: `pip install -r requirements.txt`
5. Start command: `python server.py`

### Option 2: Docker (Future)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

### Option 3: Traditional Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn (production)
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Code Quality

- **Type Hints**: Full type annotations
- **Docstrings**: Comprehensive documentation
- **Error Handling**: Try-except with logging
- **Validation**: Pydantic models
- **Separation of Concerns**: Clear layer boundaries

## 🔄 Migration from Client-Side

The client-side calculation code is still present but marked as `@deprecated`. It's kept for:
- Reference
- Fallback (if API fails)
- Gradual migration

To fully remove client-side calculations:
1. Remove `calculateNakshatraAndNadi()` function
2. Remove `calculateJulianDate()` function
3. Remove calculation constants

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SOLID Principles**: https://en.wikipedia.org/wiki/SOLID
- **Pydantic**: https://docs.pydantic.dev/

