# Khmer STT Application

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
2. Run the `KhmerSSTTetup.exe` installer.
3. Follow the on-screen instructions to complete the installation.
4. Optionally, enable the "Start automatically with Windows" option during installation.
5. Launch the application from the Start menu or desktop shortcut.
6. Open the settings dialog by clicking on the tray icon and enter your API keys.

### For Developers

1. Clone the repository:
   ```
   git clone <repository-url>
   cd khmer-stt-app
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
   This will create an installer at `output/KhmerSSTTetup.exe`.

## Usage

1. The application runs in the background with a system tray icon.
2. Press and hold the shortcut key combination (default: Ctrl+Alt+Space) in any application to start recording.
3. Release the keys to stop recording and start transcription.
4. An overlay will show the status of recording and transcription.
5. The transcribed text will be inserted at your cursor position.

## Configuration

Access the settings dialog by clicking on the system tray icon:

- **General tab**: Configure startup behavior, minimize options, and keyboard shortcut
- **API Keys tab**: Enter and test your Google Gemini and ElevenLabs API keys
- **Language tab**: Set your preferred language for transcription

## Technical Details

- Built with Python and PyQt5
- Uses pynput for global keyboard shortcuts
- Utilizes PyAudio for audio recording
- Supports two transcription models: Google Gemini Flash and ElevenLabs
- Secure API key storage via Windows Credentials Manager
- Custom overlay widget for status display

## Troubleshooting

- **Application doesn't start**: Check if you have Python installed and all dependencies.
- **Shortcut doesn't work**: Make sure no other application is using the same shortcut.
- **Transcription fails**: Verify your API keys and internet connection.
- **Text insertion issues**: The application simulates keyboard input; some applications may block this.

## License

MIT License - See LICENSE file for details.

## Acknowledgements

- Thanks to the Google Gemini and ElevenLabs teams for providing the APIs
- Special thanks to contributors and testers
