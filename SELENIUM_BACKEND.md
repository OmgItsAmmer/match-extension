# Selenium Backend Documentation

This file (`selenium_backend.py`) contains the `MatchAutomator` class, which is a specialized Selenium-based automation engine designed to handle account registration and profile setup on **Match.com**.

## Overview

The script automates the multi-step registration process, including handling dynamic forms, cookie banners, and profile-building questions. It is designed to be resilient by using "safe" element finding methods and fallbacks for interactions.

## Ultra-Aggressive Button Interaction

The `MatchAutomator` class implements a highly resilient system for finding and interacting with buttons, which is necessary to handle the complex, React-based UI of Match.com across different regions (US & UK).

### 🔍 How It Finds Buttons (`find_and_click_button`)

The search logic uses 4 distinct strategies to ensure no clickable element is missed:

1.  **Comprehensive CSS Search**: Lists all potentially clickable elements including `button`, `input[type="submit"]`, `[role="button"]`, `a`, `div[role="button"]`, `span[role="button"]`, `label`, and elements with classes containing "button" or "btn".
2.  **Multi-Attribute Text Matching**: For every candidate element, it extracts and checks:
    - Visible text (`.text`)
    - Input value (`.get_attribute("value")`)
    - Aria labels (`aria-label`)
    - Title attributes (`title`)
    - Test IDs (`data-testid`)
    Matches are case-insensitive and partial, ensuring that "Continue" matches "continue" or "Continue now".
3.  **XPath Fallback**: If standard attribute searches fail, it uses XPath to find elements containing specific text strings directly in the DOM tree (`//*[contains(text(), 'Text')]`).
4.  **SVG & Parent Detection**: Specifically looks for SVG icons (like right arrows) and attempts to click their parent or ancestor button elements if the icon itself isn't the primary click target.

### ⚡ How It Presses Buttons (`click_element`)

Finding the button is only half the battle. To ensure the click is registered by modern frameworks, the script executes 6 sequential strategies:

1.  **Wait & Prepare**:
    - Waits up to 5 seconds for the element to be "clickable".
    - Scrolls the element to the center of the screen.
    - **Overlay Removal**: Runs a JS script to remove common blocking overlays (modals, backdrops).
    - **Visibility Force**: Forces the element's CSS to `visibility: visible` and `pointer-events: auto`.
2.  **Strategy 1: ActionChains (Mouse Simulation)**: Uses Selenium's `ActionChains` to move the mouse cursor to the element, pause for 300ms, and perform a physical click. This is the most reliable method for React components that listen for pointer events.
3.  **Strategy 2 & 3: Keyboard Interaction**: Explicitly focuses the element and sends `Keys.RETURN` or `Keys.SPACE`. This triggers "onKeyDown" and "onKeyUp" handlers often used in accessible web apps.
4.  **Strategy 4: Standard Click**: The default Selenium `.click()` method.
5.  **Strategy 5: JavaScript Click**: Directly calls `.click()` on the DOM element via `execute_script`. This bypasses any elements that might be "technically" overlapping the target.
6.  **Strategy 6: Full Event Dispatch**: Dispatches a sequence of raw `MouseEvent` objects (`mousedown` → `mouseup` → `click`) directly to the element. This ensures that even if a developer used custom event listeners, the button will likely trigger.

## � Unified Region Support

The registration flow seamlessly handles both US and UK regions by using a **unified set of search terms**. Regardless of the target domain, the system aggressively searches for all known button variants used across different Match.com versions:

- **Primary Affirmations**: "That's Right", "That's me", "That's the one", "Confirm", "Join now", "Start now"
- **Navigation**: "Continue", "Next", "Start", "Begin", "Get Started"
- **Actions**: "Save", "skip", "upload photo", "Create Account", "Sign Up", "Register"

This unified approach ensures that changes in regional wording or A/B testing do not break the automation logic.

## Main Components

### `MatchAutomator` Class

- `__init__(headless=False)`: Initializes the Chrome WebDriver with specific arguments (disable notifications, start maximized).
- `run_registration(email, password, name, photo_path, region="us")`: Orchestrates the entire flow from landing on the registration page to finishing the dashboard setup.
- `click_element(element, description)`: The ultra-robust click engine described above.
- `find_and_click_button(texts)`: The aggressive search engine described above.
- `handle_profile_questions()`: A looping logic that identifies and answers various profile setup questions dynamically.
- `handle_photo_upload(photo_path)`: Bypasses UI hurdles to upload a profile image.
- `dismiss_overlays()`: Uses both CSS selectors and JavaScript injection to ensure the UI is clear for interaction.

## Flow of Execution

1.  **Landing**: Selects gender preferences and age ranges.
2.  **Location**: Handles zip code typeahead suggestions.
3.  **Account Details**: Iteratively fills out Birthday, Name, Email, and Password.
4.  **Profile Media**: Uploads a profile picture.
5.  **Profile Details**: Answers a series of questions about lifestyle and preferences.
6.  **Completion**: Navigates to the dashboard.

## Dependencies

- `selenium`: For browser automation.
- `webdriver_manager`: To automatically handle Chrome driver installation.
- `random`, `string`, `time`, `os`: For data generation and execution control.

## Usage

```python
automator = MatchAutomator(headless=False)
try:
    automator.run_registration("user@example.com", "SecurePass123!", "John")
finally:
    automator.close()
```
