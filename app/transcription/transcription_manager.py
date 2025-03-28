"""
Transcription manager to handle different STT models
"""

import os
import sys
import logging
import threading
from PyQt5.QtCore import QObject, pyqtSignal

# Import the STT models from the new location
from app.transcription.models.gemini_model import GeminiFlashModel
from app.transcription.models.elevenlabs_model import ElevenLabsModel

logger = logging.getLogger(__name__)

class TranscriptionManager(QObject):
    """
    Manager class for handling transcription with different models
    """
    # Signals
    transcription_started = pyqtSignal()
    transcription_completed = pyqtSignal(str)
    transcription_error = pyqtSignal(str)
    
    def __init__(self, settings_manager):
        """
        Initialize the transcription manager
        
        Args:
            settings_manager: Settings manager instance
        """
        super().__init__()
        self.settings_manager = settings_manager
        
        # Initialize models
        self.models = {}
        self.initialize_models()
        
        # State variables
        self.current_audio_file = None
        self.transcription_thread = None
        
    def initialize_models(self):
        """Initialize available STT models"""
        logger.info("Initializing STT models")
        
        # Clear existing models
        self.models = {}
        
        # Get current language setting
        language_code = self.settings_manager.get_setting("language")
        
        # Get API keys
        google_api_key = self.settings_manager.get_api_key("google")
        elevenlabs_api_key = self.settings_manager.get_api_key("elevenlabs")
        
        try:
            # Initialize Gemini Flash model if Google API key is available
            if google_api_key:
                self.models["gemini_flash"] = GeminiFlashModel(language_code=language_code)
                logger.info(f"Initialized Gemini Flash model with language: {language_code}")
            else:
                logger.warning("Skipping Gemini Flash model initialization - Google API key not found")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Flash model: {str(e)}")
        
        try:
            # Initialize ElevenLabs model if ElevenLabs API key is available
            if elevenlabs_api_key:
                self.models["elevenlabs"] = ElevenLabsModel(language_code=language_code)
                logger.info(f"Initialized ElevenLabs model with language: {language_code}")
            else:
                logger.warning("Skipping ElevenLabs model initialization - ElevenLabs API key not found")
        except Exception as e:
            logger.error(f"Failed to initialize ElevenLabs model: {str(e)}")
    
    def refresh_models(self):
        """Reinitialize models with current settings and API keys"""
        logger.info("Refreshing transcription models")
        self.initialize_models()
        return list(self.models.keys())
    
    def get_available_models(self):
        """Get a list of available STT models"""
        return list(self.models.keys())
    
    def transcribe(self, audio_file, model_name=None):
        """
        Transcribe audio using the selected model
        
        Args:
            audio_file: Path to audio file
            model_name: Model to use (default: from settings)
        """
        if not os.path.exists(audio_file):
            logger.error(f"Audio file does not exist: {audio_file}")
            self.transcription_error.emit(f"Audio file not found: {audio_file}")
            return
        
        # Get model from settings if not specified
        if model_name is None:
            model_name = self.settings_manager.get_setting("transcription_model")
        
        # Check if model is available
        if model_name not in self.models:
            logger.error(f"Model not available: {model_name}")
            
            # Check if this is due to missing API key
            if model_name == "gemini_flash" and not self.settings_manager.get_api_key("google"):
                logger.error(f"Google API key missing for model: {model_name}")
                self.transcription_error.emit("missing_api_key:gemini_flash")
                return
            elif model_name == "elevenlabs" and not self.settings_manager.get_api_key("elevenlabs"):
                logger.error(f"ElevenLabs API key missing for model: {model_name}")
                self.transcription_error.emit("missing_api_key:elevenlabs")
                return
            
            # General case - model not available for other reasons
            available_models = ", ".join(self.models.keys())
            self.transcription_error.emit(f"Model {model_name} not available. Available models: {available_models}")
            return
        
        # Get current language setting
        language_code = self.settings_manager.get_setting("language")
        
        # Reinitialize model with current language if it has changed 
        # (models store language at initialization time)
        current_model = self.models[model_name]
        if hasattr(current_model, 'language_code') and current_model.language_code != language_code:
            logger.info(f"Language changed to {language_code}, reinitializing {model_name} model")
            if model_name == "gemini_flash":
                self.models[model_name] = GeminiFlashModel(language_code=language_code)
            elif model_name == "elevenlabs":
                self.models[model_name] = ElevenLabsModel(language_code=language_code)
        
        # Store current audio file
        self.current_audio_file = audio_file
        
        # Emit started signal
        self.transcription_started.emit()
        
        # Start transcription in a separate thread
        self.transcription_thread = threading.Thread(
            target=self._transcribe_thread,
            args=(audio_file, model_name)
        )
        self.transcription_thread.daemon = True
        self.transcription_thread.start()
    
    def _transcribe_thread(self, audio_file, model_name):
        """Background thread for transcription"""
        logger.info(f"Starting transcription with model: {model_name}")
        
        try:
            # Get the model
            model = self.models[model_name]
            
            # Transcribe the audio
            transcription = model.transcribe(audio_file)
            
            # Log and emit result
            logger.info("Transcription completed successfully")
            self.transcription_completed.emit(transcription)
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            
            # Check for specific error types
            error_str = str(e).lower()
            
            # Check for network-related errors
            if any(network_err in error_str for network_err in [
                "connection", "network", "timeout", "unreachable", "proxy", 
                "dns", "timed out", "socket", "connect", "connection refused"
            ]):
                logger.error("Network connection error detected")
                self.transcription_error.emit(f"network_error:{model_name}")
            
            # Check for API-specific errors
            elif any(api_err in error_str for api_err in [
                "unauthorized", "403", "401", "quota", "limit", "rate limit",
                "invalid key", "api key", "service unavailable", "server error",
                "500", "502", "503", "504", "bad gateway"
            ]):
                logger.error("API service error detected")
                self.transcription_error.emit(f"api_error:{model_name}")
            
            # Generic transcription error
            else:
                self.transcription_error.emit(f"Transcription error: {str(e)}")
            
    def cancel_transcription(self):
        """Cancel ongoing transcription"""
        # Cannot directly stop the thread as the API call is blocking
        # but we can set a flag to ignore the result
        self.current_audio_file = None
        
    def update_transcription_model(self, model_name):
        """
        Update the active transcription model
        
        Args:
            model_name: Name of the model to use for transcription
        """
        logger.info(f"Updating transcription model to: {model_name}")
        
        # Check if model is available
        if model_name not in self.models:
            logger.warning(f"Model {model_name} not available, checking API keys")
            
            # Try to initialize the model if it's not available
            if model_name == "gemini_flash" and not self.settings_manager.get_api_key("google"):
                logger.error("Google API key missing for Gemini Flash model")
                self.transcription_error.emit("missing_api_key:gemini_flash")
                return
            elif model_name == "elevenlabs" and not self.settings_manager.get_api_key("elevenlabs"):
                logger.error("ElevenLabs API key missing for ElevenLabs model")
                self.transcription_error.emit("missing_api_key:elevenlabs")
                return
            
            # Try to reinitialize the models
            self.refresh_models()
            
            # Check again if model is available after refresh
            if model_name not in self.models:
                available_models = ", ".join(self.models.keys())
                logger.error(f"Model {model_name} still not available after refresh. Available models: {available_models}")
                self.transcription_error.emit(f"Model {model_name} not available. Available models: {available_models}")
                return
        
        # Update the setting
        self.settings_manager.set_setting("transcription_model", model_name)
        logger.info(f"Transcription model updated to: {model_name}")
        