"""
Configuration management for Penny Flicker mission.
Handles environment variables, service initialization, and constants.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field

class MissionConfig(BaseSettings):
    """Mission configuration with validation."""
    
    # Firebase Configuration
    firebase_credential_path: str = Field(
        default="firebase_credentials.json",
        description="Path to Firebase service account credentials"
    )
    
    # Data Sources
    yahoo_finance_base_url: str = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    # Mission Parameters
    penny_stock_threshold: float = 5.0  # Maximum price for penny stocks
    monitoring_interval_minutes: int = 5
    alert_price_change_percent: float = 10.0
    
    # Retry Configuration
    max_retries: int = 3
    retry_delay_seconds: int = 5
    
    # Firestore Collections
    firestore_collection: str = "penny_flicker"
    history_subcollection: str = "price_history"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "penny_flicker.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def initialize_environment():
    """Initialize mission environment and validate configuration."""
    config = MissionConfig()
    
    # Validate Firebase credentials exist
    if not Path(config.firebase_credential_path).exists():
        raise FileNotFoundError(
            f"Firebase credentials not found at: {config.firebase_credential_path}"
        )
    
    # Ensure log directory exists
    Path(config.log_file).