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
    
    def calculate_calories(self) -> int:
        """
        Calculate daily calorie requirements based on weight and goal.
        
        Formulas:
        - Maintain: weight × 32 kcal/kg
        - Cut: weight × 28 kcal/kg
        - Bulk: weight × 36 kcal/kg
        
        Returns:
            Daily calorie requirement in kcal
        """
        goal = self.user.goal.lower()
        multiplier = self.CALORIE_MULTIPLIERS.get(goal, 32)
        calories = self.user.weight * multiplier
        
        logger.debug(f"Calories calculated for {goal}: {calories} kcal")
        return round(calories)
    
    def calculate_protein(self) -> float:
        """
        Calculate daily protein requirements based on weight and goal.
        
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
        return {
            "age": self.user.age,
            "goal": self.user.goal,
            "bmi": self.calculate_bmi(),
            "macros": {
                "calories": self.calculate_calories(),
                "protein": self.calculate_protein()
            },
            "diet_chart": self.generate_diet_chart()
        }
