@echo off
echo Building Khmer TTS with PyApp
echo =========================

:: Download PyApp if not already present
if not exist pyapp.exe (
    echo Downloading PyApp...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/ofek/pyapp/releases/latest/download/pyapp.exe' -OutFile 'pyapp.exe'}"
)

:: Clean build directories
echo Cleaning build directories...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Create build directory
mkdir build

:: Create a PyApp configuration
echo Creating PyApp configuration...
echo { > build\pyapp.json
echo   "name": "Khmer TTS", >> build\pyapp.json
echo   "version": "1.0.0", >> build\pyapp.json
echo   "entry_point": "main:main", >> build\pyapp.json
echo   "console": false, >> build\pyapp.json
echo   "icon": "resources/icon.ico", >> build\pyapp.json
echo   "packages": [ >> build\pyapp.json
echo     "keyring", >> build\pyapp.json
echo     "PyQt5", >> build\pyapp.json
echo     "pyaudio", >> build\pyapp.json
echo     "pynput", >> build\pyapp.json
echo     "google-generativeai", >> build\pyapp.json
echo     "elevenlabs", >> build\pyapp.json
echo     "python-dotenv", >> build\pyapp.json
echo     "pyperclip" >> build\pyapp.json
echo   ], >> build\pyapp.json
echo   "exclude_packages": [ >> build\pyapp.json
echo     "tensorflow", >> build\pyapp.json
echo     "torch", >> build\pyapp.json
echo     "matplotlib", >> build\pyapp.json
echo     "pandas" >> build\pyapp.json
echo   ] >> build\pyapp.json
echo } >> build\pyapp.json

:: Copy resources
echo Copying resources...
xcopy resources build\resources\ /E /I /Y

:: Copy Python files
echo Copying Python files...
copy main.py build\

:: Build the application
echo Building with PyApp...
pyapp.exe build

:: Check if build was successful
if not exist "dist\Khmer TTS.exe" (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build complete!
echo.
echo The executable is available at: dist\Khmer TTS.exe
echo.
echo Would you like to test the application now? (Y/N)
set /p TEST_APP=

if /i "%TEST_APP%" EQU "Y" (
    echo.
    echo Running application...
    cd "dist"
    "Khmer TTS.exe"
    cd ..\
)

echo.
echo Done!
echo.
echo Press any key to exit...
pause >nul
