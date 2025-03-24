"""
Main application window
"""

import os
import sys
import logging
import threading
from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QSize
from PyQt5.QtGui import QIcon

from .base_window import BaseWindow
from .tray_manager import TrayManager
from .language_selector import LanguageSelector
from .tabs import OverviewTab, GeneralTab, ApiKeysTab, LanguageTab
from .overlay import OverlayWidget
from ..audio.recorder import AudioRecorder
from ..transcription.transcription_manager import TranscriptionManager
from ..system.text_inserter import TextInserter
from ..settings.settings_manager import SettingsManager
from ..i18n.translation_manager import TranslationManager

logger = logging.getLogger(__name__)

class MainWindow(BaseWindow):
    """Main application window"""
    
    def __init__(self, settings_manager, show_on_startup=True):
        """
        Initialize the main window
        
        Args:
            settings_manager: SettingsManager instance
            show_on_startup: Whether to show the window on startup
        """
        # Initialize base window
        super().__init__(settings_manager)
        
        # Initialize translation manager
        self.translation_manager = TranslationManager(settings_manager)
        
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
        
        # Set window title
        self.setWindowTitle(self.translation_manager.get_string("window_title"))
        
        # Show window based on startup parameter
        if show_on_startup:
            self.show()
        else:
            self.hide()
            
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
        self.overlay = OverlayWidget(translation_manager=self.translation_manager)
    
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
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)  # Reduced spacing overall
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Set up tabs
        self.create_tabs()
        
        # Add tabs to main layout
        main_layout.addWidget(self.tabs)
        
        # Add language selector above the button container
        self.language_selector = LanguageSelector(self, self.translation_manager)
        self.language_selector.languageChanged.connect(self.change_language)
        main_layout.addWidget(self.language_selector)
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        # Spacer to push buttons to the right side
        button_layout.addStretch()
        
        # Quit button (now more subtle)
        self.quit_button = QPushButton(self.translation_manager.get_string("buttons.quit"))
        self.quit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #555555;
                border: 1px solid #d0d0d0;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.setFixedWidth(120)
        self.quit_button.clicked.connect(QApplication.quit)
        button_layout.addWidget(self.quit_button)
        
        # Add some spacing between buttons
        button_layout.addSpacing(10)
        
        # Hide Window button (subtle with blue border)
        self.hide_button = QPushButton(self.translation_manager.get_string("buttons.hide_window"))
        self.hide_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #3498db;
                border: 1px solid #3498db;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
            }
            QPushButton:pressed {
                background-color: #d6e9f8;
            }
        """)
        self.hide_button.setCursor(Qt.PointingHandCursor)
        self.hide_button.setFixedWidth(120)
        self.hide_button.clicked.connect(self.hide)
        self.hide_button.setDefault(True)
        button_layout.addWidget(self.hide_button)
        
        # Add button container to main layout
        main_layout.addWidget(button_container)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
        # Apply global stylesheet
        self.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #f5f5f7;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                background-color: white;
                border-radius: 5px;
            }
            
            QTabBar::tab {
                background-color: #e6e6e6;
                color: #555555;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #d0d0d0;
                border-bottom: none;
                min-width: 80px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
                color: #3498db;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 12px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QLabel {
                color: #333333;
            }
            
            /* Define styles for input widgets */
            QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 5px;
                background-color: #ffffff;
                selection-background-color: #3498db;
                selection-color: #ffffff;
                height: 16px;
            }
            
            /* Custom dropdown arrow using the arrow image */
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #d0d0d0;
            }
            
            QComboBox::down-arrow {
                image: url(resources/arrow_down.png);
                width: 16px;
                height: 16px;
            }
            
            /* Rest of the stylesheet remains the same */
        """)
        
        # Set window properties
        self.setWindowTitle("Khmer Speech-to-Text")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resources", "icon.png")))
        self.setMinimumSize(600, 500)
        
        # Create the tray icon is handled in setup_tray() which is called from __init__
    
    def create_tabs(self):
        """Create all tabs and add them to the tab widget"""
        # Create tab instances
        self.overview_tab = OverviewTab(self, self.windowIcon(), self.translation_manager)
        self.general_tab = GeneralTab(self, self.settings_manager, self.translation_manager)
        self.api_keys_tab = ApiKeysTab(self, self.settings_manager, self.translation_manager)
        self.language_tab = LanguageTab(self, self.settings_manager, self.translation_manager)
        
        # Add tabs
        self.tabs.addTab(self.overview_tab, self.translation_manager.get_string("tabs.overview"))
        self.tabs.addTab(self.general_tab, self.translation_manager.get_string("tabs.general"))
        self.tabs.addTab(self.api_keys_tab, self.translation_manager.get_string("tabs.api_keys"))
        self.tabs.addTab(self.language_tab, self.translation_manager.get_string("tabs.language"))
    
    def load_settings(self):
        """Load current settings into the UI"""
        # Update shortcut label in overview tab
        shortcut = self.settings_manager.get_setting("shortcut")
        self.overview_tab.update_shortcut_label(shortcut)
        
        # Update language selector
        language = self.settings_manager.get_setting("ui_language")
        self.language_selector.set_language(language)
        
        # No need to load settings for each tab as they already load their settings in their constructors
    
    def setup_tray(self):
        """Set up the system tray icon"""
        # Create TrayManager with the app icon
        self.tray_manager = TrayManager(self, self.windowIcon(), self.translation_manager)
    
    def connect_signals(self):
        """Connect signals to slots"""
        # Connect transcription signals
        self.transcription_manager.transcription_started.connect(self.on_transcription_started)
        self.transcription_manager.transcription_completed.connect(self.on_transcription_completed)
        self.transcription_manager.transcription_error.connect(self.on_transcription_error)
    
    def update_shortcut_label(self):
        """Update the shortcut label in the overview tab"""
        shortcut = self.settings_manager.get_setting("shortcut")
        self.overview_tab.update_shortcut_label(shortcut)
    
    def show_main_window(self):
        """Show the main window and bring it to the front"""
        self.showNormal()  # Show the window in its normal state
        self.activateWindow()  # Bring it to the front
        self.raise_()  # Raise it to the top of the window stack
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Minimize to tray instead of closing
        if self.tray_manager.is_visible():
            QMessageBox.information(
                self, 
                self.translation_manager.get_string("app_name"),
                self.translation_manager.get_string("notifications.keep_running_notice_quit_button")
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
        self.tray_manager.hide()
        
        # Quit the application
        QTimer.singleShot(0, self.close)
        QTimer.singleShot(100, lambda: sys.exit(0))
    
    @pyqtSlot()
    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            logger.warning("Already recording")
            return
        
        logger.info("Starting recording")
        self.recording = True
        
        # Update status in UI
        self.overview_tab.set_status("status.recording")
        
        # Get overlay setting
        show_overlay = self.settings_manager.get_setting("show_overlay")
        overlay_position = self.settings_manager.get_setting("overlay_position")
        
        if show_overlay:
            # Show overlay before recording
            self.overlay.set_recording_state()
            # Position the overlay before showing it - no need to pass position to show()
            self.overlay.position_at_bottom()
            self.overlay.show()
            
            # Delayed start of recording to ensure overlay is visible
            QTimer.singleShot(100, self._start_recording_impl)
        else:
            # Start recording immediately
            self._start_recording_impl()
    
    def _start_recording_impl(self):
        """Actual recording implementation - called after overlay is shown"""
        try:
            # Start recording
            self.recorder.start_recording()
            logger.info("Recording started")
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            self.recording = False
            self.overview_tab.set_status("status.error", error_state=True)
            self.overlay.hide()
    
    @pyqtSlot()
    def stop_recording(self):
        """Stop recording and start transcription"""
        if not self.recording:
            logger.warning("Not recording")
            return
        
        logger.info("Stopping recording")
        
        try:
            # Stop recording
            audio_file = self.recorder.stop_recording()
            self.recording = False
            
            # Update status
            self.overview_tab.set_status("status.transcribing")
            
            # Update overlay
            self.overlay.set_transcribing_state()
            
            # Start transcription
            default_model = self.settings_manager.get_setting("default_model")
            language = self.settings_manager.get_setting("language")
            
            logger.info(f"Starting transcription with model: {default_model}, language: {language}")
            # Update the language setting before transcription
            self.settings_manager.set_setting("language", language)
            # Call transcribe with the correct number of arguments
            self.transcription_manager.transcribe(audio_file, default_model)
            
        except Exception as e:
            logger.error(f"Error stopping recording: {e}")
            self.recording = False
            self.overview_tab.set_status("status.error", error_state=True)
            self.overlay.hide()
    
    @pyqtSlot()
    def on_transcription_started(self):
        """Handle transcription started"""
        logger.info("Transcription started")
        self.transcribing = True
        self.overview_tab.set_status("status.transcribing")
    
    @pyqtSlot(str)
    def on_transcription_completed(self, text):
        """
        Handle transcription completed
        
        Args:
            text: Transcribed text
        """
        logger.info(f"Transcription completed: {text}")
        self.transcribing = False
        
        # Hide the overlay
        self.overlay.hide()
        
        # Set the transcribed text using the configured method
        insertion_method = self.settings_manager.get_setting("insertion_method")
        try:
            self.text_inserter.insert_text(text, method=insertion_method)
            logger.info(f"Text inserted using {insertion_method} method")
        except Exception as e:
            logger.error(f"Error inserting text: {e}")
            self.tray_manager.showMessage(
                self.translation_manager.get_string("notifications.error_title"),
                self.translation_manager.get_string("notifications.insert_error", error=str(e)),
                timeout=3000
            )
        
        # Update status
        self.overview_tab.set_status("status.idle")
    
    @pyqtSlot(str)
    def on_transcription_error(self, error):
        """
        Handle transcription error
        
        Args:
            error: Error message
        """
        logger.error(f"Transcription error: {error}")
        self.transcribing = False
        
        # Show error in overlay
        self.overlay.set_error_state()
        
        # Hide overlay after a delay
        QTimer.singleShot(3000, self.overlay.hide)
        
        # Update status
        self.overview_tab.set_status("status.error", error_state=True)
        
        # Show notification
        self.tray_manager.showMessage(
            self.translation_manager.get_string("notifications.transcription_error_title"),
            self.translation_manager.get_string("notifications.transcription_error", error=error),
            timeout=5000
        )
    
    def update_global_shortcut(self, shortcut):
        """Update the global shortcut listener"""
        # This would update the keyboard listener thread
        if hasattr(self, 'keyboard_thread') and self.keyboard_thread:
            self.keyboard_thread.update_shortcut(shortcut)
        
        # Update shortcut display in overview tab
        self.update_shortcut_label()
    
    def update_startup_registry(self, run_on_startup):
        """Update the startup registry"""
        # Implementation depends on system (Windows registry, Linux autostart, etc.)
        logger.info(f"Setting run on startup: {run_on_startup}")
        # Actual implementation would be platform-specific
    
    def change_language(self, language_code):
        """Change the UI language"""
        logger.info(f"Changing UI language to: {language_code}")
        
        # Set the language in the translation manager
        self.translation_manager.set_language(language_code)
        
        # Save the language setting
        self.settings_manager.set_setting("ui_language", language_code)
        
        # Update all UI elements
        self.update_ui_language()
    
    def update_ui_language(self):
        """Update all UI text after language change"""
        # Update window title
        self.setWindowTitle(self.translation_manager.get_string("window_title"))
        
        # Update button texts
        self.quit_button.setText(self.translation_manager.get_string("buttons.quit"))
        self.hide_button.setText(self.translation_manager.get_string("buttons.hide_window"))
        
        # Update tab titles
        self.tabs.setTabText(0, self.translation_manager.get_string("tabs.overview"))
        self.tabs.setTabText(1, self.translation_manager.get_string("tabs.general"))
        self.tabs.setTabText(2, self.translation_manager.get_string("tabs.api_keys"))
        self.tabs.setTabText(3, self.translation_manager.get_string("tabs.language"))
        
        # Update language selector
        self.language_selector.update_language()
        
        # Update each tab
        self.overview_tab.update_language()
        self.general_tab.update_language()
        self.api_keys_tab.update_language()
        self.language_tab.update_language()
        
        # Update tray menu
        self.tray_manager.update_menu_text()
        self.tray_manager.update_tooltip()
