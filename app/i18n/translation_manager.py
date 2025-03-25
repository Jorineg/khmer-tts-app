"""
Translation manager for the application.
Handles loading and accessing UI strings in English and Khmer.
"""

import os
import json
import logging
import sys
from PyQt5.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)

# Singleton instance
_instance = None

class TranslationManager(QObject):
    """Manager for translations between English and Khmer"""
    
    # Signal emitted when the language changes
    language_changed = pyqtSignal(str)
    
    @staticmethod
    def get_instance():
        """Get or create the singleton instance of TranslationManager"""
        global _instance
        if _instance is None:
            logger.info("Creating singleton TranslationManager instance")
            _instance = TranslationManager()
        return _instance
    
    def __init__(self):
        """Initialize the translation manager with default language set to English"""
        super().__init__()
        
        # Initialize default values
        self.current_language = "en"
        self.strings = {"en": {}, "km": {}}
        
        # Load the translation strings from JSON file
        self._load_strings()
        
        logger.info("TranslationManager instance initialized")
    
    def _load_strings(self):
        """Load translation strings from JSON file"""
        try:
            # Get the base path (assumes this file is in app/i18n/)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            strings_path = os.path.join(base_path, "app", "i18n", "strings.json")
            
            # Try to load the strings file
            with open(strings_path, "r", encoding="utf-8") as f:
                self.strings = json.load(f)
                logger.info(f"Loaded translations from {strings_path}")
        except Exception as e:
            logger.error(f"Failed to load translations: {e}")
            # Set a default empty dictionary to prevent errors
            self.strings = {"en": {}, "km": {}}
    
    def set_language(self, language_code):
        """Set the current language (en or km)"""
        logger.info(f"TranslationManager.set_language called with language_code: {language_code}")
        
        # Only allow English or Khmer
        if language_code not in ["en", "km"]:
            logger.warning(f"Language {language_code} not supported, falling back to English")
            language_code = "en"
        
        # Set the current language
        prev_language = self.current_language
        self.current_language = language_code
        logger.info(f"Language changed from {prev_language} to: {language_code}")
        
        # Emit the language changed signal
        # The update_all_translatable_widgets function is connected to this signal
        # in translatable.py and will handle the updates automatically
        logger.info(f"About to emit language_changed signal with {language_code}")
        self.language_changed.emit(language_code)
        logger.info("Signal emitted")
    
    def get_string(self, key, **kwargs):
        """
        Get a translated string.
        
        Args:
            key: The string key to translate
            **kwargs: Optional parameters for string formatting
            
        Returns:
            The translated string or the key itself if not found
        """
        language = self.current_language or "en"
                
        # The JSON structure has keys at the top level, then languages nested within each key
        parts = key.split(".")
        current = self.strings
        
        # Navigate to the key in the nested dictionary structure
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                # Key not found
                logger.warning(f"Key {key} not found in translation strings")
                return key
        
        # Now we have the language dictionary, get the right language
        if isinstance(current, dict) and language in current:
            result = current[language]
            
            # Format the string if needed
            if isinstance(result, str) and kwargs:
                try:
                    return result.format(**kwargs)
                except KeyError as e:
                    logger.warning(f"Missing format key in translation: {e}")
                    return result
            return result
        elif isinstance(current, dict) and "en" in current:
            # Fall back to English if the requested language isn't available for this key
            logger.warning(f"Language {language} not found for key {key}, falling back to English")
            result = current["en"]
            
            # Format the string if needed
            if isinstance(result, str) and kwargs:
                try:
                    return result.format(**kwargs)
                except KeyError as e:
                    logger.warning(f"Missing format key in translation: {e}")
                    return result
            return result
        else:
            logger.warning(f"No translation available for key {key}")
            return key
        
    def get_template_string(self, template_string, **kwargs):
        """
        Get a translated string from a template containing {key} placeholders.
        
        Args:
            template_string: A string with translation keys in curly braces
                             For example: "Hello {greeting.world}! How are {greeting.you}?"
            **kwargs: Optional parameters for string formatting
            
        Returns:
            The template with all translation keys replaced with their translations
        """
        # Find all translation keys in the template
        import re
        keys = re.findall(r'\{([^{}]+)\}', template_string)
        
        # Replace each key with its translation
        result = template_string
        for key in keys:
            if '.' in key:  # Only treat as translation key if it contains a dot
                translation = self.get_string(key, **kwargs)
                result = result.replace(f"{{{key}}}", translation)
            # If no dot, it's probably a normal format key, leave it alone
        
        # Process any remaining format strings (like {name} from kwargs)
        if kwargs:
            try:
                result = result.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing format key in template: {e}")
        
        return result
    
    def has_string(self, key):
        """
        Check if a string key exists in the translation dictionary
        
        Args:
            key: The string key to check
            
        Returns:
            True if the key exists, False otherwise
        """
        parts = key.split(".")
        current = self.strings
        
        # Navigate to the key in the nested dictionary structure
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        # Check if it's a dictionary with language keys
        return isinstance(current, dict) and (
            self.current_language in current or "en" in current
        )
    
    def get_current_language(self):
        """Get the current language code (en or km)"""
        return self.current_language
    
    def get_available_languages(self):
        """Get the available languages (always en and km)"""
        return ["en", "km"]
    
    def get_language_name(self, language_code):
        """Get the display name of a language"""
        language_names = {
            "en": "English",
            "km": "ភាសាខ្មែរ",  # Khmer
        }
        return language_names.get(language_code, language_code)

# Create a single instance to be imported by other modules
translation_manager = TranslationManager.get_instance()
