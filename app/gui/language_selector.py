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
        Initialize the language selector widget
        
        Args:
            parent: Parent widget
            translation_manager: Translation manager for UI strings
        """
        super().__init__(parent)
        self.translation_manager = translation_manager
        self.current_language = "en"  # Default language
        
        # Set current language from translation manager if available
        if self.translation_manager:
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
        
        # Add stretch to push the controls to the right
        layout.addStretch(1)
        
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
        if language_code == self.current_language:
            return
            
        self.current_language = language_code
        
        # Update translation manager if available
        if self.translation_manager:
            self.translation_manager.set_language(language_code)
        
        # Update button styles
        self.update_button_styles()
        
        # Emit signal with new language
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
