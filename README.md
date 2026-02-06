<div align="center">

# 🏋️ Diet Planner API

### *Your Personal Nutrition Companion*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.3-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12.5-E92063?style=for-the-badge&logo=pydantic)](https://docs.pydantic.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**A professional-grade REST API for personalized nutrition planning, BMI calculation, and macro-nutrient recommendations.**

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Project Structure](#-project-structure) • [Roadmap](#-roadmap)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📊 **Smart BMI Analysis**
- Accurate BMI calculation
- WHO-standard category classification
- Health status indicators

### 🔥 **Calorie Intelligence**
- Goal-based calorie recommendations
- Cut, bulk, or maintain options
- Science-backed formulas

</td>
<td width="50%">

### 💪 **Protein Optimization**
- Customized protein requirements
- Goal-specific multipliers
- Muscle preservation focus

### 🥗 **Personalized Meal Plans**
- Complete daily meal breakdown
- Breakfast, lunch, snacks & dinner
- Goal-tailored portions

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd NUTRI_PLAN

# 2. Create and activate virtual environment
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
uvicorn app.main:app --reload
```

### 🎯 Your API is now running at:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📚 API Documentation

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message & API info |
| `GET` | `/health` | Health check & status |
| `POST` | `/diet-plan` | Generate personalized diet plan |

### Example Request

**POST** `/diet-plan`

```json
{
  "age": 25,
  "height": 1.75,
  "weight": 70,
  "goal": "maintain"
}
```

### Example Response

```json
{
  "success": true,
  "data": {
    "age": 25,
    "goal": "maintain",
    "bmi": {
      "value": 22.86,
      "category": "Normal weight"
    },
    "macros": {
      "calories": 2240,
      "protein": 112.0
    },
    "diet_chart": {
      "breakfast": ["Oats 80g + Milk", "3 whole eggs", "2 bananas"],
      "lunch": ["Rice 200g", "Chicken 100g", "Dal"],
      "snacks": ["Fruits", "Curd", "1 whole egg"],
      "dinner": ["Roti (3 pieces)", "Paneer/Chicken 100g", "Dal"]
    }
  }
}
```

### Fitness Goals

| Goal | Purpose | Calorie Multiplier | Protein Multiplier |
|------|---------|-------------------|-------------------|
| **cut** | Lose weight, preserve muscle | 28 kcal/kg | 2.2 g/kg |
| **bulk** | Gain muscle mass | 36 kcal/kg | 1.8 g/kg |
| **maintain** | Maintain current weight | 32 kcal/kg | 1.6 g/kg |

---

## 📁 Project Structure

```
NUTRI_PLAN/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI application
│   ├── config.py             # Configuration & settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py       # Request validation models
│   │   └── responses.py      # Response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── diet_service.py   # Business logic
│   ├── routes/
│   │   ├── __init__.py
│   │   └── diet_routes.py    # API endpoints
│   └── exceptions/
│       └── __init__.py       # Error handlers
├── tests/
│   └── __init__.py           # Test suite
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🛠️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com) - Modern, fast web framework
- **Validation**: [Pydantic](https://docs.pydantic.dev) - Data validation using Python type hints
- **Server**: [Uvicorn](https://www.uvicorn.org) - Lightning-fast ASGI server
- **Configuration**: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Environment management

---

## 🎨 Key Highlights

### ✅ Professional Architecture
- Clean separation of concerns
- Modular package structure
- Industry best practices

### ✅ Comprehensive Validation
- Request/response validation
- Custom field validators
- Detailed error messages

### ✅ Rich Documentation
- Auto-generated OpenAPI docs
- Complete type hints
- Google-style docstrings

### ✅ Error Handling
- Global exception handlers
- Standardized error responses
- Detailed logging

### ✅ Production Ready
- CORS middleware
- Environment configuration
- Logging infrastructure
- Health check endpoint

---

## 🔮 Roadmap

### Coming Soon

> [!IMPORTANT]
> 🎨 **Frontend Integration** is currently in development!
> 
> We're building a beautiful, modern web interface to interact with this API. Stay tuned for:
> - 📱 Responsive design
> - 🎯 Interactive goal selection
> - 📊 Visual nutrition charts
> - 💾 Save and track your plans

### Future Enhancements

- [ ] User authentication & profiles
- [ ] Database integration
- [ ] Meal plan history tracking
- [ ] Advanced nutrition analysis
- [ ] Recipe recommendations
- [ ] Progress tracking & analytics
- [ ] Multi-language support
- [ ] Mobile app integration

---

## 🧪 Testing the API

### Using cURL

```bash
# Health Check
curl http://localhost:8000/health

# Generate Diet Plan
curl -X POST "http://localhost:8000/diet-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 25,
    "height": 1.75,
    "weight": 70,
    "goal": "maintain"
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/diet-plan"
data = {
    "age": 25,
    "height": 1.75,
    "weight": 70,
    "goal": "maintain"
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Biman && Sukrit**

- GitHub: [@Biman](https://github.com/biman2006)
- GitHub: [@Sukrit](https://github.com/sukrit-89)

---

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- Pydantic for powerful validation
- The Python community for continuous inspiration

---

<div align="center">

### ⭐ If you find this project useful, please consider giving it a star!

**Made with ❤️ and Python**

</div>
