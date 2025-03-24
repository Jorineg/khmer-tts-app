"""
Main application entry point
"""

import sys
import os
import logging
import ctypes
import tempfile
import time
import errno
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

# Import the main window implementation
from app.gui.main_window import MainWindow
from app.system.keyboard_listener import start_keyboard_listener
from app.settings.settings_manager import SettingsManager

# Windows API constants for window activation
SW_RESTORE = 9
SW_SHOW = 5

# Import Windows-specific functions for window activation
if sys.platform == 'win32':
    from ctypes import windll
    SetForegroundWindow = windll.user32.SetForegroundWindow
    ShowWindow = windll.user32.ShowWindow
    GetForegroundWindow = windll.user32.GetForegroundWindow

# Determine log file location in user's AppData folder
app_name = "KhmerSTT"
app_data_dir = os.path.join(os.environ.get('APPDATA', '.'), app_name)
os.makedirs(app_data_dir, exist_ok=True)
log_file = os.path.join(app_data_dir, 'app.log')

# File for single instance check
LOCK_FILE = os.path.join(app_data_dir, 'app.lock')
SIGNAL_FILE = os.path.join(app_data_dir, 'app.signal')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler for unhandled exceptions"""
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def is_started_from_autostart():
    """
    Check if application was started from Windows startup using command-line argument
    
    Returns:
        True if app was started from Windows startup with --autostart flag, False otherwise
    """
    return '--autostart' in sys.argv

def check_signal_file():
    """Check if signal file exists, if it does, delete it and return True"""
    if os.path.exists(SIGNAL_FILE):
        try:
            os.remove(SIGNAL_FILE)
            return True
        except Exception as e:
            logger.error(f"Failed to remove signal file: {e}")
    return False

def create_signal_file():
    """Create signal file to tell running instance to show window"""
    try:
        with open(SIGNAL_FILE, 'w') as f:
            f.write('SHOW')
        return True
    except Exception as e:
        logger.error(f"Failed to create signal file: {e}")
        return False

def acquire_lock():
    """Try to acquire lock file. Returns (lock_file_handle, True) if successful, (None, False) if another instance has the lock"""
    try:
        if sys.platform == 'win32':
            try:
                # Check if the lock file exists
                if os.path.exists(LOCK_FILE):
                    try:
                        # Try to read PID from the file
                        with open(LOCK_FILE, 'r') as f:
                            pid_str = f.read().strip()
                            
                        if pid_str:
                            try:
                                pid = int(pid_str)
                                # Check if the process with this PID is still running
                                import psutil
                                if not psutil.pid_exists(pid) or pid == os.getpid():
                                    logger.info(f"Stale lock file found with PID {pid}, removing it")
                                    os.remove(LOCK_FILE)
                                else:
                                    # Process is still running, another instance exists
                                    logger.info("Lock file exists with valid PID, another instance is running")
                                    create_signal_file()
                                    return None, False
                            except (ValueError, ProcessLookupError):
                                # Invalid PID or process doesn't exist
                                logger.info("Invalid PID in lock file, removing it")
                                os.remove(LOCK_FILE)
                            except ImportError:
                                # psutil not available, continue with normal check
                                logger.info("Lock file exists but can't verify PID, assuming another instance")
                                create_signal_file()
                                return None, False
                    except Exception as e:
                        logger.error(f"Error reading PID from lock file: {e}")
                        # Continue and try to create a new lock file
                
                # Try to create the lock file (Windows-specific)
                lock_handle = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                # Write PID to file
                os.write(lock_handle, str(os.getpid()).encode('utf-8'))
                return lock_handle, True
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Lock file exists, try to signal the running instance
                    logger.info("Lock file exists, another instance is running")
                    create_signal_file()
                    return None, False
                # Other error
                logger.error(f"Failed to create lock file: {e}")
                return None, False
        else:
            # Non-Windows platforms (not needed for this app but included for completeness)
            import fcntl
            lock_file = open(LOCK_FILE, 'w')
            try:
                fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                # Write PID to file
                lock_file.write(str(os.getpid()))
                lock_file.flush()
                return lock_file, True
            except IOError:
                # Lock file exists, try to signal the running instance
                logger.info("Lock file exists, another instance is running")
                create_signal_file()
                lock_file.close()
                return None, False
    except Exception as e:
        logger.error(f"Error acquiring lock: {e}")
        return None, False

def release_lock(lock_file_handle):
    """Release lock file"""
    try:
        if sys.platform == 'win32':
            os.close(lock_file_handle)
            try:
                os.remove(LOCK_FILE)
            except:
                pass
        else:
            # Non-Windows platforms
            lock_file_handle.close()
            try:
                os.remove(LOCK_FILE)
            except:
                pass
    except Exception as e:
        logger.error(f"Error releasing lock: {e}")

class SingleApplication(QApplication):
    """Application with single instance support"""
    
    show_window_signal = pyqtSignal()
    
    def __init__(self, argv):
        super().__init__(argv)
        self.activation_window = None
        self.lock_handle = None
        
        # Start a timer to check for the signal file
        self.signal_timer = QTimer(self)
        self.signal_timer.timeout.connect(self.check_for_signals)
        self.signal_timer.start(1000)  # Check every second
    
    def set_activation_window(self, window):
        """Set the window to be shown when a second instance is started"""
        self.activation_window = window
        self.show_window_signal.connect(self.show_window)
    
    def check_for_signals(self):
        """Check if signal file exists"""
        if check_signal_file():
            self.show_window_signal.emit()
    
    def show_window(self):
        """Show and activate the main window"""
        if self.activation_window:
            logger.info("Signal received, showing main window")
            try:
                # Show window
                self.activation_window.show_main_window()
                
                # Try to bring window to front (Windows-specific)
                if sys.platform == 'win32':
                    try:
                        hwnd = self.activation_window.winId()
                        # Get current foreground window
                        foreground_hwnd = GetForegroundWindow()
                        
                        # If our window is not foreground
                        if foreground_hwnd != hwnd:
                            # Show window and bring to front
                            ShowWindow(hwnd, SW_SHOW)
                            SetForegroundWindow(hwnd)
                    except Exception as e:
                        logger.error(f"Failed to bring window to front: {e}")
            except Exception as e:
                logger.error(f"Failed to bring window to front: {e}")
        else:
            logger.warning("Signal received but no activation window set")

def main():
    """Main entry point of the application"""
    try:
        logger.info("Starting application")
        
        # Set up global exception handler
        sys.excepthook = handle_exception
        
        # Acquire lock file
        lock_handle, is_first_instance = acquire_lock()
        
        # If not first instance, exit
        if not is_first_instance:
            logger.info("Another instance is already running, exiting")
            return 0
        
        # High DPI support
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create application
        app = SingleApplication(sys.argv)
        app.setApplicationName("Khmer STT")
        app.setQuitOnLastWindowClosed(False)  # Keep running when window is closed
        app.lock_handle = lock_handle
        
        # Make sure to release lock on exit
        app.aboutToQuit.connect(lambda: release_lock(lock_handle))
        
        # Check if app was started from autostart
        auto_started = is_started_from_autostart()
        if auto_started:
            logger.info("Application started from Windows startup (--autostart flag)")
        else:
            logger.info("Application started manually (no --autostart flag)")
        
        # Initialize settings
        settings_manager = SettingsManager()
        
        # Initialize main window
        main_window = MainWindow(settings_manager, show_on_startup=(not auto_started))
        
        # Set the main window to be shown when a new instance is started
        app.set_activation_window(main_window)
        
        # Start keyboard listener
        start_keyboard_listener(main_window)
        
        # Execute the application
        return app.exec_()
        
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
