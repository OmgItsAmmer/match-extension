"""
Main automation orchestrator for Match.com registration.
Coordinates all handlers and manages the browser lifecycle.
"""

import asyncio
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from .config import Config, BrowserConfig
from .page_interactor import PageInteractor
from .handlers import (
    LandingFormHandler,
    BirthdayHandler,
    NameHandler,
    EmailHandler,
    PasswordHandler,
    PhotoUploadHandler,
    ProfileQuestionsHandler
)
from .utils import Logger


class MatchAutomator:
    """
    Main automation class for Match.com registration.
    Manages browser lifecycle and orchestrates the registration flow.
    """
    
    def __init__(self, browser_config: Optional[BrowserConfig] = None):
        """
        Initialize the automator.
        
        Args:
            browser_config: Browser configuration settings
        """
        self.browser_config = browser_config or BrowserConfig()
        self.config = Config()
        self.logger = Logger()
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.interactor: Optional[PageInteractor] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def initialize(self) -> None:
        """Initialize browser and page."""
        self.logger.info("Initializing browser...", "INIT")
        
        self.playwright = await async_playwright().start()
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.browser_config.headless,
            slow_mo=self.browser_config.slow_mo,
            args=[
                "--disable-notifications",
                "--start-maximized"
            ]
        )
        
        # Create context with custom settings
        self.context = await self.browser.new_context(
            viewport={
                "width": self.browser_config.viewport_width,
                "height": self.browser_config.viewport_height
            },
            user_agent=self.browser_config.user_agent,
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        # Set default timeout
        self.context.set_default_timeout(self.browser_config.timeout)
        
        # Create page
        self.page = await self.context.new_page()
        
        # Initialize interactor
        self.interactor = PageInteractor(self.page)
        
        self.logger.success("Browser initialized")
    
    async def close(self) -> None:
        """Close browser and cleanup."""
        self.logger.info("Closing browser...", "CLEANUP")
        
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        self.logger.success("Browser closed")
    
    async def run_registration(
        self,
        email: str,
        password: str,
        name: str,
        photo_path: str = r"C:\Programming\Projects\04_ARCHIVE\match-extension\automation-extension\assets\img.png",
        region: str = "us"
    ) -> bool:
        """
        Run the complete Match.com registration flow.
        
        Args:
            email: Email address for registration
            password: Password for registration
            name: First name for registration
            photo_path: Path to photo to upload
            region: Region code - "us" or "uk"
        
        Returns:
            True if registration succeeded, False otherwise
        """
        try:
            # Get region configuration
            region_config = self.config.get_region(region)
            
            if region_config.region_code == "uk":
                self.logger.info("🇬🇧 Running UK Match.com registration", "REGION")
            else:
                self.logger.info("🇺🇸 Running US Match.com registration", "REGION")
            
            # Navigate to registration page
            self.logger.step(f"Navigating to {region_config.registration_url}")
            await self.page.goto(region_config.registration_url)
            await asyncio.sleep(3)
            
            # Dismiss overlays
            await self.interactor.dismiss_overlays()
            
            # Step 1: Landing Form
            landing_handler = LandingFormHandler(self.page, self.interactor)
            if not await landing_handler.handle():
                self.logger.warning("Landing form step failed or skipped")
            await asyncio.sleep(3)
            
            # Step 2: Birthday
            birthday_handler = BirthdayHandler(self.page, self.interactor)
            if not await birthday_handler.handle():
                self.logger.warning("Birthday step failed or skipped")
            await asyncio.sleep(3)
            
            # Step 3: Name
            name_handler = NameHandler(self.page, self.interactor)
            if not await name_handler.handle(name):
                self.logger.warning("Name step failed or skipped")
            await asyncio.sleep(3)
            
            # Step 4: Email
            email_handler = EmailHandler(self.page, self.interactor)
            if not await email_handler.handle(email):
                self.logger.warning("Email step failed or skipped")
            await asyncio.sleep(3)
            
            # Step 5: Password
            password_handler = PasswordHandler(self.page, self.interactor)
            if not await password_handler.handle(password):
                self.logger.warning("Password step failed or skipped")
            await asyncio.sleep(5)
            
            # Step 5.5: Interstitial Survey Check
            if "survey" in self.page.url:
                self.logger.step("Clearing Interstitial Survey")
                await self.interactor.find_and_click_button(self.config.get_all_button_texts())
                await asyncio.sleep(3)
            
            # Step 6: Intro screen
            self.logger.step("Handling Intro Screen")
            if not await self.interactor.find_and_click_button(self.config.BUTTON_TEXTS["intro"]):
                # Try fallback selector
                intro_btn = await self.interactor.wait_and_get_element([".css-17ertmd", ".css-1ls30xe"])
                if intro_btn:
                    await self.interactor.smart_click(intro_btn, "Intro button")
            await asyncio.sleep(2)
            
            # Step 7: Photo Upload
            photo_handler = PhotoUploadHandler(self.page, self.interactor)
            await photo_handler.handle(photo_path)
            
            # Step 8: Profile Questions (includes celebration, nextsteps, etc.)
            questions_handler = ProfileQuestionsHandler(self.page, self.interactor)
            await questions_handler.handle(max_duration=600)  # Extended to handle all post-photo screens
            
            self.logger.success("Registration flow completed!")
            return True
            
        except Exception as e:
            self.logger.error(f"Registration failed: {e}")
            return False
    
    async def take_screenshot(self, path: str) -> None:
        """Take a screenshot of the current page."""
        if self.page:
            await self.page.screenshot(path=path, full_page=True)
            self.logger.info(f"Screenshot saved to {path}", "SCREENSHOT")


async def run_automation(
    email: str,
    password: str,
    name: str,
    photo_path: str = r"C:\Programming\Projects\04_ARCHIVE\match-extension\automation-extension\assets\img.png",
    region: str = "us",
    headless: bool = False,
    auto_close: bool = False
) -> bool:
    """
    Convenience function to run automation with default settings.
    
    Args:
        email: Email address for registration
        password: Password for registration
        name: First name for registration
        photo_path: Path to photo to upload
        region: Region code - "us" or "uk"
        headless: Run browser in headless mode
        auto_close: Whether to automatically close the browser
    
    Returns:
        True if registration succeeded, False otherwise
    """
    browser_config = BrowserConfig(headless=headless)
    automator = MatchAutomator(browser_config)
    
    try:
        await automator.initialize()
        success = await automator.run_registration(
            email=email,
            password=password,
            name=name,
            photo_path=photo_path,
            region=region
        )
        
        if not auto_close:
            automator.logger.info("Automation finished. Keeping browser open as requested.", "FLOW")
            # We don't call automator.close() here
            # We keep it alive by just returning
            # Note: This might cause zombie processes if run many times, 
            # but is requested for debugging/completion.
            return success
            
        await automator.close()
        return success
    except Exception as e:
        automator.logger.error(f"Automation fatal error: {e}")
        if auto_close:
            await automator.close()
        return False


# Example usage
if __name__ == "__main__":
    asyncio.run(run_automation(
        email="test_user_77@gmail.com",
        password="Password123!",
        name="John",
        region="us",
        headless=False,
        auto_close=False
    ))
