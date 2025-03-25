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
from .styles.app_stylesheet import get_main_stylesheet, get_subtle_button_style, get_accent_button_style
from ..transcription.transcription_handler import TranscriptionHandler
from ..system.text_inserter import TextInserter
from ..settings.settings_manager import SettingsManager
from ..i18n.translation_manager import translation_manager

logger = logging.getLogger(__name__)

class MainWindow(BaseWindow):
    """Main application window"""
    
    def __init__(self, settings_manager, show_on_startup=True):
        # Initialize base window
        super().__init__(settings_manager)
        
        # No need to store the translation_manager as an instance variable
        # We'll use the imported singleton directly wherever needed
        logger.info(f"MainWindow initializing with translation language: {translation_manager.current_language}")
        
        # Store references to translatable UI elements
        self.translatable_elements = {}
        
        self.init_components()
        self.init_overlay()
        self.setup_ui()
        self.setup_tray()
        self.connect_signals()
        self.setWindowTitle(translation_manager.get_string("window_title"))
        
        # Show window based on startup parameter
        if show_on_startup:
            self.show()
        else:
            self.hide()
            
        # Load settings into the UI
        self.load_settings()
        
        # Check API keys after a short delay
        QTimer.singleShot(500, self.check_api_keys_available)
        
        # Initialize keyboard thread as None - will be set by start_keyboard_listener
        self.keyboard_thread = None
    
    def init_components(self):
        """Initialize and preload components"""
        self.text_inserter = TextInserter()
        self.transcription_handler = TranscriptionHandler(self.settings_manager)
        
        # Connect transcription handler signals
        self.transcription_handler.recording_started.connect(self.on_recording_started)
        self.transcription_handler.recording_stopped.connect(self.on_recording_stopped)
        self.transcription_handler.transcription_started.connect(self.on_transcription_started)
        self.transcription_handler.transcription_completed.connect(self.on_transcription_completed)
        self.transcription_handler.transcription_error.connect(self.on_transcription_error)
    
    def init_overlay(self):
        """Initialize the overlay"""
        # Create overlay and make it ready
        self.overlay = OverlayWidget(translation_manager=translation_manager)
    
    def setup_ui(self):
        """Set up the UI elements"""
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(16, 0, 16, 16)
        main_layout.setSpacing(8)  # Reduced spacing overall
        
        self.tabs = QTabWidget()
        self.setup_tabs()
        main_layout.addWidget(self.tabs)
        
        # Create bottom container to hold language selector and buttons side by side
        bottom_container = QWidget()
        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add language selector to the left side of bottom container
        self.language_selector = LanguageSelector(self)
        self.language_selector.languageChanged.connect(self.change_language)
        bottom_layout.addWidget(self.language_selector)
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # Spacer to push buttons to the right side
        button_layout.addStretch()
        
        # Quit button (now more subtle)
        self.quit_button = QPushButton(translation_manager.get_string("buttons.quit"))
        self.translatable_elements['quit_button'] = ('QPushButton', "buttons.quit")
        self.quit_button.setStyleSheet(get_subtle_button_style())
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.setFixedWidth(120)
        self.quit_button.clicked.connect(QApplication.quit)
        button_layout.addWidget(self.quit_button)
        
        # Add some spacing between buttons
        button_layout.addSpacing(10)
        
        # Hide Window button (subtle with blue border)
        self.hide_button = QPushButton(translation_manager.get_string("buttons.hide_window"))
        self.translatable_elements['hide_button'] = ('QPushButton', "buttons.hide_window")
        self.hide_button.setStyleSheet(get_accent_button_style())
        self.hide_button.setCursor(Qt.PointingHandCursor)
        self.hide_button.setFixedWidth(120)
        self.hide_button.clicked.connect(self.hide)
        self.hide_button.setDefault(True)
        button_layout.addWidget(self.hide_button)
        
        # Add button container to right side of bottom container
        bottom_layout.addWidget(button_container)
        
        # Add the bottom container to the main layout
        main_layout.addWidget(bottom_container)
        
        self.setCentralWidget(main_widget)
        self.setStyleSheet(get_main_stylesheet())
        self.translatable_elements['window_title'] = ('Window', "window_title")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resources", "icon.png")))
        self.setMinimumSize(600, 600)
    
    def setup_tabs(self):
        """Set up the tab view and individual tabs"""
        logger.debug("Setting up tabs")
        
        # Only settings is needed since tabs use the translation singleton directly
        settings = self.settings_manager
        
        # Create tabs
        self.overview_tab = OverviewTab(
            self,
            app_icon=self.windowIcon(),
            settings_manager=settings
        )
        self.general_tab = GeneralTab(self,settings_manager=settings)
        self.language_tab = LanguageTab(self,settings_manager=settings)
        self.api_keys_tab = ApiKeysTab(self,settings_manager=settings)
        
        # Add tabs to tab widget
        self.tabs.addTab(self.overview_tab, translation_manager.get_string("tabs.overview"))
        self.tabs.addTab(self.general_tab, translation_manager.get_string("tabs.general"))
        self.tabs.addTab(self.language_tab, translation_manager.get_string("tabs.language"))
        self.tabs.addTab(self.api_keys_tab, translation_manager.get_string("tabs.api_keys"))
        
        # Store tab title translations
        self.translatable_elements['tab_overview'] = ('TabTitle', "tabs.overview", 0)
        self.translatable_elements['tab_general'] = ('TabTitle', "tabs.general", 1)
        self.translatable_elements['tab_language'] = ('TabTitle', "tabs.language", 2)
        self.translatable_elements['tab_api_keys'] = ('TabTitle', "tabs.api_keys", 3)
    
    def connect_signals(self):
        """Connect signals to slots"""
        # API Keys tab signals only
        self.api_keys_tab.api_key_changed.connect(self.on_api_key_changed)
        
        # Connect language tab signals directly to transcription handler where possible
        self.language_tab.language_changed.connect(self.transcription_handler.update_language)
        self.language_tab.model_changed.connect(self.on_model_changed)
    
    def load_settings(self):
        """Load current settings into the UI"""
        # Update shortcut label in overview tab
        shortcut = self.settings_manager.get_setting("shortcut")
        self.overview_tab.update_shortcut_label(shortcut)
        
        # Update the shortcut in the general tab if it exists
        if hasattr(self, 'general_tab') and self.general_tab and hasattr(self.general_tab, 'shortcut_input'):
            self.general_tab.shortcut_input.set_shortcut(shortcut)
            logger.debug(f"Initialized General tab shortcut input with: {shortcut}")
        
        # Update language selector
        language = self.settings_manager.get_setting("ui_language")
        self.language_selector.set_language(language)
        
        # Also update the keyboard listener if it's already created
        if hasattr(self, 'keyboard_thread') and self.keyboard_thread:
            self.keyboard_thread.update_shortcut(shortcut)
            logger.debug(f"Updated keyboard listener with shortcut: {shortcut}")
    
    def setup_tray(self):
        """Set up the system tray icon"""
        # Create TrayManager with the app icon
        self.tray_manager = TrayManager(self, self.windowIcon())
    
    def update_shortcut_label(self):
        """Update the shortcut label in the overview tab"""
        shortcut = self.settings_manager.get_setting("shortcut")
        if self.overview_tab:
            self.overview_tab.update_shortcut_label(shortcut)
            
    def update_global_shortcut(self, shortcut):
        """Update the keyboard listener with the new shortcut and update UI labels"""
        logger.info(f"Updating global shortcut to: {shortcut}")
        
        # Update the keyboard listener if it exists
        if hasattr(self, 'keyboard_thread') and self.keyboard_thread:
            self.keyboard_thread.update_shortcut(shortcut)
            logger.info(f"Updated keyboard listener with new shortcut: {shortcut}")
        
        # Update the shortcut label in the overview tab
        self.update_shortcut_label()
    
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
                translation_manager.get_string("app_name"),
                translation_manager.get_string("notifications.keep_running_notice_quit_button")
            )
            self.hide()
            event.ignore()
        else:
            event.accept()
    
    def close_application(self):
        """Close the application"""
        # Clean up resources
        self.transcription_handler.close()
        
        # Hide the tray icon
        self.tray_manager.hide()
        
        # Quit the application
        QTimer.singleShot(0, self.close)
        QTimer.singleShot(100, lambda: sys.exit(0))
    
    @pyqtSlot()
    def start_recording(self):
        """Start recording audio"""
        # Get overlay setting
        show_overlay = self.settings_manager.get_setting("show_overlay")
        overlay_position = self.settings_manager.get_setting("overlay_position")
        
        if show_overlay:
            # Show overlay before recording
            self.overlay.set_recording_state()
            # Position the overlay before showing it
            self.overlay.position_overlay(overlay_position)
            self.overlay.show()
        
        # Start recording through the handler
        self.transcription_handler.start_recording()
    
    @pyqtSlot()
    def stop_recording(self):
        """Stop recording and start transcription"""
        # Stop recording through the handler
        self.transcription_handler.stop_recording()
    
    @pyqtSlot()
    def on_recording_started(self):
        """Handle recording started signal"""
        # Update status in UI
        self.overview_tab.set_status("status.recording")
    
    @pyqtSlot(str)
    def on_recording_stopped(self, audio_file):
        """Handle recording stopped signal"""
        # Update status
        self.overview_tab.set_status("status.transcribing")
        
        # Update overlay
        self.overlay.set_transcribing_state()
        overlay_position = self.settings_manager.get_setting("overlay_position")
        self.overlay.position_overlay(overlay_position)
    
    @pyqtSlot()
    def on_transcription_started(self):
        """Handle transcription started"""
        logger.info("Transcription started")
        self.overview_tab.set_status("status.transcribing")
    
    @pyqtSlot(str)
    def on_transcription_completed(self, text):
        logger.info(f"Transcription completed: {text}")
        
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
                translation_manager.get_string("notifications.error_title"),
                translation_manager.get_string("notifications.insert_error", error=str(e)),
                timeout=3000
            )
        
        # Update status
        self.overview_tab.set_status("status.idle")
    
    @pyqtSlot(str)
    def on_transcription_error(self, error):
        logger.error(f"Transcription error: {error}")
        self.overlay.set_error_state()
        QTimer.singleShot(3000, self.overlay.hide)
        self.overview_tab.set_status("status.error", error_state=True)
        
        if error.startswith("missing_api_key:"):
            model_name = error.split(":")[1]
            self.overview_tab.update_api_key_warning(True, model_name)
            
            # Get the display name for the model
            if model_name == "gemini_flash":
                display_model = translation_manager.get_string("general_tab.model_gemini")
            elif model_name == "elevenlabs":
                display_model = translation_manager.get_string("general_tab.model_elevenlabs")
            else:
                display_model = model_name
            
            # Show more explicit notification about missing API key
            self.tray_manager.showMessage(
                translation_manager.get_string("notifications.missing_api_key_title"),
                translation_manager.get_string("notifications.missing_api_key_error", model_name=display_model),
                timeout=7000  # Longer timeout for this important message
            )
        elif error.startswith("network_error:"):
            # Show network error notification
            self.tray_manager.showMessage(
                translation_manager.get_string("notifications.network_error_title"),
                translation_manager.get_string("notifications.network_error_message"),
                timeout=7000  # Longer timeout for this important message
            )
        elif error.startswith("api_error:"):
            # Extract model name from error message
            model_name = error.split(":")[1]
            
            # Get the display name for the model
            if model_name == "gemini_flash":
                display_model = translation_manager.get_string("general_tab.model_gemini")
            elif model_name == "elevenlabs":
                display_model = translation_manager.get_string("general_tab.model_elevenlabs")
            else:
                display_model = model_name
            
            # Show API service error notification
            self.tray_manager.showMessage(
                translation_manager.get_string("notifications.api_error_title"),
                translation_manager.get_string("notifications.api_error_message", model_name=display_model),
                timeout=7000  # Longer timeout for this important message
            )
        else:
            # Normal error handling for other errors
            self.tray_manager.showMessage(
                translation_manager.get_string("notifications.transcription_error_title"),
                translation_manager.get_string("notifications.transcription_error", error=error),
                timeout=5000
            )
    
    def change_language(self, language_code):
        """Change the UI language"""
        logger.info(f"Changing UI language to: {language_code}")
        
        # Set the language in the translation manager
        translation_manager.set_language(language_code)
        
        # Save the language setting
        self.settings_manager.set_setting("ui_language", language_code)
        
        # Update the main window UI elements directly
        self.update_language()
        
        # Update translatable widgets directly - this ensures they update regardless of signal connection
        from app.gui.widgets import update_all_translatable_widgets
        logger.debug("Manually triggering update of all translatable widgets")
        update_all_translatable_widgets()
    
    def update_ui_language(self):
        """Update all UI text after language change"""
        # This method is kept for backward compatibility
        # but actual update is now handled by translation manager
        pass
    
    def update_language(self):
        """Update window UI text for the current language"""
        # Update translatable elements using the dictionary
        for widget_name, data in self.translatable_elements.items():
            widget_type = data[0]
            string_key = data[1]
            
            if widget_type == 'Window':
                self.setWindowTitle(translation_manager.get_string(string_key))
            elif widget_type == 'QPushButton':
                widget = getattr(self, widget_name, None)
                if widget:
                    widget.setText(translation_manager.get_string(string_key))
            elif widget_type == 'TabTitle':
                tab_index = data[2]
                self.tabs.setTabText(tab_index, translation_manager.get_string(string_key))
        
        # Update language selector (it handles its own translation)
        self.language_selector.update_language()
        
        # Update the feature list in the overview tab
        if hasattr(self, 'overview_tab') and hasattr(self.overview_tab, 'update_feature_list'):
            self.overview_tab.update_feature_list()
        
        # Update tray menu
        self.tray_manager.update_menu_text()
        self.tray_manager.update_tooltip()
    
    def on_model_changed(self, model_name):
        self.transcription_handler.update_transcription_model(model_name)
        self.check_model_api_key(model_name)
    
    def on_api_key_changed(self, service_name, api_key):
        logger.info(f"API key changed for {service_name}")
        current_model = self.settings_manager.get_setting("default_model")
        self.check_model_api_key(current_model)
        logger.info(f"API key changed for {service_name}")
        
        # Check if current model's API key is now available
        current_model = self.settings_manager.get_setting("default_model")
        self.check_model_api_key(current_model)
    
    def check_model_api_key(self, model_name):
        """Check if API key is available for the specified model"""
        # Use the transcription handler to check API key availability
        has_key = self.transcription_handler.check_model_api_key(model_name)
        
        # Update UI based on result
        if not has_key:
            self.overview_tab.update_api_key_warning(True, model_name)
        else:
            self.overview_tab.update_api_key_warning(False)
    
    def check_api_keys_available(self):
        """Check if API keys are available for the selected model and update UI accordingly"""
        try:
            selected_model = self.settings_manager.get_setting("default_model")
            self.check_model_api_key(selected_model)
        except Exception as e:
            logger.error(f"Error checking API keys: {e}")
