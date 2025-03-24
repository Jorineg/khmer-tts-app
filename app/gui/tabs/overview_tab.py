"""
Overview tab for the main application window
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt, QSize

logger = logging.getLogger(__name__)

class OverviewTab(QWidget):
    """Overview tab showing application information"""
    
    def __init__(self, parent=None, app_icon=None, translation_manager=None, settings_manager=None):
        """
        Initialize the overview tab
        
        Args:
            parent: Parent widget
            app_icon: Application icon to display
            translation_manager: Translation manager for UI strings
            settings_manager: Settings manager
        """
        super().__init__(parent)
        self.parent = parent
        self.app_icon = app_icon
        self.translation_manager = translation_manager
        self.settings_manager = settings_manager
        self.feature_labels = []
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # App info section
        self.app_info_group = QGroupBox(self.get_string("overview_tab.app_info"))
        self.app_info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2980b9;
            }
        """)
        app_info_layout = QVBoxLayout()
        app_info_layout.setContentsMargins(15, 15, 15, 15)
        
        # App name and version
        self.app_name_label = QLabel("<b>Khmer Speech-to-Text App</b> - v1.0.0")
        self.app_name_label.setStyleSheet("font-size: 16px; color: #2c3e50; margin-bottom: 5px;")
        app_info_layout.addWidget(self.app_name_label)
        
        # App description
        self.app_desc_label = QLabel(self.get_string("overview_tab.app_description"))
        self.app_desc_label.setWordWrap(True)
        self.app_desc_label.setStyleSheet("color: #34495e; line-height: 1.4;")
        app_info_layout.addWidget(self.app_desc_label)
        
        self.app_info_group.setLayout(app_info_layout)
        layout.addWidget(self.app_info_group)
        
        # Status section
        self.status_group = QGroupBox(self.get_string("overview_tab.status"))
        self.status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2980b9;
            }
        """)
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        # Current status row
        status_row_layout = QHBoxLayout()
        
        self.status_label = QLabel(self.get_string("overview_tab.current_status"))
        self.status_label.setStyleSheet("font-weight: bold; margin-right: 10px;")
        
        self.status_text = QLabel(self.get_string("status.ready"))
        self.status_text.setStyleSheet("color: #27ae60;")
        
        status_row_layout.addWidget(self.status_label)
        status_row_layout.addWidget(self.status_text)
        status_row_layout.addStretch()
        
        status_layout.addLayout(status_row_layout)
        
        # Instructions
        self.instructions_label = QLabel(self.get_string("overview_tab.instructions") + "\n\n" +
                                         self.get_string("overview_tab.api_keys_info") + "\n" +
                                         self.get_string("overview_tab.api_keys_link"))
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setStyleSheet("color: #34495e; line-height: 1.4; margin-top: 10px;")
        self.instructions_label.setTextFormat(Qt.RichText)
        self.instructions_label.setOpenExternalLinks(False)
        
        # Extract the text parts
        instructions_text = self.get_string("overview_tab.instructions")
        api_keys_info = self.get_string("overview_tab.api_keys_info")
        api_keys_link = f"<a href='#api_keys' style='color: #3498db;'>{self.get_string('overview_tab.api_keys_link')}</a>"
        
        # Set rich text with clickable link
        self.instructions_label.setText(f"{instructions_text}\n\n<b>{api_keys_info}</b>\n{api_keys_link}")
        
        # Connect the link clicked signal
        self.instructions_label.linkActivated.connect(self.on_api_keys_link_clicked)
        
        status_layout.addWidget(self.instructions_label)
        
        self.status_group.setLayout(status_layout)
        layout.addWidget(self.status_group)
        
        # Features section
        self.features_group = QGroupBox(self.get_string("overview_tab.features"))
        self.features_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2980b9;
            }
        """)
        features_layout = QVBoxLayout()
        features_layout.setContentsMargins(15, 15, 15, 15)
        
        # Feature list
        self.feature_labels = []
        feature_items = self.get_string("overview_tab.feature_list").split("\n")
        for item in feature_items:
            if item.strip():
                feature_label = QLabel("• " + item.strip())
                feature_label.setStyleSheet("color: #34495e; padding-left: 5px;")
                features_layout.addWidget(feature_label)
                self.feature_labels.append(feature_label)
        
        self.features_group.setLayout(features_layout)
        layout.addWidget(self.features_group)
        
        # Add spacer
        layout.addStretch()
        
        self.setLayout(layout)
    
    def get_string(self, key, **kwargs):
        """Get a translated string using the translation manager"""
        if self.translation_manager:
            return self.translation_manager.get_string(key, **kwargs)
        return key
    
    def update_language(self):
        """Update UI text for the current language"""
        # App info group
        self.app_info_group.setTitle(self.get_string("overview_tab.app_info"))
        
        # App description
        self.app_desc_label.setText(self.get_string("overview_tab.app_description"))
        
        # Status group
        self.status_group.setTitle(self.get_string("overview_tab.status"))
        
        # Status label
        self.status_label.setText(self.get_string("overview_tab.current_status"))
        
        # Get current status text and update it with new language
        current_status_key = self.status_text.property("current_status_key")
        if current_status_key:
            self.set_status(current_status_key)
        else:
            # Default status if none is set
            self.set_status("status.ready")
        
        # Instructions - Update with the new language texts
        instructions_text = self.get_string("overview_tab.instructions")
        api_keys_info = self.get_string("overview_tab.api_keys_info")
        api_keys_link = f"<a href='#api_keys' style='color: #3498db;'>{self.get_string('overview_tab.api_keys_link')}</a>"
        
        # Set rich text with clickable link
        self.instructions_label.setText(f"{instructions_text}\n\n<b>{api_keys_info}</b>\n{api_keys_link}")
        
        # Features group
        self.features_group.setTitle(self.get_string("overview_tab.features"))
        
        # Feature list
        feature_items = self.get_string("overview_tab.feature_list").split("\n")
        for i, label in enumerate(self.feature_labels):
            if i < len(feature_items) and feature_items[i].strip():
                label.setText("• " + feature_items[i].strip())

    def set_status(self, status_key, error_state=False, **kwargs):
        """
        Set the current status text
        
        Args:
            status_key: Translation key for the status text
            error_state: Whether this is an error state
            kwargs: Additional parameters for string formatting
        """
        # Save the status key as a property of the status_text label
        self.status_text.setProperty("current_status_key", status_key)
        
        status_text = self.get_string(status_key, **kwargs)
        self.status_text.setText(status_text)
        
        if error_state:
            self.status_text.setStyleSheet("color: #e74c3c;")
        else:
            self.status_text.setStyleSheet("color: #27ae60;")
    
    def update_shortcut_label(self, shortcut):
        """
        Update the shortcut label with the current shortcut
        
        Args:
            shortcut: Current shortcut string
        """
        # No shortcut label in this version
        pass

    def on_api_keys_link_clicked(self, link):
        """Handle click on API keys link"""
        if link == "#api_keys" and self.parent and hasattr(self.parent, 'tabs'):
            # Find the index of the API Keys tab
            api_keys_tab_index = -1
            for i in range(self.parent.tabs.count()):
                if self.parent.tabs.tabText(i) == self.get_string("tabs.api_keys"):
                    api_keys_tab_index = i
                    break
            
            # Switch to API Keys tab if found
            if api_keys_tab_index >= 0:
                self.parent.tabs.setCurrentIndex(api_keys_tab_index)
