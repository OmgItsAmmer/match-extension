"""
Quick test script to verify button clicking works
"""
from selenium_backend import MatchAutomator
import time

def test_button_clicking():
    print("Starting button click test...")
    automator = MatchAutomator(headless=False)
    
    try:
        # Navigate to Match.com registration
        automator.driver.get("https://www.match.com/reg")
        time.sleep(3)
        
        # Dismiss any overlays
        automator.dismiss_overlays()
        
        # Try to find and click a button
        print("\n=== Testing button finding and clicking ===")
        result = automator.find_and_click_button(['View Singles', 'Get Started', 'Continue'])
        
        if result:
            print("\n✅ SUCCESS! Button was clicked!")
        else:
            print("\n❌ FAILED! Could not click button")
        
        # Keep browser open for inspection
        print("\nBrowser will stay open for 10 seconds for inspection...")
        time.sleep(10)
        
    finally:
        automator.close()

if __name__ == "__main__":
    test_button_clicking()
