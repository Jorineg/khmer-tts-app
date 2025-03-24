"""
General settings tab for the main application window
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QGroupBox, QLabel, QLineEdit, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt

from ..shortcut_recorder import ShortcutRecorder

logger = logging.getLogger(__name__)

class GeneralTab(QWidget):
    """General settings tab for application preferences"""
    
    def __init__(self, parent=None, settings_manager=None, translation_manager=None):
        """
        Initialize the general settings tab
        
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
        
        # Shortcut Group
        self.shortcut_group = QGroupBox(self.get_string("general_tab.shortcut_group"))
        shortcut_layout = QVBoxLayout()
        shortcut_layout.setContentsMargins(15, 15, 15, 15)
        
        # Shortcut description
        self.shortcut_description = QLabel(self.get_string("general_tab.shortcut_description"))
        self.shortcut_description.setWordWrap(True)
        self.shortcut_description.setStyleSheet("color: #34495e; line-height: 1.4; margin-bottom: 10px;")
        shortcut_layout.addWidget(self.shortcut_description)
        
        # Shortcut input row
        shortcut_input_layout = QHBoxLayout()
        self.shortcut_label = QLabel(self.get_string("general_tab.recording_shortcut"))
        self.shortcut_label.setStyleSheet("font-weight: bold;")
        self.shortcut_input = QLineEdit()
        self.shortcut_input.setPlaceholderText(self.get_string("general_tab.shortcut_placeholder"))
        self.shortcut_input.setReadOnly(True)
        self.shortcut_input.setMaximumWidth(250)
        self.shortcut_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 5px;
                background-color: #ffffff;
                height: 16px;
            }
        """)
        shortcut_input_layout.addWidget(self.shortcut_label)
        shortcut_input_layout.addWidget(self.shortcut_input)
        shortcut_input_layout.addStretch()
        shortcut_layout.addLayout(shortcut_input_layout)
        
        self.shortcut_group.setLayout(shortcut_layout)
        layout.addWidget(self.shortcut_group)
        
        # Model Group
        self.model_group = QGroupBox(self.get_string("general_tab.model_group"))
        model_layout = QVBoxLayout()
        model_layout.setContentsMargins(15, 15, 15, 15)
        
        # Default model combo
        self.model_label = QLabel(self.get_string("general_tab.default_model"))
        self.model_label.setStyleSheet("font-weight: bold;")
        self.model_combo = QComboBox()
        self.model_combo.setEditable(False)
        self.model_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 5px;
                background-color: #ffffff;
                height: 16px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #d0d0d0;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)
        self.model_combo.addItem(self.get_string("general_tab.model_gemini"), "gemini_flash")
        self.model_combo.addItem(self.get_string("general_tab.model_elevenlabs"), "elevenlabs")
        
        model_input_layout = QHBoxLayout()
        model_input_layout.addWidget(self.model_label)
        model_input_layout.addWidget(self.model_combo)
        model_layout.addLayout(model_input_layout)
        
        self.model_group.setLayout(model_layout)
        layout.addWidget(self.model_group)
        
        # Appearance Group
        self.appearance_group = QGroupBox(self.get_string("general_tab.appearance_group"))
        appearance_layout = QVBoxLayout()
        appearance_layout.setContentsMargins(15, 15, 15, 15)
        
        # Show overlay checkbox
        self.show_overlay_checkbox = QCheckBox(self.get_string("general_tab.show_overlay"))
        self.show_overlay_checkbox.setStyleSheet("margin-bottom: 5px;")
        appearance_layout.addWidget(self.show_overlay_checkbox)
        
        # Overlay position
        position_layout = QHBoxLayout()
        self.position_label = QLabel(self.get_string("general_tab.overlay_position"))
        self.position_label.setStyleSheet("margin-right: 10px;")
        
        self.overlay_position_combo = QComboBox()
        self.overlay_position_combo.setEditable(False)
        self.overlay_position_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 5px;
                background-color: #ffffff;
                height: 16px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #d0d0d0;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)
        self.overlay_position_combo.addItem(self.get_string("general_tab.position_bottom"), "bottom")
        self.overlay_position_combo.addItem(self.get_string("general_tab.position_top"), "top")
        
        position_layout.addWidget(self.position_label)
        position_layout.addWidget(self.overlay_position_combo)
        position_layout.addStretch()
        
        appearance_layout.addLayout(position_layout)
        
        self.appearance_group.setLayout(appearance_layout)
        layout.addWidget(self.appearance_group)
        
        # Startup Group
        self.startup_group = QGroupBox(self.get_string("general_tab.startup_group"))
        startup_layout = QVBoxLayout()
        startup_layout.setContentsMargins(15, 15, 15, 15)
        
        # Run on startup checkbox
        self.run_on_startup_checkbox = QCheckBox(self.get_string("general_tab.run_on_startup"))
        self.run_on_startup_checkbox.setStyleSheet("margin-bottom: 5px;")
        
        startup_layout.addWidget(self.run_on_startup_checkbox)
        
        self.startup_group.setLayout(startup_layout)
        layout.addWidget(self.startup_group)
        
        # Add spacer
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
            
        # Load shortcut
        shortcut = self.settings_manager.get_setting("shortcut")
        self.shortcut_input.setText(shortcut)
        
        # Load default model
        default_model = self.settings_manager.get_setting("default_model")
        index = self.model_combo.findData(default_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        # Load overlay settings
        show_overlay = self.settings_manager.get_setting("show_overlay")
        self.show_overlay_checkbox.setChecked(show_overlay)
        
        overlay_position = self.settings_manager.get_setting("overlay_position")
        index = self.overlay_position_combo.findData(overlay_position)
        if index >= 0:
            self.overlay_position_combo.setCurrentIndex(index)
        
        # Load startup setting
        run_on_startup = self.settings_manager.get_setting("run_on_startup")
        self.run_on_startup_checkbox.setChecked(run_on_startup)
    
    def connect_signals(self):
        """Connect signal handlers for UI controls"""
        # Shortcut signal
        # self.shortcut_input.shortcutChanged.connect(self.on_shortcut_changed)
        
        # Model combo signal
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        
        # Overlay signals
        self.show_overlay_checkbox.stateChanged.connect(self.on_show_overlay_changed)
        self.overlay_position_combo.currentIndexChanged.connect(self.on_overlay_position_changed)
        
        # Startup signal
        self.run_on_startup_checkbox.stateChanged.connect(self.on_run_on_startup_changed)
    
    def update_language(self):
        """Update UI text for the current language"""
        # Update group titles
        self.shortcut_group.setTitle(self.get_string("general_tab.shortcut_group"))
        self.model_group.setTitle(self.get_string("general_tab.model_group"))
        self.appearance_group.setTitle(self.get_string("general_tab.appearance_group"))
        self.startup_group.setTitle(self.get_string("general_tab.startup_group"))
        
        # Update descriptions and labels
        self.shortcut_description.setText(self.get_string("general_tab.shortcut_description"))
        self.shortcut_label.setText(self.get_string("general_tab.recording_shortcut"))
        self.model_label.setText(self.get_string("general_tab.default_model"))
        self.position_label.setText(self.get_string("general_tab.overlay_position"))
        
        # Update checkbox texts
        self.show_overlay_checkbox.setText(self.get_string("general_tab.show_overlay"))
        self.run_on_startup_checkbox.setText(self.get_string("general_tab.run_on_startup"))
        
        # Update combobox items while preserving selection
        # Model combo
        current_model = self.model_combo.currentData()
        self.model_combo.clear()
        self.model_combo.addItem(self.get_string("general_tab.model_gemini"), "gemini_flash")
        self.model_combo.addItem(self.get_string("general_tab.model_elevenlabs"), "elevenlabs")
        model_index = self.model_combo.findData(current_model)
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        
        # Position combo
        current_position = self.overlay_position_combo.currentData()
        self.overlay_position_combo.clear()
        self.overlay_position_combo.addItem(self.get_string("general_tab.position_bottom"), "bottom")
        self.overlay_position_combo.addItem(self.get_string("general_tab.position_top"), "top")
        position_index = self.overlay_position_combo.findData(current_position)
        if position_index >= 0:
            self.overlay_position_combo.setCurrentIndex(position_index)
        
        # Update shortcut placeholder
        self.shortcut_input.setPlaceholderText(self.get_string("general_tab.shortcut_placeholder"))
    
    def on_shortcut_changed(self):
        """Handle shortcut change"""
        shortcut = self.shortcut_input.text()
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("shortcut", shortcut)
            # No need for save_settings() as set_setting() automatically saves
            
            # Update parent shortcut (if method exists)
            if hasattr(self.parent, 'update_global_shortcut'):
                self.parent.update_global_shortcut(shortcut)
        
        # Update shortcut label on overview tab (if method exists)
        if hasattr(self.parent, 'update_shortcut_label'):
            self.parent.update_shortcut_label()
    
    def on_model_changed(self, index):
        """Handle model change"""
        model = self.model_combo.itemData(index)
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("default_model", model)
            # No need for save_settings() as set_setting() automatically saves
    
    def on_show_overlay_changed(self, state):
        """Handle show overlay change"""
        show_overlay = state == Qt.Checked
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("show_overlay", show_overlay)
            # No need for save_settings() as set_setting() automatically saves
    
    def on_overlay_position_changed(self, index):
        """Handle overlay position change"""
        position = self.overlay_position_combo.itemData(index)
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("overlay_position", position)
            # No need for save_settings() as set_setting() automatically saves
    
    def on_run_on_startup_changed(self, state):
        """Handle run on startup change"""
        run_on_startup = state == Qt.Checked
        
        # Save to settings
        if self.settings_manager:
            self.settings_manager.set_setting("run_on_startup", run_on_startup)
            # No need for save_settings() as set_setting() automatically saves
            
            # Update the startup registry if method exists
            if hasattr(self.parent, 'update_startup_registry'):
                self.parent.update_startup_registry(run_on_startup)
