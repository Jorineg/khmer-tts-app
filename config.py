"""
Configuration utilities for the STT project
"""

import os
import keyring
from dotenv import load_dotenv

# Load environment variables from .env file (fallback)
load_dotenv()

# Constants
API_KEY_SERVICE = "KhmerTTSApp"

# API Keys
ASSEMBLYAI_API_KEY = None
ELEVENLABS_API_KEY = None
GOOGLE_API_KEY = None
OPENAI_API_KEY = None

def get_assemblyai_api_key():
    """
    Get the AssemblyAI API key from Windows Credential Manager or environment variables
    
    Returns:
        str: AssemblyAI API key, or None if not found
    """
    global ASSEMBLYAI_API_KEY
    # Try to get API key from Windows Credentials Manager first
    api_key = keyring.get_password(API_KEY_SERVICE, "assemblyai")
    
    # Fall back to environment variable if not found in Credentials Manager
    if not api_key:
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            print("Warning: AssemblyAI API key not found in Credentials Manager or environment variables")
    
    ASSEMBLYAI_API_KEY = api_key
    return api_key

def get_elevenlabs_api_key():
    """
    Get the ElevenLabs API key from Windows Credential Manager or environment variables
    
    Returns:
        str: ElevenLabs API key, or None if not found
    """
    global ELEVENLABS_API_KEY
    # Try to get API key from Windows Credentials Manager first
    api_key = keyring.get_password(API_KEY_SERVICE, "elevenlabs")
    
    # Fall back to environment variable if not found in Credentials Manager
    if not api_key:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("Warning: ElevenLabs API key not found in Credentials Manager or environment variables")
    
    ELEVENLABS_API_KEY = api_key
    return api_key

def get_google_api_key():
    """
    Get the Google API key from Windows Credential Manager or environment variables
    
    Returns:
        str: Google API key, or None if not found
    """
    global GOOGLE_API_KEY
    # Try to get API key from Windows Credentials Manager first
    api_key = keyring.get_password(API_KEY_SERVICE, "google")
    
    # Fall back to environment variable if not found in Credentials Manager
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: Google API key not found in Credentials Manager or environment variables")
    
    GOOGLE_API_KEY = api_key
    return api_key

def get_openai_api_key():
    """
    Get the OpenAI API key from Windows Credential Manager or environment variables
    
    Returns:
        str: OpenAI API key, or None if not found
    """
    global OPENAI_API_KEY
    # Try to get API key from Windows Credentials Manager first
    api_key = keyring.get_password(API_KEY_SERVICE, "openai")
    
    # Fall back to environment variable if not found in Credentials Manager
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OpenAI API key not found in Credentials Manager or environment variables")
    
    OPENAI_API_KEY = api_key
    return api_key
