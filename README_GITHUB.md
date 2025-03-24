# Khmer TTS Application

A standalone Windows 11 application for voice recording and transcription with a global keyboard shortcut. Specializing in Khmer language support, but works with multiple languages.

## Features

- Global keyboard shortcut (Ctrl+Alt+Space by default) that works in any application
- Records audio while the shortcut is held down
- Transcribes recordings using Google Gemini or ElevenLabs
- Inserts transcribed text at the cursor position
- Elegant overlay during recording and transcription
- System tray integration for easy access
- Secure API key storage using Windows Credentials Manager

## Demo

[Screenshot/GIF would be here]

## Installation

You can install Khmer TTS in two ways:

### Download the Installer

1. Go to the [Releases](../../releases) page
2. Download the latest `KhmerTTS_Setup.exe`
3. Run the installer and follow the instructions

### Build from Source

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Build Your Own Installer

This repo includes GitHub Actions workflows that automatically build Windows installers. To use this:

1. Fork this repository
2. Enable GitHub Actions for your fork
3. Make any changes you want to the code
4. Push to your repository
5. Go to the Actions tab to download the built installer

## Configuration

When you first run the application, it will appear in your system tray. Click the icon to open the settings dialog where you can:

- Set your API keys for Google Gemini and ElevenLabs
- Change the global keyboard shortcut
- Select your preferred language (including Khmer)
- Customize other application settings

## API Keys

You'll need to obtain API keys from:
- [Google AI Studio](https://aistudio.google.com/) for Gemini
- [ElevenLabs](https://elevenlabs.io/app/settings/api-keys) for ElevenLabs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Pillow](https://python-pillow.org/) for image processing
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio recording
- [Google Gemini](https://ai.google.dev/) for transcription
- [ElevenLabs](https://elevenlabs.io/) for transcription
