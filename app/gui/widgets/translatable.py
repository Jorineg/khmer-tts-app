"""
Translatable UI widget classes that automatically handle language updates.

These classes use multi-inheritance to combine Qt widget functionality with
automatic translation capabilities. Each widget registers itself with the
translation manager and handles its own updates when the language changes.
"""

import logging
import re
from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QCheckBox, QRadioButton, QLineEdit, QAction

# Import the global translation manager instance
from ...i18n.translation_manager import translation_manager

# Global registry of all translatable widgets
_translatable_widgets = []

logger = logging.getLogger(__name__)

class TranslatableMixin:
    """
    Mixin class that provides translation capabilities to Qt widgets.
    
    This mixin is designed to be used with multi-inheritance to create
    translatable versions of standard Qt widgets.
    """
    
    def __init__(self, string_key):
        """
        Initialize the translatable mixin.
        
        Args:
            string_key: The translation key to use for this widget
                        OR a template string with <<key>> placeholders
                        For example: "Click <a href='#'><<buttons.here>></a> to continue"
        """
        # Don't call super() here - it will be called by the concrete widget class
        self.string_key = string_key
        
        # Register with global registry
        _translatable_widgets.append(self)
        
        # Update the initial text
        self.update_text()
    
    def get_string(self, key=None, **kwargs):
        """Get the translated string for this widget"""
        if not key:
            key = self.string_key
            
        # Check if this is a template string (containing <<key>>)
        if "<<" in key and ">>" in key:
            return self._process_template(key, **kwargs)
        else:
            # Simple translation key
            if translation_manager:
                return translation_manager.get_string(key, **kwargs)
            return key
    
    def _process_template(self, template, **kwargs):
        """Process a template string with <<key>> placeholders"""
        # Define a regex pattern to match <<key>> placeholders
        pattern = r'<<([^<>]+)>>'
        
        # Find all matches
        def replace(match):
            key = match.group(1)
            # Get the translation for this key
            if translation_manager:
                return translation_manager.get_string(key, **kwargs)
            else:
                logger.warning(f"Translation manager not initialized for key: {key}")
            return key
            
        
        # Replace all <<key>> with their translations
        result = re.sub(pattern, replace, template)
        return result
    
    def update_text(self):
        """Update the text for this widget"""
        translated_text = self.get_string()
        self._update_text(translated_text)
    
    def _update_text(self, text):
        """
        Abstract method to update the actual widget text.
        
        This should be implemented by each specific widget class.
        """
        pass


class TranslatableLabel(TranslatableMixin, QLabel):
    def __init__(self, string_key, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setText(text)


class TranslatableGroupBox(TranslatableMixin, QGroupBox):
    def __init__(self, string_key, *args, **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setTitle(text)


class TranslatablePushButton(TranslatableMixin, QPushButton):
    def __init__(self, string_key, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setText(text)


class TranslatableCheckBox(TranslatableMixin, QCheckBox):
    def __init__(self, string_key, *args, **kwargs):
        QCheckBox.__init__(self, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setText(text)


class TranslatableRadioButton(TranslatableMixin, QRadioButton):
    def __init__(self, string_key, *args, **kwargs):
        QRadioButton.__init__(self, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setText(text)


class TranslatableLineEdit(TranslatableMixin, QLineEdit):
    def __init__(self, string_key, *args, **kwargs):
        QLineEdit.__init__(self, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setPlaceholderText(text)


class TranslatableQAction(TranslatableMixin, QAction):
    def __init__(self, string_key, parent=None, *args, **kwargs):
        QAction.__init__(self, parent, *args, **kwargs)
        TranslatableMixin.__init__(self, string_key)
    
    def _update_text(self, text):
        self.setText(text)


# Function to update all translatable widgets
def update_all_translatable_widgets():
    """Update all translatable widgets that have been created"""
    logger.debug(f"Updating {len(_translatable_widgets)} translatable widgets")
    for widget in _translatable_widgets[:]:
        try:
            # if not widget.isVisible():
            #     # Widget might have been destroyed
            #     _translatable_widgets.remove(widget)
            #     continue
                
            widget.update_text()
        except RuntimeError:
            # Widget has been deleted
            _translatable_widgets.remove(widget)
        except Exception as e:
            logger.error(f"Error updating widget: {e}")

# Ensure translation signals are connected (called when translatable.py is imported)
def ensure_translation_signals_connected():
    """Ensure signal is connected to update function"""
    logger.debug("Setting up translation signals...")
    try:
        # First try to disconnect to avoid duplicate connections
        translation_manager.language_changed.disconnect(update_all_translatable_widgets)
        logger.debug("Successfully disconnected existing signal")
    except (TypeError, RuntimeError) as e:
        # Signal was not connected, which is fine
        logger.debug(f"Signal was not previously connected: {e}")
        pass
    
    # Connect the signal
    try:
        translation_manager.language_changed.connect(update_all_translatable_widgets)
        logger.debug(f"Translation signal connected! Registered widgets: {len(_translatable_widgets)}")
        
        # Test the connection by directly calling update_all_translatable_widgets
        logger.debug("Testing signal by directly calling update_all_translatable_widgets")
        update_all_translatable_widgets()
        logger.debug("Signal test completed")
        
        return True
    except Exception as e:
        logger.error(f"Failed to connect signal: {e}")
        return False

# This will try to connect immediately when the module is imported
_connection_established = ensure_translation_signals_connected()
logger.debug(f"Translatable module initialized, connection status: {_connection_established}")
logger.debug("Translation manager initialization completed")
logger.debug("Translation manager initialized")
