# 🔍 Codebase Explanation - Diet Planner API

> **Note**: This file is for developer reference only and is excluded from version control.

---

## 📖 Overview

This document provides a comprehensive explanation of the Diet Planner API codebase architecture, design decisions, and implementation details for developers working on this project.

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Client App    │
│  (Frontend/API  │
│    Consumer)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI App   │
│   (app/main.py) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Routes  │ │Exception │
│ Layer   │ │Handlers  │
└────┬────┘ └──────────┘
     │
     ▼
┌─────────────┐
│  Services   │
│   Layer     │
└─────────────┘
```

### Layer Responsibilities

1. **Routes Layer** (`app/routes/`)
   - Handle HTTP requests and responses
   - Validate input using Pydantic models
   - Call appropriate service methods
   - Return formatted responses

2. **Services Layer** (`app/services/`)
   - Implement business logic
   - Perform calculations (BMI, calories, protein)
   - Generate meal plans
   - Independent of HTTP concerns

3. **Models Layer** (`app/models/`)
   - Define request/response schemas
   - Implement validation rules
   - Provide type safety

4. **Exception Layer** (`app/exceptions/`)
   - Global error handling
   - Custom exception classes
   - Standardized error responses

---

## 📁 Directory Structure Explained

```
NUTRI_PLAN/
│
├── app/                          # Main application package
│   │
│   ├── __init__.py               # Package marker & version info
│   ├── main.py                   # Application entry point
│   │                             # - Creates FastAPI instance
│   │                             # - Registers middleware (CORS)
│   │                             # - Registers exception handlers
│   │                             # - Includes routers
│   │                             # - Configures logging
│   │
│   ├── config.py                 # Configuration management
│   │                             # - Environment variables
│   │                             # - API metadata
│   │                             # - CORS settings
│   │                             # - Uses pydantic-settings
│   │
│   ├── models/                   # Pydantic models
│   │   ├── __init__.py           # Export all models
│   │   ├── requests.py           # Request validation models
│   │   │                         # - DietRequest with validators
│   │   └── responses.py          # Response schemas
│   │       ├── BMIInfo           # - BMI data structure
│   │       ├── MacroNutrients    # - Calories & protein
│   │       ├── DietChart         # - Meal plan structure
│   │       ├── DietPlanResponse  # - Complete response
│   │       ├── HealthCheckResponse
│   │       └── ErrorResponse     # - Standardized errors
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   └── diet_service.py       # DietService class
│   │       ├── calculate_bmi()   # - BMI calculation & classification
│   │       ├── calculate_calories() # - Daily calorie needs
│   │       ├── calculate_protein()  # - Protein requirements
│   │       ├── generate_diet_chart() # - Meal planning
│   │       └── get_complete_plan()   # - Full plan generation
│   │
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   └── diet_routes.py        # Router with endpoints
│   │       ├── GET /             # - Welcome message
│   │       ├── GET /health       # - Health check
│   │       └── POST /diet-plan   # - Generate diet plan
│   │
│   └── exceptions/               # Error handling
│       └── __init__.py
│           ├── DietServiceException      # - Custom exceptions
│           ├── ValidationException
│           ├── validation_exception_handler
│           ├── diet_service_exception_handler
│           └── general_exception_handler
│
├── tests/                        # Test suite (to be implemented)
│   └── __init__.py
│
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # User-facing documentation
```

---

## 🔄 Request Flow

### Example: POST /diet-plan

```
1. Client Request
   ↓
2. FastAPI receives request at POST /diet-plan
   ↓
3. Pydantic validates request body against DietRequest model
   │
   ├─ ✅ Valid → Continue
   └─ ❌ Invalid → ValidationException → 422 Response
   ↓
4. Route handler calls DietService.get_complete_plan()
   ↓
5. DietService methods:
   ├─ calculate_bmi()          # Calls helper _get_bmi_category()
   ├─ calculate_calories()     # Goal-based multiplier
   ├─ calculate_protein()      # Goal-based multiplier
   └─ generate_diet_chart()    # Meal plan selection
   ↓
6. Service returns Dict with all data
   ↓
7. Route wraps in DietPlanResponse
   ↓
8. FastAPI serializes to JSON
   ↓
9. Response sent to client
```

---

## 💡 Key Design Decisions

### 1. **Separation of Concerns**
- **Why**: Makes code maintainable, testable, and scalable
- **How**: Separate layers for routes, services, models, and config
- **Benefit**: Can change one layer without affecting others

### 2. **Pydantic for Validation**
- **Why**: Type safety + automatic validation
- **How**: Request/Response models with Field validators
- **Benefit**: Catches errors early, auto-generates OpenAPI docs

### 3. **Dependency Injection Ready**
- **Why**: Future database/auth integration
- **How**: Service classes accept user data, not tied to HTTP
- **Benefit**: Easy to test and extend

### 4. **Configuration via Environment**
- **Why**: Different settings for dev/prod
- **How**: pydantic-settings with .env support
- **Benefit**: No code changes for deployment

### 5. **Comprehensive Error Handling**
- **Why**: Better user experience
- **How**: Global exception handlers + custom exceptions
- **Benefit**: Consistent error format across API

---

## 🧮 Business Logic Formulas

### BMI Calculation
```python
BMI = weight (kg) / height² (m²)

Categories (WHO Standard):
- Underweight: BMI < 18.5
- Normal weight: 18.5 ≤ BMI < 25
- Overweight: 25 ≤ BMI < 30
- Obese: BMI ≥ 30
```

### Calorie Requirements (Harris-Benedict Simplified)
```python
Maintain: weight × 32 kcal/kg
Cut:      weight × 28 kcal/kg  (deficit for fat loss)
Bulk:     weight × 36 kcal/kg  (surplus for muscle gain)
```

### Protein Requirements
```python
Maintain: weight × 1.6 g/kg  (standard recommendation)
Cut:      weight × 2.2 g/kg  (higher to preserve muscle)
Bulk:     weight × 1.8 g/kg  (support muscle synthesis)
```

---

## 🔧 Development Workflow

### Starting the Server

```bash
# Activate virtual environment
cd d:\GymNutritionApi\NUTRI_PLAN
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # Linux/Mac

# Run development server
python -m uvicorn app.main:app --reload

# Server runs at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### Making Changes

1. **Adding a new endpoint**:
   - Add route function to `app/routes/diet_routes.py`
   - Define request model in `app/models/requests.py`
   - Define response model in `app/models/responses.py`
   - Add business logic to relevant service

2. **Adding a new calculation**:
   - Add method to `DietService` class
   - Update `get_complete_plan()` to include it
   - Update response models if needed

3. **Changing validation rules**:
   - Modify field constraints in `app/models/requests.py`
   - Add custom validators using `@field_validator`

---

## 🧪 Testing Strategy (Future)

### Unit Tests
- Test service methods in isolation
- Mock user data
- Verify calculations are correct

### Integration Tests
- Test endpoints with TestClient
- Verify request/response flow
- Check validation errors

### Example Test Structure
```python
# tests/test_diet_service.py
def test_calculate_bmi():
    user = DietRequest(age=25, height=1.75, weight=70, goal="maintain")
    service = DietService(user)
    bmi = service.calculate_bmi()
    assert bmi["value"] == 22.86
    assert bmi["category"] == "Normal weight"
```

---

## 🚀 Deployment Considerations

### Environment Variables
Create `.env` file (not committed to git):
```env
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=["https://yourdomain.com"]
```

### Production Server
```bash
# Use production ASGI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Future)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📝 Code Standards

### Docstrings (Google Style)
```python
def calculate_bmi(self) -> Dict[str, any]:
    """
    Calculate Body Mass Index and determine BMI category.
    
    BMI = weight (kg) / height (m)²
    
    Returns:
        Dict containing BMI value and category
        
    Raises:
        CalculationException: If calculation fails
    """
```

### Type Hints
- All function parameters and returns have type hints
- Use `typing` module for complex types
- Helps IDE autocomplete and catches errors early

### Logging
```python
logger.info("Normal operation messages")
logger.warning("Warning conditions")
logger.error("Error conditions")
logger.exception("Exceptions with traceback")
```

---

## 🔮 Future Enhancements

### Database Integration
```python
# Add SQLAlchemy models
# Store user profiles and history
# Track meal plan adherence
```

### Authentication
```python
# Add JWT authentication
# User registration/login
# Protected endpoints
```

### Advanced Features
- Micronutrient tracking (vitamins, minerals)
- Meal plan customization (allergies, preferences)
- Progress tracking and analytics
- Recipe recommendations with ingredients
- Shopping list generation

---

## 🐛 Common Issues & Solutions

### Issue: Module not found errors
**Solution**: Make sure you're running from the NUTRI_PLAN directory and venv is activated

### Issue: Port already in use
**Solution**: Change port: `uvicorn app.main:app --port 8001`

### Issue: CORS errors in browser
**Solution**: Update `CORS_ORIGINS` in config.py or .env

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [REST API Best Practices](https://restfulapi.net)

---

## 👥 Contributing

When adding new features:
1. Follow existing code structure
2. Add comprehensive docstrings
3. Use type hints
4. Update this document if architecture changes
5. Test your changes thoroughly

---

**Last Updated**: 2026-02-07  
**Version**: 1.0.0  
**Maintained By**: Development Team
