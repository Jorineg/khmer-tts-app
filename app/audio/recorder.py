"""
Audio recording functionality
"""

import os
import wave
import tempfile
import logging
import threading
import time
import pyaudio

logger = logging.getLogger(__name__)

class AudioRecorder:
    """Class to handle audio recording functionality"""
    
    def __init__(self, sample_rate=16000, channels=1, format_=pyaudio.paInt16):
        """
        Initialize the audio recorder
        
        Args:
            sample_rate: Sample rate for recording (default: 16000 Hz)
            channels: Number of audio channels (default: 1 - mono)
            format_: Audio format (default: 16-bit PCM)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format_
        self.chunk_size = 1024
        
        # Initialize PyAudio on startup to avoid delay when recording begins
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        
        self.is_recording = False
        self.record_thread = None
        self.temp_dir = tempfile.gettempdir()
        self.output_filename = None
        
        # Pre-initialize a stream to detect audio devices
        # This ensures all device initialization happens at startup rather than during recording
        self._init_test_stream()
        
    def _init_test_stream(self):
        """Initialize a test stream to get device ready"""
        try:
            test_stream = self.pyaudio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                start=False  # Don't actually start recording
            )
            # Close immediately - we just want to initialize the audio system
            test_stream.close()
            logger.debug("Audio system pre-initialized successfully")
        except Exception as e:
            logger.warning(f"Could not pre-initialize audio system: {str(e)}")
        
    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            logger.warning("Already recording")
            return
        
        logger.info("Starting audio recording")
        self.is_recording = True
        self.frames = []
        
        # Open audio stream
        self.stream = self.pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        # Start recording thread
        self.record_thread = threading.Thread(target=self._record)
        self.record_thread.daemon = True
        self.record_thread.start()
        
    def _record(self):
        """Record audio data in a separate thread"""
        logger.debug("Recording thread started")
        
        try:
            while self.is_recording:
                data = self.stream.read(self.chunk_size)
                self.frames.append(data)
                
        except Exception as e:
            logger.error(f"Error during recording: {str(e)}")
            self.is_recording = False
            
        logger.debug("Recording thread finished")
        
    def stop_recording(self):
        """Stop recording and save the recorded audio to a file"""
        if not self.is_recording:
            logger.warning("Not recording")
            return None
        
        logger.info("Stopping audio recording")
        self.is_recording = False
        
        # Wait for recording thread to finish
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.join(timeout=1.0)
        
        # Close the stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        # Save the recorded audio to a file
        self.output_filename = self._save_to_wav()
        
        return self.output_filename
        
    def _save_to_wav(self):
        """Save recorded frames to a WAV file"""
        if not self.frames:
            logger.warning("No audio data to save")
            return None
        
        # Create a unique filename
        timestamp = int(time.time())
        filename = os.path.join(self.temp_dir, f"recording_{timestamp}.wav")
        
        logger.info(f"Saving recording to {filename}")
        
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.pyaudio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
                
            return filename
            
        except Exception as e:
            logger.error(f"Error saving WAV file: {str(e)}")
            return None
            
    def close(self):
        """Clean up resources"""
        if self.stream:
            self.stream.close()
            
        if self.pyaudio:
            self.pyaudio.terminate()
            
        self.stream = None
        self.pyaudio = None
