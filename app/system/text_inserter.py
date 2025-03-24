"""
Utility for inserting text into active applications via clipboard or simulated key presses
"""

import time
import logging
import threading
import pyperclip
from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

class TextInserter:
    """Class to handle text insertion via clipboard or key simulation"""
    
    def __init__(self):
        """Initialize the text inserter"""
        self.keyboard = Controller()
        
    def insert_text(self, text, method="clipboard"):
        """
        Insert text into the active application
        
        Args:
            text: Text to insert
            method: Method to use (clipboard or keypress)
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            logger.warning("No text to insert")
            return False
            
        if method == "clipboard":
            return self._insert_via_clipboard(text)
        elif method == "keypress":
            return self._insert_via_keypress(text)
        else:
            logger.error(f"Unknown insertion method: {method}")
            return False
            
    def _insert_via_clipboard(self, text):
        """
        Insert text using clipboard (Ctrl+V)
        
        Args:
            text: Text to insert
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Store original clipboard content
            original_clipboard = pyperclip.paste()
            
            # Copy text to clipboard
            pyperclip.copy(text)
            
            # Small delay to ensure clipboard is updated
            time.sleep(0.2)
            
            # Paste text (Ctrl+V)
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('v')
            self.keyboard.release('v')
            self.keyboard.release(Key.ctrl)
            
            # Small delay after paste
            time.sleep(0.2)
            
            # Restore original clipboard content
            pyperclip.copy(original_clipboard)
            
            logger.info("Text inserted via clipboard")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting text via clipboard: {str(e)}")
            return False
            
    def _insert_via_keypress(self, text):
        """
        Insert text by simulating key presses
        
        Args:
            text: Text to insert
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Type the text character by character
            for char in text:
                self.keyboard.press(char)
                self.keyboard.release(char)
                # Small delay between keypresses
                time.sleep(0.01)
                
            logger.info("Text inserted via key presses")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting text via key presses: {str(e)}")
            return False
            
    def insert_text_async(self, text, method="clipboard", delay=0.5):
        """
        Insert text asynchronously
        
        Args:
            text: Text to insert
            method: Method to use (clipboard or keypress)
            delay: Delay before insertion (seconds)
            
        Returns:
            Threading thread object
        """
        # Create a thread for insertion
        thread = threading.Thread(
            target=self._insert_with_delay,
            args=(text, method, delay)
        )
        thread.daemon = True
        thread.start()
        
        return thread
        
    def _insert_with_delay(self, text, method, delay):
        """Helper function for delayed insertion"""
        # Wait for the specified delay
        time.sleep(delay)
        
        # Insert the text
        self.insert_text(text, method)
