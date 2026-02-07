"""
Registration flow handlers for Match.com automation.
Each handler manages a specific step in the registration process.
"""

import asyncio
import random
from typing import Optional
from playwright.async_api import Page
from .page_interactor import PageInteractor
from .config import Config
from .utils import DataGenerator, PathHelper, Logger


class LandingFormHandler:
    """Handles the initial landing form."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self) -> bool:
        """Handle the landing form step."""
        self.logger.step("Handling Landing Form")
        
        selectors = self.config.SELECTORS["landing_form"]
        
        # Gender selection
        gender_select = await self.interactor.wait_and_get_element(selectors["gender_select"])
        if gender_select:
            await self.interactor.select_dropdown(
                gender_select, 
                index=random.randint(1, 4),
                description="Gender preference"
            )
            await asyncio.sleep(0.5)
        
        # Age range selection
        min_age_select = await self.interactor.wait_and_get_element(selectors["min_age"])
        max_age_select = await self.interactor.wait_and_get_element(selectors["max_age"])
        
        if min_age_select and max_age_select:
            min_age, max_age = DataGenerator.random_age_range()
            await self.interactor.select_dropdown(min_age_select, value=str(min_age), description="Min age")
            await asyncio.sleep(0.3)
            await self.interactor.select_dropdown(max_age_select, value=str(max_age), description="Max age")
            await asyncio.sleep(0.3)
        
        # ZIP code with typeahead
        zip_input = await self.interactor.wait_and_get_element(selectors["zip_input"])
        if zip_input:
            await self.interactor.dismiss_overlays()
            
            # Type partial ZIP to trigger suggestions
            partial_zip = "90" 
            self.logger.info(f"Typing partial ZIP: {partial_zip}", "ZIP")
            await zip_input.click()
            await zip_input.fill("") # Clear first
            await zip_input.type(partial_zip, delay=100)
            await asyncio.sleep(2)  # Wait for typeahead suggestions
            
            # Try to click first suggestion
            try:
                # Prioritize suggestions based on common Match.com patterns
                suggestion_selectors = selectors["zip_suggestions"]
                suggestion = await self.interactor.wait_and_get_element(
                    suggestion_selectors, 
                    timeout=5000
                )
                
                if suggestion:
                    await self.interactor.smart_click(suggestion, "First ZIP suggestion", force=True)
                else:
                    self.logger.warning("No ZIP suggestions found, pressing Enter")
                    await zip_input.press("Enter")
            except Exception as e:
                self.logger.debug(f"ZIP suggestion error: {e}")
                await zip_input.press("Enter")
            
            await asyncio.sleep(1)
        
        # Submit the form
        return await self.interactor.find_and_click_button(selectors["submit_buttons"])


class BirthdayHandler:
    """Handles the birthday input step."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self) -> bool:
        """Handle the birthday step."""
        self.logger.step("Handling Birthday Input")
        
        selectors = self.config.SELECTORS["registration"]
        
        # Wait for birthday input
        birthday_input = await self.interactor.wait_and_get_element(
            selectors["birthday_input"],
            timeout=self.config.TIMEOUTS["long"]
        )
        
        if not birthday_input:
            self.logger.warning("Birthday input not found")
            return False
        
        # Dismiss any cookie overlays
        await self.interactor.dismiss_overlays()
        
        # Fill birthday
        birthday = DataGenerator.random_birthday()
        await self.interactor.smart_fill(birthday_input, birthday, "Birthday", simulate_typing=True)
        await asyncio.sleep(1)
        
        # Try specific submit button first
        try:
            submit_btn = self.page.locator(selectors["birthday_submit"][0]).first
            if await submit_btn.is_visible(timeout=2000):
                return await self.interactor.smart_click(submit_btn, "Birthday submit")
        except Exception:
            pass
        
        # Fallback to generic buttons
        return await self.interactor.find_and_click_button(
            self.config.BUTTON_TEXTS["confirm"] + self.config.BUTTON_TEXTS["continue"]
        )


class NameHandler:
    """Handles the name input step."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self, name: str) -> bool:
        """Handle the name step."""
        self.logger.step("Handling Name Input")
        
        selectors = self.config.SELECTORS["registration"]
        
        name_input = await self.interactor.wait_and_get_element(
            selectors["name_input"],
            timeout=self.config.TIMEOUTS["medium"]
        )
        
        if not name_input:
            self.logger.warning("Name input not found")
            return False
        
        await self.interactor.smart_fill(name_input, name, "Name", simulate_typing=True)
        await asyncio.sleep(1)
        
        return await self.interactor.find_and_click_button(
            self.config.BUTTON_TEXTS["confirm"] + self.config.BUTTON_TEXTS["continue"]
        )


class EmailHandler:
    """Handles the email input step."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self, email: str) -> bool:
        """Handle the email step."""
        self.logger.step("Handling Email Input")
        
        selectors = self.config.SELECTORS["registration"]
        
        email_input = await self.interactor.wait_and_get_element(
            selectors["email_input"],
            timeout=self.config.TIMEOUTS["medium"]
        )
        
        if not email_input:
            self.logger.warning("Email input not found")
            return False
        
        await self.interactor.smart_fill(email_input, email, "Email", simulate_typing=True)
        await asyncio.sleep(1)
        
        return await self.interactor.find_and_click_button(
            self.config.BUTTON_TEXTS["confirm"] + self.config.BUTTON_TEXTS["continue"]
        )


class PasswordHandler:
    """Handles the password input step."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self, password: str) -> bool:
        """Handle the password step."""
        self.logger.step("Handling Password Input")
        
        selectors = self.config.SELECTORS["registration"]
        
        password_input = await self.interactor.wait_and_get_element(
            selectors["password_input"],
            timeout=self.config.TIMEOUTS["medium"]
        )
        
        if not password_input:
            self.logger.warning("Password input not found")
            return False
        
        await self.interactor.smart_fill(password_input, password, "Password", simulate_typing=True)
        await asyncio.sleep(1)
        
        return await self.interactor.find_and_click_button(
            self.config.BUTTON_TEXTS["confirm"] + 
            self.config.BUTTON_TEXTS["submit"] + 
            self.config.BUTTON_TEXTS["continue"]
        )


class PhotoUploadHandler:
    """Handles photo upload step."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self, photo_path: str) -> bool:
        """Handle photo upload with specific ID targeting and React bypass."""
        self.logger.step(f"Automating Photo Upload: {photo_path}")
        
        # Resolve photo path
        resolved_path = PathHelper.resolve_path(photo_path)
        if not resolved_path:
            self.logger.warning(f"Photo not found at {photo_path}")
            return False
        
        selectors = self.config.SELECTORS["photo_upload"]
        
        # Priority selectors including the specific ID provided by the user
        input_selectors = ["#photo-to-upload", "input#photo-to-upload"] + selectors["file_input"]
        
        for selector in input_selectors:
            try:
                # 1. Wait for element to exist (even if hidden)
                file_input = self.page.locator(selector).first
                if await file_input.count() == 0:
                    continue

                self.logger.info(f"Targeting photo input: {selector}", "PHOTO")

                # 2. Force visibility and interaction via JS
                await self.page.evaluate("""(sel) => {
                    const el = document.querySelector(sel);
                    if (el) {
                        el.style.display = 'block';
                        el.style.visibility = 'visible';
                        el.style.opacity = '1';
                        el.style.position = 'fixed';
                        el.style.top = '10px';
                        el.style.left = '10px';
                        el.style.width = '100px';
                        el.style.height = '100px';
                        el.style.zIndex = '100000';
                        el.removeAttribute('hidden');
                        // Also try to find parent label or div and make it visible
                        let parent = el.parentElement;
                        while (parent && parent.tagName !== 'BODY') {
                            parent.style.display = 'block';
                            parent.style.visibility = 'visible';
                            parent = parent.parentElement;
                        }
                    }
                }""", selector)

                # 2.5 Ensure the element is focused/clicked to awaken React listeners
                try:
                    await file_input.focus()
                    await file_input.click(force=True, timeout=2000)
                except:
                    pass

                # 3. Upload the file
                self.logger.info("Setting input files...", "PHOTO")
                await file_input.set_input_files(resolved_path)
                
                # 4. Comprehensive React event dispatch (Safe for file inputs)
                await self.page.evaluate("""(sel) => {
                    const el = document.querySelector(sel);
                    if (el) {
                        // For file inputs, we MUST NOT try to set .value via prototype setter
                        // Standard event sequence that React/Angular/Vue usually listen for
                        const events = ['input', 'change', 'blur'];
                        events.forEach(eventName => {
                            const event = new Event(eventName, { 
                                bubbles: true, 
                                cancelable: true,
                                composed: true 
                            });
                            el.dispatchEvent(event);
                        });
                        
                        // Additional specific check for React 16+ 
                        // sometimes it needs the 'change' event to be specifically a UIEvent or similar
                        const changeEvent = document.createEvent('HTMLEvents');
                        changeEvent.initEvent('change', true, true);
                        el.dispatchEvent(changeEvent);
                    }
                }""", selector)
                
                self.logger.success("File uploaded to input and events dispatched")
                await asyncio.sleep(3)  # Short wait for React state syncd click the finalize button (Save/Apply/Upload)
                # Specifically targeting the 'Adjust your photo' screen provided by the user
                self.logger.info("Waiting for finalize/cropper button to appear...", "PHOTO")
                
                # Extended list of selectors, prioritized for the specific section reported
                finalize_selectors = [
                    "section.css-uyx57 button.css-44m5wj",  # Exact match for user's HTML
                    "button.css-44m5wj",
                    "button:has-text('Upload')", 
                    "button:has(span:text('Upload'))",
                    "button[data-sourcedesc='04c57f']"       # Specific data attribute from user's HTML
                ] + selectors["finalize_button"]
                
                # Try multiple times with a short sleep between attempts
                for attempt in range(8): # Increased retry count
                    for f_selector in finalize_selectors:
                        try:
                            # Use a broader locator to find the button even if nested
                            btn = self.page.locator(f_selector).first
                            
                            if await btn.is_visible():
                                self.logger.info(f"Finalize button found via {f_selector}, checking state...", "PHOTO")
                                
                                # Check if button is disabled via attribute (Match.com specific)
                                is_disabled = await btn.get_attribute("data-uia-button-disabled")
                                if is_disabled == "true":
                                    self.logger.debug("Button is technically visible but disabled, waiting...")
                                    continue

                                # Force interaction: Click AND dispatch event to be safe
                                self.logger.info("Clicking Upload...", "PHOTO")
                                await self.interactor.smart_click(btn, "Finalize upload", force=True)
                                
                                # Backup: Dispatch click via JS in case React swallowed the Playwright click
                                await self.page.evaluate("(sel) => { const b = document.querySelector(sel); if(b) b.click(); }", f_selector)
                                
                                await asyncio.sleep(4)
                                
                                # If we are still on the same screen, the click might have failed or processing is slow
                                if "photo_upload" in self.page.url:
                                    self.logger.debug("Still on photo page, trying one more click...")
                                    continue
                                
                                return True
                        except Exception:
                            continue
                    
                    self.logger.debug(f"Adjust/Upload button not ready, retrying... (attempt {attempt+1}/8)")
                    await asyncio.sleep(1.5)
                
                # If we made it this far, maybe it auto-submitted or we need to skip/continue
                self.logger.info("Finalize button not found, checking for generic Continue/Next...", "PHOTO")
                if await self.interactor.find_and_click_button(self.config.get_all_button_texts()):
                    return True
                    
            except Exception as e:
                self.logger.debug(f"Upload attempt failed for {selector}: {e}")
                continue
        
        # Final fallback: If input found but upload failed, try clicking the label
        try:
            label = self.page.locator("label[for='photo-to-upload']").first
            if await label.is_visible(timeout=2000):
                self.logger.info("Clicking label fallback", "PHOTO")
                async with self.page.expect_file_chooser(timeout=5000) as fc_info:
                    await label.click()
                    file_chooser = await fc_info.value
                    await file_chooser.set_files(resolved_path)
                    
                    # Also wait for the button here
                    await asyncio.sleep(5)
                    await self.interactor.find_and_click_button(["Upload", "Save", "Continue"])
                    return True
        except Exception:
            pass
            
        return False


class ProfileQuestionsHandler:
    """Handles post-registration profile questions."""
    
    def __init__(self, page: Page, interactor: PageInteractor):
        self.page = page
        self.interactor = interactor
        self.config = Config()
        self.logger = Logger()
    
    async def handle(self, max_duration: int = 300) -> None:
        """
        Handle profile questions loop.
        
        Args:
            max_duration: Maximum duration in seconds
        """
        self.logger.step("Handling Profile Questions")
        
        start_time = asyncio.get_event_loop().time()
        selectors = self.config.SELECTORS["profile_questions"]
        
        # Track photo upload pages we've already processed to avoid infinite loops
        processed_photo_urls = set()
        
        while (asyncio.get_event_loop().time() - start_time) < max_duration:
            try:
                # URL Flow Control: Check if current screen is known
                current_url = self.page.url
                base_url = current_url.split('?')[0].rstrip('/')
                is_known = any(base_url == known.split('?')[0].rstrip('/') for known in self.config.KNOWN_URLS)
                
                # Check if this is a photo upload screen
                if "photo_upload" in base_url or "photo-upload" in base_url:
                    # CRITICAL: Skip additional_photos entirely - just press Continue/Skip
                    if "photo_upload_additional_photos" in base_url:
                        self.logger.info("Additional photos screen - SKIPPING without upload...", "FLOW")
                        # Mark as processed immediately to prevent re-entry
                        processed_photo_urls.add(base_url)
                        # Just click Skip/Continue without opening upload dialog
                        if await self.interactor.find_and_click_button(["Skip", "skip", "Continue", "Next"]):
                            self.logger.success("Skipped additional photos screen")
                            await asyncio.sleep(2)
                        else:
                            await asyncio.sleep(2)
                        continue
                    
                    # If we already uploaded here, don't do it again - try to move forward
                    if base_url in processed_photo_urls:
                        self.logger.info(f"Already processed photo upload for {base_url}, looking for continue button...", "FLOW")
                        if await self.interactor.find_and_click_button(self.config.BUTTON_TEXTS["continue"] + ["Next", "Continue", "Skip"]):
                            await asyncio.sleep(2)
                        else:
                            # If no button, maybe it's still processing, just wait a bit
                            await asyncio.sleep(3)
                        continue

                    self.logger.info(f"Photo upload screen detected ({base_url}), handing off...", "FLOW")
                    from .handlers import PhotoUploadHandler
                    photo_handler = PhotoUploadHandler(self.page, self.interactor)
                    
                    # Get photo path from automator if possible, otherwise use default
                    photo_path = r"C:\Programming\Projects\04_ARCHIVE\match-extension\automation-extension\assets\img.png"
                    
                    upload_success = await photo_handler.handle(photo_path)
                    if upload_success:
                        processed_photo_urls.add(base_url)
                        self.logger.success(f"Photo upload handled for {base_url}")
                    
                    await asyncio.sleep(2)
                    continue

                if not is_known:
                    self.logger.info(f"Unknown screen detected: {base_url}", "FLOW")
                    self.logger.info("Attempting to skip unknown screen...", "FLOW")
                    
                    # Try skip/continue buttons specifically for unknown screens
                    skip_texts = self.config.BUTTON_TEXTS["skip"] + self.config.BUTTON_TEXTS["continue"]
                    if await self.interactor.find_and_click_button(skip_texts):
                        await asyncio.sleep(2)
                        continue
                else:
                    self.logger.info(f"On known screen: {base_url}", "FLOW")

                # Get page text for context
                page_text = await self.page.text_content("body")
                page_text_lower = page_text.lower() if page_text else ""
                
                # Special handling for ethnicities (must select before continue)
                if "self_ethnicities" in base_url:
                    self.logger.info("Ethnicities screen detected, ensuring selection...", "FLOW")
                    ethnicity_list = self.page.locator("ul.css-1ls30xe li")
                    try:
                        options = await ethnicity_list.all()
                        visible_options = [opt for opt in options if await opt.is_visible()]
                        if visible_options:
                            chosen = random.choice(visible_options)
                            await self.interactor.smart_click(chosen, "Ethnicity selection")
                            await asyncio.sleep(1)
                    except Exception as e:
                        self.logger.debug(f"Ethnicity selection error: {e}")
                
                # Special handling for Core Values screen
                if "core_values" in base_url:
                    self.logger.info("Core Values screen detected, skipping with 'I'd rather not say'...", "FLOW")
                    if await self.interactor.find_and_click_button(["I'd rather not say", "I’d rather not say"]):
                        await asyncio.sleep(2)
                        continue

                # Special handling for Celebration screen
                if "celebration" in base_url:
                    self.logger.info("Celebration screen detected, clicking 'Show me how'...", "FLOW")
                    # Try test-id first then text
                    if await self.interactor.smart_click(self.page.locator("[data-testid='celebration-advance-button']"), "Celebration button"):
                        await asyncio.sleep(2)
                        continue
                    if await self.interactor.find_and_click_button(["Show me how"]):
                        await asyncio.sleep(2)
                        continue

                # Special handling for Next Steps screen
                if "nextsteps" in base_url:
                    self.logger.info("Next Steps screen detected, clicking 'No, thanks'...", "FLOW")
                    # Try test-id first then text
                    if await self.interactor.smart_click(self.page.locator("[data-testid='continue-with-free-cta']"), "Next steps button"):
                        await asyncio.sleep(2)
                        continue
                    if await self.interactor.find_and_click_button(["No, thanks", "No thanks"]):
                        await asyncio.sleep(2)
                        continue

                # Normal Flow Logic: Only answer questions on known screens 
                if is_known:
                    # Handle dropdowns
                    if any(keyword in page_text_lower for keyword in ["kids", "children", "education", "degree", "smoke"]):
                        select_elements = await self.page.locator("select").all()
                        if select_elements:
                            for select_elem in select_elements:
                                if await select_elem.is_visible():
                                    await self.interactor.select_dropdown(
                                        select_elem,
                                        index=random.randint(1, 4),
                                        description="Profile question"
                                    )
                                    await asyncio.sleep(0.5)
                    
                    # Handle radio buttons and checkboxes
                    all_selectors = selectors["radio_buttons"] + selectors["checkboxes"]
                    if "self_ethnicities" not in base_url:
                        all_selectors += selectors["list_items"]
                    
                    # SAFETY CHECK: Don't click generic labels on photo screens if they missed the handoff
                    if "photo" not in base_url:
                        for selector in all_selectors:
                            try:
                                options = await self.page.locator(selector).all()
                                visible_options = []
                                for opt in options:
                                    if await opt.is_visible():
                                        # Filter out those "profile you might like" labels
                                        text = await opt.inner_text()
                                        if "profile you might like" in text.lower():
                                            continue
                                        visible_options.append(opt)
                                
                                if visible_options:
                                    chosen = random.choice(visible_options)
                                    await self.interactor.smart_click(chosen, "Profile option")
                                    await asyncio.sleep(1)
                                    break
                            except Exception:
                                continue
                
                # Check for "Continue", "That's Me", etc.
                all_button_texts = self.config.get_all_button_texts()
                if await self.interactor.find_and_click_button(all_button_texts):
                    await asyncio.sleep(2)
                else:
                    # Check if we reached dashboard or home (registration complete)
                    current_url_lower = self.page.url.lower()
                    if "dashboard" in current_url_lower or "/home" in current_url_lower or self.page.url == "https://www.match.com/home":
                        self.logger.success(f"Reached completion page: {self.page.url}")
                        break
                    
                    # Log current position for debugging
                    self.logger.debug(f"No button found on {base_url}, waiting...")
                    await asyncio.sleep(2)
                    
            except Exception as e:
                self.logger.debug(f"Profile questions loop error: {e}")
                await asyncio.sleep(2)
