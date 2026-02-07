# 🏋️ NUTRI PLAN

**Professional Nutrition Planning Application** - A full-stack health and fitness platform combining scientific metabolic calculations with a stunning, art-driven interface.

![Version](https://img.shields.io/badge/version-1.0.0-coral)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-19.2.0-blue)

---

## ✨ Features

### 🔬 **Scientific Calculations**
- **BMI Analysis** with WHO health category classification
- **BMR Calculation** using Mifflin-St Jeor equation (gender-specific)
- **TDEE Computation** with 5 activity level multipliers
- **Macro Targets** with goal-based calorie adjustments

### 🎨 **Art-Driven Design**
- Warm, organic color palette (Coral, Forest Green, Golden Amber)
- Editorial typography with DM Serif Display + Outfit
- Purposeful micro-animations and smooth transitions
- Fully responsive (mobile, tablet, desktop)

### 📊 **Comprehensive API**
- FastAPI backend with auto-generated docs
- Pydantic validation for all inputs
- Professional error handling and logging
- CORS-enabled for frontend integration

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 18+**
- **Git**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/biman2006/NUTRI_PLAN.git
cd NUTRI_PLAN
```

### 2️⃣ Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn app.main:app --reload
```

**Backend runs on**: http://127.0.0.1:8000  
**API Docs**: http://127.0.0.1:8000/docs

###3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs on**: http://localhost:5173

---

## 📋 API Usage

### Endpoint: `POST /diet-plan`

Generate a personalized nutrition plan based on user metrics.

#### Request Body

```json
{
  "age": 25,
  "gender": "male",
  "height": 1.75,
  "weight": 70,
  "activity_level": "moderately_active",
  "goal": "maintain"
}
```

#### Field Specifications

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `age` | integer | 9-119 | User age in years |
| `gender` | string | "male", "female" | Biological gender for BMR calculation |
| `height` | float | 0.5-3.0 | Height in meters |
| `weight` | float | 26-299 | Weight in kilograms |
| `activity_level` | string | "sedentary", "lightly_active", "moderately_active", "very_active", "extra_active" | Daily physical activity level |
| `goal` | string | "cut", "bulk", "maintain" | Fitness objective |

#### Response

```json
{
  "success": true,
  "data": {
    "age": 25,
    "gender": "male",
    "activity_level": "moderately_active",
    "goal": "maintain",
    "bmi": {
      "value": 22.86,
      "category": "Normal weight"
    },
    "metabolism": {
      "bmr": 1686,
      "tdee": 2613
    },
    "macros": {
      "calories": 2613,
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

---

## 🏗️ Project Structure

```
NUTRI_PLAN/
├── app/                          # Backend (FastAPI)
│   ├── main.py                  # Application entry point
│   ├── config.py                # Settings & CORS configuration
│   ├── models/                  # Pydantic request/response models
│   │   ├── requests.py         # API request schemas
│   │   └── responses.py        # API response schemas
│   ├── services/                # Business logic
│   │   └── diet_service.py     # BMR/TDEE/macro calculations
│   ├── routes/                  # API endpoints
│   │   └── diet_routes.py      # Diet planning routes
│   └── exceptions/              # Custom error handling
│       └── __init__.py         # Exception handlers
│
├── frontend/                     # Frontend (React + Vite)
│   ├── src/
│   │   ├── App.jsx              # Main application component
│   │   ├── App.css              # Component-specific styles
│   │   ├── index.css            # Global design system
│   │   └── main.jsx             # React entry point
│   ├── public/
│   │   └── NutiPlanLogo.png    # Application logo
│   ├── .env                     # Environment configuration
│   └── package.json             # Dependencies
│
├── tests/                        # Test suite
├── requirements.txt              # Python dependencies
├── .env                          # Backend configuration
├── .gitignore                    # Git exclusions
└── README.md                     # This file
```

---

## 🔧 Configuration

### Backend Environment (`.env`)

```env
LOG_LEVEL=INFO
DEBUG=True
```

### Frontend Environment (`frontend/.env`)

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production, update `VITE_API_URL` to your deployed backend URL.

---

## 🎨 Design System

### Color Palette

```css
/* Primary Colors */
--vitality-coral: #FF6F59    /* Energy & Action */
--forest-green: #2D6A4F      /* Health & Growth */
--golden-amber: #F2B705       /* Nutrition & Vitality */

/* Base Colors */
--rich-earth: #1A1310         /* Text & Depth */
--soft-cream: #FFFCF2         /* Background */
```

### Typography

- **Display**: DM Serif Display (Editorial authority)
- **Body**: Outfit (Modern readability)

### Visual Principles

- **Warm & Organic**: Earth tones create human connection
- **Editorial Confidence**: Serif headlines establish authority
- **Purposeful Motion**: Animations serve the narrative
- **Accessible**: WCAG AA contrast compliance

---

## 🧮 Calculation Methods

### BMR (Basal Metabolic Rate)
**Mifflin-St Jeor Equation**:
- Male: `(10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5`
- Female: `(10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161`

### TDEE (Total Daily Energy Expenditure)
`TDEE = BMR × Activity Multiplier`

**Activity Multipliers**:
- Sedentary: 1.2
- Lightly Active: 1.375
- Moderately Active: 1.55
- Very Active: 1.725
- Extra Active: 1.9

### Goal-Based Calorie Targets
- **Maintain**: TDEE (no change)
- **Cut**: TDEE - 500 kcal (≈0.5kg/week loss)
- **Bulk**: TDEE + 300 kcal (lean muscle gain)

### Protein Requirements
- **Maintain**: weight × 1.6 g/kg
- **Cut**: weight × 2.2 g/kg (muscle preservation)
- **Bulk**: weight × 1.8 g/kg

---

## 📦 Production Build

### Frontend Build

```bash
cd frontend
npm run build
```

Output: `frontend/dist/` (static files ready for deployment)

### Deployment Options

**Backend**:
- Heroku, Railway, AWS EC2, Google Cloud Run
- Update CORS origins in `app/config.py` for production

**Frontend**:
- Vercel, Netlify, GitHub Pages
- Set `VITE_API_URL` environment variable

---

## 🧪 Testing

### Run Backend Tests

```bash
pytest tests/
```

### Manual Testing

1. Start both backend and frontend servers
2. Navigate to http://localhost:5173
3. Fill in all 6 required fields
4. Submit form and verify response

**Success Criteria**:
- ✅ Form accepts all inputs
- ✅ API returns 200 OK
- ✅ Results display with BMI, BMR, TDEE, Calories, Protein
- ✅ Meal plan renders correctly

---

## 🐛 Troubleshooting

### "Failed to fetch" Error

**Issue**: Frontend cannot connect to backend  
**Solution**: Ensure backend is running on http://127.0.0.1:8000

```bash
curl http://127.0.0.1:8000/health
```

### CORS Errors

**Issue**: Cross-origin requests blocked  
**Solution**: CORS is pre-configured. For production, update `app/config.py`:

```python
cors_origins: List[str] = ["https://your-frontend-domain.com"]
```

### Module Not Found (Backend)

**Issue**: `ModuleNotFoundError: No module named 'app'`  
**Solution**: Run uvicorn from the correct directory:

```bash
cd NUTRI_PLAN  # Not the parent directory!
uvicorn app.main:app --reload
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🌟 Acknowledgments

- **Mifflin-St Jeor Equation**: For scientifically accurate BMR calculation
- **FastAPI**: For the powerful, modern Python framework
- **React + Vite**: For the lightning-fast frontend tooling
- **Design Inspiration**: Editorial health magazines & nutritional science

---

## 📞 Support

For questions or issues:
- **GitHub Issues**: [Report a bug](https://github.com/biman2006/NUTRI_PLAN/issues)
- **API Documentation**: http://127.0.0.1:8000/docs

---

<div align="center">

**Made with ❤️ and Science**

*Your body is a living system deserving of vibrant, intelligent nutrition.*

</div>
