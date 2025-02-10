"""
Configuration management for Ask Gloom Core.
Handles loading, saving, and validating configuration settings.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from ..exceptions.core_exceptions import ConfigurationException

logger = logging.getLogger(__name__)

class Config:
    """
    Manages configuration settings for Ask Gloom Core.
    Supports both global and local configurations.
    """

    DEFAULT_CONFIG = {
        "browser": {
            "default_profile": "default",
            "headless": False,
            "window_size": {
                "width": 1920,
                "height": 1080
            },
            "user_agent": None,
            "timeout": 30
        },
        "profiles": {
            "location": None,  # Will be set based on OS
            "create_on_start": True
        },
        "logging": {
            "level": "INFO",
            "file": None,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "automation": {
            "wait_time": 5,
            "retry_attempts": 3,
            "screenshot_on_error": True
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path (str, optional): Path to configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config: Dict[str, Any] = {}
        self.load_config()

    def _get_default_config_path(self) -> str:
        """Get default configuration file path based on OS."""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.getenv('APPDATA')) / 'AskGloom'
        else:  # Unix-like
            config_dir = Path.home() / '.config' / 'askgloom'

        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / 'config.json')

    def load_config(self) -> None:
        """Load configuration from file or create default."""
        try:
            config_file = Path(self.config_path)
            
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all required fields exist
                    self.config = self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
                logger.debug("Configuration loaded successfully")
            else:
                logger.info("No configuration file found, creating default")
                self.config = self.DEFAULT_CONFIG.copy()
                self._set_os_specific_defaults()
                self.save_config()

        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise ConfigurationException(f"Configuration loading failed: {str(e)}")

    def _set_os_specific_defaults(self) -> None:
        """Set OS-specific default values."""
        if os.name == 'nt':  # Windows
            profiles_location = str(Path(os.getenv('LOCALAPPDATA')) / 'AskGloom' / 'Profiles')
        else:  # Unix-like
            profiles_location = str(Path.home() / '.config' / 'askgloom' / 'profiles')

        self.config['profiles']['location'] = profiles_location

    def _merge_configs(self, default: Dict, custom: Dict) -> Dict:
        """
        Recursively merge custom config with defaults.
        
        Args:
            default (Dict): Default configuration
            custom (Dict): Custom configuration to merge
            
        Returns:
            Dict: Merged configuration
        """
        result = default.copy()
        
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
                
        return result

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            logger.debug("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}")
            raise ConfigurationException(f"Configuration saving failed: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key (str): Configuration key (dot notation supported)
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any, save: bool = True) -> None:
        """
        Set configuration value.
        
        Args:
            key (str): Configuration key (dot notation supported)
            value (Any): Value to set
            save (bool): Whether to save to file immediately
        """
        try:
            keys = key.split('.')
            current = self.config
            
            # Navigate to the correct nested level
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
                
            # Set the value
            current[keys[-1]] = value
            
            if save:
                self.save_config()
                
            logger.debug(f"Configuration updated: {key} = {value}")
            
        except Exception as e:
            logger.error(f"Failed to set configuration: {str(e)}")
            raise ConfigurationException(f"Failed to set configuration value: {str(e)}")

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self._set_os_specific_defaults()
        self.save_config()
        logger.info("Configuration reset to defaults")