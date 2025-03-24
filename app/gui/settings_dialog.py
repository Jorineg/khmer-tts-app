"""
Settings dialog for the application
"""

import os
import logging
from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QCheckBox, QGroupBox, QFormLayout, QSpinBox,
    QMessageBox, QRadioButton, QButtonGroup, QWidget
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon

from ..settings.settings_manager import SettingsManager

logger = logging.getLogger(__name__)

class SettingsDialog(QDialog):
    """Settings dialog for configuring the application"""
    
    def __init__(self, settings_manager, parent=None):
        """
        Initialize the settings dialog
        
        Args:
            settings_manager: SettingsManager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.settings_manager = settings_manager
        
        # Set up the UI
        self.setup_ui()
        
        # Load current settings
        self.load_settings()
        
    def setup_ui(self):
        """Set up the UI elements"""
        # Set window properties
        self.setWindowTitle("Settings")
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Create the tabs
        self.create_general_tab()
        self.create_api_keys_tab()
        self.create_language_tab()
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.api_keys_tab, "API Keys")
        self.tabs.addTab(self.language_tab, "Language")
        
        # Add tabs to layout
        layout.addWidget(self.tabs)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        buttons_layout.addWidget(self.save_button)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        # Add buttons to layout
        layout.addLayout(buttons_layout)
        
        # Set the layout
        self.setLayout(layout)
        
    def create_general_tab(self):
        """Create the general settings tab"""
        self.general_tab = QWidget()
        layout = QVBoxLayout()
        
        # Shortcut group
        shortcut_group = QGroupBox("Shortcut")
        shortcut_layout = QFormLayout()
        
        # Shortcut input
        self.shortcut_input = QLineEdit()
        self.shortcut_input.setPlaceholderText("Press shortcut to record")
        shortcut_layout.addRow("Recording shortcut:", self.shortcut_input)
        
        # Set the layout for the shortcut group
        shortcut_group.setLayout(shortcut_layout)
        
        # Transcription model group
        model_group = QGroupBox("Transcription Model")
        model_layout = QFormLayout()
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItem("Gemini Flash", "gemini_flash")
        self.model_combo.addItem("ElevenLabs", "elevenlabs")
        model_layout.addRow("Default model:", self.model_combo)
        
        # Set the layout for the model group
        model_group.setLayout(model_layout)
        
        # Appearance group
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout()
        
        # Show overlay checkbox
        self.show_overlay_checkbox = QCheckBox("Show overlay during recording and transcription")
        appearance_layout.addRow("", self.show_overlay_checkbox)
        
        # Overlay position
        self.overlay_position_combo = QComboBox()
        self.overlay_position_combo.addItem("Bottom", "bottom")
        self.overlay_position_combo.addItem("Top", "top")
        appearance_layout.addRow("Overlay position:", self.overlay_position_combo)
        
        # Set the layout for the appearance group
        appearance_group.setLayout(appearance_layout)
        
        # Startup group
        startup_group = QGroupBox("Startup")
        startup_layout = QFormLayout()
        
        # Run on startup checkbox
        self.run_on_startup_checkbox = QCheckBox("Run on Windows startup")
        startup_layout.addRow("", self.run_on_startup_checkbox)
        
        # Minimize to tray checkbox
        self.minimize_to_tray_checkbox = QCheckBox("Minimize to system tray on startup")
        startup_layout.addRow("", self.minimize_to_tray_checkbox)
        
        # Set the layout for the startup group
        startup_group.setLayout(startup_layout)
        
        # Add all groups to the tab layout
        layout.addWidget(shortcut_group)
        layout.addWidget(model_group)
        layout.addWidget(appearance_group)
        layout.addWidget(startup_group)
        layout.addStretch()
        
        # Set the layout for the tab
        self.general_tab.setLayout(layout)
        
    def create_api_keys_tab(self):
        """Create the API keys tab"""
        self.api_keys_tab = QWidget()
        layout = QVBoxLayout()
        
        # Google API key group
        google_group = QGroupBox("Google API Key")
        google_layout = QFormLayout()
        
        # Google API key input
        self.google_api_key_input = QLineEdit()
        self.google_api_key_input.setEchoMode(QLineEdit.Password)
        self.google_api_key_input.setPlaceholderText("Enter your Google API key")
        google_layout.addRow("Google API Key:", self.google_api_key_input)
        
        # Set the layout for the Google group
        google_group.setLayout(google_layout)
        
        # ElevenLabs API key group
        elevenlabs_group = QGroupBox("ElevenLabs API Key")
        elevenlabs_layout = QFormLayout()
        
        # ElevenLabs API key input
        self.elevenlabs_api_key_input = QLineEdit()
        self.elevenlabs_api_key_input.setEchoMode(QLineEdit.Password)
        self.elevenlabs_api_key_input.setPlaceholderText("Enter your ElevenLabs API key")
        elevenlabs_layout.addRow("ElevenLabs API Key:", self.elevenlabs_api_key_input)
        
        # Set the layout for the ElevenLabs group
        elevenlabs_group.setLayout(elevenlabs_layout)
        
        # Add all groups to the tab layout
        layout.addWidget(google_group)
        layout.addWidget(elevenlabs_group)
        layout.addStretch()
        
        # Note about API keys
        note_label = QLabel(
            "API keys are stored securely using Windows Credentials Manager. "
            "They are not stored in plain text."
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(note_label)
        
        # Set the layout for the tab
        self.api_keys_tab.setLayout(layout)
        
    def create_language_tab(self):
        """Create the language tab"""
        self.language_tab = QWidget()
        layout = QVBoxLayout()
        
        # Language selection group
        language_group = QGroupBox("Language")
        language_layout = QFormLayout()
        
        # Language combo box
        self.language_combo = QComboBox()
        # Get available languages from settings manager
        languages = self.settings_manager.get_available_languages()
        for name, code in languages.items():
            self.language_combo.addItem(name, code)
        language_layout.addRow("Transcription language:", self.language_combo)
        
        # Set the layout for the language group
        language_group.setLayout(language_layout)
        
        # Text insertion group
        insertion_group = QGroupBox("Text Insertion")
        insertion_layout = QFormLayout()
        
        # Insertion method
        self.clipboard_radio = QRadioButton("Via clipboard (recommended)")
        self.keypress_radio = QRadioButton("Via simulated keypresses")
        
        # Add radio buttons to a button group
        self.insertion_method_group = QButtonGroup()
        self.insertion_method_group.addButton(self.clipboard_radio, 0)
        self.insertion_method_group.addButton(self.keypress_radio, 1)
        
        insertion_layout.addRow("Insert text:", self.clipboard_radio)
        insertion_layout.addRow("", self.keypress_radio)
        
        # Set the layout for the insertion group
        insertion_group.setLayout(insertion_layout)
        
        # Add all groups to the tab layout
        layout.addWidget(language_group)
        layout.addWidget(insertion_group)
        layout.addStretch()
        
        # Set the layout for the tab
        self.language_tab.setLayout(layout)
        
    def load_settings(self):
        """Load current settings into the UI"""
        # General tab
        shortcut = self.settings_manager.get_setting("shortcut", "ctrl+alt+space")
        self.shortcut_input.setText(shortcut)
        
        # Model selection
        model = self.settings_manager.get_setting("transcription_model", "gemini_flash")
        index = self.model_combo.findData(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        # Appearance
        show_overlay = self.settings_manager.get_setting("show_overlay", True)
        self.show_overlay_checkbox.setChecked(show_overlay)
        
        overlay_position = self.settings_manager.get_setting("overlay_position", "bottom")
        index = self.overlay_position_combo.findData(overlay_position)
        if index >= 0:
            self.overlay_position_combo.setCurrentIndex(index)
        
        # Startup
        run_on_startup = self.settings_manager.get_setting("run_on_startup", True)
        self.run_on_startup_checkbox.setChecked(run_on_startup)
        
        minimize_to_tray = self.settings_manager.get_setting("minimize_to_tray", True)
        self.minimize_to_tray_checkbox.setChecked(minimize_to_tray)
        
        # API keys tab
        google_api_key = self.settings_manager.get_api_key("google") or ""
        self.google_api_key_input.setText(google_api_key)
        
        elevenlabs_api_key = self.settings_manager.get_api_key("elevenlabs") or ""
        self.elevenlabs_api_key_input.setText(elevenlabs_api_key)
        
        # Language tab
        language_code = self.settings_manager.get_setting("language", "khm")
        index = self.language_combo.findData(language_code)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        # Insertion method
        insertion_method = self.settings_manager.get_setting("insertion_method", "clipboard")
        if insertion_method == "clipboard":
            self.clipboard_radio.setChecked(True)
        else:
            self.keypress_radio.setChecked(True)
        
    def save_settings(self):
        """Save settings from the UI"""
        try:
            # General tab
            shortcut = self.shortcut_input.text()
            self.settings_manager.set_setting("shortcut", shortcut)
            
            model = self.model_combo.currentData()
            self.settings_manager.set_setting("transcription_model", model)
            
            show_overlay = self.show_overlay_checkbox.isChecked()
            self.settings_manager.set_setting("show_overlay", show_overlay)
            
            overlay_position = self.overlay_position_combo.currentData()
            self.settings_manager.set_setting("overlay_position", overlay_position)
            
            run_on_startup = self.run_on_startup_checkbox.isChecked()
            self.settings_manager.set_setting("run_on_startup", run_on_startup)
            
            minimize_to_tray = self.minimize_to_tray_checkbox.isChecked()
            self.settings_manager.set_setting("minimize_to_tray", minimize_to_tray)
            
            # API keys tab
            google_api_key = self.google_api_key_input.text()
            if google_api_key:
                self.settings_manager.set_api_key("google", google_api_key)
            
            elevenlabs_api_key = self.elevenlabs_api_key_input.text()
            if elevenlabs_api_key:
                self.settings_manager.set_api_key("elevenlabs", elevenlabs_api_key)
            
            # Language tab
            language_code = self.language_combo.currentData()
            self.settings_manager.set_setting("language", language_code)
            
            # Insertion method
            insertion_method = "clipboard" if self.clipboard_radio.isChecked() else "keypress"
            self.settings_manager.set_setting("insertion_method", insertion_method)
            
            # Accept the dialog without showing a message
            self.accept()
            
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error saving settings: {str(e)}")
            
    def get_selected_shortcut(self):
        """Get the selected shortcut"""
        return self.shortcut_input.text()




