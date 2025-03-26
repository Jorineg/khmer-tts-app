"""
Language settings tab for the main application window
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                            QComboBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, pyqtSignal

from ..widgets import (
    TranslatableLabel,
    TranslatableGroupBox,
)
from ..styles.app_stylesheet import (
    get_group_box_style, get_description_label_style,
    get_combo_box_style, get_note_label_style, get_radio_button_style
)
from ...i18n.translation_manager import translation_manager

logger = logging.getLogger(__name__)

class LanguageTab(QWidget):
    """Language settings tab for transcription and input preferences"""
    
    # Define signals for changes
    language_changed = pyqtSignal(str)  # Emits language code
    transcription_language_changed = pyqtSignal(str)  # Emits language code for transcription
    model_changed = pyqtSignal(str)  # Emits model name
    
    def __init__(self, parent=None, settings_manager=None, translation_manager=None):
        """
        Initialize the language tab
        
        Args:
            parent: Parent widget
            settings_manager: Settings manager for accessing/saving settings
            translation_manager: Translation manager for UI strings (no longer needed)
        """
        super().__init__(parent)
        self.parent = parent
        self.settings_manager = settings_manager
        # We're already importing the singleton at the top of the file, no need to store passed instance
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the tab UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Language selection group
        self.language_group = TranslatableGroupBox("<<language_tab.select_language>>")
        self.language_group.setStyleSheet(get_group_box_style())
        language_layout = QVBoxLayout()
        language_layout.setContentsMargins(15, 15, 15, 15)
        
        # Language selection description
        self.description_label = TranslatableLabel("<<language_tab.language_description>>")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(get_description_label_style())
        language_layout.addWidget(self.description_label)
        
        # Language selection combo
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet(get_combo_box_style())
        
        # Get available languages from settings manager
        if self.settings_manager:
            languages = self.settings_manager.get_available_languages()
            for name, code in languages.items():
                self.language_combo.addItem(name, code)
        
        # Connect change signal
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        language_layout.addWidget(self.language_combo)
        
        # Add note about language selection
        self.note_label = TranslatableLabel("<<language_tab.language_note>>")
        self.note_label.setWordWrap(True)
        self.note_label.setStyleSheet(get_note_label_style())
        language_layout.addWidget(self.note_label)
        
        self.language_group.setLayout(language_layout)
        layout.addWidget(self.language_group)
        
        # Models group
        self.models_group = TranslatableGroupBox("<<language_tab.transcription_models>>")
        self.models_group.setStyleSheet(get_group_box_style())
        models_layout = QVBoxLayout()
        models_layout.setContentsMargins(15, 15, 15, 15)
        
        # Models description
        self.models_description = TranslatableLabel("<<language_tab.models_description>>")
        self.models_description.setWordWrap(True)
        self.models_description.setStyleSheet(get_description_label_style())
        models_layout.addWidget(self.models_description)
        
        # Model selection
        self.model_radio_gemini = QRadioButton("Google Gemini Flash")
        self.model_radio_gemini.setStyleSheet(get_radio_button_style())
        self.model_radio_elevenlabs = QRadioButton("ElevenLabs")
        self.model_radio_elevenlabs.setStyleSheet(get_radio_button_style())
        
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
            
        # Load model selection using default_model setting
        default_model = self.settings_manager.get_setting("default_model")
        if default_model == "gemini_flash":
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
        
        # Save to settings using the enhanced SettingsManager method
        if self.settings_manager:
            # This will save the setting and handle any callbacks if needed
            self.settings_manager.update_language(language)
            
            # Emit signal for any listeners to update UI
            self.language_changed.emit(language)
    
    def on_model_selection_changed(self):
        """Handle model selection change"""
        model_selection = "Google Gemini Flash" if self.model_radio_gemini.isChecked() else "ElevenLabs"
        
        # Save to settings
        if self.settings_manager:
            # Save the display name
            self.settings_manager.set_setting("model_selection", model_selection)
            
            # Update the model code name using the enhanced method
            default_model = "gemini_flash" if self.model_radio_gemini.isChecked() else "elevenlabs"
            self.settings_manager.update_transcription_model(default_model)
            
            # Emit signal for any listeners
            self.model_changed.emit(default_model)
