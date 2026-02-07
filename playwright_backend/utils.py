"""
Utility functions for the Match.com automation.
Provides helper functions for data generation and common operations.
"""

import random
import string
import os
from typing import Optional


class DataGenerator:
    """Generate random data for form filling."""
    
    @staticmethod
    def random_zip_code() -> str:
        """Return hardcoded ZIP code."""
        return "90210"
    
    @staticmethod
    def random_birthday() -> str:
        """Return hardcoded birthday in MMDDYYYY format."""
        return "02022003"
    
    @staticmethod
    def random_age_range() -> tuple[int, int]:
        """Generate a random age range."""
        min_age = random.randint(18, 35)
        max_age = random.randint(min_age + 5, 55)
        return min_age, max_age
    
    @staticmethod
    def random_string(length: int = 10) -> str:
        """Generate a random string."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class PathHelper:
    """Helper functions for file path operations."""
    
    @staticmethod
    def resolve_path(path: str) -> Optional[str]:
        """
        Resolve a file path to absolute path.
        Returns None if file doesn't exist.
        """
        if not path:
            return None
            
        if os.path.exists(path):
            return os.path.abspath(path)
        
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
        
        return None
    
    @staticmethod
    def ensure_directory(path: str) -> str:
        """Ensure directory exists, create if it doesn't."""
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        return path


class Logger:
    """Simple logger for automation steps."""
    
    @staticmethod
    def info(message: str, prefix: str = "INFO"):
        """Log info message."""
        print(f"[{prefix}] {message}")
    
    @staticmethod
    def success(message: str):
        """Log success message."""
        Logger.info(message, "SUCCESS")
    
    @staticmethod
    def error(message: str):
        """Log error message."""
        Logger.info(message, "ERROR")
    
    @staticmethod
    def warning(message: str):
        """Log warning message."""
        Logger.info(message, "WARNING")
    
    @staticmethod
    def debug(message: str):
        """Log debug message."""
        Logger.info(message, "DEBUG")
    
    @staticmethod
    def step(message: str):
        """Log a step in the automation process."""
        Logger.info(message, "STEP")
