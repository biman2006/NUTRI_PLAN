"""
API routes for diet planning endpoints.
"""

from fastapi import APIRouter, status, HTTPException
from app.models.requests import DietRequest
from app.models.responses import DietPlanResponse, HealthCheckResponse
from app.services.diet_service import DietService
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Diet Planning"])


@router.get(
    "/",
    response_model=dict,
    summary="Welcome Endpoint",
    description="Welcome message for the Diet Planner API"
)
async def home():
    """
    Welcome endpoint providing basic API information.
    
    Returns:
        Welcome message and API information
    """
    logger.info("Home endpoint accessed")
    return {
        "message": "Welcome to Diet Planner API! 🏋️",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running and operational"
)
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        HealthCheckResponse with status and version information
    """
    logger.info("Health check endpoint accessed")
    return HealthCheckResponse(
        status="ok",
        message="API is running smoothly ✅",
        version=settings.app_version
    )


@router.post(
    "/diet-plan",
    response_model=DietPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Diet Plan",
    description="""
    Generate a personalized diet plan based on your fitness goals.
    
    **This endpoint provides:**
    - BMI calculation with category classification
    - Daily calorie requirements
    - Protein intake recommendations
    - Customized meal plan for the day
    
    **Goals:**
    - **cut**: Lose weight while preserving muscle
    - **bulk**: Gain muscle mass
    - **maintain**: Maintain current weight and fitness level
    """,
    responses={
        200: {
            "description": "Successful diet plan generation",
            "content": {
                "application/json": {
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
                                "breakfast": ["Oats 80g + Milk", "3 whole eggs", "2 bananas"],
                                "lunch": ["Rice 200g", "Chicken 100g", "Dal"],
                                "snacks": ["Fruits", "Curd", "1 whole egg"],
                                "dinner": ["Roti (3 pieces)", "Paneer/Chicken 100g", "Dal"]
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "ValidationError",
                        "message": "Invalid input data provided",
                        "details": {
                            "field": "age",
                            "issue": "Age must be between 9 and 119"
                        }
                    }
                }
            }
        }
    }
)
async def create_diet_plan(user: DietRequest):
    """
    Generate a complete personalized diet plan.
    
    Args:
        user: DietRequest containing age, height, weight, and fitness goal
        
    Returns:
        DietPlanResponse with complete nutritional information and meal plan
        
    Raises:
        HTTPException: If diet plan generation fails
    """
    try:
        logger.info(f"Diet plan requested for user: age={user.age}, goal={user.goal}")
        
        # Create service instance
        service = DietService(user)
        
        # Generate complete plan
        plan_data = service.get_complete_plan()
        
        logger.info(f"Diet plan generated successfully for goal: {user.goal}")
        
        return DietPlanResponse(
            success=True,
            data=plan_data
        )
        
    except Exception as e:
        logger.error(f"Error generating diet plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate diet plan"
        )
