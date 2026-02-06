"""
Configuration settings for the Diet Planner API.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # API Metadata
    app_name: str = "Diet Planner API"
    app_version: str = "1.0.0"
    app_description: str = """
    🏋️ **Professional Diet Planning API** 
    
    Get personalized nutrition plans based on your fitness goals!
    
    ## Features
    - 📊 BMI Calculation
    - 🔥 Calorie Requirements
    - 💪 Protein Recommendations
    - 🥗 Customized Meal Plans
    
    **Frontend Integration Coming Soon!** 🚀
    """
    
    # CORS Settings
    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # API Settings
    api_prefix: str = "/api/v1"
    debug: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
