import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MatchAutomator:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def delay(self, ms=1000):
        time.sleep(ms / 1000)

    def find_element_safe(self, selectors, timeout=10):
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                return element
            except:
                continue
        return None

    def click_element(self, element, description="element"):
        try:
            # Wait for element to be clickable
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(element)
                )
            except:
                print(f"[CLICK] Element not immediately clickable, proceeding anyway...")
            
            # Scroll into view for visibility
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.delay(300)
            
            # Remove any overlays that might be blocking
            self.driver.execute_script("""
                // Remove common overlay elements
                var overlays = document.querySelectorAll('.overlay, .modal-backdrop, [class*="overlay"]');
                overlays.forEach(function(el) { el.style.display = 'none'; });
                
                // Ensure element is visible and clickable
                arguments[0].style.pointerEvents = 'auto';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.display = 'block';
            """, element)
            
            tag = element.tag_name
            text = (element.text or element.get_attribute("value") or "").strip()
            cls = element.get_attribute("class")
            
            log_msg = f"[CLICK] {description} (<{tag}> text='{text}' class='{cls}')"
            print(log_msg)
            
            # ALWAYS focus the element first
            try:
                self.driver.execute_script("arguments[0].focus();", element)
                self.delay(200)
                print(f"[CLICK] Focused element")
            except:
                pass
            
            # Strategy 1: ActionChains (most reliable for React)
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(element).pause(0.3).click().perform()
                print(f"[CLICK SUCCESS] ActionChains worked for {description}")
                self.delay(500)
                return True
            except Exception as e1:
                print(f"[CLICK] ActionChains failed: {e1}, trying Enter key...")
            
            # Strategy 2: Focus + Enter (works well for React buttons)
            try:
                element.send_keys(Keys.RETURN)
                print(f"[CLICK SUCCESS] Enter key worked for {description}")
                self.delay(500)
                return True
            except Exception as e2:
                print(f"[CLICK] Enter key failed: {e2}, trying Space key...")
            
            # Strategy 3: Focus + Space (alternative for buttons)
            try:
                element.send_keys(Keys.SPACE)
                print(f"[CLICK SUCCESS] Space key worked for {description}")
                self.delay(500)
                return True
            except Exception as e3:
                print(f"[CLICK] Space key failed: {e3}, trying regular click...")
            
            # Strategy 4: Regular click
            try:
                element.click()
                print(f"[CLICK SUCCESS] Regular click worked for {description}")
                self.delay(500)
                return True
            except Exception as e4:
                print(f"[CLICK] Regular click failed: {e4}, trying JS click...")
                
            # Strategy 5: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                print(f"[CLICK SUCCESS] JS click worked for {description}")
                self.delay(500)
                return True
            except Exception as e5:
                print(f"[CLICK] JS click failed: {e5}, trying event dispatch...")
                
            # Strategy 6: Dispatch multiple events (mousedown, mouseup, click)
            try:
                self.driver.execute_script("""
                    var element = arguments[0];
                    
                    // Dispatch mousedown
                    var mousedown = new MouseEvent('mousedown', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    element.dispatchEvent(mousedown);
                    
                    // Dispatch mouseup
                    var mouseup = new MouseEvent('mouseup', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    element.dispatchEvent(mouseup);
                    
                    // Dispatch click
                    var click = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    element.dispatchEvent(click);
                """, element)
                print(f"[CLICK SUCCESS] Full event sequence worked for {description}")
                self.delay(500)
                return True
            except Exception as e6:
                print(f"[CLICK] Event dispatch failed: {e6}")
                        
            return False
        except Exception as e:
            print(f"[CLICK ERROR] Failed to click {description}: {e}")
            return False

    def find_and_click_button(self, texts):
        """
        Aggressively find and click buttons matching any of the provided texts.
        Uses multiple strategies to ensure buttons are found and clicked.
        """
        print(f"[BUTTON SEARCH] Looking for buttons with texts: {texts}")
        
        # Strategy 1: Find ALL potentially clickable elements
        try:
            all_clickables = self.driver.find_elements(By.CSS_SELECTOR, 
                'button, '
                'input[type="submit"], '
                'input[type="button"], '
                '[role="button"], '
                'a, '
                '[role="link"], '
                'div[role="button"], '
                'span[role="button"], '
                'label, '
                '[data-testid*="button"], '
                '[data-testid*="submit"], '
                '[class*="button"], '
                '[class*="btn"], '
                '[class*="submit"]'
            )
            
            print(f"[BUTTON SEARCH] Found {len(all_clickables)} potentially clickable elements")
            
            # Strategy 2: Try exact and partial text matches
            for search_text in texts:
                search_lower = search_text.lower()
                print(f"[BUTTON SEARCH] Searching for: '{search_text}'")
                
                for element in all_clickables:
                    try:
                        # Skip if not visible
                        if not element.is_displayed():
                            continue
                        
                        # Get all possible text sources
                        element_text = (element.text or "").strip()
                        element_value = (element.get_attribute("value") or "").strip()
                        element_aria_label = (element.get_attribute("aria-label") or "").strip()
                        element_title = (element.get_attribute("title") or "").strip()
                        element_data_testid = (element.get_attribute("data-testid") or "").strip()
                        
                        # Combine all text sources
                        all_text = f"{element_text} {element_value} {element_aria_label} {element_title} {element_data_testid}".lower()
                        
                        # Check for match (case-insensitive partial match)
                        if search_lower in all_text:
                            print(f"[BUTTON MATCH] Found match! Text: '{element_text}', Value: '{element_value}', Aria: '{element_aria_label}'")
                            
                            # Try clicking the element
                            if self.click_element(element, f"Button '{search_text}'"):
                                return True
                            
                            # If direct click failed, try clicking parent
                            try:
                                parent = element.find_element(By.XPATH, "./..")
                                if self.click_element(parent, f"Parent of Button '{search_text}'"):
                                    return True
                            except:
                                pass
                                
                    except Exception as e:
                        # Silently continue to next element
                        continue
            
            # Strategy 3: XPath text-based search as fallback
            for search_text in texts:
                try:
                    # Try exact text match
                    xpath_exact = f"//*[text()='{search_text}']"
                    elements = self.driver.find_elements(By.XPATH, xpath_exact)
                    for elem in elements:
                        if elem.is_displayed():
                            print(f"[XPATH MATCH] Found exact match via XPath for '{search_text}'")
                            if self.click_element(elem, f"XPath Exact '{search_text}'"):
                                return True
                    
                    # Try contains match
                    xpath_contains = f"//*[contains(text(), '{search_text}')]"
                    elements = self.driver.find_elements(By.XPATH, xpath_contains)
                    for elem in elements:
                        if elem.is_displayed():
                            print(f"[XPATH MATCH] Found partial match via XPath for '{search_text}'")
                            if self.click_element(elem, f"XPath Contains '{search_text}'"):
                                return True
                                
                except Exception as e:
                    print(f"[XPATH ERROR] {e}")
                    continue
            
            # Strategy 4: SVG/Arrow Fallback for navigation
            if any(t.lower() in ["right arrow", "next", "continue"] for t in texts):
                try:
                    print("[SVG SEARCH] Looking for SVG navigation elements...")
                    arrow_selectors = [
                        'svg[id*="arrow"]',
                        'svg[class*="arrow"]',
                        '[data-testid*="arrow"]',
                        '[aria-label*="Next"]',
                        '[aria-label*="Continue"]'
                    ]
                    
                    for selector in arrow_selectors:
                        try:
                            arrows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for arrow in arrows:
                                if arrow.is_displayed():
                                    # Try to find clickable parent
                                    parent = arrow.find_element(By.XPATH, "./ancestor::button | ./ancestor::*[role='button'] | ./..")
                                    if self.click_element(parent, "SVG Arrow Parent"):
                                        return True
                        except:
                            continue
                except Exception as e:
                    print(f"[SVG ERROR] {e}")
                    
        except Exception as e:
            print(f"[BUTTON SEARCH ERROR] {e}")
        
        print(f"[BUTTON SEARCH] No matching button found for any of: {texts}")
        return False

    def simulate_interaction(self, element, value):
        try:
            self.click_element(element, "Input Field Focus")
            
            # React-friendly clearing
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
            
            for char in value:
                element.send_keys(char)
                self.delay(random.randint(50, 150))
            element.send_keys(Keys.TAB)
        except Exception as e:
            print(f"Interaction error: {e}")

    def get_random_zip(self):
        return str(random.randint(10000, 99999))

    def get_random_birthday(self):
        day = str(random.randint(1, 28)).zfill(2)
        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(1985, 2000))
        return f"{month}{day}{year}"

    def handle_profile_questions(self):
        print("Handling Post-Login Profile Questions...")
        timeout = time.time() + 300 # 5 minutes max
        while time.time() < timeout:
            try:
                page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
                
                # Kids
                if 'kids' in page_text or 'children' in page_text:
                    selects = self.driver.find_elements(By.TAG_NAME, 'select')
                    if selects:
                        Select(selects[0]).select_by_value(str(random.randint(1, 2)))
                        self.delay(500)
                
                # Education
                if 'education' in page_text or 'degree' in page_text:
                    selects = self.driver.find_elements(By.TAG_NAME, 'select')
                    if selects:
                        Select(selects[0]).select_by_value(str(random.randint(2, 3)))
                        self.delay(500)

                # Smoke
                if 'smoke' in page_text:
                    selects = self.driver.find_elements(By.TAG_NAME, 'select')
                    if selects:
                        Select(selects[0]).select_by_value("1")
                        self.delay(500)

                # Check for Radio Buttons, Fieldset Options, or List Items (Ethnicities)
                options = self.driver.find_elements(By.CSS_SELECTOR, 'button[role="radio"], .radio-button, fieldset.css-0 label, fieldset.css-0 input[type="radio"], fieldset.css-0 input[type="checkbox"], ul.css-1ls30xe li')
                if options:
                    # Filter for visible ones
                    visible_options = [o for o in options if o.is_displayed()]
                    if visible_options:
                        self.click_element(random.choice(visible_options), "Random Profile Option/Ethnicity")
                        self.delay(1000)

                # Unified button search for all regions
                if self.find_and_click_button(['continue', 'Continue', 'Next', 'Save', 'skip', 'Skip', 'Skip for now', 'upload photo', 'Upload photo', "That's Right", "That's right", "That's me", "That's Me", "That's the one", "That's The One", 'Confirm', 'Join now', 'Start now', 'Done']):
                    self.delay(2000)
                else:
                    if self.handle_special_pages():
                        self.delay(2000)
                        continue
                    
                    # Check if we are on the dashboard
                    if "dashboard" in self.driver.current_url:
                        print("Reached dashboard, automation finished.")
                        break
                    
                    self.delay(2000)
            except Exception as e:
                print(f"Loop error: {e}")
                self.delay(2000)

    def handle_photo_upload(self, photo_path):
        print(f"Handling Photo Upload with path: {photo_path}")
        if not os.path.exists(photo_path):
            abs_path = os.path.abspath(photo_path)
            if not os.path.exists(abs_path):
                print(f"Photo not found at {photo_path} or {abs_path}, skipping upload.")
                return
            photo_path = abs_path
        else:
            photo_path = os.path.abspath(photo_path)

        # 1. Find the file input - Match often hides it
        file_input = self.find_element_safe([
            'input[type="file"]', 
            'input[name="photo"]',
            '#photo-to-upload',
            'input[accept*="image"]'
        ], timeout=20)

        if file_input:
            print("Found file input, attempting upload...")
            try:
                # Force visibility via JS in case it's hidden/styled
                self.driver.execute_script(
                    "arguments[0].style.display = 'block'; "
                    "arguments[0].style.visibility = 'visible'; "
                    "arguments[0].style.opacity = '1'; "
                    "arguments[0].style.width = '100px'; "
                    "arguments[0].style.height = '100px';", 
                    file_input
                )
                self.delay(500)
                
                file_input.send_keys(photo_path)
                print("Send_keys successful, waiting for upload to process...")
                self.delay(5000) # Increased wait for upload to process
                
                # 2. Finalize/Submit the photo
                # Match often shows a "Save" or "Done" button after upload
                finalize_btn = self.find_element_safe([
                    '.css-44m5wj', 
                    'button[data-testid="save-photo"]',
                    'button[aria-label="Save"]',
                    '//button[contains(text(), "Save")]',
                    '//button[contains(text(), "Done")]',
                    '.css-d0wbpf' # Re-using celebration button class as it might be shared
                ], timeout=15)
                
                if finalize_btn:
                    self.click_element(finalize_btn, "Upload Finalize Button")
                    self.delay(3000)
                else:
                    print("Could not find finalize button, checking if we auto-proceeded...")
            except Exception as e:
                print(f"Error during file upload: {e}")
        else:
            print("File input not found. Checking if we need to click a trigger first.")
            # Sometimes you click a button to reveal the file input
            trigger = self.find_element_safe(['.css-17ertmd', '[aria-label="Add photo"]'])
            if trigger:
                self.click_element(trigger, "Photo Upload Trigger")
                self.delay(2000)
                # Recurse once if we clicked a trigger
                self.handle_photo_upload(photo_path)

    def handle_special_pages(self):
        url = self.driver.current_url
        if 'photo_upload_additional_photos' in url:
            print("On Additional Photos page...")
            return self.find_and_click_button(['Continue'])
            
        if '/create/celebration' in url:
            print("On Celebration page...")
            celebration_btn = self.find_element_safe(['.css-d0wbpf'])
            if celebration_btn:
                return self.click_element(celebration_btn, "Celebration Button")

        if '/create/intro' in url:
            print("On Intro page...")
            intro_btn = self.find_element_safe(['.css-17ertmd'])
            if intro_btn:
                return self.click_element(intro_btn, "Intro Page Button (.css-17ertmd)")
        return False

    def dismiss_overlays(self):
        print("Checking for overlays...")
        overlay_selectors = [
            '#onetrust-accept-btn-handler',
            '.onetrust-close-btn-handler',
            'button[id*="accept"]',
            '.close-button',
            '[aria-label="Close"]'
        ]
        for selector in overlay_selectors:
            try:
                btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                if btn.is_displayed():
                    self.click_element(btn, f"Overlay ({selector})")
                    self.delay(1000)
            except:
                continue
        
        # Absolute fallback: Remove OneTrust filter via JS if it still exists
        try:
            self.driver.execute_script("""
                var overlay = document.querySelector('.onetrust-pc-dark-filter');
                if (overlay) overlay.remove();
                var banner = document.querySelector('#onetrust-banner-sdk');
                if (banner) banner.remove();
            """)
        except:
            pass

    def run_registration(self, email, password, name, photo_path="automation-extension/assets/img.png", region="us"):
        """
        Run the Match.com registration automation.
        
        Args:
            email: Email address for registration
            password: Password for registration
            name: First name for registration
            photo_path: Path to photo to upload
            region: Region code - "us" for match.com or "uk" for uk.match.com
        """
        # Determine URL based on region
        if region.lower() == "uk":
            url = "https://uk.match.com/registration"
            print("🇬🇧 Running UK Match.com registration")
        else:
            url = "https://www.match.com/reg"
            print("🇺🇸 Running US Match.com registration")
        
        self.driver.get(url)
        self.delay(3000)
        
        self.dismiss_overlays()

        # 1. Landing Form
        gender_select = self.find_element_safe(['select#ggs_select', '[name="genderSeek"]'])
        if gender_select:
            print("Handling Landing Form (ggs_select)...")
            Select(gender_select).select_by_index(random.randint(1, 4)) 
            self.delay(500)

            # Age Selection
            min_age_select = self.find_element_safe(['select#desktop_landing_ages_lw'])
            max_age_select = self.find_element_safe(['select#desktop_landing_ages_hg'])
            if min_age_select and max_age_select:
                print("Selecting ages...")
                min_age = random.randint(18, 35)
                max_age = random.randint(min_age + 5, 55)
                Select(min_age_select).select_by_value(str(min_age))
                self.delay(300)
                Select(max_age_select).select_by_value(str(max_age))
                self.delay(300)
            
            # Zip Code (Typeahead)
            zip_input = self.find_element_safe(['.css-13wap6q', 'input#postalcode_input', '[name="postalCode"]'])
            if zip_input:
                print("Typing zip code...")
                zip_code = "90210"
                # Check for overlays before interaction
                self.dismiss_overlays()
                
                self.click_element(zip_input, "Zip Input Focus")
                
                zip_input.clear()
                for char in zip_code:
                    zip_input.send_keys(char)
                    self.delay(random.randint(100, 200))
                
                self.delay(2000) # Wait for typeahead results
                
                try:
                    suggestions = self.driver.find_elements(By.CSS_SELECTOR, '[role="listbox"] [role="option"], .suggestion-item, .typeahead-result, li[id*="suggestion"]')
                    if suggestions:
                        self.click_element(suggestions[0], "First Zip Suggestion")
                    else:
                        print("No suggestions found, pressing Tab + Enter...")
                        zip_input.send_keys(Keys.TAB)
                        self.delay(500)
                        zip_input.send_keys(Keys.ENTER)
                except Exception as e:
                    print(f"Zip suggestion error: {e}")
                    zip_input.send_keys(Keys.ENTER)
            
            self.delay(1000)
            # Unified login/start buttons
            self.find_and_click_button(['View Singles', 'Get Started', 'Continue', 'Start now', 'Begin', 'Start', 'Confirm'])
            self.delay(3000)

        # 2. Birthday Step
        print("Waiting for Birthday screen...")
        bday_input = self.find_element_safe(['input[data-testid="birthday"]', 'input[name="birthdate"]'], timeout=20)
        if bday_input:
            print("Detected Birthday screen.")
            
            # Step 2a: Dismiss privacy/cookie center first if present
            try:
                cookie_settings = self.driver.find_element(By.ID, "onetrust-pc-btn-handler")
                if cookie_settings.is_displayed():
                    self.click_element(cookie_settings, "Cookie Settings Button")
                    self.delay(1000)
            except:
                pass

            print("Filling Birthday...")
            birthday = self.get_random_birthday()
            self.simulate_interaction(bday_input, birthday)
            self.delay(1000)
            
            # Click the specific button requested
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, ".css-erglzy")
                self.click_element(submit_btn, "Birthday Submit Button (.css-erglzy)")
                self.delay(3000)
            except Exception as e:
                print(f"Specific birthday button not found, falling back: {e}")
                self.find_and_click_button(["That's Right", "That's right", "Next", "continue", "Continue", "Confirm", "Join now", "Start now"])
                self.delay(3000)

        # 3. Name Step
        print("Waiting for Name screen...")
        name_input = self.find_element_safe(['input[data-testid="firstName"]', 'input[name="firstName"]'], timeout=15)
        if name_input:
            print("Filling Name...")
            self.simulate_interaction(name_input, name)
            self.find_and_click_button(["That's me", "That's Me", "Next", "continue", "Continue", "Confirm", "That's Right", "That's right", "Join now", "Start now"])
            self.delay(3000)

        # 4. Email Step
        print("Waiting for Email screen...")
        email_input = self.find_element_safe(['input[name="email"]', 'input[type="email"]'], timeout=15)
        if email_input:
            print("Filling Email...")
            self.simulate_interaction(email_input, email)
            self.find_and_click_button(["That's the one", "That's The One", "Next", "continue", "Continue", "Confirm", "That's Right", "That's right", "Join now", "Start now"])
            self.delay(3000)

        # 5. Password Step
        print("Waiting for Password screen...")
        pwd_input = self.find_element_safe(['input[name="password"]', 'input[type="password"]'], timeout=15)
        if pwd_input:
            print("Filling Password...")
            self.simulate_interaction(pwd_input, password)
            self.find_and_click_button(["That's Right", "That's right", "Create Account", "Sign Up", "continue", "Continue", "Join now", "Register", "Start now", "Confirm"])
            self.delay(5000)

        # 6. Intro Screen
        print("Waiting for Intro screen...")
        if not self.find_and_click_button(["Click here to get started"]):
            # Fallback for SVG-only button on intro page
            intro_btn = self.find_element_safe(['.css-17ertmd'])
            if intro_btn:
                self.click_element(intro_btn, "Intro Page Button (.css-17ertmd)")
        self.delay(2000)

        # 7. Photo Upload & Questions
        self.handle_photo_upload(photo_path)
        self.handle_profile_questions()

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    automator = MatchAutomator()
    try:
        automator.run_registration("test_user_77@gmail.com", "Password123!", "John")
    finally:
        # automator.close()
        pass
