"""
Response models for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Literal


class BMIInfo(BaseModel):
    """BMI information with category classification."""
    
    value: float = Field(description="BMI value")
    category: str = Field(description="BMI category (Underweight, Normal, Overweight, Obese)")


class MacroNutrients(BaseModel):
    """Daily macro nutrient requirements."""
    
    calories: int = Field(description="Daily calorie requirement in kcal")
    protein: float = Field(description="Daily protein requirement in grams")


class DietChart(BaseModel):
    """Customized meal plan for the day."""
    
    breakfast: List[str] = Field(description="Breakfast items")
    lunch: List[str] = Field(description="Lunch items")
    snacks: List[str] = Field(description="Snack items")
    dinner: List[str] = Field(description="Dinner items")


class DietPlanResponse(BaseModel):
    """
    Complete diet plan response with all nutritional information.
    """
    
    success: bool = Field(default=True, description="Request success status")
    data: Dict = Field(description="Diet plan data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
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
                        "breakfast": ["Oats 80g + Milk", "3 whole eggs", "2 banana"],
                        "lunch": ["Rice 200g", "Chicken 100g", "Dal"],
                        "snacks": ["Fruits", "Curd", "1 whole egg"],
                        "dinner": ["Roti(3 piece)", "Paneer/chicken 100g", "Dal"]
                    }
                }
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check endpoint response."""
    
    status: str = Field(description="Service status")
    message: str = Field(description="Status message")
    version: str = Field(description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "message": "API is running smoothly",
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Standardized error response."""
    
    success: bool = Field(default=False, description="Request success status")
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Dict = Field(default={}, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {
                    "field": "age",
                    "issue": "Age must be between 9 and 119"
                }
            }
        }
