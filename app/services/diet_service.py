"""
Diet service module for nutritional calculations and meal planning.

This module provides the core business logic for calculating BMI, daily calorie
requirements, protein needs, and generating personalized meal plans based on
fitness goals.
"""

from typing import Dict, List, Literal
from app.models.requests import DietRequest
from app.exceptions import CalculationException
import logging

logger = logging.getLogger(__name__)


class DietService:
    """
    Service class for diet-related calculations and meal planning.
    
    This class encapsulates all business logic for:
    - BMI calculation and classification
    - Daily calorie requirement estimation
    - Protein intake recommendations
    - Customized meal plan generation
    
    Attributes:
        user: DietRequest object containing user information
    """
    
    # Constants for calculations
    CALORIE_MULTIPLIERS = {
        "maintain": 32,
        "cut": 28,
        "bulk": 36
    }
    
    # Activity level multipliers for TDEE calculation
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,           # Little or no exercise
        "lightly_active": 1.375,    # Light exercise 1-3 days/week
        "moderately_active": 1.55,  # Moderate exercise 3-5 days/week
        "very_active": 1.725,       # Hard exercise 6-7 days/week
        "extra_active": 1.9         # Very hard exercise & physical job
    }
    
    # Goal-based calorie adjustments (applied to TDEE)
    GOAL_ADJUSTMENTS = {
        "maintain": 0,      # No adjustment
        "cut": -500,        # 500 calorie deficit
        "bulk": 300         # 300 calorie surplus
    }
    
    PROTEIN_MULTIPLIERS = {
        "maintain": 1.6,
        "cut": 2.2,
        "bulk": 1.8
    }
    
    BMI_CATEGORIES = [
        (0, 18.5, "Underweight"),
        (18.5, 25, "Normal weight"),
        (25, 30, "Overweight"),
        (30, float('inf'), "Obese")
    ]
    
    def __init__(self, user: DietRequest):
        """
        Initialize the diet service with user information.
        
        Args:
            user: DietRequest object containing age, height, weight, and goal
        """
        self.user = user
        logger.info(f"DietService initialized for user with goal: {user.goal}")
    
    def calculate_bmi(self) -> Dict[str, any]:
        """
        Calculate Body Mass Index and determine BMI category.
        
        BMI = weight (kg) / height (m)²
        
        Returns:
            Dict containing BMI value and category
            
        Raises:
            CalculationException: If calculation fails
        """
        try:
            bmi_value = self.user.weight / (self.user.height ** 2)
            category = self._get_bmi_category(bmi_value)
            
            logger.debug(f"BMI calculated: {bmi_value:.2f} ({category})")
            
            return {
                "value": round(bmi_value, 2),
                "category": category
            }
        except ZeroDivisionError:
            raise CalculationException(
                "Invalid height value for BMI calculation",
                {"height": self.user.height}
            )
        except Exception as e:
            raise CalculationException(f"BMI calculation failed: {str(e)}")
    
    def calculate_bmr(self) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation.
        
        This is the number of calories your body burns at rest.
        
        Formulas:
        - Male: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age) + 5
        - Female: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age) - 161
        
        Returns:
            Basal Metabolic Rate in kcal/day
        """
        weight_kg = self.user.weight
        height_cm = self.user.height * 100  # Convert meters to cm
        age = self.user.age
        
        if self.user.gender.lower() == "male":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
        logger.debug(f"BMR calculated for {self.user.gender}: {bmr:.0f} kcal")
        return round(bmr, 1)
    
    def calculate_tdee(self) -> float:
        """
        Calculate Total Daily Energy Expenditure.
        
        TDEE = BMR × Activity Multiplier
        
        Returns:
            Total daily calories needed to maintain current weight
        """
        bmr = self.calculate_bmr()
        activity_multiplier = self.ACTIVITY_MULTIPLIERS.get(
            self.user.activity_level.lower(),
            1.55  # Default to moderately active
        )
        
        tdee = bmr * activity_multiplier
        logger.debug(f"TDEE calculated: {tdee:.0f} kcal (BMR: {bmr}, Activity: {self.user.activity_level})")
        return round(tdee, 1)
    
    def calculate_calories(self) -> int:
        """
        Calculate daily calorie requirements based on TDEE and fitness goal.
        
        Uses scientifically accurate Mifflin-St Jeor equation with activity multipliers,
        then adjusts for fitness goals:
        - Maintain: TDEE (no change)
        - Cut: TDEE - 500 kcal (for ~0.5kg/week loss)
        - Bulk: TDEE + 300 kcal (for lean muscle gain)
        
        Returns:
            Daily calorie target in kcal
        """
        tdee = self.calculate_tdee()
        goal = self.user.goal.lower()
        adjustment = self.GOAL_ADJUSTMENTS.get(goal, 0)
        
        calories = tdee + adjustment
        logger.debug(f"Calories calculated for {goal}: {calories:.0f} kcal (TDEE: {tdee}, Adjustment: {adjustment:+d})")
        return round(calories)
    
    def calculate_protein(self) -> float:
        """
        Calculate daily protein requirements based on weight and goal.
        
        Protein needs are adjusted based on activity level and goals.
        Higher activity and cutting phases require more protein.
        
        Formulas:
        - Maintain: weight × 1.6 g/kg
        - Cut: weight × 2.2 g/kg (higher for muscle preservation)
        - Bulk: weight × 1.8 g/kg
        
        Returns:
            Daily protein requirement in grams
        """
        goal = self.user.goal.lower()
        multiplier = self.PROTEIN_MULTIPLIERS.get(goal, 1.6)
        protein = self.user.weight * multiplier
        
        logger.debug(f"Protein calculated for {goal}: {protein}g")
        return round(protein, 1)
    
    def generate_diet_chart(self) -> Dict[str, List[str]]:
        """
        Generate a customized meal plan based on fitness goal.
        
        Creates a complete daily meal plan with breakfast, lunch,
        snacks, and dinner tailored to the user's fitness objective.
        
        Returns:
            Dictionary with meal categories and food items
        """
        goal = self.user.goal.lower()
        
        meal_plans = {
            "cut": {
                "breakfast": ["Oats 50g + Milk", "2 egg whites and 1 whole egg"],
                "lunch": ["Rice 150g", "Chicken breast 150g", "Salad"],
                "snacks": ["Curd 200g", "One seasonal fruit"],
                "dinner": ["Roti (2 pieces)", "Paneer 100g / Chicken breast 100g", "Vegetables"]
            },
            "bulk": {
                "breakfast": ["Oats 100g + Milk", "4 whole eggs", "3 bananas"],
                "lunch": ["Rice 250g", "Chicken 200g", "Dal", "Boiled potato (2 pieces)", "Curd 150g"],
                "snacks": ["Banana shake", "Curd 100g", "Peanut butter", "2 whole eggs"],
                "dinner": ["Roti (3 pieces)", "Paneer/Chicken 150g", "Vegetables"]
            },
            "maintain": {
                "breakfast": ["Oats 80g + Milk", "3 whole eggs", "2 bananas"],
                "lunch": ["Rice 200g", "Chicken 100g", "Dal"],
                "snacks": ["Fruits", "Curd", "1 whole egg"],
                "dinner": ["Roti (3 pieces)", "Paneer/Chicken 100g", "Dal"]
            }
        }
        
        diet_chart = meal_plans.get(goal, meal_plans["maintain"])
        logger.debug(f"Diet chart generated for goal: {goal}")
        
        return diet_chart
    
    def _get_bmi_category(self, bmi: float) -> str:
        """
        Determine BMI category based on WHO standards.
        
        Args:
            bmi: Calculated BMI value
            
        Returns:
            BMI category string
        """
        for lower, upper, category in self.BMI_CATEGORIES:
            if lower <= bmi < upper:
                return category
        return "Unknown"
    
    def get_complete_plan(self) -> Dict:
        """
        Generate a complete diet plan with all information.
        
        Returns:
            Complete diet plan dictionary with all calculated values
        """
        bmr = self.calculate_bmr()
        tdee = self.calculate_tdee()
        
        return {
            "age": self.user.age,
            "gender": self.user.gender,
            "activity_level": self.user.activity_level,
            "goal": self.user.goal,
            "bmi": self.calculate_bmi(),
            "metabolism": {
                "bmr": round(bmr),
                "tdee": round(tdee)
            },
            "macros": {
                "calories": self.calculate_calories(),
                "protein": self.calculate_protein()
            },
            "diet_chart": self.generate_diet_chart()
        }
