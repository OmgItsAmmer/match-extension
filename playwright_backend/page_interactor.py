"""
Page interaction handlers for Playwright automation.
Provides high-level methods for interacting with web pages.
"""

import asyncio
import random
from typing import List, Optional, Union
from playwright.async_api import Page, Locator, ElementHandle
from .config import Config
from .utils import Logger


class PageInteractor:
    """Handles all page interactions with smart waiting and error handling."""
    
    def __init__(self, page: Page):
        self.page = page
        self.config = Config()
        self.logger = Logger()
    
    async def wait_and_get_element(
        self, 
        selectors: List[str], 
        timeout: int = None,
        state: str = "visible"
    ) -> Optional[Locator]:
        """
        Try multiple selectors and return the first matching element.
        
        Args:
            selectors: List of CSS selectors to try
            timeout: Timeout in milliseconds
            state: Element state to wait for (visible, attached, hidden, detached)
        
        Returns:
            Locator if found, None otherwise
        """
        timeout = timeout or self.config.TIMEOUTS["medium"]
        
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                await locator.wait_for(state=state, timeout=timeout)
                return locator
            except Exception:
                continue
        
        return None
    
    async def smart_click(
        self, 
        element: Union[Locator, str], 
        description: str = "element",
        force: bool = False
    ) -> bool:
        """
        Click an element with multiple fallback strategies.
        Playwright handles React events much better than Selenium.
        
        Args:
            element: Locator or CSS selector
            description: Description for logging
            force: Force click even if element is not visible
        
        Returns:
            True if click succeeded, False otherwise
        """
        try:
            # Convert string selector to Locator
            if isinstance(element, str):
                element = self.page.locator(element).first
            
            # Log the click attempt
            tag = await element.evaluate("el => el.tagName")
            text = await element.text_content() or ""
            self.logger.info(f"Clicking {description} (<{tag}> text='{text.strip()}')", "CLICK")
            
            # Scroll into view
            await element.scroll_into_view_if_needed()
            await asyncio.sleep(0.3)
            
            # Strategy 1: Regular click (Playwright handles React events automatically)
            try:
                await element.click(timeout=5000, force=force)
                self.logger.success(f"Clicked {description}")
                await asyncio.sleep(0.5)
                return True
            except Exception as e:
                self.logger.debug(f"Regular click failed: {e}")
            
            # Strategy 2: Click with position (center of element)
            try:
                await element.click(position={"x": 0, "y": 0}, timeout=5000, force=force)
                self.logger.success(f"Clicked {description} with position")
                await asyncio.sleep(0.5)
                return True
            except Exception as e:
                self.logger.debug(f"Position click failed: {e}")
            
            # Strategy 3: Dispatch click event via JavaScript
            try:
                await element.dispatch_event("click")
                self.logger.success(f"Clicked {description} via dispatch")
                await asyncio.sleep(0.5)
                return True
            except Exception as e:
                self.logger.debug(f"Dispatch click failed: {e}")
            
            # Strategy 4: Press Enter key
            try:
                await element.press("Enter")
                self.logger.success(f"Pressed Enter on {description}")
                await asyncio.sleep(0.5)
                return True
            except Exception as e:
                self.logger.debug(f"Enter press failed: {e}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to click {description}: {e}")
            return False
    
    async def find_and_click_button(self, texts: List[str]) -> bool:
        """
        Find and click a button matching any of the provided texts.
        Uses Playwright's powerful text matching capabilities.
        
        Args:
            texts: List of text variations to search for
        
        Returns:
            True if button was found and clicked, False otherwise
        """
        self.logger.info(f"Searching for buttons with texts: {texts}", "BUTTON")
        
        for text in texts:
            try:
                # Playwright's get_by_role with text matching
                button = self.page.get_by_role("button", name=text, exact=False).first
                if await button.is_visible(timeout=2000):
                    if await self.smart_click(button, f"Button '{text}'"):
                        return True
            except Exception:
                pass
            
            # Try with get_by_text
            try:
                element = self.page.get_by_text(text, exact=False).first
                if await element.is_visible(timeout=2000):
                    if await self.smart_click(element, f"Element with text '{text}'"):
                        return True
            except Exception:
                pass
            
            # Try with locator and text filter
            try:
                button = self.page.locator("button").filter(has_text=text).first
                if await button.is_visible(timeout=2000):
                    # For ZIP code completion, sometimes we need to force the click
                    # if a transparent backdrop or dropdown is technically "covering" it
                    if await self.smart_click(button, f"Button containing '{text}'", force=True):
                        return True
            except Exception:
                pass
        
        # Fallback: Find all clickable elements and match text
        try:
            clickable_selectors = [
                "button",
                "input[type='submit']",
                "input[type='button']",
                "[role='button']",
                "a"
            ]
            
            for selector in clickable_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    try:
                        if not await element.is_visible():
                            continue
                        
                        # Get all text content
                        text_content = await element.text_content() or ""
                        aria_label = await element.get_attribute("aria-label") or ""
                        title = await element.get_attribute("title") or ""
                        value = await element.get_attribute("value") or ""
                        
                        combined_text = f"{text_content} {aria_label} {title} {value}".lower()
                        
                        # Check if any search text matches
                        for search_text in texts:
                            if search_text.lower() in combined_text:
                                self.logger.info(f"Found match: {text_content.strip()}", "BUTTON")
                                if await self.smart_click(element, f"Button '{search_text}'"):
                                    return True
                    except Exception:
                        continue
        except Exception as e:
            self.logger.debug(f"Fallback button search error: {e}")
        
        self.logger.warning(f"No matching button found for: {texts}")
        return False
    
    async def smart_fill(
        self, 
        element: Union[Locator, str], 
        value: str,
        description: str = "input",
        simulate_typing: bool = True
    ) -> bool:
        """
        Fill an input field with smart typing simulation.
        
        Args:
            element: Locator or CSS selector
            value: Value to fill
            description: Description for logging
            simulate_typing: Whether to simulate human typing
        
        Returns:
            True if fill succeeded, False otherwise
        """
        try:
            # Convert string selector to Locator
            if isinstance(element, str):
                element = self.page.locator(element).first
            
            self.logger.info(f"Filling {description} with value: {value}", "FILL")
            
            # Focus the element
            await element.focus()
            await asyncio.sleep(0.2)
            
            # Clear existing content
            await element.press("Control+A")
            await element.press("Backspace")
            await asyncio.sleep(0.2)
            
            if simulate_typing:
                # Type character by character with random delays
                for char in value:
                    await element.type(char, delay=random.randint(
                        self.config.DELAYS["typing_min"],
                        self.config.DELAYS["typing_max"]
                    ))
            else:
                # Fast fill
                await element.fill(value)
            
            # Trigger blur event to ensure React state updates
            await element.press("Tab")
            await asyncio.sleep(0.3)
            
            self.logger.success(f"Filled {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to fill {description}: {e}")
            return False
    
    async def select_dropdown(
        self, 
        element: Union[Locator, str], 
        value: Optional[str] = None,
        index: Optional[int] = None,
        description: str = "dropdown"
    ) -> bool:
        """
        Select an option from a dropdown.
        
        Args:
            element: Locator or CSS selector
            value: Value to select
            index: Index to select (if value not provided)
            description: Description for logging
        
        Returns:
            True if selection succeeded, False otherwise
        """
        try:
            # Convert string selector to Locator
            if isinstance(element, str):
                element = self.page.locator(element).first
            
            self.logger.info(f"Selecting from {description}", "SELECT")
            
            if value is not None:
                await element.select_option(value=value)
            elif index is not None:
                await element.select_option(index=index)
            else:
                # Select random option
                options = await element.locator("option").all()
                if len(options) > 1:
                    await element.select_option(index=random.randint(1, len(options) - 1))
            
            await asyncio.sleep(0.3)
            self.logger.success(f"Selected from {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to select from {description}: {e}")
            return False
    
    async def dismiss_overlays(self) -> None:
        """Dismiss any overlays, modals, or cookie banners."""
        self.logger.info("Checking for overlays...", "OVERLAY")
        
        overlay_selectors = self.config.SELECTORS["overlays"]["cookie_accept"] + \
                          self.config.SELECTORS["overlays"]["close_buttons"]
        
        for selector in overlay_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=2000):
                    await self.smart_click(element, f"Overlay ({selector})")
                    await asyncio.sleep(1)
            except Exception:
                continue
        
        # Remove overlay elements via JavaScript
        try:
            await self.page.evaluate("""
                () => {
                    const overlays = document.querySelectorAll(
                        '.onetrust-pc-dark-filter, #onetrust-banner-sdk, .modal-backdrop, [class*="overlay"]'
                    );
                    overlays.forEach(el => el.remove());
                }
            """)
        except Exception:
            pass
    
    async def wait_for_navigation(self, timeout: int = None) -> None:
        """Wait for page navigation to complete."""
        timeout = timeout or self.config.TIMEOUTS["medium"]
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            # Fallback to domcontentloaded
            await self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
