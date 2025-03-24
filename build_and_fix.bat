@echo off
echo Khmer TTS Builder and Fixer
echo =========================

:: Create icon if needed
echo Creating application icon...
python create_icon.py

:: STEP 1: Find dependencies and DLLs
echo.
echo STEP 1: Analyzing system for required DLLs...
python find_dlls.py

:: Clean previous builds
echo.
echo STEP 2: Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: STEP 2: Build the executable with the system Python approach
echo.
echo STEP 3: Building with standard PyInstaller approach...
echo This may take a few minutes...

pyinstaller --clean ^
  --icon=resources\icon.ico ^
  --add-data="resources;resources" ^
  --hidden-import=keyring.backends.Windows ^
  --hidden-import=pynput.keyboard._win32 ^
  --hidden-import=pynput.mouse._win32 ^
  --hidden-import=google.generativeai ^
  --hidden-import=elevenlabs ^
  --hidden-import=_ctypes ^
  --collect-all=pynput ^
  --collect-all=elevenlabs ^
  --collect-all=pyaudio ^
  --collect-all=keyring ^
  --collect-all=google.generativeai ^
  --collect-all=google.api_core ^
  --collect-binaries=_ctypes ^
  --console ^
  --name="Khmer TTS" main.py

:: Check if build was successful
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo Build failed!
    pause
    exit /b 1
)

:: STEP 3: Copy required DLLs to the dist directory
echo.
echo STEP 4: Copying required DLLs to distribution directory...
python copy_dlls_to_dist.py

:: STEP 4: Create a test batch file in the dist directory
echo.
echo STEP 5: Creating test launcher script...
set TEST_BAT=dist\Khmer TTS\test_run.bat
echo @echo off > %TEST_BAT%
echo echo Testing Khmer TTS executable >> %TEST_BAT%
echo echo ========================= >> %TEST_BAT%
echo echo. >> %TEST_BAT%
echo echo If you see Python errors about missing DLLs, please copy them >> %TEST_BAT%
echo echo from your Python installation to this directory. >> %TEST_BAT%
echo echo. >> %TEST_BAT%
echo "Khmer TTS.exe" >> %TEST_BAT%
echo echo. >> %TEST_BAT%
echo echo If there were errors, please report them. >> %TEST_BAT%
echo pause >> %TEST_BAT%

echo.
echo Build complete!
echo.
echo The executable is available at: dist\Khmer TTS\Khmer TTS.exe
echo A test launcher is available at: dist\Khmer TTS\test_run.bat
echo.
echo Would you like to test the application now? (Y/N)
set /p TEST_APP=

if /i "%TEST_APP%" EQU "Y" (
    echo.
    echo Running test_run.bat...
    cd "dist\Khmer TTS"
    call test_run.bat
    cd ..\..\
)

echo.
echo Done!
echo.
echo Press any key to exit...
pause >nul
