# Migration Guide: Selenium to Playwright

This guide explains the key differences and improvements when migrating from Selenium to Playwright.

## Table of Contents
1. [Key Differences](#key-differences)
2. [Architecture Improvements](#architecture-improvements)
3. [Code Comparison](#code-comparison)
4. [Migration Steps](#migration-steps)

## Key Differences

### 1. Async/Await vs Synchronous

**Selenium (Synchronous)**
```python
def click_element(self, element):
    element.click()
    time.sleep(1)
```

**Playwright (Async)**
```python
async def smart_click(self, element):
    await element.click()
    await asyncio.sleep(1)
```

### 2. Element Selection

**Selenium**
```python
# Multiple strategies needed
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "button"))
)
```

**Playwright**
```python
# Built-in smart waiting
element = page.locator("button")
await element.click()  # Automatically waits until actionable
```

### 3. React Event Handling

**Selenium**
```python
# Required 6 different strategies to handle React clicks
try:
    ActionChains(driver).move_to_element(element).click().perform()
except:
    try:
        element.send_keys(Keys.RETURN)
    except:
        try:
            driver.execute_script("arguments[0].click();", element)
        except:
            # ... 3 more fallback strategies
```

**Playwright**
```python
# Just works with React
await element.click()
# Playwright automatically handles React synthetic events
```

### 4. File Uploads

**Selenium**
```python
# Had to manipulate visibility
driver.execute_script("""
    arguments[0].style.display = 'block';
    arguments[0].style.visibility = 'visible';
    arguments[0].style.opacity = '1';
""", file_input)
file_input.send_keys(file_path)
```

**Playwright**
```python
# Clean and simple
await file_input.set_input_files(file_path)
```

### 5. Text Matching

**Selenium**
```python
# Manual iteration through all elements
all_clickables = driver.find_elements(By.CSS_SELECTOR, 'button, a, [role="button"]')
for element in all_clickables:
    text = element.text or element.get_attribute("value") or ""
    if search_text.lower() in text.lower():
        element.click()
        break
```

**Playwright**
```python
# Built-in text matching
button = page.get_by_role("button", name="Continue", exact=False)
await button.click()
```

## Architecture Improvements

### Modularity

**Selenium (Monolithic)**
- Single 643-line class
- All logic in one file
- Hard to test individual components

**Playwright (Modular)**
```
playwright_backend/
├── config.py          # Configuration
├── utils.py           # Utilities
├── page_interactor.py # Low-level interactions
├── handlers.py        # Step handlers
└── automator.py       # Orchestrator
```

### Scalability

**Selenium**
- Synchronous blocking operations
- Sequential execution only
- Resource-intensive waits

**Playwright**
- Async/await for non-blocking operations
- Can run multiple operations concurrently
- Efficient smart waiting

**Example:**
```python
# Playwright can do concurrent operations
await asyncio.gather(
    page.wait_for_load_state("networkidle"),
    page.wait_for_selector("button"),
    page.screenshot(path="screenshot.png")
)
```

### Flexibility

**Selenium**
- Hard-coded selectors
- Magic numbers for timeouts
- Difficult to customize

**Playwright**
- Configuration-driven
- Easy to extend
- Dependency injection

## Code Comparison

### Example: Clicking a Button

**Selenium (50+ lines)**
```python
def click_element(self, element, description="element"):
    try:
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(element)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.delay(300)
        
        # Remove overlays
        self.driver.execute_script("""
            var overlays = document.querySelectorAll('.overlay, .modal-backdrop');
            overlays.forEach(function(el) { el.style.display = 'none'; });
        """, element)
        
        # Try ActionChains
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).pause(0.3).click().perform()
            return True
        except:
            pass
        
        # Try Enter key
        try:
            element.send_keys(Keys.RETURN)
            return True
        except:
            pass
        
        # ... 4 more strategies
        
    except Exception as e:
        print(f"Failed: {e}")
        return False
```

**Playwright (15 lines)**
```python
async def smart_click(self, element, description="element"):
    try:
        await element.scroll_into_view_if_needed()
        await element.click(timeout=5000)
        return True
    except:
        # Fallback strategies if needed
        try:
            await element.dispatch_event("click")
            return True
        except:
            await element.press("Enter")
            return True
    except Exception as e:
        self.logger.error(f"Failed: {e}")
        return False
```

### Example: Finding and Clicking Button by Text

**Selenium (90+ lines)**
```python
def find_and_click_button(self, texts):
    # Find ALL clickable elements
    all_clickables = self.driver.find_elements(By.CSS_SELECTOR, 
        'button, input[type="submit"], [role="button"], a, ...')
    
    for search_text in texts:
        for element in all_clickables:
            if not element.is_displayed():
                continue
            
            element_text = (element.text or "").strip()
            element_value = (element.get_attribute("value") or "").strip()
            element_aria = (element.get_attribute("aria-label") or "").strip()
            
            all_text = f"{element_text} {element_value} {element_aria}".lower()
            
            if search_text.lower() in all_text:
                # Try clicking
                # ... complex click logic
                return True
    
    # XPath fallback
    for search_text in texts:
        xpath = f"//*[contains(text(), '{search_text}')]"
        elements = self.driver.find_elements(By.XPATH, xpath)
        # ... more logic
    
    return False
```

**Playwright (20 lines)**
```python
async def find_and_click_button(self, texts):
    for text in texts:
        try:
            # Built-in role and text matching
            button = self.page.get_by_role("button", name=text, exact=False)
            if await button.is_visible(timeout=2000):
                await self.smart_click(button, f"Button '{text}'")
                return True
        except:
            pass
        
        try:
            # Text-based matching
            element = self.page.get_by_text(text, exact=False)
            if await element.is_visible(timeout=2000):
                await self.smart_click(element, f"Text '{text}'")
                return True
        except:
            pass
    
    return False
```

## Migration Steps

### Step 1: Install Playwright

```bash
pip install playwright
playwright install chromium
```

### Step 2: Update Imports

**Before (Selenium)**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

**After (Playwright)**
```python
from playwright.async_api import async_playwright, Page
import asyncio
```

### Step 3: Convert to Async

**Before**
```python
def run_automation():
    driver = webdriver.Chrome()
    driver.get("https://example.com")
    # ... automation logic
    driver.quit()

if __name__ == "__main__":
    run_automation()
```

**After**
```python
async def run_automation():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        # ... automation logic
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
```

### Step 4: Update Element Interactions

| Selenium | Playwright |
|----------|------------|
| `driver.find_element(By.CSS_SELECTOR, "button")` | `page.locator("button")` |
| `element.click()` | `await element.click()` |
| `element.send_keys("text")` | `await element.fill("text")` |
| `Select(element).select_by_value("value")` | `await element.select_option(value="value")` |
| `element.text` | `await element.text_content()` |
| `element.get_attribute("attr")` | `await element.get_attribute("attr")` |

### Step 5: Update Waits

**Before**
```python
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "button"))
)
```

**After**
```python
# Automatic waiting built-in
await page.locator("button").click()

# Or explicit wait
await page.wait_for_selector("button", state="visible", timeout=10000)
```

## Benefits Summary

### Code Reduction
- **Selenium**: 643 lines
- **Playwright**: ~400 lines (split across 6 files)
- **Reduction**: ~38% less code with better organization

### Reliability
- ✅ No need for complex click strategies
- ✅ Automatic waiting for React state updates
- ✅ Better error messages
- ✅ More stable element interactions

### Performance
- ✅ Async operations
- ✅ Concurrent execution possible
- ✅ Faster page loads with smart waiting

### Maintainability
- ✅ Modular architecture
- ✅ Configuration-driven
- ✅ Easy to test
- ✅ Clear separation of concerns

### Developer Experience
- ✅ Better documentation
- ✅ Type hints support
- ✅ Cleaner API
- ✅ Built-in debugging tools

## Conclusion

The Playwright implementation provides:
1. **Better React support** - No complex workarounds needed
2. **Cleaner code** - 38% reduction with better organization
3. **More reliable** - Fewer flaky tests
4. **Better architecture** - Modular, scalable, flexible
5. **Modern patterns** - Async/await, type hints, context managers

The migration effort is worthwhile for any project that needs reliable web automation, especially for React applications.
