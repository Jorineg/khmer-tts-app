@echo off
echo Simple Windows 11 Build Script for Khmer TTS
echo =========================================

:: Clean previous build
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Create icon if needed
echo Creating application icon if needed...
if not exist resources\icon.ico python create_icon.py

:: Set up PyInstaller command
set PYINSTALLER_CMD=pyinstaller --clean --noconfirm

:: Set up PyInstaller options
:: --window: Create a windowed app (no console)
:: --add-data: Include the resources folder
:: --hidden-import: Include these imports explicitly
set PYINSTALLER_OPTS=--windowed --icon=resources\icon.ico --add-data="resources;resources" ^
--collect-all=pynput --collect-all=elevenlabs --collect-all=keyring ^
--hidden-import=keyring.backends.Windows ^
--hidden-import=pynput.keyboard._win32 ^
--hidden-import=pynput.mouse._win32 ^
--hidden-import=google.generativeai ^
--hidden-import=elevenlabs

:: Create an onefile build (simplest installer)
echo Building one-file executable...
%PYINSTALLER_CMD% %PYINSTALLER_OPTS% --onefile --name="Khmer TTS" main.py

:: Create a test script
echo Creating test script...
echo @echo off > "dist\test_app.bat"
echo echo Testing Khmer TTS... >> "dist\test_app.bat"
echo "Khmer TTS.exe" >> "dist\test_app.bat"
echo pause >> "dist\test_app.bat"

echo.
echo Build complete!
echo.
echo The executable is available at: dist\Khmer TTS.exe
echo You can test it with: dist\test_app.bat
echo.
echo Would you like to test the application now? (Y/N)
set /p TEST_APP=

if /i "%TEST_APP%" EQU "Y" (
    echo.
    echo Running application...
    cd "dist"
    call test_app.bat
    cd ..
)

echo.
echo Done!
echo.
pause
