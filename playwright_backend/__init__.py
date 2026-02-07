"""
Playwright-based Match.com automation backend.

This package provides a modular, scalable, and flexible automation framework
for Match.com registration using Playwright instead of Selenium.

Key improvements over Selenium:
- Better React support with automatic waiting
- More reliable element interactions
- Async/await for better performance
- Built-in network interception capabilities
- More stable cross-browser support

Usage:
    from playwright_backend import run_automation
    
    await run_automation(
        email="user@example.com",
        password="SecurePassword123!",
        name="John",
        region="us",
        headless=False
    )

Or use the class directly for more control:
    from playwright_backend import MatchAutomator, BrowserConfig
    
    config = BrowserConfig(headless=True, slow_mo=100)
    async with MatchAutomator(config) as automator:
        await automator.run_registration(...)
"""

from .automator import MatchAutomator, run_automation
from .config import Config, BrowserConfig, RegionConfig
from .utils import DataGenerator, PathHelper, Logger
from .page_interactor import PageInteractor

__version__ = "1.0.0"
__all__ = [
    "MatchAutomator",
    "run_automation",
    "Config",
    "BrowserConfig",
    "RegionConfig",
    "DataGenerator",
    "PathHelper",
    "Logger",
    "PageInteractor"
]
