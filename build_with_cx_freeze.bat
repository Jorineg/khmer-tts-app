@echo off
echo Building Khmer TTS with cx_Freeze
echo ===============================

:: Install cx_Freeze if not already installed
echo Installing cx_Freeze...
pip install cx_Freeze

:: Create icon if needed
echo Creating application icon...
python create_icon.py

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Build with cx_Freeze
echo Building with cx_Freeze...
python setup.py build

:: Check if build was successful
if not exist "build\exe.win-amd64-3.11\Khmer TTS.exe" (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build successful!
echo.
echo The executable is available at: build\exe.win-amd64-3.11\Khmer TTS.exe
echo.
echo Would you like to test the executable now? (Y/N)
set /p TEST_EXE=

if /i "%TEST_EXE%" EQU "Y" (
    echo Running test...
    cd "build\exe.win-amd64-3.11"
    "Khmer TTS.exe"
    cd ..\..\
)

echo.
echo Done!
echo.
echo Press any key to exit...
pause >nul
