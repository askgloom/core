"""
Browser profile management for Ask Gloom Core.
Handles profile creation, loading, and configuration.
"""

import os
import json
import shutil
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from ..exceptions.core_exceptions import ProfileException

logger = logging.getLogger(__name__)

class Profile:
    """
    Manages browser profiles including preferences, extensions, and cookies.
    """

    def __init__(
        self,
        profile_path: Optional[str] = None,
        create_if_missing: bool = True
    ):
        """
        Initialize profile manager.

        Args:
            profile_path (str, optional): Path to profile directory
            create_if_missing (bool): Create profile if it doesn't exist
        """
        self.path = profile_path or self._get_default_profile_path()
        self.preferences: Dict[str, Any] = {}
        
        if create_if_missing:
            self._ensure_profile_exists()
        
        self.load_profile()

    def _get_default_profile_path(self) -> str:
        """Get default profile path based on OS."""
        home = Path.home()
        
        if os.name == 'nt':  # Windows
            return str(home / 'AppData' / 'Local' / 'AskGloom' / 'Profiles' / 'Default')
        else:  # Unix-like
            return str(home / '.config' / 'askgloom' / 'profiles' / 'default')

    def _ensure_profile_exists(self) -> None:
        """Create profile directory structure if it doesn't exist."""
        try:
            profile_dir = Path(self.path)
            
            # Create main profile directory
            profile_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            (profile_dir / 'Extensions').mkdir(exist_ok=True)
            (profile_dir / 'Cache').mkdir(exist_ok=True)
            
            # Create default preferences if they don't exist
            prefs_file = profile_dir / 'Preferences'
            if not prefs_file.exists():
                self._create_default_preferences(prefs_file)
                
            logger.debug(f"Profile directory structure created at {self.path}")
            
        except Exception as e:
            logger.error(f"Failed to create profile directory: {str(e)}")
            raise ProfileException(f"Profile creation failed: {str(e)}")

    def _create_default_preferences(self, prefs_file: Path) -> None:
        """Create default preferences file."""
        default_prefs = {
            "profile": {
                "name": "Default",
                "created_at": "",  # Will be set when saving
            },
            "browser": {
                "window_size": {
                    "width": 1920,
                    "height": 1080
                },
                "startup_page": "about:blank",
                "download_path": str(Path(self.path) / "Downloads")
            },
            "privacy": {
                "clear_on_exit": False,
                "block_third_party_cookies": True
            }
        }
        
        self.save_preferences(default_prefs)

    def load_profile(self) -> None:
        """Load profile preferences and settings."""
        try:
            prefs_file = Path(self.path) / 'Preferences'
            if prefs_file.exists():
                with open(prefs_file, 'r', encoding='utf-8') as f:
                    self.preferences = json.load(f)
                logger.debug("Profile preferences loaded successfully")
            else:
                logger.warning("No preferences file found, using defaults")
                self._create_default_preferences(prefs_file)
                
        except Exception as e:
            logger.error(f"Failed to load profile: {str(e)}")
            raise ProfileException(f"Profile loading failed: {str(e)}")

    def save_preferences(self, preferences: Optional[Dict[str, Any]] = None) -> None:
        """
        Save preferences to profile directory.

        Args:
            preferences (Dict[str, Any], optional): Preferences to save
        """
        try:
            if preferences is not None:
                self.preferences = preferences
                
            prefs_file = Path(self.path) / 'Preferences'
            with open(prefs_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=4)
                
            logger.debug("Profile preferences saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save preferences: {str(e)}")
            raise ProfileException(f"Failed to save preferences: {str(e)}")

    def delete(self) -> None:
        """Delete profile directory and all contents."""
        try:
            shutil.rmtree(self.path)
            logger.info(f"Profile deleted: {self.path}")
        except Exception as e:
            logger.error(f"Failed to delete profile: {str(e)}")
            raise ProfileException(f"Profile deletion failed: {str(e)}")

    def get_extension_path(self, extension_id: str) -> str:
        """
        Get path to specific extension.

        Args:
            extension_id (str): Extension ID

        Returns:
            str: Path to extension directory
        """
        return str(Path(self.path) / 'Extensions' / extension_id)

    def clear_cache(self) -> None:
        """Clear profile cache."""
        try:
            cache_dir = Path(self.path) / 'Cache'
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                cache_dir.mkdir()
            logger.debug("Profile cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {str(e)}")
            raise ProfileException(f"Cache clearing failed: {str(e)}")