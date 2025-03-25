"""
Transcription handler to manage recording and transcription processes
"""

import logging
import threading
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from ..audio.recorder import AudioRecorder
from .transcription_manager import TranscriptionManager

logger = logging.getLogger(__name__)

class TranscriptionHandler(QObject):
    """
    Handler class for recording and transcription processes
    
    This class manages the audio recording and transcription workflow, 
    allowing the main window to focus on UI concerns.
    """
    
    # Define signals for state changes
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal(str)  # Audio file path
    transcription_started = pyqtSignal()
    transcription_completed = pyqtSignal(str)  # Transcribed text
    transcription_error = pyqtSignal(str)  # Error message
    
    def __init__(self, settings_manager):
        """
        Initialize the transcription handler
        
        Args:
            settings_manager: SettingsManager instance
        """
        super().__init__()
        
        self.settings_manager = settings_manager
        self.recording = False
        self.transcribing = False
        
        # Initialize components
        self.recorder = AudioRecorder()
        self.transcription_manager = TranscriptionManager(settings_manager)
        
        # Connect transcription manager signals
        self.transcription_manager.transcription_started.connect(self._on_transcription_started)
        self.transcription_manager.transcription_completed.connect(self._on_transcription_completed)
        self.transcription_manager.transcription_error.connect(self._on_transcription_error)
        
        # Preload models in background
        self._preload_models()
    
    def _preload_models(self):
        """Preload transcription models in a background thread"""
        def _preload():
            try:
                logger.info("Preloading transcription models")
                # The transcription manager already initializes models in its constructor
                logger.info("Transcription models are ready")
            except Exception as e:
                logger.error(f"Error preloading models: {e}")
                
        # Start preloading in background
        preload_thread = threading.Thread(target=_preload)
        preload_thread.daemon = True
        preload_thread.start()
    
    def start_recording(self, show_overlay=None):
        """
        Start recording audio
        
        Args:
            show_overlay: Optional callback to show overlay
        """
        if self.recording:
            logger.warning("Already recording")
            return
        
        logger.info("Starting recording")
        self.recording = True
        
        # Emit signal
        self.recording_started.emit()
        
        # Show overlay if callback provided
        if show_overlay and callable(show_overlay):
            # Delayed start of recording to ensure overlay is visible
            QTimer.singleShot(100, self._start_recording_impl)
        else:
            # Start recording immediately
            self._start_recording_impl()
    
    def _start_recording_impl(self):
        """Internal method to actually start the recording"""
        try:
            # Start recording
            self.recorder.start_recording()
            logger.info("Recording started")
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            self.recording = False
            self.transcription_error.emit(f"recording_error:{str(e)}")
    
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
            
            # Emit signal
            self.recording_stopped.emit(audio_file)
            
            # Start transcription
            default_model = self.settings_manager.get_setting("default_model")
            language = self.settings_manager.get_setting("language")
            
            logger.info(f"Starting transcription with model: {default_model}, language: {language}")
            
            # Call transcribe
            self.transcription_manager.transcribe(audio_file, default_model)
            
        except Exception as e:
            logger.error(f"Error stopping recording: {e}")
            self.recording = False
            self.transcription_error.emit(f"recording_error:{str(e)}")
    
    def _on_transcription_started(self):
        """Handle transcription started"""
        logger.info("Transcription started")
        self.transcribing = True
        self.transcription_started.emit()
    
    def _on_transcription_completed(self, text):
        """
        Handle transcription completed
        
        Args:
            text: Transcribed text
        """
        logger.info(f"Transcription completed: {text}")
        self.transcribing = False
        self.transcription_completed.emit(text)
    
    def _on_transcription_error(self, error):
        """
        Handle transcription error
        
        Args:
            error: Error message
        """
        logger.error(f"Transcription error: {error}")
        self.transcribing = False
        self.transcription_error.emit(error)
    
    def update_transcription_model(self, model_name):
        """
        Update the transcription model
        
        Args:
            model_name: Model name to use for transcription
        """
        self.transcription_manager.update_transcription_model(model_name)
    
    def update_language(self, language):
        """
        Update the transcription language
        
        Args:
            language: Language code to use for transcription
        """
        self.transcription_manager.update_language(language)
    
    def check_model_api_key(self, model_name):
        """
        Check if API key is available for the specified model
        
        Args:
            model_name: Model name to check
            
        Returns:
            True if API key is available, False otherwise
        """
        if model_name == "gemini_flash" and not self.settings_manager.get_api_key("google"):
            logger.warning(f"No Google API key available for selected model: {model_name}")
            return False
        elif model_name == "elevenlabs" and not self.settings_manager.get_api_key("elevenlabs"):
            logger.warning(f"No ElevenLabs API key available for selected model: {model_name}")
            return False
        else:
            return True
    
    def close(self):
        """Close the handler and free resources"""
        self.recorder.close()
