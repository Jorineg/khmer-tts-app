"""
Main application window and system tray icon
"""

import os
import sys
import logging
import threading
from PyQt5.QtWidgets import (
    QMainWindow, QSystemTrayIcon, QMenu, QAction, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox,
    QFormLayout, QLineEdit, QComboBox, QCheckBox, QGroupBox, QSpinBox,
    QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QFont

from .overlay import OverlayWidget
from ..audio.recorder import AudioRecorder
from ..transcription.transcription_manager import TranscriptionManager
from ..system.text_inserter import TextInserter
from ..settings.settings_manager import SettingsManager

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, settings_manager):
        """
        Initialize the main window
        
        Args:
            settings_manager: SettingsManager instance
        """
        super().__init__()
        
        self.settings_manager = settings_manager
        
        # Initialize components - do this before UI setup to start preloading
        self.init_components()
        
        # Pre-load the overlay and make it ready to display
        self.init_overlay()
        
        # Set up the UI
        self.setup_ui()
        
        # Set up system tray
        self.setup_tray()
        
        # Connect signals
        self.connect_signals()
        
        # Current state
        self.recording = False
        self.transcribing = False
        
        # Set window icon (same as tray icon)
        self.setWindowIcon(self.create_app_icon())
        
        # Minimize to tray if configured
        if self.settings_manager.get_setting("minimize_to_tray", True):
            self.hide()
        else:
            self.show()
            
        # Start a background thread to preload transcription models
        self.preload_models()
        
        # Load settings into the UI
        self.load_settings()
    
    def init_components(self):
        """Initialize and preload components"""
        # Initialize recorder with preloaded audio system
        self.recorder = AudioRecorder()
        
        # Initialize transcription manager
        self.transcription_manager = TranscriptionManager(self.settings_manager)
        
        # Initialize text inserter
        self.text_inserter = TextInserter()
    
    def init_overlay(self):
        """Initialize the overlay"""
        # Create overlay and make it ready
        self.overlay = OverlayWidget()
        
        # Preload overlay states
        # This is now handled in OverlayWidget.__init__
        
    def preload_models(self):
        """Preload transcription models in a background thread"""
        def _preload():
            try:
                logger.info("Preloading transcription models")
                # The transcription manager already initializes models in its constructor
                # Just log that we've completed preloading
                logger.info("Transcription models are ready")
            except Exception as e:
                logger.error(f"Error preloading models: {e}")
                
        # Start preloading in background
        preload_thread = threading.Thread(target=_preload)
        preload_thread.daemon = True
        preload_thread.start()
        
    def setup_ui(self):
        """Set up the UI elements"""
        # Set window properties
        self.setWindowTitle("Khmer TTS")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.create_overview_tab()
        self.create_general_tab()
        self.create_api_keys_tab()
        self.create_language_tab()
        
        # Add tabs
        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.api_keys_tab, "API Keys")
        self.tabs.addTab(self.language_tab, "Language")
        
        # Add tabs to main layout
        main_layout.addWidget(self.tabs)
        
        # Save button container (right-aligned)
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add spacer to push button to the right
        button_layout.addStretch()
        
        # Save button
        save_button = QPushButton("Save Settings")
        save_button.setFixedWidth(120)  # Set fixed width for the button
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        # Add button container to main layout
        main_layout.addWidget(button_container)
    
    def create_overview_tab(self):
        """Create the overview tab"""
        self.overview_tab = QWidget()
        layout = QVBoxLayout()
        
        # Add app logo/icon
        icon_label = QLabel()
        icon_pixmap = self.create_app_icon().pixmap(QSize(128, 128))
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title label
        title_label = QLabel("Khmer TTS Application")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Description label
        description_label = QLabel(
            "Press the configured shortcut to record audio. "
            "The audio will be transcribed and inserted at the cursor position."
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # Shortcut label
        self.shortcut_label = QLabel()
        self.shortcut_label.setAlignment(Qt.AlignCenter)
        self.shortcut_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.shortcut_label)
        
        # Update shortcut text
        self.update_shortcut_label()
        
        # Status area
        status_group = QGroupBox("Current Status")
        status_layout = QVBoxLayout()
        
        # Status labels
        self.status_label = QLabel("Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Spacer
        layout.addStretch()
        
        self.overview_tab.setLayout(layout)
    
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
        
        # Add link to get API key
        google_link_label = QLabel("<a href='https://aistudio.google.com/'>Get API key here</a>")
        google_link_label.setOpenExternalLinks(True)
        google_layout.addRow("", google_link_label)
        
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
        
        # Add link to get API key
        elevenlabs_link_label = QLabel("<a href='https://elevenlabs.io/app/settings/api-keys'>Get API key here</a>")
        elevenlabs_link_label.setOpenExternalLinks(True)
        elevenlabs_layout.addRow("", elevenlabs_link_label)
        
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
            
            # Update UI elements that depend on settings
            self.update_shortcut_label()
            
            # Update keyboard listener shortcut if changed
            new_shortcut = self.shortcut_input.text()
            if hasattr(self, 'keyboard_thread') and self.keyboard_thread:
                self.keyboard_thread.update_shortcut(new_shortcut)
            
            # No confirmation dialog, just minimize to tray
            self.hide()
            
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error saving settings: {str(e)}")
    
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
    
    def setup_tray(self):
        """Set up the system tray icon"""
        # Create the tray icon with the same icon as the application
        self.tray_icon = QSystemTrayIcon(self.create_app_icon(), self)
        self.tray_icon.setToolTip("Khmer TTS - Voice to Text")
        
        # Create tray menu
        tray_menu = QMenu()
        
        # Open action - we're not adding this as the click behavior will open the app
        # Instead, show this in the menu for clarity
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.show_main_window)
        tray_menu.addAction(open_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close_application)
        tray_menu.addAction(exit_action)
        
        # Set the tray menu
        self.tray_icon.setContextMenu(tray_menu)
        
        # Show the tray icon
        self.tray_icon.show()
        
        # Connect tray icon activation - changed to use clicked instead of DoubleClick
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
    def connect_signals(self):
        """Connect signals to slots"""
        # Connect transcription signals
        self.transcription_manager.transcription_started.connect(self.on_transcription_started)
        self.transcription_manager.transcription_completed.connect(self.on_transcription_completed)
        self.transcription_manager.transcription_error.connect(self.on_transcription_error)
        
        # Load settings on show
        self.tabs.currentChanged.connect(self.on_tab_changed)
    
    def on_tab_changed(self, index):
        """Handle tab changed event"""
        # If switching to a settings tab, load the latest settings
        if index > 0:  # First tab (index 0) is the overview
            self.load_settings()
    
    def update_shortcut_label(self):
        """Update the shortcut label with the current shortcut"""
        shortcut = self.settings_manager.get_setting("shortcut", "ctrl+alt+space")
        self.shortcut_label.setText(f"Current shortcut: {shortcut}")
    
    def show_main_window(self):
        """Show the main window and bring it to the front"""
        self.showNormal()  # Show the window in its normal state
        self.activateWindow()  # Bring it to the front
        self.raise_()  # Raise it to the top of the window stack
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Minimize to tray instead of closing
        if self.tray_icon.isVisible():
            QMessageBox.information(
                self, "Khmer TTS",
                "The application will keep running in the system tray. "
                "To terminate the program, choose 'Exit' in the context menu "
                "of the system tray icon."
            )
            self.hide()
            event.ignore()
        else:
            event.accept()
    
    def close_application(self):
        """Close the application"""
        # Clean up resources
        self.recorder.close()
        
        # Hide the tray icon
        self.tray_icon.hide()
        
        # Quit the application
        QTimer.singleShot(0, self.close)
        QTimer.singleShot(100, lambda: sys.exit(0))
    
    def tray_icon_activated(self, reason):
        """
        Handle tray icon activation
        Now responds to single clicks instead of requiring double-clicks
        """
        if reason == QSystemTrayIcon.Trigger:  # Single click
            self.show_main_window()
    
    @pyqtSlot()
    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            logger.warning("Already recording")
            return
        
        logger.info("Starting recording")
        self.recording = True
        
        # Update status in UI
        self.status_label.setText("Recording...")
        self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        
        # Update overlay first to give immediate visual feedback
        if self.settings_manager.get_setting("show_overlay", True):
            self.overlay.set_state("recording")
            
        # Start recording in a very short timer to prevent UI blocking
        QTimer.singleShot(10, self._start_recording_impl)
    
    def _start_recording_impl(self):
        """Actual recording implementation - called after overlay is shown"""
        # Start the actual recording
        self.recorder.start_recording()
    
    @pyqtSlot()
    def stop_recording(self):
        """Stop recording and start transcription"""
        if not self.recording:
            logger.warning("Not recording")
            return
        
        logger.info("Stopping recording")
        self.recording = False
        
        # Update status in UI
        self.status_label.setText("Processing recording...")
        self.status_label.setStyleSheet("color: #3498db; font-weight: bold;")
        
        # Stop recording and get the audio file
        audio_file = self.recorder.stop_recording()
        
        if audio_file:
            logger.info(f"Recording saved to {audio_file}")
            
            # Start transcription
            model_name = self.settings_manager.get_setting("transcription_model", "gemini_flash")
            self.transcription_manager.transcribe(audio_file, model_name)
        else:
            logger.error("Failed to save recording")
            
            # Update UI
            self.status_label.setText("Failed to save recording")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            
            # Update overlay
            if self.settings_manager.get_setting("show_overlay", True):
                self.overlay.set_state("idle")
    
    @pyqtSlot()
    def on_transcription_started(self):
        """Handle transcription started"""
        logger.info("Transcription started")
        self.transcribing = True
        
        # Update status in UI
        self.status_label.setText("Transcribing...")
        self.status_label.setStyleSheet("color: #3498db; font-weight: bold;")
        
        # Update overlay
        if self.settings_manager.get_setting("show_overlay", True):
            self.overlay.set_state("transcribing")
    
    @pyqtSlot(str)
    def on_transcription_completed(self, text):
        """
        Handle transcription completed
        
        Args:
            text: Transcribed text
        """
        logger.info("Transcription completed")
        self.transcribing = False
        
        # Update status in UI
        self.status_label.setText("Idle")
        self.status_label.setStyleSheet("")
        
        # Update overlay
        if self.settings_manager.get_setting("show_overlay", True):
            self.overlay.set_state("idle")
        
        if text:
            logger.info(f"Transcription result: {text}")
            
            # Insert the text
            insertion_method = self.settings_manager.get_setting("insertion_method", "clipboard")
            self.text_inserter.insert_text_async(text, insertion_method)
            
            # Show notification
            self.tray_icon.showMessage(
                "Transcription Completed",
                "The transcribed text has been inserted.",
                QSystemTrayIcon.Information,
                3000
            )
        else:
            logger.warning("Empty transcription result")
            
            # Show notification
            self.tray_icon.showMessage(
                "Transcription Failed",
                "The transcription result was empty.",
                QSystemTrayIcon.Warning,
                3000
            )
    
    @pyqtSlot(str)
    def on_transcription_error(self, error):
        """
        Handle transcription error
        
        Args:
            error: Error message
        """
        logger.error(f"Transcription error: {error}")
        self.transcribing = False
        
        # Update status in UI
        self.status_label.setText("Error during transcription")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        
        # Update overlay
        if self.settings_manager.get_setting("show_overlay", True):
            self.overlay.set_state("idle")
        
        # Show notification
        self.tray_icon.showMessage(
            "Transcription Error",
            f"Error during transcription: {error}",
            QSystemTrayIcon.Critical,
            3000
        )