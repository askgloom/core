"""
Basic usage examples for Ask Gloom Core.
Demonstrates common operations and features.
"""

import logging
from pathlib import Path
from askgloom.core import Browser, Profile, Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def basic_browser_example():
    """Demonstrate basic browser operations."""
    try:
        # Initialize browser with default profile
        with Browser() as browser:
            # Navigate to a website
            browser.navigate("https://example.com")
            logger.info(f"Current URL: {browser.current_url()}")
            
            # Take a screenshot
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            browser.screenshot(str(screenshots_dir / "example.png"))
            
    except Exception as e:
        logger.error(f"Browser example failed: {e}")

def custom_profile_example():
    """Demonstrate custom profile usage."""
    try:
        # Create a custom profile
        profile = Profile("custom_profile")
        
        # Customize profile preferences
        profile.preferences.update({
            "browser": {
                "window_size": {
                    "width": 1600,
                    "height": 900
                },
                "startup_page": "https://example.com"
            }
        })
        profile.save_preferences()
        
        # Use custom profile with browser
        with Browser(profile=profile, headless=True) as browser:
            browser.navigate("https://example.com")
            logger.info("Successfully used custom profile")
            
    except Exception as e:
        logger.error(f"Custom profile example failed: {e}")

def config_example():
    """Demonstrate configuration management."""
    try:
        # Initialize config
        config = Config()
        
        # Update some settings
        config.set("browser.timeout", 60)
        config.set("automation.screenshot_on_error", True)
        
        # Use configuration with browser
        browser_config = {
            "headless": config.get("browser.headless", False),
            "window_size": config.get("browser.window_size")
        }
        
        with Browser(options=browser_config) as browser:
            browser.navigate("https://example.com")
            logger.info("Successfully used custom configuration")
            
    except Exception as e:
        logger.error(f"Configuration example failed: {e}")

def main():
    """Run all examples."""
    logger.info("Starting Ask Gloom Core examples...")
    
    logger.info("\n1. Basic Browser Example")
    basic_browser_example()
    
    logger.info("\n2. Custom Profile Example")
    custom_profile_example()
    
    logger.info("\n3. Configuration Example")
    config_example()
    
    logger.info("\nExamples completed!")

if __name__ == "__main__":
    main()