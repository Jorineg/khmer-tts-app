"""
Overview tab for the main application window
"""

import logging
import webbrowser
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGroupBox, QDesktopWidget
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon

from ..widgets.translatable import TranslatableLabel, TranslatableGroupBox
from ..styles.app_stylesheet import (
    get_features_group_box_style, get_warning_label_style,
    get_feature_label_style
)
from ...i18n.translation_manager import translation_manager

logger = logging.getLogger(__name__)

class OverviewTab(QWidget):
    """Overview tab showing application information"""
    
    def __init__(self, parent=None, app_icon=None, translation_manager=None, settings_manager=None):
        """
        Initialize the overview tab
        
        Args:
            parent: Parent widget
            app_icon: Application icon to display
            translation_manager: Translation manager for UI strings (deprecated - singleton instance used instead)
            settings_manager: Settings manager for accessing settings
        """
        super().__init__(parent)
        self.parent = parent
        self.app_icon = app_icon
        self.settings_manager = settings_manager
        # We're already importing the singleton at the top of the file, no need to store passed instance
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Top section with app icon and status
        top_layout = QVBoxLayout()
        
        # App icon
        if self.app_icon:
            icon_label = QLabel()
            icon_pixmap = self.app_icon.pixmap(QSize(64, 64))
            icon_label.setPixmap(icon_pixmap)
            top_layout.addWidget(icon_label)
        
        # App title and status
        title_layout = QVBoxLayout()
        
        # App title with heading style
        self.app_title = TranslatableLabel("<h1><<overview_tab.title>></h1>")
        title_layout.addWidget(self.app_title)
        
        status_layout = QHBoxLayout()
        
        # Status label in bold
        self.status_label = TranslatableLabel("<b><<overview_tab.status>></b>")
        status_layout.addWidget(self.status_label)
        
        # Status text is not translatable on its own, it will be set programmatically
        self.status_text = QLabel()
        self.status_text.setText(translation_manager.get_string("status.ready"))
        self.status_text.setStyleSheet("color: #27ae60;")
        self.status_text.setProperty("current_status_key", "status.ready")
        status_layout.addWidget(self.status_text)
        
        status_layout.addStretch()
        title_layout.addLayout(status_layout)
        
        top_layout.addLayout(title_layout)
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # API key warning (initially hidden)
        self.api_key_warning = QLabel()
        self.api_key_warning.setWordWrap(True)
        self.api_key_warning.setStyleSheet(get_warning_label_style())
        self.api_key_warning.hide()
        layout.addWidget(self.api_key_warning)
        
        # Shortcut section
        shortcut_layout = QHBoxLayout()
        
        # Shortcut label in bold
        self.shortcut_label = TranslatableLabel("<b><<overview_tab.shortcut>></b>")
        shortcut_layout.addWidget(self.shortcut_label)
        
        # Shortcut text is not translatable, just shows the current shortcut
        self.shortcut_text = QLabel()
        self.shortcut_text.setText("Ctrl+Alt+Space")
        shortcut_layout.addWidget(self.shortcut_text)
        
        shortcut_layout.addStretch()
        layout.addLayout(shortcut_layout)
        
        # Instructions section
        self.instructions_label = TranslatableLabel("<<overview_tab.instructions>>")
        self.instructions_label.setWordWrap(True)
        layout.addWidget(self.instructions_label)
        
        # API keys info section (separate from instructions)
        self.api_keys_info_label = TranslatableLabel(
            "<b><<overview_tab.api_keys_info>>\n<a href='#api_keys' style='color: #3498db;'><<overview_tab.api_keys_link>></a> <<overview_tab.api_keys_info2>></b>"
        )
        self.api_keys_info_label.setWordWrap(True)
        self.api_keys_info_label.setTextFormat(Qt.RichText)
        self.api_keys_info_label.setOpenExternalLinks(False)
        
        # Connect the link clicked signal
        self.api_keys_info_label.linkActivated.connect(self.on_api_keys_link_clicked)
        
        layout.addWidget(self.api_keys_info_label)
        
        # Features section
        self.features_group = TranslatableGroupBox("<<overview_tab.features>>")
        self.features_group.setStyleSheet(get_features_group_box_style())
        features_layout = QVBoxLayout()
        features_layout.setContentsMargins(15, 15, 15, 15)
        
        # Feature list
        self.feature_labels = []
        
        # Create the feature list by looking at the current translation
        feature_items = translation_manager.get_string("overview_tab.feature_list").split("\n")
        for item in feature_items:
            if item.strip():
                feature_label = QLabel("• " + item.strip())
                feature_label.setStyleSheet(get_feature_label_style())
                features_layout.addWidget(feature_label)
                self.feature_labels.append(feature_label)
        
        # Store this widget instance in the main window's list of things to update
        # when language changes
        self.language_update_callback = lambda: self.update_feature_list()
        
        self.features_group.setLayout(features_layout)
        layout.addWidget(self.features_group)
        
        # Add spacer
        layout.addStretch()
        
        self.setLayout(layout)
    
    def set_status(self, status_key, **kwargs):
        """
        Set the status text
        
        Args:
            status_key: Key for status text in translation strings
            kwargs: Formatting arguments for the string
        """
        error_state = kwargs.pop("error_state", False)
        text = translation_manager.get_string(status_key, **kwargs)
        
        # Store the status key as a property for translation updates
        self.status_text.setProperty("current_status_key", status_key)
        
        # Set the text
        self.status_text.setText(text)
        
        # Set color based on state
        color = "#e74c3c" if error_state else "#27ae60"  # Red for error, green for normal
        self.status_text.setStyleSheet(f"color: {color};")
    
    def update_shortcut_label(self, shortcut):
        """
        Update the shortcut text display
        
        Args:
            shortcut: Shortcut key combination to display
        """
        if shortcut:
            self.shortcut_text.setText(shortcut)
        else:
            self.shortcut_text.setText(translation_manager.get_string("general_tab.shortcut_placeholder"))
    
    def on_api_keys_link_clicked(self, link):
        """Handle click on API keys link"""
        if link == "#api_keys" and self.parent and hasattr(self.parent, 'tabs'):
            # Find the index of the API Keys tab
            api_keys_tab_index = -1
            for i in range(self.parent.tabs.count()):
                if self.parent.tabs.tabText(i) == translation_manager.get_string("tabs.api_keys"):
                    api_keys_tab_index = i
                    break
            
            # Switch to API Keys tab if found
            if api_keys_tab_index >= 0:
                self.parent.tabs.setCurrentIndex(api_keys_tab_index)

    def update_api_key_warning(self, show_warning=True, model_name=None):
        """
        Update the API key warning message visibility
        
        Args:
            show_warning: Whether to show the warning
            model_name: Name of the model missing an API key
        """
        if show_warning and model_name:
            # Get the display name for the model
            if model_name == "gemini_flash":
                display_model = translation_manager.get_string("general_tab.model_gemini")
            elif model_name == "elevenlabs":
                display_model = translation_manager.get_string("general_tab.model_elevenlabs")
            else:
                display_model = model_name
                
            # Show warning with specific model name
            self.api_key_warning.setText(f" {translation_manager.get_string('notifications.missing_api_key_error', model_name=display_model)}")
            self.api_key_warning.show()
            
            # Update status to show missing API key
            self.set_status("status.no_api_key", model_name=display_model)
            
            # Highlight the API key info
            api_keys_info = translation_manager.get_string("overview_tab.api_keys_info")
            api_keys_info2 = translation_manager.get_string("overview_tab.api_keys_info2")
            api_keys_link = f"<a href='#api_keys' style='color: #e74c3c; font-weight: bold;'>{translation_manager.get_string('overview_tab.api_keys_link')}</a>"
            
            # Set rich text with highlighted link
            self.api_keys_info_label.setText(f"<b style='color: #e74c3c;'>{api_keys_info}\n{api_keys_link} {api_keys_info2}</b>")
        else:
            # Hide warning
            self.api_key_warning.hide()
            
            # Reset status to ready
            self.set_status("status.ready")
            
            # Reset normal instructions display
            api_keys_info = translation_manager.get_string("overview_tab.api_keys_info")
            api_keys_info2 = translation_manager.get_string("overview_tab.api_keys_info2")
            api_keys_link = f"<a href='#api_keys' style='color: #3498db;'>{translation_manager.get_string('overview_tab.api_keys_link')}</a>"
            
            # Set rich text with normal styling
            self.api_keys_info_label.setText(f"<b>{api_keys_info}\n{api_keys_link} {api_keys_info2}</b>")
    
    def update_feature_list(self):
        """Update the feature list when language changes"""
        # Remove existing feature labels
        for label in self.feature_labels:
            self.layout().removeWidget(label)
            label.deleteLater()
        self.feature_labels.clear()
        
        # Recreate feature labels with new language
        features_layout = self.features_group.layout()
        feature_items = translation_manager.get_string("overview_tab.feature_list").split("\n")
        
        for item in feature_items:
            if item.strip():
                feature_label = QLabel("• " + item.strip())
                feature_label.setStyleSheet(get_feature_label_style())
                features_layout.addWidget(feature_label)
                self.feature_labels.append(feature_label)