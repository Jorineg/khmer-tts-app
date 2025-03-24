"""
Shortcut recorder widget for capturing keyboard shortcuts
"""

import logging
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent

logger = logging.getLogger(__name__)

# Special key mapping for display
KEY_DISPLAY_NAMES = {
    Qt.Key_Control: "Ctrl",
    Qt.Key_Alt: "Alt",
    Qt.Key_Shift: "Shift",
    Qt.Key_Meta: "Meta",
    Qt.Key_Super_L: "Win",
    Qt.Key_Super_R: "Win",
    Qt.Key_Space: "Space",
    Qt.Key_Return: "Enter",
    Qt.Key_Escape: "Esc",
    Qt.Key_Tab: "Tab",
    Qt.Key_Backspace: "Backspace",
    Qt.Key_CapsLock: "CapsLock",
    Qt.Key_F1: "F1",
    Qt.Key_F2: "F2",
    Qt.Key_F3: "F3",
    Qt.Key_F4: "F4",
    Qt.Key_F5: "F5",
    Qt.Key_F6: "F6",
    Qt.Key_F7: "F7",
    Qt.Key_F8: "F8",
    Qt.Key_F9: "F9",
    Qt.Key_F10: "F10",
    Qt.Key_F11: "F11",
    Qt.Key_F12: "F12",
}

# Keys that should only be used as modifiers
MODIFIER_KEYS = {
    Qt.Key_Control,
    Qt.Key_Alt,
    Qt.Key_Shift,
    Qt.Key_Meta,
    Qt.Key_Super_L,
    Qt.Key_Super_R,
}

# Mapping from Qt modifier flags to key names
MODIFIER_MAP = {
    Qt.ControlModifier: "ctrl",
    Qt.AltModifier: "alt",
    Qt.ShiftModifier: "shift", 
    Qt.MetaModifier: "meta",
}

class ShortcutRecorder(QLineEdit):
    """Widget for recording keyboard shortcuts"""
    
    shortcutChanged = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(True)
        self.setPlaceholderText("Click here and press keys to record shortcut")
        self.setClearButtonEnabled(True)
        
        # Current key combination
        self.current_keys = set()
        self.key_string = ""
        
        # Flag to indicate if we're recording
        self.recording = False
        
        # Connect signals
        self.textChanged.connect(self._text_changed)
    
    def focusInEvent(self, event):
        """Called when the widget receives focus"""
        super().focusInEvent(event)
        self.recording = True
        self.setPlaceholderText("Press keyboard shortcut...")
        self.selectAll()
        
        # Highlight that we're recording
        self.setStyleSheet("background-color: #ffeeee;")
        
        # Log for debugging
        logger.debug("ShortcutRecorder started recording")
    
    def focusOutEvent(self, event):
        """Called when the widget loses focus"""
        super().focusOutEvent(event)
        self.recording = False
        self.setPlaceholderText("Click here and press keys to record shortcut")
        
        # Reset highlight
        self.setStyleSheet("")
        
        # Log for debugging
        logger.debug(f"ShortcutRecorder stopped recording. Final shortcut: {self.text()}")
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events"""
        if not self.recording:
            return super().keyPressEvent(event)
        
        # Prevent default handling
        event.accept()
        
        # Get the key code
        key = event.key()
        
        # Escape cancels recording and restores previous value
        if key == Qt.Key_Escape:
            self.clearFocus()
            return
        
        # Add key to current combination
        if key not in self.current_keys:
            self.current_keys.add(key)
            self._update_display()
    
    def keyReleaseEvent(self, event: QKeyEvent):
        """Handle key release events"""
        if not self.recording:
            return super().keyReleaseEvent(event)
        
        # Prevent default handling
        event.accept()
        
        # Get the key code
        key = event.key()
        
        # Remove key from current combination
        if key in self.current_keys:
            self.current_keys.remove(key)
            
        # If all keys are released and we had a non-modifier key,
        # finish recording
        if not self.current_keys and key not in MODIFIER_KEYS:
            self.clearFocus()
    
    def _update_display(self):
        """Update the display with current key combination"""
        if not self.current_keys:
            self.clear()
            return
        
        # Build a display string and internal string
        display_parts = []
        internal_parts = []
        
        # Add modifier keys first (in a consistent order)
        for mod_key in [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta, Qt.Key_Super_L, Qt.Key_Super_R]:
            if mod_key in self.current_keys:
                display_parts.append(KEY_DISPLAY_NAMES.get(mod_key, "Unknown"))
                
                # Map the modifier key to its internal name
                if mod_key in [Qt.Key_Control, Qt.Key_Super_L, Qt.Key_Super_R]:
                    internal_parts.append("ctrl")
                elif mod_key == Qt.Key_Alt:
                    internal_parts.append("alt")
                elif mod_key == Qt.Key_Shift:
                    internal_parts.append("shift")
                elif mod_key == Qt.Key_Meta:
                    internal_parts.append("meta")
        
        # Add non-modifier keys
        for key in sorted(self.current_keys):
            if key not in MODIFIER_KEYS:
                key_name = KEY_DISPLAY_NAMES.get(key)
                if key_name is None:
                    # For letter keys or other keys, use their text
                    key_name = chr(key).upper() if key >= 32 and key <= 126 else f"Key({key})"
                
                display_parts.append(key_name)
                
                # For the internal representation
                if key == Qt.Key_Space:
                    internal_parts.append("space")
                elif key >= 32 and key <= 126:
                    internal_parts.append(chr(key).lower())
                else:
                    # Use the display name for special keys
                    internal_parts.append(key_name.lower())
        
        # Set the text with display version (using + as separator)
        display_text = " + ".join(display_parts)
        self.setText(display_text)
        
        # Store the internal version
        self.key_string = "+".join(internal_parts)
        
        # Log for debugging
        logger.debug(f"ShortcutRecorder updated: display='{display_text}', internal='{self.key_string}'")
    
    def _text_changed(self, text):
        """Handle text changes (only emit our signal when done recording)"""
        if not self.recording and text:
            self.shortcutChanged.emit(self.key_string)
    
    def get_shortcut(self):
        """Get the current shortcut as a string in internal format (for keyboard_listener)"""
        return self.key_string
    
    def set_shortcut(self, shortcut):
        """Set the shortcut display from a string"""
        if not shortcut:
            self.clear()
            return
            
        # Parse the shortcut string and display it nicely
        parts = shortcut.split('+')
        display_parts = []
        
        for part in parts:
            part = part.strip().lower()
            if part == 'ctrl':
                display_parts.append('Ctrl')
            elif part == 'alt':
                display_parts.append('Alt')  
            elif part == 'shift':
                display_parts.append('Shift')
            elif part == 'meta':
                display_parts.append('Meta')
            elif part == 'space':
                display_parts.append('Space')
            else:
                # Capitalize single characters
                display_parts.append(part.upper() if len(part) == 1 else part.capitalize())
        
        display_text = " + ".join(display_parts)
        self.setText(display_text)
        self.key_string = shortcut
