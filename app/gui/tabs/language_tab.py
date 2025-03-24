"""
Language settings tab for the main application window
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                            QGroupBox, QLabel, QComboBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)

class LanguageTab(QWidget):
    """Language settings tab for transcription and input preferences"""
    
    def __init__(self, parent=None, settings_manager=None, translation_manager=None):
        """
        Initialize the language tab
        
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
        
        # Language selection group
        self.language_group = QGroupBox(self.get_string("language_tab.select_language"))
        self.language_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2980b9; }")
        language_layout = QVBoxLayout()
        language_layout.setContentsMargins(15, 15, 15, 15)
        
        # Language selection description
        self.description_label = QLabel(self.get_string("language_tab.language_description"))
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: #34495e; line-height: 1.4; margin-bottom: 10px;")
        language_layout.addWidget(self.description_label)
        
        # Language selection combo
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 5px;
                background-color: #ffffff;
                height: 16px;
            }
        """)
        
        # Get available languages from settings manager
        languages = self.settings_manager.get_available_languages()
        for name, code in languages.items():
            self.language_combo.addItem(name, code)
        
        # Connect change signal
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        language_layout.addWidget(self.language_combo)
        
        # Add note about language selection
        self.note_label = QLabel(self.get_string("language_tab.language_note"))
        self.note_label.setWordWrap(True)
        self.note_label.setStyleSheet("font-style: italic; color: #7f8c8d; margin-top: 10px;")
        language_layout.addWidget(self.note_label)
        
        self.language_group.setLayout(language_layout)
        layout.addWidget(self.language_group)
        
        # Models group
        self.models_group = QGroupBox(self.get_string("language_tab.transcription_models"))
        self.models_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2980b9; }")
        models_layout = QVBoxLayout()
        models_layout.setContentsMargins(15, 15, 15, 15)
        
        # Models description
        self.models_description = QLabel(self.get_string("language_tab.models_description"))
        self.models_description.setWordWrap(True)
        self.models_description.setStyleSheet("color: #34495e; line-height: 1.4; margin-bottom: 10px;")
        models_layout.addWidget(self.models_description)
        
        # Model selection
        self.model_radio_gemini = QRadioButton("Google Gemini Flash")
        self.model_radio_elevenlabs = QRadioButton("ElevenLabs")
        
        # Connect signals
        self.model_radio_gemini.toggled.connect(self.on_model_selection_changed)
        self.model_radio_elevenlabs.toggled.connect(self.on_model_selection_changed)
        
        # Add to layout
        models_layout.addWidget(self.model_radio_gemini)
        models_layout.addWidget(self.model_radio_elevenlabs)
        
        self.models_group.setLayout(models_layout)
        layout.addWidget(self.models_group)
        
        # Add spacer
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Load settings
        self.load_settings()
    
    def get_string(self, key, **kwargs):
        """Get a translated string using the translation manager"""
        if self.translation_manager:
            return self.translation_manager.get_string(key, **kwargs)
        return key
    
    def load_settings(self):
        """Load settings from the settings manager"""
        if not self.settings_manager:
            return
            
        # Load language
        language = self.settings_manager.get_setting("language")
        index = -1
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == language:
                index = i
                break
                
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
            
        # Load model selection
        model_selection = self.settings_manager.get_setting("model_selection")
        if model_selection == "Google Gemini Flash":
            self.model_radio_gemini.setChecked(True)
        else:
            self.model_radio_elevenlabs.setChecked(True)
    
    def connect_signals(self):
        """Connect signal handlers for UI controls"""
        # Language combo signal
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        # Model selection signals
        self.model_radio_gemini.toggled.connect(self.on_model_selection_changed)
        self.model_radio_elevenlabs.toggled.connect(self.on_model_selection_changed)
    
    def on_language_changed(self, index):
        """Handle language change"""
        language = self.language_combo.itemData(index)
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("language", language)
            # No need for save_settings() as set_setting() automatically saves
    
    def on_model_selection_changed(self):
        """Handle model selection change"""
        model_selection = "Google Gemini Flash" if self.model_radio_gemini.isChecked() else "ElevenLabs"
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("model_selection", model_selection)
            # No need for save_settings() as set_setting() automatically saves
    
    def update_language(self):
        """Update UI text for the current language"""
        # Update group titles
        self.language_group.setTitle(self.get_string("language_tab.select_language"))
        self.models_group.setTitle(self.get_string("language_tab.transcription_models"))
        
        # Update text labels
        self.description_label.setText(self.get_string("language_tab.language_description"))
        self.note_label.setText(self.get_string("language_tab.language_note"))
        self.models_description.setText(self.get_string("language_tab.models_description"))
        
        # Update radio button texts - using fixed model names, not translated
        self.model_radio_gemini.setText("Google Gemini Flash")
        self.model_radio_elevenlabs.setText("ElevenLabs")
