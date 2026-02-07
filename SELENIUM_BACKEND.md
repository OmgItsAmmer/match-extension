# Selenium Backend Documentation

This file (`selenium_backend.py`) contains the `MatchAutomator` class, which is a specialized Selenium-based automation engine designed to handle account registration and profile setup on **Match.com**.

## Overview

The script automates the multi-step registration process, including handling dynamic forms, cookie banners, and profile-building questions. It is designed to be resilient by using "safe" element finding methods and fallbacks for interactions.

## Key Features

- **Robust Element Selection**: Uses multiple selector fallbacks and explicit waits to handle dynamic web elements.
- **Human-like Interaction**: Simulates typing with random delays and clears inputs in a way that is compatible with React-based forms.
- **Automated Profile Building**: Randomly selects options for profile questions (education, smoking, etc.) to complete account setup.
- **Photo Upload Support**: Specifically handles hidden file inputs commonly found in modern web applications.
- **Overlay Management**: Automatically detects and dismisses cookie consent banners (OneTrust) and other pop-ups.

## Main Components

### `MatchAutomator` Class

- `__init__(headless=False)`: Initializes the Chrome WebDriver with specific arguments (disable notifications, start maximized).
- `run_registration(email, password, name, photo_path)`: Orchestrates the entire flow from landing on the registration page to finishing the dashboard setup.
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
