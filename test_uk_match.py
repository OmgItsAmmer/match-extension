"""
Test script for UK Match.com registration automation
"""
from selenium_backend import MatchAutomator
import time

def test_uk_match():
    print("🇬🇧 Starting UK Match.com test...")
    automator = MatchAutomator(headless=False)
    
    try:
        # Test UK Match.com
        automator.run_registration(
            email="test_uk_user@gmail.com",
            password="TestPassword123!",
            name="James",
            region="uk"
        )
        
        print("\n✅ UK Match.com automation completed!")
        
        # Keep browser open for inspection
        print("\nBrowser will stay open for 30 seconds for inspection...")
        time.sleep(30)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        time.sleep(10)
    finally:
        automator.close()

if __name__ == "__main__":
    test_uk_match()
