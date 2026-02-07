# Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER APPLICATION                             │
│                                                                      │
│  import asyncio                                                      │
│  from playwright_backend import run_automation                       │
│                                                                      │
│  asyncio.run(run_automation(email, password, name))                 │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AUTOMATOR LAYER                                 │
│                     (automator.py)                                   │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  MatchAutomator                                             │    │
│  │  ├─ Browser lifecycle management                            │    │
│  │  ├─ Context manager (__aenter__, __aexit__)                │    │
│  │  ├─ Orchestrates registration flow                          │    │
│  │  └─ Coordinates all handlers                                │    │
│  └────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       HANDLER LAYER                                  │
│                      (handlers.py)                                   │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Landing    │  │   Birthday   │  │     Name     │             │
│  │    Form      │  │   Handler    │  │   Handler    │             │
│  │   Handler    │  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    Email     │  │   Password   │  │    Photo     │             │
│  │   Handler    │  │   Handler    │  │   Upload     │             │
│  │              │  │              │  │   Handler    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────────────────────────────────────────┐              │
│  │         Profile Questions Handler                 │              │
│  │         (loops through questions)                 │              │
│  └──────────────────────────────────────────────────┘              │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   PAGE INTERACTION LAYER                             │
│                   (page_interactor.py)                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  PageInteractor                                             │    │
│  │  ├─ wait_and_get_element()    - Smart element finding      │    │
│  │  ├─ smart_click()              - Reliable clicking          │    │
│  │  ├─ smart_fill()               - Form filling               │    │
│  │  ├─ select_dropdown()          - Dropdown selection         │    │
│  │  ├─ find_and_click_button()    - Button text matching       │    │
│  │  └─ dismiss_overlays()         - Overlay removal            │    │
│  └────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      UTILITY LAYER                                   │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    Config    │  │    Utils     │  │   Logging    │             │
│  │  (config.py) │  │  (utils.py)  │  │              │             │
│  │              │  │              │  │              │             │
│  │ • Regions    │  │ • DataGen    │  │ • Logger     │             │
│  │ • Selectors  │  │ • PathHelper │  │ • Info       │             │
│  │ • Timeouts   │  │ • Random     │  │ • Success    │             │
│  │ • Buttons    │  │   data       │  │ • Error      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PLAYWRIGHT API                                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Browser ──► Context ──► Page ──► Locator ──► Element      │    │
│  │                                                              │    │
│  │  • Chromium browser                                         │    │
│  │  • Browser context (isolated session)                       │    │
│  │  • Page (tab)                                               │    │
│  │  • Locator (element selector)                               │    │
│  │  • Element (DOM element)                                    │    │
│  └────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         WEB BROWSER                                  │
│                      (Chromium Engine)                               │
│                                                                      │
│                    ┌─────────────────┐                              │
│                    │   Match.com     │                              │
│                    │   Website       │                              │
│                    └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘


DATA FLOW:
═══════════

1. User calls run_automation() or creates MatchAutomator instance
   ↓
2. Automator initializes browser, context, and page
   ↓
3. Automator creates PageInteractor with the page
   ↓
4. Automator calls handlers in sequence:
   - LandingFormHandler
   - BirthdayHandler
   - NameHandler
   - EmailHandler
   - PasswordHandler
   - PhotoUploadHandler
   - ProfileQuestionsHandler
   ↓
5. Each handler uses PageInteractor methods:
   - wait_and_get_element() to find elements
   - smart_click() to click buttons
   - smart_fill() to fill forms
   - select_dropdown() for dropdowns
   ↓
6. PageInteractor uses Playwright API:
   - page.locator() to find elements
   - element.click() to interact
   - element.fill() to input text
   ↓
7. Playwright controls the browser
   ↓
8. Browser interacts with Match.com website
   ↓
9. Results flow back up the chain
   ↓
10. Automator returns success/failure to user


DEPENDENCY INJECTION:
═══════════════════════

┌─────────────┐
│  Automator  │
└──────┬──────┘
       │ creates
       ▼
┌─────────────────┐
│ PageInteractor  │
└──────┬──────────┘
       │ injected into
       ▼
┌─────────────┐
│  Handlers   │
└─────────────┘

Each handler receives:
- page: Playwright Page object
- interactor: PageInteractor instance

This allows:
- Easy testing (mock dependencies)
- Loose coupling
- Flexibility to swap implementations


CONFIGURATION FLOW:
═══════════════════

┌──────────┐
│ config.py│
└────┬─────┘
     │
     ├─► BrowserConfig ──► Automator (browser settings)
     │
     ├─► RegionConfig ──► Automator (URL selection)
     │
     ├─► SELECTORS ──► Handlers (element finding)
     │
     ├─► TIMEOUTS ──► PageInteractor (waiting)
     │
     └─► BUTTON_TEXTS ──► PageInteractor (button matching)


ERROR HANDLING:
═══════════════

Try/Catch at multiple levels:

1. Automator level:
   - Catches fatal errors
   - Ensures cleanup (browser close)
   - Returns success/failure

2. Handler level:
   - Catches step-specific errors
   - Logs warnings
   - Continues to next step

3. PageInteractor level:
   - Catches interaction errors
   - Tries fallback strategies
   - Returns success/failure

4. Playwright level:
   - Automatic retries
   - Smart waiting
   - Detailed error messages


ASYNC EXECUTION:
════════════════

┌─────────────────────────────────────┐
│  asyncio.run(run_automation())      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  async with MatchAutomator():       │
│    await run_registration()         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  await handler.handle()             │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  await interactor.smart_click()     │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  await element.click()              │
└─────────────────────────────────────┘

All async operations use await
No blocking operations
Event loop manages concurrency


COMPARISON WITH SELENIUM:
═══════════════════════════

SELENIUM ARCHITECTURE:          PLAYWRIGHT ARCHITECTURE:
┌─────────────────┐            ┌─────────────────┐
│  Monolithic     │            │    Modular      │
│  Class          │            │   Architecture  │
│  (643 lines)    │            │  (6 files)      │
│                 │            │                 │
│  • All logic    │            │  • Separated    │
│    in one file  │            │    concerns     │
│  • Hard to      │            │  • Easy to      │
│    test         │            │    test         │
│  • Synchronous  │            │  • Async/await  │
│  • Complex      │            │  • Simple       │
│    workarounds  │            │    interactions │
└─────────────────┘            └─────────────────┘
