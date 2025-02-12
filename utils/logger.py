"""
Logging module for Ask Gloom.
Provides customizable logging functionality with different output formats and levels.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, Dict, Any

# Default logging format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class Logger:
    """Custom logger class with enhanced functionality."""
    
    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        format_string: str = DEFAULT_FORMAT,
        date_format: str = DEFAULT_DATE_FORMAT,
        log_file: Optional[Union[str, Path]] = None,
        rotation: bool = True,
        max_bytes: int = 10_485_760,  # 10MB
        backup_count: int = 5
    ):
        """Initialize logger with custom configuration.
        
        Args:
            name: Logger name
            level: Logging level
            format_string: Log message format
            date_format: Date format in log messages
            log_file: Path to log file (optional)
            rotation: Whether to use rotating file handler
            max_bytes: Maximum bytes per log file
            backup_count: Number of backup files to keep
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(format_string, date_format)
        
        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_file:
            if rotation:
                from logging.handlers import RotatingFileHandler
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=max_bytes,
                    backupCount=backup_count
                )
            else:
                file_handler = logging.FileHandler(log_file)
            
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message."""
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log exception message with traceback."""
        self.logger.exception(msg, *args, **kwargs)

def setup_logging(
    config: Dict[str, Any],
    default_level: int = logging.INFO
) -> None:
    """Set up logging configuration from a dictionary.
    
    Args:
        config: Logging configuration dictionary
        default_level: Default logging level if config fails
    """
    try:
        logging.config.dictConfig(config)
    except Exception as e:
        print(f"Error in logging configuration: {e}")
        print("Using default logging configuration")
        logging.basicConfig(level=default_level)

def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None
) -> Logger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Path to log file (optional)
    
    Returns:
        Configured Logger instance
    """
    return Logger(name, level, log_file=log_file)

class LogContext:
    """Context manager for temporary logging configuration."""
    
    def __init__(self, logger: Logger, **kwargs: Any):
        """Initialize with logger and temporary settings.
        
        Args:
            logger: Logger instance to modify
            **kwargs: Temporary logger settings
        """
        self.logger = logger
        self.kwargs = kwargs
        self.old_settings = {}

    def __enter__(self) -> Logger:
        """Save current settings and apply temporary ones."""
        for key, value in self.kwargs.items():
            if hasattr(self.logger, key):
                self.old_settings[key] = getattr(self.logger, key)
                setattr(self.logger, key, value)
        return self.logger

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Restore original settings."""
        for key, value in self.old_settings.items():
            setattr(self.logger, key, value)

def create_timed_rotating_logger(
    name: str,
    log_dir: Union[str, Path],
    when: str = 'midnight',
    interval: int = 1,
    backup_count: int = 7
) -> Logger:
    """Create a logger that rotates files based on time.
    
    Args:
        name: Logger name
        log_dir: Directory for log files
        when: When to rotate ('S', 'M', 'H', 'D', 'midnight')
        interval: Interval between rotations
        backup_count: Number of backup files to keep
    
    Returns:
        Configured Logger instance
    """
    from logging.handlers import TimedRotatingFileHandler
    
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"{name}_{datetime.now():%Y%m%d}.log"
    
    logger = Logger(name)
    handler = TimedRotatingFileHandler(
        log_file,
        when=when,
        interval=interval,
        backupCount=backup_count
    )
    
    logger.logger.addHandler(handler)
    return logger