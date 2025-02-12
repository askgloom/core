"""
Helper functions for Ask Gloom.
Provides utility functions used throughout the framework.
"""

import os
import re
import time
import random
import string
import shutil
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from pathlib import Path
from urllib.parse import urlparse

from ..exceptions import ValidationException, TimeoutException

T = TypeVar('T')

def retry_on_exception(
    func: Callable[..., T],
    exceptions: tuple = (Exception,),
    attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    logger: Optional[Any] = None
) -> T:
    """Retry a function on exception with exponential backoff.
    
    Args:
        func: Function to retry
        exceptions: Tuple of exceptions to catch
        attempts: Maximum number of attempts
        delay: Initial delay between attempts
        backoff: Multiplier for delay after each attempt
        logger: Logger instance for debugging
    
    Returns:
        Result of the function call
    
    Raises:
        The last exception if all attempts fail
    """
    for attempt in range(attempts):
        try:
            return func()
        except exceptions as e:
            if logger:
                logger.warning(f"Attempt {attempt + 1}/{attempts} failed: {str(e)}")
            if attempt == attempts - 1:
                raise
            time.sleep(delay * (backoff ** attempt))

def wait_until(
    condition: Callable[[], bool],
    timeout: float = 30.0,
    interval: float = 0.5,
    message: str = "Condition not met"
) -> None:
    """Wait until a condition is met or timeout occurs.
    
    Args:
        condition: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        interval: Time between checks in seconds
        message: Error message if timeout occurs
    
    Raises:
        TimeoutException: If condition is not met within timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition():
            return
        time.sleep(interval)
    raise TimeoutException(message, timeout=timeout)

def validate_type(value: Any, expected_type: type, field: str = "") -> None:
    """Validate that a value is of the expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type
        field: Field name for error message
    
    Raises:
        ValidationException: If type validation fails
    """
    if not isinstance(value, expected_type):
        raise ValidationException(
            f"Expected {expected_type.__name__}, got {type(value).__name__}",
            field=field
        )

def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
    
    Returns:
        True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def generate_random_string(
    length: int = 10,
    chars: str = string.ascii_letters + string.digits
) -> str:
    """Generate a random string of specified length.
    
    Args:
        length: Length of the string
        chars: Characters to choose from
    
    Returns:
        Random string
    """
    return ''.join(random.choice(chars) for _ in range(length))

def create_directory(path: Union[str, Path], exist_ok: bool = True) -> Path:
    """Create a directory and its parents if they don't exist.
    
    Args:
        path: Directory path
        exist_ok: Don't raise error if directory exists
    
    Returns:
        Path object of created directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=exist_ok)
    return path

def remove_directory(path: Union[str, Path], ignore_errors: bool = False) -> None:
    """Remove a directory and its contents.
    
    Args:
        path: Directory path
        ignore_errors: Don't raise error if directory doesn't exist
    """
    shutil.rmtree(path, ignore_errors=ignore_errors)

def is_valid_path(path: Union[str, Path]) -> bool:
    """Check if a path is valid for the current OS.
    
    Args:
        path: Path to validate
    
    Returns:
        True if path is valid, False otherwise
    """
    try:
        Path(path).resolve()
        return True
    except (OSError, RuntimeError):
        return False

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (overrides dict1)
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def parse_selector(selector: str) -> tuple:
    """Parse a selector string into method and value.
    
    Args:
        selector: Selector string (e.g., "css:.class", "xpath://div")
    
    Returns:
        Tuple of (method, value)
    """
    if ':' not in selector:
        return 'css', selector
    method, value = selector.split(':', 1)
    return method.lower(), value

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove control characters
    filename = "".join(char for char in filename if ord(char) >= 32)
    return filename.strip()

def format_timespan(seconds: float) -> str:
    """Format a timespan in seconds to a human-readable string.
    
    Args:
        seconds: Number of seconds
    
    Returns:
        Formatted string (e.g., "2h 30m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)