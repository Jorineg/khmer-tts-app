"""
Language selector component for the application UI
"""

import logging
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

logger = logging.getLogger(__name__)

class LanguageSelector(QWidget):
    """Widget for selecting the UI language"""
    
    # Signal emitted when language is changed
    languageChanged = pyqtSignal(str)
    
    def __init__(self, parent=None, translation_manager=None):
        """
        Initialize the language selector.
        
        Args:
            parent: Parent widget
            translation_manager: Translation manager for UI strings (deprecated - singleton instance used instead)
        """
        super().__init__(parent)
        
        # Always use singleton instance
        from ..i18n.translation_manager import translation_manager as tm_singleton
        self.translation_manager = tm_singleton  # Always use the singleton instance
        logger.info(f"LanguageSelector using singleton TranslationManager instance with language: {self.translation_manager.current_language}")
        
        self.current_language = self.translation_manager.get_current_language()
            
        self.setup_ui()
        self.update_button_styles()
    
    def setup_ui(self):
        """Set up the selector UI with hyperlink-style buttons"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Spacing between elements
        
        # English language button
        self.en_button = QPushButton("English")
        self.en_button.setCursor(Qt.PointingHandCursor)
        self.en_button.setFlat(True)
        self.en_button.clicked.connect(lambda: self.on_language_button_clicked("en"))
        self.en_button.setProperty("lang_code", "en")
        
        # Vertical separator
        self.separator = QLabel("|")
        
        # Khmer language button
        self.km_button = QPushButton("ខ្មែរ")
        self.km_button.setCursor(Qt.PointingHandCursor)
        self.km_button.setFlat(True)
        self.km_button.clicked.connect(lambda: self.on_language_button_clicked("km"))
        self.km_button.setProperty("lang_code", "km")
        
        # Add widgets to layout
        layout.addWidget(self.en_button)
        layout.addWidget(self.separator)
        layout.addWidget(self.km_button)
        
        # Remove the stretch that pushed buttons to right - we want them aligned left now
        # since the selector is on the left side of the window
        
        self.setLayout(layout)
        
        # Apply hyperlink style to buttons
        self.set_hyperlink_style()
    
    def set_hyperlink_style(self):
        """Set hyperlink-like style for language buttons"""
        base_style = """
            QPushButton {
                color: #0078D7;
                background-color: transparent;
                border: none;
                padding: 2px;
                text-align: center;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        
        self.en_button.setStyleSheet(base_style)
        self.km_button.setStyleSheet(base_style)
    
    def update_button_styles(self):
        """Update button styles to show the selected language"""
        # Get selected and non-selected buttons
        selected_button = self.en_button if self.current_language == "en" else self.km_button
        non_selected_button = self.km_button if self.current_language == "en" else self.en_button
        
        # Set specific styles for selected and non-selected buttons
        selected_style = """
            QPushButton {
                color: #0078D7;
                background-color: transparent;
                border: none;
                padding: 2px;
                text-align: center;
                font-weight: bold;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        
        non_selected_style = """
            QPushButton {
                color: #0078D7;
                background-color: transparent;
                border: none;
                padding: 2px;
                text-align: center;
                font-weight: normal;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        
        # Apply the appropriate styles
        selected_button.setStyleSheet(selected_style)
        non_selected_button.setStyleSheet(non_selected_style)
    
    def get_string(self, key, **kwargs):
        """Get a translated string using the translation manager"""
        if self.translation_manager:
            return self.translation_manager.get_string(key, **kwargs)
        return key
    
    def on_language_button_clicked(self, language_code):
        """Handle language button click"""
        logger.info(f"Language button clicked: {language_code}, current: {self.current_language}")
        if language_code == self.current_language:
            logger.info("No change needed - same language")
            return
            
        self.current_language = language_code
        
        # Update translation manager if available
        if self.translation_manager:
            logger.info(f"Setting language in translation manager to {language_code}")
            self.translation_manager.set_language(language_code)
        else:
            logger.warning("Translation manager not available")
        
        # Update button styles
        self.update_button_styles()
        
        # Emit signal with new language
        logger.info(f"Emitting languageChanged signal with {language_code}")
        self.languageChanged.emit(language_code)
    
    def update_language(self):
        """Update UI text for the current language"""
        # Nothing to update here since the button texts are static
        pass
    
    def get_current_language(self):
        """Get the currently selected language code"""
        return self.current_language
    
    def set_language(self, lang_code):
        """Set the current language"""
        if lang_code not in ["en", "km"]:
            logger.warning(f"Unsupported language code: {lang_code}")
            return
            
        self.current_language = lang_code
        self.update_button_styles()
        
        # Also update the translation manager when setting language from settings
        if self.translation_manager and self.translation_manager.get_current_language() != lang_code:
            logger.info(f"Setting TranslationManager language to {lang_code} from set_language()")
            self.translation_manager.set_language(lang_code)
