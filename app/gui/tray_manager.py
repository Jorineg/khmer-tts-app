"""
System tray icon manager
"""

import logging
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

logger = logging.getLogger(__name__)

class TrayManager:
    """Manages the system tray icon and menu"""
    
    def __init__(self, parent, icon, translation_manager):
        """
        Initialize the tray manager
        
        Args:
            parent: Parent window that owns the tray icon
            icon: Icon to use for the tray
            translation_manager: Translation manager for localized strings
        """
        self.parent = parent
        self.translation_manager = translation_manager
        
        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(icon, parent)
        self.update_tooltip()
        
        # Create tray menu
        self.setup_menu()
        
        # Connect tray icon activation to handle single clicks
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Show the tray icon
        self.tray_icon.show()
    
    def setup_menu(self):
        """Set up the tray menu"""
        tray_menu = QMenu(self.parent)
        
        # Open action
        self.open_action = QAction(self.translation_manager.get_string("buttons.open"), self.parent)
        self.open_action.triggered.connect(self.parent.show_main_window)
        tray_menu.addAction(self.open_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Exit action
        self.exit_action = QAction(self.translation_manager.get_string("buttons.exit"), self.parent)
        self.exit_action.triggered.connect(self.parent.close_application)
        tray_menu.addAction(self.exit_action)
        
        # Set the tray menu
        self.tray_icon.setContextMenu(tray_menu)
    
    def update_menu_text(self):
        """Update menu text with current language"""
        self.open_action.setText(self.translation_manager.get_string("buttons.open"))
        self.exit_action.setText(self.translation_manager.get_string("buttons.exit"))
    
    def update_tooltip(self):
        """Update tray tooltip with current language"""
        self.tray_icon.setToolTip(self.translation_manager.get_string("tray_tooltip"))
    
    def tray_icon_activated(self, reason):
        """
        Handle tray icon activation
        Now responds to single clicks instead of requiring double-clicks
        """
        if reason == QSystemTrayIcon.Trigger:  # Single click
            self.parent.show_main_window()
    
    def showMessage(self, title, message, icon=QSystemTrayIcon.Information, timeout=3000):
        """Show a notification message through the tray icon"""
        self.tray_icon.showMessage(title, message, icon, timeout)
    
    def hide(self):
        """Hide the tray icon"""
        self.tray_icon.hide()
    
    def is_visible(self):
        """Check if the tray icon is visible"""
        return self.tray_icon.isVisible()
