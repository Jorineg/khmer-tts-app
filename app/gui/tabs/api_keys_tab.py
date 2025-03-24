"""
API keys settings tab for the main application window
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                            QGroupBox, QLabel, QLineEdit)
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)

class ApiKeysTab(QWidget):
    """API keys settings tab for managing service credentials"""
    
    def __init__(self, parent=None, settings_manager=None, translation_manager=None):
        """
        Initialize the API keys tab
        
        Args:
            parent: Parent widget
            settings_manager: Settings manager for accessing/saving settings
            translation_manager: Translation manager for UI strings
        """
        super().__init__(parent)
        self.parent = parent
        self.settings_manager = settings_manager
        self.translation_manager = translation_manager
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the tab UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Google API key group
        self.google_group = QGroupBox(self.get_string("api_keys_tab.google_api_key"))
        self.google_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2980b9; }")
        google_layout = QVBoxLayout()
        google_layout.setContentsMargins(15, 15, 15, 15)
        
        # Google API key description
        self.google_description = QLabel(self.get_string("api_keys_tab.google_description"))
        self.google_description.setWordWrap(True)
        self.google_description.setStyleSheet("color: #34495e; line-height: 1.4;")
        google_layout.addWidget(self.google_description)
        
        # Link to get API key
        self.google_link = QLabel(f"<a href='https://aistudio.google.com/apikey'>{self.get_string('api_keys_tab.google_get_key')}</a>")
        self.google_link.setOpenExternalLinks(True)
        self.google_link.setStyleSheet("margin-top: 5px; margin-bottom: 10px; color: #2980b9;")
        google_layout.addWidget(self.google_link)
        
        # API key input
        self.google_api_key_input = QLineEdit()
        self.google_api_key_input.setPlaceholderText(self.get_string("api_keys_tab.api_key_placeholder"))
        self.google_api_key_input.setEchoMode(QLineEdit.Password)
        self.google_api_key_input.textChanged.connect(self.on_google_api_key_changed)
        google_layout.addWidget(self.google_api_key_input)
        
        # API key status
        self.google_status_label = QLabel("")
        self.google_status_label.setStyleSheet("color: #7f8c8d; margin-top: 5px;")
        google_layout.addWidget(self.google_status_label)
        
        self.google_group.setLayout(google_layout)
        layout.addWidget(self.google_group)
        
        # ElevenLabs API key group
        self.elevenlabs_group = QGroupBox(self.get_string("api_keys_tab.elevenlabs_api_key"))
        self.elevenlabs_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2980b9; }")
        elevenlabs_layout = QVBoxLayout()
        elevenlabs_layout.setContentsMargins(15, 15, 15, 15)
        
        # ElevenLabs API key description
        self.elevenlabs_description = QLabel(self.get_string("api_keys_tab.elevenlabs_description"))
        self.elevenlabs_description.setWordWrap(True)
        self.elevenlabs_description.setStyleSheet("color: #34495e; line-height: 1.4;")
        elevenlabs_layout.addWidget(self.elevenlabs_description)
        
        # Link to get API key
        self.elevenlabs_link = QLabel(f"<a href='https://elevenlabs.io/api'>{self.get_string('api_keys_tab.elevenlabs_get_key')}</a>")
        self.elevenlabs_link.setOpenExternalLinks(True)
        self.elevenlabs_link.setStyleSheet("margin-top: 5px; margin-bottom: 10px; color: #2980b9;")
        elevenlabs_layout.addWidget(self.elevenlabs_link)
        
        # API key input
        self.elevenlabs_api_key_input = QLineEdit()
        self.elevenlabs_api_key_input.setPlaceholderText(self.get_string("api_keys_tab.api_key_placeholder"))
        self.elevenlabs_api_key_input.setEchoMode(QLineEdit.Password)
        self.elevenlabs_api_key_input.textChanged.connect(self.on_elevenlabs_api_key_changed)
        elevenlabs_layout.addWidget(self.elevenlabs_api_key_input)
        
        # API key status
        self.elevenlabs_status_label = QLabel("")
        self.elevenlabs_status_label.setStyleSheet("color: #7f8c8d; margin-top: 5px;")
        elevenlabs_layout.addWidget(self.elevenlabs_status_label)
        
        self.elevenlabs_group.setLayout(elevenlabs_layout)
        layout.addWidget(self.elevenlabs_group)
        
        # Add spacer at the bottom
        layout.addStretch()
        
        self.setLayout(layout)
    
    def get_string(self, key, **kwargs):
        """Get a translated string using the translation manager"""
        if self.translation_manager:
            return self.translation_manager.get_string(key, **kwargs)
        return key
    
    def load_settings(self):
        """Load settings from the settings manager"""
        if not self.settings_manager:
            return
            
        # Load API keys from secure storage
        google_api_key = self.settings_manager.get_api_key("google_api_key")
        self.google_api_key_input.setText(google_api_key or "")
        
        elevenlabs_api_key = self.settings_manager.get_api_key("elevenlabs_api_key")
        self.elevenlabs_api_key_input.setText(elevenlabs_api_key or "")
    
    def connect_signals(self):
        """Connect signal handlers for UI controls"""
        # API Key signals
        self.google_api_key_input.editingFinished.connect(self.on_google_api_key_changed)
        self.elevenlabs_api_key_input.editingFinished.connect(self.on_elevenlabs_api_key_changed)
    
    def on_google_api_key_changed(self):
        """Handle Google API key change"""
        api_key = self.google_api_key_input.text()
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_api_key("google_api_key", api_key)
    
    def on_elevenlabs_api_key_changed(self):
        """Handle ElevenLabs API key change"""
        api_key = self.elevenlabs_api_key_input.text()
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_api_key("elevenlabs_api_key", api_key)
    
    def update_language(self):
        """Update UI text for the current language"""
        # Update group titles
        self.google_group.setTitle(self.get_string("api_keys_tab.google_api_key"))
        self.elevenlabs_group.setTitle(self.get_string("api_keys_tab.elevenlabs_api_key"))
        
        # Update descriptions and links
        # For Google group
        self.google_description.setText(self.get_string("api_keys_tab.google_description"))
        self.google_link.setText(f"<a href='https://aistudio.google.com/apikey'>{self.get_string('api_keys_tab.google_get_key')}</a>")
        
        # For ElevenLabs group
        self.elevenlabs_description.setText(self.get_string("api_keys_tab.elevenlabs_description"))
        self.elevenlabs_link.setText(f"<a href='https://elevenlabs.io/api'>{self.get_string('api_keys_tab.elevenlabs_get_key')}</a>")
        
        # Update input placeholders
        self.google_api_key_input.setPlaceholderText(self.get_string("api_keys_tab.api_key_placeholder"))
        self.elevenlabs_api_key_input.setPlaceholderText(self.get_string("api_keys_tab.api_key_placeholder"))
