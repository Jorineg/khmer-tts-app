"""
API keys settings tab for the main application window
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QLabel)
from PyQt5.QtCore import pyqtSignal, Qt

from ..widgets import ( 
    TranslatableLabel,
    TranslatableGroupBox,
    TranslatableLineEdit
)
from ..styles.app_stylesheet import (
    get_group_box_style, get_description_label_style, 
    get_link_style, get_status_label_style
)
from ...i18n.translation_manager import translation_manager

logger = logging.getLogger(__name__)

class ApiKeysTab(QWidget):
    """API keys settings tab for managing service credentials"""
    
    # Signal emitted when API keys change
    api_key_changed = pyqtSignal(str, str)  # service_name, new_value
    
    def __init__(self, parent=None, settings_manager=None, translation_manager=None):
        """
        Initialize the API keys tab
        
        Args:
            parent: Parent widget
            settings_manager: Settings manager for accessing/saving settings
            translation_manager: Translation manager for UI strings (deprecated - singleton instance used instead)
        """
        super().__init__(parent)
        self.parent = parent
        self.settings_manager = settings_manager
        # We're using the singleton imported at the top of the file
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the tab UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Google API key group
        self.google_group = TranslatableGroupBox("<<api_keys_tab.google_api_key>>")
        self.google_group.setStyleSheet(get_group_box_style())
        google_layout = QVBoxLayout()
        google_layout.setContentsMargins(15, 15, 15, 15)
        
        # Google API key description
        self.google_description = TranslatableLabel("<<api_keys_tab.google_description>>")
        self.google_description.setWordWrap(True)
        self.google_description.setStyleSheet(get_description_label_style())
        google_layout.addWidget(self.google_description)
        
        # Link to get API key
        self.google_link = TranslatableLabel(
            "<a href='https://aistudio.google.com/apikey'><<api_keys_tab.google_get_key>></a>"
        )
        self.google_link.setOpenExternalLinks(True)
        self.google_link.setStyleSheet(get_link_style())
        google_layout.addWidget(self.google_link)
        
        # API key input
        self.google_api_key_input = TranslatableLineEdit("<<api_keys_tab.api_key_placeholder>>")
        self.google_api_key_input.setEchoMode(QLineEdit.Password)
        self.google_api_key_input.textChanged.connect(self.on_google_api_key_changed)
        google_layout.addWidget(self.google_api_key_input)
        
        # API key status
        self.google_status_label = TranslatableLabel("")
        self.google_status_label.setStyleSheet(get_status_label_style())
        google_layout.addWidget(self.google_status_label)
        
        self.google_group.setLayout(google_layout)
        layout.addWidget(self.google_group)
        
        # ElevenLabs API key group
        self.elevenlabs_group = TranslatableGroupBox("<<api_keys_tab.elevenlabs_api_key>>")
        self.elevenlabs_group.setStyleSheet(get_group_box_style())
        elevenlabs_layout = QVBoxLayout()
        elevenlabs_layout.setContentsMargins(15, 15, 15, 15)
        
        # ElevenLabs API key description
        self.elevenlabs_description = TranslatableLabel("<<api_keys_tab.elevenlabs_description>>")
        self.elevenlabs_description.setWordWrap(True)
        self.elevenlabs_description.setTextFormat(Qt.RichText)
        self.elevenlabs_description.setStyleSheet(get_description_label_style())
        elevenlabs_layout.addWidget(self.elevenlabs_description)
        
        # Link to get API key
        self.elevenlabs_link = TranslatableLabel(
            "<a href='https://elevenlabs.io/api'><<api_keys_tab.elevenlabs_get_key>></a>"
        )
        self.elevenlabs_link.setOpenExternalLinks(True)
        self.elevenlabs_link.setStyleSheet(get_link_style())
        elevenlabs_layout.addWidget(self.elevenlabs_link)
        
        # API key input
        self.elevenlabs_api_key_input = TranslatableLineEdit("<<api_keys_tab.api_key_placeholder>>")
        self.elevenlabs_api_key_input.setEchoMode(QLineEdit.Password)
        self.elevenlabs_api_key_input.textChanged.connect(self.on_elevenlabs_api_key_changed)
        elevenlabs_layout.addWidget(self.elevenlabs_api_key_input)
        
        # API key status
        self.elevenlabs_status_label = TranslatableLabel("")
        self.elevenlabs_status_label.setStyleSheet(get_status_label_style())
        elevenlabs_layout.addWidget(self.elevenlabs_status_label)
        
        self.elevenlabs_group.setLayout(elevenlabs_layout)
        layout.addWidget(self.elevenlabs_group)
        
        # Add spacer at the bottom
        layout.addStretch()
        
        self.setLayout(layout)
    
    def get_placeholder_text(self, key):
        """Get placeholder text for input fields"""
        return translation_manager.get_string(key)
    
    def load_settings(self):
        """Load settings from the settings manager"""
        if not self.settings_manager:
            return
            
        # Load API keys from secure storage
        google_api_key = self.settings_manager.get_api_key("google")
        self.google_api_key_input.setText(google_api_key or "")
        
        elevenlabs_api_key = self.settings_manager.get_api_key("elevenlabs")
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
            self.settings_manager.set_api_key("google", api_key)
            
        # Emit signal that key changed
        self.api_key_changed.emit("google", api_key)
    
    def on_elevenlabs_api_key_changed(self):
        """Handle ElevenLabs API key change"""
        api_key = self.elevenlabs_api_key_input.text()
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_api_key("elevenlabs", api_key)
            
        # Emit signal that key changed
        self.api_key_changed.emit("elevenlabs", api_key)
