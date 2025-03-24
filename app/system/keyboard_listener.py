"""
Keyboard listener for global shortcuts
"""

import threading
import time
import logging
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal, QThread

logger = logging.getLogger(__name__)

class KeyboardThread(QThread):
    """Thread for listening to keyboard events"""
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()
    
    def __init__(self, shortcut_keys=None):
        """Initialize the keyboard listener thread"""
        super().__init__()
        self.shortcut_keys = shortcut_keys or {"ctrl_l", "alt_l", "space"}
        self.currently_pressed = set()
        self.listener = None
        self.running = True
        self.is_recording = False
        
        # Set high priority for this thread to reduce latency
        self.setPriority(QThread.HighestPriority)
    
    def on_press(self, key):
        """Handle key press events"""
        try:
            # Convert key to string representation
            key_str = key.name if hasattr(key, 'name') else key.char
            
            # Add to currently pressed keys
            if key_str:
                self.currently_pressed.add(key_str)
            
            # Check if shortcut is pressed
            if self.check_shortcut_pressed() and not self.is_recording:
                logger.info("Shortcut pressed - Starting recording")
                self.is_recording = True
                # Emit signal directly without extra processing
                self.recording_started.emit()
                
        except Exception as e:
            logger.error(f"Error in on_press: {str(e)}")
    
    def on_release(self, key):
        """Handle key release events"""
        try:
            # Convert key to string representation
            key_str = key.name if hasattr(key, 'name') else key.char
            
            # Remove from currently pressed keys
            if key_str in self.currently_pressed:
                self.currently_pressed.remove(key_str)
            
            # If we were recording and shortcut is released, stop recording
            if self.is_recording and not self.check_shortcut_pressed():
                logger.info("Shortcut released - Stopping recording")
                self.is_recording = False
                # Emit signal directly without extra processing
                self.recording_stopped.emit()
                
        except Exception as e:
            logger.error(f"Error in on_release: {str(e)}")
        
        # Continue listening
        return self.running
    
    def check_shortcut_pressed(self):
        """Check if the configured shortcut combination is pressed"""
        # Fast path for common case
        if not self.currently_pressed:
            return False
            
        # Check if all required keys are pressed
        return all(k in self.currently_pressed for k in self.shortcut_keys)
    
    def update_shortcut(self, new_shortcut):
        """Update the shortcut keys"""
        if isinstance(new_shortcut, str):
            # Convert string like "ctrl+alt+space" to set
            self.shortcut_keys = set(new_shortcut.lower().split('+'))
        elif isinstance(new_shortcut, (list, set)):
            self.shortcut_keys = set(k.lower() for k in new_shortcut)
    
    def run(self):
        """Run the keyboard listener thread"""
        logger.info("Starting keyboard listener thread")
        
        try:
            # Start the keyboard listener with minimal blocking
            with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release,
                suppress=False  # Don't suppress events for faster processing
            ) as self.listener:
                self.listener.join()
                
        except Exception as e:
            logger.error(f"Error in keyboard listener: {str(e)}")
    
    def stop(self):
        """Stop the keyboard listener thread"""
        logger.info("Stopping keyboard listener thread")
        self.running = False
        if self.listener:
            self.listener.stop()


def start_keyboard_listener(main_window):
    """Start the keyboard listener thread"""
    # Create and start keyboard listener thread
    keyboard_thread = KeyboardThread()
    
    # Connect signals
    keyboard_thread.recording_started.connect(main_window.start_recording)
    keyboard_thread.recording_stopped.connect(main_window.stop_recording)
    
    # Start thread with high priority
    keyboard_thread.start()
    
    return keyboard_thread