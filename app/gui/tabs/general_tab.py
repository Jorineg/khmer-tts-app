"""
General settings tab for the main application window
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QComboBox)
from PyQt5.QtCore import Qt

from ..widgets import (
    TranslatableLabel,
    TranslatableGroupBox,
    TranslatableCheckBox
)
from ..shortcut_recorder import ShortcutRecorder
from ..styles.app_stylesheet import (
    get_group_box_style, get_description_label_style,
    get_combo_box_style, get_label_style, get_checkbox_style
)
from ...i18n.translation_manager import translation_manager

logger = logging.getLogger(__name__)

class GeneralTab(QWidget):
    """General settings tab for application preferences"""
    
    def __init__(self, parent=None, settings_manager=None, translation_manager=None):
        """
        Initialize the general settings tab
        
        Args:
            parent: Parent widget
            settings_manager: Settings manager for accessing/saving settings
            translation_manager: Translation manager for UI strings (deprecated - singleton instance used instead)
        """
        super().__init__(parent)
        self.parent = parent
        self.settings_manager = settings_manager
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the tab UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Shortcut Group
        self.shortcut_group = TranslatableGroupBox("<<general_tab.shortcut_group>>")
        self.shortcut_group.setStyleSheet(get_group_box_style())
        shortcut_layout = QVBoxLayout()
        shortcut_layout.setContentsMargins(15, 15, 15, 15)
        
        # Shortcut description
        self.shortcut_description = TranslatableLabel("<<general_tab.shortcut_description>>")
        self.shortcut_description.setWordWrap(True)
        self.shortcut_description.setStyleSheet(get_description_label_style())
        shortcut_layout.addWidget(self.shortcut_description)
        
        # Shortcut input row
        shortcut_input_layout = QHBoxLayout()
        self.shortcut_label = TranslatableLabel("<<general_tab.recording_shortcut>>")
        self.shortcut_label.setStyleSheet(get_label_style())
        self.shortcut_input = ShortcutRecorder()
        self.shortcut_input.setPlaceholderText(translation_manager.get_string("general_tab.shortcut_placeholder"))
        self.shortcut_input.setMaximumWidth(250)
        self.shortcut_input.shortcutChanged.connect(self.on_shortcut_changed)
        shortcut_input_layout.addWidget(self.shortcut_label)
        shortcut_input_layout.addWidget(self.shortcut_input)
        shortcut_input_layout.addStretch()
        shortcut_layout.addLayout(shortcut_input_layout)
        
        self.shortcut_group.setLayout(shortcut_layout)
        layout.addWidget(self.shortcut_group)
        
        # Appearance Group
        self.appearance_group = TranslatableGroupBox("<<general_tab.appearance_group>>")
        self.appearance_group.setStyleSheet(get_group_box_style())
        appearance_layout = QVBoxLayout()
        appearance_layout.setContentsMargins(15, 15, 15, 15)
        
        # Show overlay checkbox
        self.show_overlay_checkbox = TranslatableCheckBox("<<general_tab.show_overlay>>")
        self.show_overlay_checkbox.setStyleSheet(get_checkbox_style())
        appearance_layout.addWidget(self.show_overlay_checkbox)
        
        # Overlay position
        position_layout = QHBoxLayout()
        self.position_label = TranslatableLabel("<<general_tab.overlay_position>>")
        self.position_label.setStyleSheet(get_label_style())
        
        self.overlay_position_combo = QComboBox()
        self.overlay_position_combo.setEditable(False)
        self.overlay_position_combo.setStyleSheet(get_combo_box_style())
        self._update_position_combo()
        
        position_layout.addWidget(self.position_label)
        position_layout.addWidget(self.overlay_position_combo)
        position_layout.addStretch()
        
        appearance_layout.addLayout(position_layout)
        
        self.appearance_group.setLayout(appearance_layout)
        layout.addWidget(self.appearance_group)
        
        # Startup Group
        self.startup_group = TranslatableGroupBox("<<general_tab.startup_group>>")
        self.startup_group.setStyleSheet(get_group_box_style())
        startup_layout = QVBoxLayout()
        startup_layout.setContentsMargins(15, 15, 15, 15)
        
        # Run on startup checkbox
        self.run_on_startup_checkbox = TranslatableCheckBox("<<general_tab.run_on_startup>>")
        self.run_on_startup_checkbox.setStyleSheet(get_checkbox_style())
        
        startup_layout.addWidget(self.run_on_startup_checkbox)
        
        self.startup_group.setLayout(startup_layout)
        layout.addWidget(self.startup_group)
        
        # Add spacer
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Connect to language_changed signal to update combo box
        translation_manager.language_changed.connect(self._update_position_combo)
    
    def _update_position_combo(self):
        """Update the position combo box with translated items"""
        current_position = self.overlay_position_combo.currentData() if self.overlay_position_combo.count() > 0 else "bottom"
        self.overlay_position_combo.clear()
        self.overlay_position_combo.addItem(translation_manager.get_string("general_tab.position_bottom"), "bottom")
        self.overlay_position_combo.addItem(translation_manager.get_string("general_tab.position_top"), "top")
        position_index = self.overlay_position_combo.findData(current_position)
        if position_index >= 0:
            self.overlay_position_combo.setCurrentIndex(position_index)
    
    def load_settings(self):
        """Load settings from the settings manager"""
        if not self.settings_manager:
            return
            
        # Load shortcut
        shortcut = self.settings_manager.get_setting("shortcut")
        logger.info(f"General tab loading shortcut: {shortcut}")
        if shortcut:
            self.shortcut_input.set_shortcut(shortcut)
            # Ensure key_string is also set correctly
            if hasattr(self.shortcut_input, 'key_string'):
                self.shortcut_input.key_string = shortcut
                logger.debug(f"Set shortcut_input.key_string = {shortcut}")
        
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
        # Overlay signals
        self.show_overlay_checkbox.stateChanged.connect(self.on_show_overlay_changed)
        self.overlay_position_combo.currentIndexChanged.connect(self.on_overlay_position_changed)
        
        # Startup signal
        self.run_on_startup_checkbox.stateChanged.connect(self.on_run_on_startup_changed)
        
        # Shortcut signal
        self.shortcut_input.shortcutChanged.connect(self.on_shortcut_changed)
    
    def on_shortcut_changed(self, shortcut):
        """Handle shortcut change"""
        logger.info(f"Shortcut changed to: {shortcut}")
        # Ensure shortcut is a properly formatted string before saving
        if shortcut and isinstance(shortcut, str):
            # Save shortcut to settings
            self.settings_manager.set_setting("shortcut", shortcut)
            logger.debug(f"Saved shortcut to settings: {shortcut}")
            
            # Force settings to sync to disk
            if hasattr(self.settings_manager.settings, 'sync'):
                self.settings_manager.settings.sync()
                logger.debug("Forced QSettings sync to ensure persistence")
                
            # Notify main window to update global shortcut
            if self.parent and hasattr(self.parent, 'update_global_shortcut'):
                self.parent.update_global_shortcut(shortcut)
                logger.debug("Notified main window to update global shortcut")
        else:
            logger.warning(f"Invalid shortcut format: {shortcut} (type: {type(shortcut)})")
    
    def on_show_overlay_changed(self, state):
        """Handle show overlay checkbox change"""
        show_overlay = bool(state)
        logger.debug(f"Show overlay changed to: {show_overlay}")
        
        if self.settings_manager:
            self.settings_manager.set_setting("show_overlay", show_overlay)
    
    def on_overlay_position_changed(self, index):
        """Handle overlay position change"""
        position = self.overlay_position_combo.itemData(index)
        logger.debug(f"Overlay position changed to: {position}")
        
        if self.settings_manager:
            self.settings_manager.set_setting("overlay_position", position)
    
    def on_run_on_startup_changed(self, state):
        """Handle run on startup checkbox change"""
        run_on_startup = bool(state)
        logger.debug(f"Run on startup changed to: {run_on_startup}")
        
        if self.settings_manager:
            self.settings_manager.set_setting("run_on_startup", run_on_startup)
            
            # Handle Windows startup registration
            try:
                from ...utils.startup_utils import set_run_at_startup
                set_run_at_startup(run_on_startup)
            except Exception as e:
                logger.error(f"Failed to set startup registration: {e}")
