"""
Example usage scripts for the Playwright backend.
"""

import asyncio
from playwright_backend import run_automation, MatchAutomator, BrowserConfig


async def example_simple():
    """Simple example using the convenience function."""
    print("=== Simple Example ===\n")
    
    success = await run_automation(
        email="test_user_123@gmail.com",
        password="SecurePassword123!",
        name="John",
        photo_path="automation-extension/assets/img.png",
        region="us",
        headless=False
    )
    
    if success:
        print("\n✅ Registration completed successfully!")
    else:
        print("\n❌ Registration failed!")


async def example_advanced():
    """Advanced example with custom configuration."""
    print("=== Advanced Example ===\n")
    
    # Custom browser configuration
    config = BrowserConfig(
        headless=False,
        viewport_width=1920,
        viewport_height=1080,
        slow_mo=100,  # Slow down by 100ms for better visibility
        timeout=30000
    )
    
    # Use context manager for automatic cleanup
    async with MatchAutomator(config) as automator:
        success = await automator.run_registration(
            email="test_user_456@gmail.com",
            password="SecurePassword123!",
            name="Jane",
            photo_path="automation-extension/assets/img.png",
            region="us"
        )
        
        if success:
            # Take screenshot on success
            await automator.take_screenshot("registration_success.png")
            print("\n✅ Registration completed! Screenshot saved.")
        else:
            # Take screenshot on failure for debugging
            await automator.take_screenshot("registration_failed.png")
            print("\n❌ Registration failed! Screenshot saved for debugging.")
        
        return success


async def example_uk_region():
    """Example for UK Match.com registration."""
    print("=== UK Region Example ===\n")
    
    success = await run_automation(
        email="test_user_uk@gmail.com",
        password="SecurePassword123!",
        name="Oliver",
        photo_path="automation-extension/assets/img.png",
        region="uk",  # UK region
        headless=False
    )
    
    if success:
        print("\n✅ UK Registration completed successfully!")
    else:
        print("\n❌ UK Registration failed!")


async def example_multiple_registrations():
    """Example running multiple registrations sequentially."""
    print("=== Multiple Registrations Example ===\n")
    
    users = [
        {"email": "user1@example.com", "name": "Alice"},
        {"email": "user2@example.com", "name": "Bob"},
        {"email": "user3@example.com", "name": "Charlie"},
    ]
    
    results = []
    
    for user in users:
        print(f"\nProcessing {user['name']}...")
        success = await run_automation(
            email=user["email"],
            password="SecurePassword123!",
            name=user["name"],
            photo_path="automation-extension/assets/img.png",
            region="us",
            headless=True  # Run headless for batch processing
        )
        results.append({"user": user["name"], "success": success})
        
        # Wait between registrations
        await asyncio.sleep(5)
    
    # Print summary
    print("\n=== Summary ===")
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['user']}: {'Success' if result['success'] else 'Failed'}")


async def example_with_error_handling():
    """Example with comprehensive error handling."""
    print("=== Error Handling Example ===\n")
    
    try:
        config = BrowserConfig(headless=False)
        
        async with MatchAutomator(config) as automator:
            success = await automator.run_registration(
                email="test@example.com",
                password="SecurePassword123!",
                name="Test User",
                photo_path="automation-extension/assets/img.png",
                region="us"
            )
            
            if success:
                print("\n✅ Registration successful!")
            else:
                print("\n⚠️ Registration completed with warnings")
                
    except Exception as e:
        print(f"\n❌ Fatal error occurred: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function to run examples."""
    print("Playwright Backend Examples\n")
    print("Choose an example to run:")
    print("1. Simple example")
    print("2. Advanced example with custom config")
    print("3. UK region example")
    print("4. Multiple registrations")
    print("5. Error handling example")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    examples = {
        "1": example_simple,
        "2": example_advanced,
        "3": example_uk_region,
        "4": example_multiple_registrations,
        "5": example_with_error_handling
    }
    
    if choice in examples:
        asyncio.run(examples[choice]())
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    # Run simple example by default
    asyncio.run(example_simple())
    
    # Or run the interactive menu
    # main()
