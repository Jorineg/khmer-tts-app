"""
Translation manager for the application
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

class TranslationManager:
    """Manager for handling translations in the application"""
    
    def __init__(self, settings_manager=None):
        """
        Initialize the translation manager
        
        Args:
            settings_manager: Optional SettingsManager instance to save/load UI language preference
        """
        self.settings_manager = settings_manager
        self.strings = {}
        self.current_language = "en"  # Default language
        
        # Load translations from file
        self.load_translations()
        
        # Set initial language from settings if available
        if settings_manager:
            self.current_language = settings_manager.get_setting("ui_language")
    
    def load_translations(self):
        """Load translations from the JSON file"""
        try:
            # Get the path to the strings.json file
            strings_file = os.path.join(os.path.dirname(__file__), "strings.json")
            
            # Check if file exists
            if not os.path.exists(strings_file):
                logger.error(f"Translation file not found: {strings_file}")
                return
            
            # Load the JSON data
            with open(strings_file, 'r', encoding='utf-8') as f:
                self.strings = json.load(f)
                
            logger.info(f"Translations loaded successfully from {strings_file}")
            
        except Exception as e:
            logger.error(f"Error loading translations: {str(e)}")
    
    def get_string(self, key, default=None, **kwargs):
        """
        Get a translated string by key
        
        Args:
            key: The string key (can be nested using dot notation, e.g., 'tabs.overview')
            default: Default value if key not found
            **kwargs: Format parameters for string placeholders
            
        Returns:
            The translated string
        """
        try:
            # Split the key by dots for nested access
            parts = key.split('.')
            value = self.strings
            
            # Navigate through the nested dictionary
            for part in parts:
                value = value[part]
            
            # Get the translation for the current language
            translation = value.get(self.current_language)
            
            # Fallback to English if translation not available
            if translation is None:
                translation = value.get("en", default)
                
            # Apply format parameters if any
            if kwargs and translation:
                translation = translation.format(**kwargs)
                
            return translation or default
            
        except (KeyError, AttributeError) as e:
            logger.warning(f"Translation key not found: {key}, error: {str(e)}")
            return default or key
    
    def set_language(self, language_code):
        """
        Set the current language
        
        Args:
            language_code: The language code to set (e.g., 'en', 'km')
            
        Returns:
            True if successful, False otherwise
        """
        if language_code in ["en", "km"]:
            self.current_language = language_code
            
            # Save language preference if settings manager available
            if self.settings_manager:
                self.settings_manager.set_setting("ui_language", language_code)
                self.settings_manager.save()
                
            logger.info(f"Language set to: {language_code}")
            return True
        else:
            logger.warning(f"Unsupported language code: {language_code}")
            return False
    
    def get_current_language(self):
        """Get the current language code"""
        return self.current_language
    
    def get_available_languages(self):
        """
        Get a dictionary of available languages
        
        Returns:
            Dictionary with language names as keys and codes as values
        """
        return {
            "English": "en",
            "ខ្មែរ": "km"  # Khmer
        }
