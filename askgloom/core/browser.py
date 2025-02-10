"""
Core browser automation functionality for Ask Gloom.
Provides a high-level interface for browser control and automation.
"""

import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ..exceptions.core_exceptions import BrowserException
from .profile import Profile

logger = logging.getLogger(__name__)

class Browser:
    """
    Main browser automation class that handles browser initialization,
    profile management, and core automation functions.
    """

    def __init__(
        self,
        profile: Optional[Profile] = None,
        headless: bool = False,
        options: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize browser instance.

        Args:
            profile (Profile, optional): Browser profile to use
            headless (bool): Whether to run in headless mode
            options (Dict[str, Any], optional): Additional browser options
        """
        self.profile = profile or Profile()
        self.headless = headless
        self.options = options or {}
        self.driver = None
        self._initialize_browser()

    def _initialize_browser(self) -> None:
        """Set up and initialize the browser instance."""
        try:
            chrome_options = Options()
            
            # Apply profile settings
            if self.profile.path:
                chrome_options.add_argument(f"user-data-dir={self.profile.path}")

            # Set headless mode if requested
            if self.headless:
                chrome_options.add_argument("--headless")

            # Apply additional options
            for option, value in self.options.items():
                if isinstance(value, bool) and value:
                    chrome_options.add_argument(f"--{option}")
                else:
                    chrome_options.add_argument(f"--{option}={value}")

            # Initialize ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            logger.info("Browser initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            raise BrowserException(f"Browser initialization failed: {str(e)}")

    def navigate(self, url: str) -> None:
        """
        Navigate to specified URL.

        Args:
            url (str): URL to navigate to
        """
        try:
            self.driver.get(url)
            logger.debug(f"Navigated to {url}")
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            raise BrowserException(f"Failed to navigate to {url}: {str(e)}")

    def current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url

    def screenshot(self, path: str) -> bool:
        """
        Take screenshot of current page.

        Args:
            path (str): Path to save screenshot

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return self.driver.save_screenshot(path)
        except Exception as e:
            logger.error(f"Screenshot failed: {str(e)}")
            return False

    def quit(self) -> None:
        """Close browser and clean up resources."""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Failed to close browser: {str(e)}")
            raise BrowserException(f"Browser cleanup failed: {str(e)}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit()
