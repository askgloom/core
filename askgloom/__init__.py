"""
Ask Gloom Core - Browser Automation Framework
-------------------------------------------

Core functionality for browser automation and profile management.
This module provides the foundation for other Ask Gloom projects.

Example:
    from askgloom.core import Browser
    browser = Browser()
    browser.navigate("https://example.com")
"""

__version__ = "0.1.0"
__author__ = "Ask Gloom"
__license__ = "MIT"

from .core.browser import Browser
from .core.profile import Profile
from .exceptions.core_exceptions import (
    BrowserException,
    ProfileException,
    ConfigurationException
)

__all__ = [
    "Browser",
    "Profile",
    "BrowserException",
    "ProfileException",
    "ConfigurationException",
]