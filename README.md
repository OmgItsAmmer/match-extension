# Match.com Selenium Automation - Region Support

## 🌍 Multi-Region Support

The automation now supports both **US** and **UK** versions of Match.com!

### Supported Regions

- **US** (default): `match.com`
- **UK**: `uk.match.com`

## 📝 Usage

### Python API

```python
from selenium_backend import MatchAutomator

# US Match.com (default)
automator = MatchAutomator()
automator.run_registration(
    email="user@example.com",
    password="SecurePass123!",
    name="John",
    region="us"  # or omit for default
)

# UK Match.com
automator = MatchAutomator()
automator.run_registration(
    email="user@example.com",
    password="SecurePass123!",
    name="James",
    region="uk"  # 🇬🇧
)
```

### REST API

#### US Match.com
```bash
curl -X POST http://localhost:8000/automate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John",
    "region": "us"
  }'
```

#### UK Match.com
```bash
curl -X POST http://localhost:8000/automate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "James",
    "region": "uk"
  }'
```

## 🎯 Button Clicking - Ultra Aggressive Mode

The automation uses **6 different click strategies** to ensure buttons are clicked:

1. **ActionChains** - Mouse movement + click (best for React)
2. **Enter Key** - Keyboard RETURN key
3. **Space Key** - Keyboard SPACE key
4. **Regular Click** - Standard Selenium click
5. **JavaScript Click** - Direct JS execution
6. **Full Event Dispatch** - mousedown → mouseup → click sequence

### Button Text Variants

The automation searches for multiple button text variants to support both regions:

**Birthday Step:**
- "That's Right", "That's right", "Next", "continue", "Continue", "Confirm"

**Name Step:**
- "That's me", "That's Me", "Next", "continue", "Continue", "Confirm"

**Email Step:**
- "That's the one", "That's The One", "Next", "continue", "Continue", "Confirm"

**Password Step:**
- "That's Right", "That's right", "Create Account", "Sign Up", "continue", "Continue", "Join now", "Register"

**Profile Questions:**
- "continue", "Continue", "Next", "Save", "skip", "Skip", "Skip for now", "upload photo", "Upload photo", "That's Right", "That's right", "Confirm", "Done"

## 🔍 Search Strategy

The button finder uses **4 comprehensive strategies**:

1. **CSS Selector Search** - Finds all clickable elements (buttons, inputs, divs, spans, labels)
2. **Multi-Attribute Matching** - Checks text, value, aria-label, title, data-testid
3. **XPath Text Search** - Exact and partial text matching
4. **SVG/Arrow Detection** - For navigation elements

## 🧪 Testing

### Test US Match.com
```bash
python test_clicking.py
```

### Test UK Match.com
```bash
python test_uk_match.py
```

## 🚀 Running the API

```bash
python api.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `POST /automate` - Start automation

### Request Schema

```json
{
  "email": "string",
  "password": "string",
  "name": "string",
  "region": "us" | "uk",  // optional, defaults to "us"
  "photo_path": "string"  // optional, defaults to "automation-extension/assets/img.png"
}
```

## 📊 Features

✅ Multi-region support (US & UK)  
✅ Ultra-aggressive button clicking (6 strategies)  
✅ Comprehensive button text matching  
✅ Overlay removal  
✅ Element visibility forcing  
✅ Detailed logging  
✅ Photo upload support  
✅ Profile questions automation  
✅ REST API with background tasks  

## 🛠️ Technical Details

### Click Element Process

1. Wait for element to be clickable (5s timeout)
2. Scroll element into view
3. Remove any blocking overlays
4. Force element visibility via JS
5. Focus the element
6. Try 6 different click strategies in sequence
7. Wait 500ms after successful click

### Button Search Process

1. Find all potentially clickable elements
2. Check multiple text sources (text, attributes)
3. Case-insensitive partial matching
4. Try clicking element directly
5. Try clicking parent element if direct fails
6. Fallback to XPath text search
7. Fallback to SVG/arrow detection

## 🎨 Logging

The automation provides detailed logging:

- `[BUTTON SEARCH]` - Button search operations
- `[BUTTON MATCH]` - When a button is found
- `[CLICK]` - Click attempts
- `[CLICK SUCCESS]` - Which strategy worked
- `[XPATH MATCH]` - XPath-based matches
- `[SVG SEARCH]` - SVG element searches

## 💡 Tips

- The automation works best with **headless=False** for debugging
- Check the console logs to see which click strategy worked
- UK Match.com uses slightly different button text
- The automation handles overlays and cookie banners automatically
- Profile questions are answered randomly
