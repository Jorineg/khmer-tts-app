@echo off
echo Setting up Briefcase for Khmer TTS
echo ===============================

:: Install Briefcase
echo Installing Briefcase...
pip install briefcase

:: Create a pyproject.toml file for Briefcase
echo Creating project configuration...
echo [build-system] > pyproject.toml
echo requires = ["briefcase"] >> pyproject.toml
echo build-backend = "briefcase.bootstrap" >> pyproject.toml
echo. >> pyproject.toml
echo [tool.briefcase] >> pyproject.toml
echo project_name = "Khmer TTS" >> pyproject.toml
echo bundle = "com.khmertts" >> pyproject.toml
echo version = "1.0.0" >> pyproject.toml
echo url = "https://khmertts.com" >> pyproject.toml
echo license = "MIT license" >> pyproject.toml
echo author = "Khmer TTS" >> pyproject.toml
echo author_email = "info@khmertts.com" >> pyproject.toml
echo. >> pyproject.toml
echo [tool.briefcase.app.khmertts] >> pyproject.toml
echo formal_name = "Khmer TTS" >> pyproject.toml
echo description = "A Khmer TTS application" >> pyproject.toml
echo icon = "resources/icon" >> pyproject.toml
echo sources = ["main.py", "app"] >> pyproject.toml
echo requires = [ >> pyproject.toml
echo     "keyring", >> pyproject.toml
echo     "PyQt5", >> pyproject.toml
echo     "pyaudio", >> pyproject.toml
echo     "pynput", >> pyproject.toml
echo     "google-generativeai", >> pyproject.toml
echo     "elevenlabs", >> pyproject.toml
echo     "python-dotenv", >> pyproject.toml
echo     "pyperclip", >> pyproject.toml
echo ] >> pyproject.toml
echo. >> pyproject.toml
echo [tool.briefcase.app.khmertts.windows] >> pyproject.toml
echo requires = [] >> pyproject.toml
echo system_requires = [] >> pyproject.toml
echo. >> pyproject.toml

:: Ensure app directory exists
if not exist app mkdir app

:: Move Python files into app directory
echo Moving Python files to app directory...
echo import main > app\__init__.py
echo # Just importing main module > app\__init__.py

echo.
echo Setup complete! You can now run:
echo.
echo   briefcase new    - To set up the application
echo   briefcase build  - To build the application
echo   briefcase run    - To run the application
echo   briefcase package - To package the application as an installer
echo.
echo Press any key to exit...
pause >nul
