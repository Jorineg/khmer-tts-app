"""
Settings manager to handle application settings and API keys
"""

import os
import json
import logging
import sys
import winreg
from PyQt5.QtCore import QSettings
import keyring
import keyring.errors

logger = logging.getLogger(__name__)

# Constants
APP_NAME = "KhmerSTT"
SETTINGS_FILE = "settings.json"
API_KEY_SERVICE = "KhmerSTTApp"

class SettingsManager:
    """
    Manager class for handling application settings and API keys
    """
    
    def __init__(self):
        """Initialize the settings manager"""
        self.settings = QSettings(APP_NAME, APP_NAME)
        
        # Default settings
        self.defaults = {
            "shortcut": "ctrl+alt+space",
            "transcription_model": "gemini_flash",
            "language": "khm",
            "show_overlay": True,
            "overlay_position": "bottom",
            "run_on_startup": True,
            "minimize_to_tray": True,
        }
        
        # Initialize settings with defaults if they don't exist
        self._initialize_settings()
        
        # Sync registry with settings
        self.sync_autostart_with_setting()
    
    def _initialize_settings(self):
        """Initialize settings with default values if they don't exist"""
        for key, value in self.defaults.items():
            if not self.settings.contains(key):
                self.settings.setValue(key, value)
    
    def get_setting(self, key, default=None):
        """
        Get a setting value
        
        Args:
            key: Setting key
            default: Default value if setting doesn't exist
            
        Returns:
            Setting value
        """
        if default is None and key in self.defaults:
            default = self.defaults[key]
            
        value = self.settings.value(key, default)
        
        # Convert string representations of bool back to bool
        if isinstance(default, bool) and isinstance(value, str):
            return value.lower() in ('true', 'yes', '1')
            
        return value
    
    def set_setting(self, key, value):
        """
        Set a setting value
        
        Args:
            key: Setting key
            value: Setting value
        """
        self.settings.setValue(key, value)
        self.settings.sync()
        
        # Update autostart if this setting changed
        if key == "run_on_startup":
            self.update_autostart_status()
    
    def get_api_key(self, service):
        """
        Get API key from Windows Credentials Manager
        
        Args:
            service: Service name (google, elevenlabs)
            
        Returns:
            API key or None if not found
        """
        try:
            # Get API key from Windows Credentials Manager
            return keyring.get_password(API_KEY_SERVICE, service)
        except keyring.errors.KeyringError as e:
            logger.error(f"Failed to get API key for {service}: {str(e)}")
            return None
    
    def set_api_key(self, service, api_key):
        """
        Set API key in Windows Credentials Manager
        
        Args:
            service: Service name (google, elevenlabs)
            api_key: API key to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Store API key in Windows Credentials Manager
            keyring.set_password(API_KEY_SERVICE, service, api_key)
            return True
        except keyring.errors.KeyringError as e:
            logger.error(f"Failed to set API key for {service}: {str(e)}")
            return False
    
    def get_available_languages(self):
        """
        Get a list of available languages with their codes
        
        Returns:
            Dictionary of language names and codes
        """
        # Common languages and their ISO codes
        languages = {
            "Khmer": "khm",
            "English": "eng",
            "Thai": "tha",
            "Vietnamese": "vie",
            "Chinese": "zho",
            "Japanese": "jpn",
            "Korean": "kor",
            "French": "fra",
            "Spanish": "spa",
            "German": "deu",
            "Russian": "rus",
            "Arabic": "ara",
            "Hindi": "hin"
        }
        
        return languages
        
    def update_autostart_status(self):
        """Update autostart registry based on current setting"""
        run_on_startup = self.get_setting("run_on_startup", True)
        self.set_autostart_registry(run_on_startup)
        
    def sync_autostart_with_setting(self):
        """
        Sync the registry autostart status with the application setting.
        This ensures registry and settings are aligned at startup.
        """
        run_on_startup = self.get_setting("run_on_startup", True)
        registry_status = self.check_autostart_status()
        
        # If there's a mismatch, update the registry to match the setting
        if run_on_startup != registry_status:
            self.set_autostart_registry(run_on_startup)
    
    def set_autostart_registry(self, enable=True):
        """
        Set or remove autostart registry entry
        
        Args:
            enable: Whether to enable or disable autostart
            
        Returns:
            True if successful, False otherwise
        """
        app_path = sys.executable
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )
            
            if enable:
                winreg.SetValueEx(registry_key, APP_NAME, 0, winreg.REG_SZ, f'"{app_path}"')
                logger.info(f"Added {APP_NAME} to startup registry")
            else:
                try:
                    winreg.DeleteValue(registry_key, APP_NAME)
                    logger.info(f"Removed {APP_NAME} from startup registry")
                except FileNotFoundError:
                    # Key doesn't exist, nothing to delete
                    pass
                    
            winreg.CloseKey(registry_key)
            return True
            
        except Exception as e:
            logger.error(f"Error managing autostart registry: {str(e)}")
            return False
    
    def check_autostart_status(self):
        """
        Check if application is set to autostart in registry
        
        Returns:
            True if enabled, False otherwise
        """
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            
            try:
                value, _ = winreg.QueryValueEx(registry_key, APP_NAME)
                winreg.CloseKey(registry_key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(registry_key)
                return False
                
        except Exception as e:
            logger.error(f"Error checking autostart registry: {str(e)}")
            return False
