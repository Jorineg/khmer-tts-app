@echo off
echo Building Khmer TTS with System Python
echo ==================================

:: This script attempts to build the app using the system Python
:: instead of a Conda environment, which often resolves DLL issues

echo Checking for system Python...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo System Python not found!
    echo Please install Python from python.org
    pause
    exit /b 1
)

:: Create a virtual environment
echo Creating a virtual environment...
python -m venv build_env

:: Activate the environment
echo Activating virtual environment...
call build_env\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller==6.1.0 pillow

:: Create resources dir if it doesn't exist
if not exist resources mkdir resources

:: Create icon
echo Creating application icon...
python create_icon.py

:: Build with PyInstaller
echo Building with PyInstaller using system Python...
echo This may take a few minutes...

pyinstaller --clean ^
  --name="Khmer TTS" ^
  --icon=resources\icon.ico ^
  --add-data="resources;resources" ^
  --noconsole ^
  main.py

:: Deactivate the virtual environment
echo Deactivating virtual environment...
call build_env\Scripts\deactivate.bat

:: Check if build was successful
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build successful!
echo.
echo The executable is available at: dist\Khmer TTS\Khmer TTS.exe
echo.
echo Press any key to exit...
pause >nul
