# Playwright Backend for Match.com Automation

A modern, modular automation framework for Match.com registration using Playwright.

## Features

- ✨ **Better React Support**: Playwright handles React applications flawlessly with automatic waiting and event handling
- 🏗️ **Modular Architecture**: Clean separation of concerns with dedicated handlers for each step
- ⚡ **Async/Await**: Better performance with asynchronous operations
- 🔧 **Flexible Configuration**: Easy to customize browser settings, timeouts, and selectors
- 📝 **Type Safety**: Uses dataclasses and type hints for better code quality
- 🌍 **Multi-Region Support**: Built-in support for US and UK Match.com sites

## API Testing (Postman)

You can run a local API server to test the automation via Postman.

### 1. Start the Server
```bash
# From the project root
python -m playwright_backend.server
```
The server will start at `http://localhost:8000`.

### 2. Import Postman Collection
Import the file `playwright_test.postman_collection.json` into Postman.

### 3. Run Requests
- **Health Check**: `GET /health` to verify the server is running.
- **Register**: `POST /register` with a JSON body to start the automation.

---

## Architecture

The codebase follows clean software construction principles:

### Modularity
- **`config.py`**: Centralized configuration management
- **`utils.py`**: Reusable utility functions (data generation, logging, path handling)
- **`page_interactor.py`**: Low-level page interaction methods
- **`handlers.py`**: High-level handlers for each registration step
- **`automator.py`**: Main orchestrator that coordinates all handlers

### Scalability
- Async/await pattern for non-blocking operations
- Efficient element waiting strategies
- Resource cleanup with context managers

### Flexibility
- Configuration-driven selectors and timeouts
- Easy to add new regions or modify existing flows
- Dependency injection pattern for handlers

## Installation

```bash
# Install Playwright
pip install playwright

# Install browser binaries
playwright install chromium
```

## Usage

### Simple Usage

```python
import asyncio
from playwright_backend import run_automation

asyncio.run(run_automation(
    email="user@example.com",
    password="SecurePassword123!",
    name="John",
    photo_path="path/to/photo.jpg",
    region="us",  # or "uk"
    headless=False
))
```

### Advanced Usage

```python
import asyncio
from playwright_backend import MatchAutomator, BrowserConfig

async def main():
    # Custom browser configuration
    config = BrowserConfig(
        headless=True,
        viewport_width=1920,
        viewport_height=1080,
        slow_mo=100  # Slow down by 100ms for debugging
    )
    
    # Use context manager for automatic cleanup
    async with MatchAutomator(config) as automator:
        success = await automator.run_registration(
            email="user@example.com",
            password="SecurePassword123!",
            name="John",
            photo_path="path/to/photo.jpg",
            region="us"
        )
        
        if success:
            # Take screenshot on success
            await automator.take_screenshot("success.png")
        
        return success

asyncio.run(main())
```

## Key Improvements Over Selenium

### 1. Better React Handling
Playwright automatically waits for React state updates and handles synthetic events properly, eliminating the need for complex click strategies.

```python
# Selenium required multiple fallback strategies
# Playwright just works:
await element.click()
```

### 2. Smart Waiting
Playwright has built-in smart waiting that automatically waits for elements to be actionable.

```python
# No need for explicit WebDriverWait
locator = page.locator("button")
await locator.click()  # Automatically waits until clickable
```

### 3. Async Performance
Async/await allows for better resource utilization and concurrent operations.

```python
# Multiple operations can be awaited efficiently
await asyncio.gather(
    page.wait_for_load_state("networkidle"),
    page.wait_for_selector("button")
)
```

### 4. Reliable File Uploads
File uploads are much simpler and more reliable.

```python
# Selenium required visibility manipulation
# Playwright handles it elegantly:
await file_input.set_input_files("path/to/file.jpg")
```

## Configuration

### Browser Settings

Modify `BrowserConfig` in `config.py` or pass custom config:

```python
config = BrowserConfig(
    headless=False,
    viewport_width=1920,
    viewport_height=1080,
    timeout=30000,  # 30 seconds
    slow_mo=0  # No slowdown
)
```

### Region Settings

Add new regions in `Config.REGIONS`:

```python
REGIONS = {
    "us": RegionConfig(...),
    "uk": RegionConfig(...),
    "de": RegionConfig(...)  # Add new region
}
```

### Selectors

Update selectors in `Config.SELECTORS` if the website changes:

```python
SELECTORS = {
    "landing_form": {
        "gender_select": ["select#ggs_select", "[name='genderSeek']"],
        # Add more selectors
    }
}
```

## Project Structure

```
playwright_backend/
├── __init__.py          # Package exports
├── config.py            # Configuration management
├── utils.py             # Utility functions
├── page_interactor.py   # Low-level page interactions
├── handlers.py          # Step-specific handlers
└── automator.py         # Main orchestrator
```

## Error Handling

The framework includes comprehensive error handling:

- Automatic retries for transient failures
- Graceful degradation with fallback strategies
- Detailed logging for debugging
- Proper resource cleanup

## Logging

Built-in logger provides clear feedback:

```
[INIT] Initializing browser...
[SUCCESS] Browser initialized
[STEP] Handling Landing Form
[CLICK] Clicking Gender preference (<SELECT> text='')
[SUCCESS] Selected from Gender preference
...
```

## Contributing

To extend the framework:

1. Add new handlers in `handlers.py`
2. Update configuration in `config.py`
3. Modify the flow in `automator.py`

## License

This is a demonstration project for automation purposes.
