# Quick Start Guide

Get started with the Playwright backend in 5 minutes!

## Installation

### 1. Install Dependencies

```bash
# Navigate to the playwright_backend directory
cd playwright_backend

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Verify Installation

```bash
# Test that Playwright is installed correctly
python -c "from playwright.sync_api import sync_playwright; print('✅ Playwright installed successfully!')"
```

## Basic Usage

### Run Your First Automation

Create a file `test_automation.py`:

```python
import asyncio
from playwright_backend import run_automation

async def main():
    success = await run_automation(
        email="your_email@example.com",
        password="YourSecurePassword123!",
        name="YourName",
        photo_path="path/to/your/photo.jpg",  # Optional
        region="us",  # or "uk"
        headless=False  # Set to True to hide browser
    )
    
    if success:
        print("✅ Registration completed!")
    else:
        print("❌ Registration failed!")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python test_automation.py
```

## Common Use Cases

### 1. Run in Headless Mode (Background)

```python
await run_automation(
    email="test@example.com",
    password="Password123!",
    name="Test",
    headless=True  # Browser runs in background
)
```

### 2. Custom Browser Settings

```python
from playwright_backend import MatchAutomator, BrowserConfig

config = BrowserConfig(
    headless=False,
    slow_mo=100,  # Slow down by 100ms (useful for debugging)
    timeout=30000  # 30 second timeout
)

async with MatchAutomator(config) as automator:
    await automator.run_registration(
        email="test@example.com",
        password="Password123!",
        name="Test"
    )
```

### 3. Take Screenshots

```python
from playwright_backend import MatchAutomator, BrowserConfig

async with MatchAutomator(BrowserConfig()) as automator:
    await automator.run_registration(
        email="test@example.com",
        password="Password123!",
        name="Test"
    )
    
    # Take screenshot
    await automator.take_screenshot("result.png")
```

### 4. UK Region

```python
await run_automation(
    email="test@example.com",
    password="Password123!",
    name="Test",
    region="uk"  # Use UK Match.com
)
```

## Configuration

### Modify Timeouts

Edit `playwright_backend/config.py`:

```python
TIMEOUTS = {
    "short": 5000,    # 5 seconds
    "medium": 10000,  # 10 seconds
    "long": 20000,    # 20 seconds
    "upload": 30000   # 30 seconds
}
```

### Modify Selectors

If the website changes, update selectors in `config.py`:

```python
SELECTORS = {
    "landing_form": {
        "gender_select": ["select#ggs_select", "[name='genderSeek']"],
        # Add more selectors here
    }
}
```

### Add New Button Texts

```python
BUTTON_TEXTS = {
    "continue": ["continue", "Continue", "Next", "Proceed"],
    # Add more variations
}
```

## Troubleshooting

### Issue: "Playwright not found"

**Solution:**
```bash
pip install playwright
playwright install chromium
```

### Issue: "Browser crashes"

**Solution:**
Try running in non-headless mode to see what's happening:
```python
await run_automation(..., headless=False)
```

### Issue: "Element not found"

**Solution:**
1. Check if selectors have changed in `config.py`
2. Increase timeout:
```python
config = BrowserConfig(timeout=60000)  # 60 seconds
```

### Issue: "Photo upload fails"

**Solution:**
Make sure the photo path is correct:
```python
import os
photo_path = os.path.abspath("path/to/photo.jpg")
print(f"Photo exists: {os.path.exists(photo_path)}")
```

## Advanced Features

### Custom Logging

```python
from playwright_backend.utils import Logger

logger = Logger()
logger.info("Custom message")
logger.success("Success message")
logger.error("Error message")
```

### Generate Random Data

```python
from playwright_backend.utils import DataGenerator

zip_code = DataGenerator.random_zip_code()
birthday = DataGenerator.random_birthday()
min_age, max_age = DataGenerator.random_age_range()
```

### Direct Page Interaction

```python
from playwright_backend import MatchAutomator, BrowserConfig

async with MatchAutomator(BrowserConfig()) as automator:
    # Access the page directly
    page = automator.page
    
    # Use Playwright's full API
    await page.goto("https://example.com")
    await page.click("button")
    await page.fill("input", "text")
    
    # Use the interactor for smart interactions
    interactor = automator.interactor
    await interactor.smart_click("button", "My Button")
```

## Examples

Check out `examples.py` for more usage patterns:

```bash
python playwright_backend/examples.py
```

Available examples:
1. Simple registration
2. Advanced with custom config
3. UK region
4. Multiple registrations (batch)
5. Error handling

## Next Steps

1. **Read the README**: `playwright_backend/README.md`
2. **Check Migration Guide**: `playwright_backend/MIGRATION_GUIDE.md`
3. **Explore Examples**: `playwright_backend/examples.py`
4. **Customize Config**: `playwright_backend/config.py`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the migration guide for code examples
3. Enable debug logging by setting `slow_mo` in BrowserConfig

## Tips

✅ **DO:**
- Use headless mode for production
- Set appropriate timeouts
- Handle errors gracefully
- Take screenshots for debugging

❌ **DON'T:**
- Run too many parallel instances (can be resource-intensive)
- Use very short timeouts (websites need time to load)
- Ignore error messages (they provide valuable debugging info)

Happy automating! 🚀
