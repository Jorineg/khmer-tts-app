"""
Overlay window displayed during recording and transcription
"""

import logging
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QMovie, QIcon, QPixmap

logger = logging.getLogger(__name__)

class OverlayWidget(QWidget):
    """Overlay widget displayed during recording and transcription"""
    
    def __init__(self, parent=None):
        """Initialize the overlay widget"""
        super().__init__(parent)
        
        # Current state - initialize before setting up the UI
        self.current_state = "idle"
        
        # Set up the UI
        self.setup_ui()
        
        # Set window flags
        self.setup_window()
        
        # Pre-position the overlay at startup to avoid delay
        self.position_at_bottom()
        
        # Pre-render the overlay to avoid delay when showing
        self.prepare_states()
        
    def setup_window(self):
        """Set up window properties"""
        # Make the window stay on top
        self.setWindowFlags(
            Qt.Tool |  # Doesn't show in taskbar
            Qt.FramelessWindowHint |  # No window frame
            Qt.WindowStaysOnTopHint  # Always on top
        )
        
        # Make the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def setup_ui(self):
        """Set up the UI elements"""
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Create a container widget with rounded corners
        self.container = QWidget(self)
        self.container.setObjectName("overlay_container")
        self.container.setStyleSheet("""
            #overlay_container {
                background-color: rgba(30, 30, 30, 0.8);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: white;
            }
        """)
        
        # Container layout
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(15, 10, 15, 10)
        
        # Status layout
        status_layout = QHBoxLayout()
        
        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        status_layout.addWidget(self.icon_label)
        
        # Status label
        self.status_label = QLabel("Idle")
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        status_layout.addWidget(self.status_label)
        
        # Add status layout to container
        container_layout.addLayout(status_layout)
        
        # Progress bar for recording or transcription
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(100, 100, 100, 0.2);
                border-radius: 2px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 2px;
            }
        """)
        container_layout.addWidget(self.progress_bar)
        
        # Add container to main layout
        layout.addWidget(self.container)
        
        # Set the layout
        self.setLayout(layout)
        
        # Set initial icons
        self.update_icons()
        
    def update_icons(self):
        """Update the icons based on the current state"""
        if self.current_state == "recording":
            # Recording icon (red circle)
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.transparent)
            self.icon_label.setPixmap(pixmap)
            self.icon_label.setStyleSheet("""
                background-color: #e74c3c;
                border-radius: 12px;
            """)
        elif self.current_state == "transcribing":
            # Transcribing icon (blue waves)
            self.icon_label.setStyleSheet("")
            # Create a simple blue wave icon instead of loading from resources
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.transparent)
            self.icon_label.setPixmap(pixmap)
            self.icon_label.setStyleSheet("""
                background-color: #3498db;
                border-radius: 6px;
            """)
        else:
            # Idle icon (empty)
            self.icon_label.setStyleSheet("")
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.transparent)
            self.icon_label.setPixmap(pixmap)
    
    def prepare_states(self):
        """
        Pre-render all states of the overlay to avoid delay when showing
        """
        # Prepare recording state
        self.status_label.setText("Recording...")
        self.progress_bar.setRange(0, 0)
        self.current_state = "recording"
        self.update_icons()
        
        # Prepare transcribing state
        self.status_label.setText("Transcribing...")
        self.current_state = "transcribing"
        self.update_icons()
        
        # Reset to idle state
        self.status_label.setText("Idle")
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.current_state = "idle"
        self.update_icons()
        
    def set_state(self, state):
        """
        Set the current state of the overlay
        
        Args:
            state: Current state (idle, recording, transcribing)
        """
        # Only update if state has changed
        if self.current_state == state:
            return
            
        self.current_state = state
        
        if state == "idle":
            self.status_label.setText("Idle")
            self.progress_bar.setRange(0, 1)
            self.progress_bar.setValue(0)
            self.hide()
        elif state == "recording":
            self.status_label.setText("Recording...")
            self.progress_bar.setRange(0, 0)  # Indeterminate
            # Update icons before showing for smoother transition
            self.update_icons()
            # Use show() instead of setVisible for faster display
            self.show()
        elif state == "transcribing":
            self.status_label.setText("Transcribing...")
            self.progress_bar.setRange(0, 0)  # Indeterminate
            # Update icons before showing for smoother transition
            self.update_icons()
            self.show()
        
    def position_at_bottom(self):
        """Position the overlay at the bottom of the screen"""
        # Get screen geometry
        screen_geometry = self.screen().geometry()
        
        # Calculate position
        width = 200  # Fixed width
        height = 60  # Fixed height
        x = (screen_geometry.width() - width) // 2
        y = screen_geometry.height() - height - 50  # 50px from bottom
        
        # Set position and size
        self.setGeometry(x, y, width, height)
