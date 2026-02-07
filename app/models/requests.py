"""
Request models for API endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Annotated


class DietRequest(BaseModel):
    """
    Request model for diet plan generation.
    
    Attributes:
        age: User's age in years (9-119)
        gender: User's biological gender (male/female)
        height: User's height in meters (e.g., 1.75)
        weight: User's weight in kilograms (26-299)
        activity_level: Physical activity level (sedentary to very_active)
        goal: Fitness goal - cut (lose weight), bulk (gain muscle), or maintain
    """
    
    age: Annotated[
        int,
        Field(
            gt=8,
            lt=120,
            title="Age",
            description="Your age in years (must be between 9 and 119)",
            examples=[25, 30, 45]
        )
    ]
    
    gender: Annotated[
        Literal["male", "female"],
        Field(
            title="Gender",
            description="Biological gender for accurate calorie calculations",
            examples=["male"]
        )
    ]
    
    height: Annotated[
        float,
        Field(
            gt=0.5,
            lt=3.0,
            title="Height",
            description="Your height in meters (e.g., 1.75 for 175cm)",
            examples=[1.75, 1.68, 1.82]
        )
    ]
    
    weight: Annotated[
        float,
        Field(
            gt=25,
            lt=300,
            title="Weight",
            description="Your weight in kilograms",
            examples=[70, 65, 85]
        )
    ]
    
    activity_level: Annotated[
        Literal["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"],
        Field(
            title="Activity Level",
            description="Daily physical activity level: sedentary (little/no exercise), lightly_active (1-3 days/week), moderately_active (3-5 days/week), very_active (6-7 days/week), extra_active (very hard exercise/physical job)",
            examples=["moderately_active"]
        )
    ]
    
    goal: Annotated[
        Literal["cut", "bulk", "maintain"],
        Field(
            title="Fitness Goal",
            description="Your fitness objective: 'cut' to lose weight, 'bulk' to gain muscle, 'maintain' to maintain current weight",
            examples=["maintain"]
        )
    ]
    
    @field_validator('height')
    @classmethod
    def validate_height(cls, v: float) -> float:
        """Validate that height is within reasonable human range."""
        if v < 0.5 or v > 3.0:
            raise ValueError('Height must be between 0.5 and 3.0 meters')
        return v
    
    @field_validator('weight')
    @classmethod
    def validate_weight(cls, v: float) -> float:
        """Validate that weight is within reasonable range."""
        if v < 25 or v > 300:
            raise ValueError('Weight must be between 25 and 300 kilograms')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 25,
                "gender": "male",
                "height": 1.75,
                "weight": 70,
                "activity_level": "moderately_active",
                "goal": "maintain"
            }
        }
