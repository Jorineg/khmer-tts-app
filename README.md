# Khmer TTS Application

A Windows application that allows recording audio with a global shortcut and transcribing it using different models.

## Features

- Global shortcut (default: Ctrl+Alt+Space) to record audio in any application
- Audio transcription using Gemini Flash and ElevenLabs models
- Insertion of transcribed text at the cursor position
- Overlay showing recording and transcription status
- System tray icon for easy access
- Settings dialog for customization
- Secure API key storage using Windows Credentials Manager
- Support for multiple languages, with special focus on Khmer

## Requirements

- Windows 11
- Python 3.8 or higher
- API keys for Google Gemini and ElevenLabs (for transcription)

## Installation

### For End Users

1. Download the installer from the releases page or request it from the developer.
2. Run the `KhmerTTSSetup.exe` installer.
3. Follow the on-screen instructions to complete the installation.
4. Optionally, enable the "Start automatically with Windows" option during installation.
5. Launch the application from the Start menu or desktop shortcut.
6. Open the settings dialog by clicking on the tray icon and enter your API keys.

### For Developers

1. Clone the repository:
   ```
   git clone <repository-url>
   cd khmer-tts-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys (optional, you can also set them in the settings dialog):
   ```
   GOOGLE_API_KEY=your_google_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

4. Run the application:
   ```
   python main.py
   ```

### Building the Application

You have several options to build the executable:

#### Option 1: Simple Build (Recommended for most users)
1. Run the `simple_win11_build.bat` script:
   ```
   simple_win11_build.bat
   ```
   This creates a single-file executable that's easy to distribute.

#### Option 2: GUI-based Build
1. Run the `use_auto_py_to_exe.bat` script:
   ```
   use_auto_py_to_exe.bat
   ```
   This opens a graphical interface where you can configure and build the executable.

#### Option 3: GitHub Actions (Recommended for CI/CD)
1. Push your code to a GitHub repository with the included workflow file.
2. GitHub will automatically build the executable and installer.
3. Download the installer from the GitHub Actions artifacts.

#### Option 4: Alternative Packaging Tools
The repository also includes setup scripts for other packaging tools:
- `setup_briefcase.bat` - Uses BeeWare's Briefcase for cross-platform packaging
- `setup_pyoxidizer.bat` - Uses PyOxidizer for more optimized executables
- `build_with_pyapp.bat` - Uses PyApp for simpler Windows packaging

### Building the Installer

To build the Windows installer:

1. Make sure you have all requirements installed:
   ```
   pip install -r requirements.txt
   pip install pillow
   ```

2. Install Inno Setup:
   - Run `install_inno_setup.bat` to download and install Inno Setup, or
   - Download and install manually from [Inno Setup website](https://jrsoftware.org/isdl.php)

3. Build the installer:
   ```
   build_installer.bat
   ```

4. The installer (`KhmerTTSSetup.exe`) will be created in the project root directory.

## Usage

1. Start the application. It will automatically minimize to the system tray.
2. Press and hold the configured shortcut (default: Ctrl+Alt+Space) to record audio.
3. Release the shortcut to stop recording and start transcription.
4. The transcribed text will be inserted at the cursor position.

## Configuration

Click on the system tray icon and select "Settings" to configure the application:

- Change the recording shortcut
- Select the default transcription model
- Configure API keys
- Change the language
- Customize the overlay appearance
- Configure startup behavior

## License

[MIT License](LICENSE)

## Acknowledgements

This application uses the following open-source libraries:
- PyQt5 for the GUI
- pynput for global keyboard shortcuts
- pyaudio for audio recording
- Google Generative AI Python SDK for Gemini API
- ElevenLabs Python SDK for ElevenLabs API
