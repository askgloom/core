"""
Utility module for Ask Gloom.
Provides helper functions and utilities used throughout the framework.
"""

from .logger import Logger, setup_logging, get_logger
from .helpers import (
    retry_on_exception,
    wait_until,
    validate_type,
    validate_url,
    generate_random_string,
    create_directory,
    remove_directory,
    is_valid_path,
    merge_dicts,
    parse_selector,
    sanitize_filename,
    format_timespan,
)

__all__ = [
    # Logging utilities
    'Logger',
    'setup_logging',
    'get_logger',
    
    # General helpers
    'retry_on_exception',
    'wait_until',
    'validate_type',
    'validate_url',
    'generate_random_string',
    
    # File system helpers
    'create_directory',
    'remove_directory',
    'is_valid_path',
    'sanitize_filename',
    
    # Data structure helpers
    'merge_dicts',
    'parse_selector',
    
    # Formatting helpers
    'format_timespan',
]

# Version of the utils module
__version__ = '0.1.0'

# Default configuration
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 1.0
DEFAULT_TIMEOUT = 30.0
DEFAULT_RANDOM_STRING_LENGTH = 10