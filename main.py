"""
Main application entry point
"""

import sys
import logging
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from app.gui.main_window import MainWindow
from app.system.keyboard_listener import start_keyboard_listener
from app.settings.settings_manager import SettingsManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Global exception handler to log uncaught exceptions
    """
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def main():
    """Main entry point of the application"""
    try:
        logger.info("Starting application")
        
        # Set up global exception handler
        sys.excepthook = handle_exception
        
        # High DPI support
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Khmer TTS")
        app.setQuitOnLastWindowClosed(False)  # Keep running when window is closed
        
        # Initialize settings manager
        settings_manager = SettingsManager()
        
        # Create main window
        main_window = MainWindow(settings_manager)
        
        # Start keyboard listener
        keyboard_thread = start_keyboard_listener(main_window)
        
        # Store keyboard thread reference in main window
        main_window.keyboard_thread = keyboard_thread
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
