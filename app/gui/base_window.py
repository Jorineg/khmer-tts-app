"""
Base window class with common functionality
"""

import os
import logging
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor

logger = logging.getLogger(__name__)

class BaseWindow(QMainWindow):
    """Base window class with common functionality"""
    
    def __init__(self, settings_manager):
        """
        Initialize the base window
        
        Args:
            settings_manager: SettingsManager instance
        """
        super().__init__()
        
        self.settings_manager = settings_manager
        
        # Set window icon
        self.setWindowIcon(self.create_app_icon())
    
    def create_app_icon(self):
        """
        Create application icon
        First tries to load from file, falls back to generated icon if file not found
        """
        # Try to load from file
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resources", "icon.png")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        
        # Create custom icon if file not found
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up colors
        mic_color = QColor(52, 152, 219)  # Blue
        circle_color = QColor(236, 240, 241, 160)  # Light gray with transparency
        
        # Draw background circle
        painter.setBrush(circle_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(4, 4, size-8, size-8)
        
        # Draw microphone icon
        mic_rect = QRect(size//3, size//5, size//3, size//2)
        painter.setBrush(mic_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(mic_rect, 8, 8)
        
        # Draw microphone base stand
        base_width = size//2
        base_height = size//15
        base_x = (size - base_width) // 2
        base_y = mic_rect.bottom() + size//10
        painter.drawRoundedRect(base_x, base_y, base_width, base_height, 4, 4)
        
        # Draw connection line
        line_width = size//25
        line_height = size//10
        line_x = (size - line_width) // 2
        line_y = mic_rect.bottom()
        painter.drawRoundedRect(line_x, line_y, line_width, line_height, 2, 2)
        
        # End painting
        painter.end()
        
        # Create icon from pixmap
        return QIcon(pixmap)
    
    def closeEvent(self, event):
        """Handle window close event - can be overridden by subclasses"""
        event.accept()
    
    def showMessage(self, title, message, icon=QMessageBox.Information):
        """Show a message box to the user"""
        QMessageBox.information(self, title, message, icon)
