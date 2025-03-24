"""
ElevenLabs Speech-to-Text model implementation
"""

import os
import json
import sys
import re
from io import BytesIO

# Add parent directory to path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from config import get_elevenlabs_api_key
from app.transcription.models.base_model import BaseSTTModel

# Import the official ElevenLabs SDK
from elevenlabs.client import ElevenLabs

class ElevenLabsModel(BaseSTTModel):
    """
    STT model implementation for ElevenLabs API using the official SDK
    """
    
    def __init__(self, api_key=None, language_code="khm"):
        """Initialize the ElevenLabs STT model"""
        self.api_key = api_key or get_elevenlabs_api_key()
        if not self.api_key:
            raise ValueError("ElevenLabs API key is required. Set the ELEVENLABS_API_KEY environment variable in your .env file or provide it when initializing the model.")
        
        # Initialize the ElevenLabs client
        self.client = ElevenLabs(api_key=self.api_key)
        
        # Set language code
        self.language_code = language_code
    
    @property
    def name(self) -> str:
        """Return the name of the model"""
        return "ElevenLabs"
    
    def transcribe(self, audio_file):
        """
        Transcribe audio using ElevenLabs API
        
        Args:
            audio_file (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        try:
            print(f"Reading audio file: {os.path.basename(audio_file)}")
            
            # Read the audio file
            with open(audio_file, "rb") as f:
                audio_data = BytesIO(f.read())
            
            print(f"Sending audio to ElevenLabs API (model: scribe_v1, language: {self.language_code})")
            
            # Call the ElevenLabs API using the SDK
            response = self.client.speech_to_text.convert(
                file=audio_data,
                model_id="scribe_v1",  # Correct model ID as per documentation
                language_code=self.language_code,   # Use language code from settings
                diarize=False,         # Whether to identify different speakers
                tag_audio_events=False # Whether to tag audio events like laughter, etc.
            )
            
            print("Transcription request completed")
            
            # The response from ElevenLabs can be in different formats depending on the SDK version
            # Let's handle each possibility
            
            # Get the text from the response
            if hasattr(response, 'text'):
                # Direct text attribute
                transcribed_text = response.text
            elif isinstance(response, dict) and 'text' in response:
                # Dictionary with text key
                transcribed_text = response['text']
            elif hasattr(response, 'transcript'):
                # Some versions use 'transcript' instead of 'text'
                transcribed_text = response.transcript
            elif isinstance(response, dict) and 'transcript' in response:
                # Dictionary with transcript key
                transcribed_text = response['transcript']
            elif isinstance(response, str):
                # Direct string response
                transcribed_text = response
            else:
                # If we can't find a standard attribute, convert to string
                transcribed_text = str(response)
                
                # Try to extract just the text part if it's a complex string
                # Looking for patterns like {'text': '...', 'other_key': '...'}
                text_match = re.search(r"'text':\s*'([^']*)'", transcribed_text)
                if text_match:
                    transcribed_text = text_match.group(1)
            
            # Clean up the transcribed text
            transcribed_text = transcribed_text.strip()
            
            return transcribed_text
                
        except Exception as e:
            print(f"Error transcribing with ElevenLabs: {str(e)}")
            
            # Try to extract and print detailed error information
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                try:
                    error_json = e.response.json()
                    print(f"Error details: {json.dumps(error_json, indent=2)}")
                except:
                    print(f"Response content: {e.response.text}")
            
            return ""
