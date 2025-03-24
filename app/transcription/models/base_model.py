"""
Base model interface for Speech-to-Text models
"""

from abc import ABC, abstractmethod

class BaseSTTModel(ABC):
    """
    Abstract base class for Speech-to-Text models.
    All STT model implementations should inherit from this class.
    """
    
    @abstractmethod
    def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to the audio file to transcribe
            
        Returns:
            Transcribed text
            
        Raises:
            Exception: If transcription fails
        """
        pass
    
    @property
    def name(self) -> str:
        """Return the name of the model"""
        return self.__class__.__name__
