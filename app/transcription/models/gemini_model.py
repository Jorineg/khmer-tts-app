"""
Google Gemini Pro and Gemini Flash STT model implementation
"""

import os
import sys
import time
from google import genai
from google.genai import types

# Add path to include root directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from config import get_google_api_key
from app.transcription.models.base_model import BaseSTTModel
class GeminiModel(BaseSTTModel):
    """
    Base class for Google Gemini models
    """
    
    def __init__(self, model_name="gemini-2.0-pro-exp-02-05", language_code="khm"):
        """
        Initialize the Google Gemini model
        
        Args:
            model_name: The model to use (gemini-2.0-pro-exp-02-05, gemini-2.0-flash, etc.)
            language_code: The ISO language code for transcription
        """
        self.api_key = get_google_api_key()
        if not self.api_key:
            raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file")
        
        # Initialize the Google Generative AI client
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        self.language_code = language_code
        
        # Get language name from ISO code
        self.language_name = self._get_language_name(language_code)
        
        # Define the system prompt for transcription
        self.system_prompt = f"""
        You are a professional {self.language_name} language transcriber. 
        Your task is to transcribe the provided {self.language_name} language audio file accurately.
        Respond ONLY with the exact transcription in {self.language_name} script.
        Do not include any explanations, notes, or additional text.
        Do not translate the content.
        """
    
    def _get_language_name(self, iso_code):
        """Get the full language name from ISO code"""
        language_map = {
            "khm": "Khmer",
            "eng": "English",
            "tha": "Thai",
            "vie": "Vietnamese",
            "zho": "Chinese",
            "jpn": "Japanese",
            "kor": "Korean",
            "fra": "French",
            "spa": "Spanish",
            "deu": "German",
            "rus": "Russian",
            "ara": "Arabic",
            "hin": "Hindi"
        }
        return language_map.get(iso_code, "Unknown")
    
    def transcribe(self, audio_file):
        """
        Transcribe an audio file using Google Gemini
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Transcription text
        """
        # Check if the file exists
        if not os.path.isfile(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        print(f"Sending audio to Google Gemini API (model: {self.model_name}, language: {self.language_name})")
        
        try:
            # Prepare the audio file to be sent to the API
            with open(audio_file, "rb") as f:
                audio_data = f.read()
            
            # Create a request to the Gemini API with the audio content
            response = self.client.models.generate_content(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.0,  # Use lowest temperature for accurate transcription
                ),
                contents=[
                    f"Please transcribe this {self.language_name} audio file. Return ONLY the transcription without any explanations.",
                    types.Part.from_bytes(
                        data=audio_data,
                        mime_type=self._get_mime_type(audio_file),
                    )
                ]
            )
            
            # Extract the transcription text from the response
            transcription = response.text.strip()
            
            return transcription
            
        except Exception as e:
            raise Exception(f"Error transcribing with Google Gemini: {str(e)}")
    
    def _get_mime_type(self, audio_file):
        """
        Get the MIME type of an audio file based on its extension
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            MIME type string
        """
        ext = os.path.splitext(audio_file)[1].lower()
        mime_types = {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mpeg',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.m4a': 'audio/mp4',
        }
        
        return mime_types.get(ext, 'audio/wav')  # Default to wav if unknown


class GeminiProModel(GeminiModel):
    """
    Google Gemini Pro model for STT
    """
    
    def __init__(self, language_code="khm"):
        """Initialize with the Gemini Pro model"""
        super().__init__(model_name="gemini-2.0-pro-exp-02-05", language_code=language_code)


class GeminiFlashModel(GeminiModel):
    """
    Google Gemini Flash model for STT
    """
    
    def __init__(self, language_code="khm"):
        """Initialize with the Gemini Flash model"""
        super().__init__(model_name="gemini-2.0-flash", language_code=language_code)


class GeminiFlashLiteModel(GeminiModel):
    """
    Google Gemini Flash Lite model for STT
    """
    
    def __init__(self, language_code="khm"):
        """Initialize with the Gemini Flash Lite model"""
        super().__init__(model_name="gemini-2.0-flash-lite", language_code=language_code)