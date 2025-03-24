@echo off
echo Building Khmer TTS Application Installer
echo =======================================

:: Create icon
echo Creating application icon...
python create_icon.py

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Create a lighter version for debugging
echo Building application with PyInstaller (with console for debugging)...
echo This may take a few minutes...
pyinstaller --clean --noconfirm khmer_tts.spec

:: Check if build was successful
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo PyInstaller build successful!
echo.
echo Do you want to proceed with building the installer? (Y/N)
set /p BUILD_INSTALLER=

if /i "%BUILD_INSTALLER%" NEQ "Y" (
    echo Installer build skipped.
    echo You can find the built application in the dist\Khmer TTS directory.
    pause
    exit /b 0
)

:: Build the installer with Inno Setup
echo Building installer with Inno Setup...
:: Try common Inno Setup installation paths
set ISCC_CMD=iscc
where %ISCC_CMD% >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    set ISCC_CMD="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if not exist %ISCC_CMD% (
        set ISCC_CMD="C:\Program Files\Inno Setup 6\ISCC.exe"
        if not exist %ISCC_CMD% (
            echo Inno Setup not found in PATH or common installation locations.
            echo Please install Inno Setup from https://jrsoftware.org/isdl.php
            echo After installation, either:
            echo 1. Make sure the Inno Setup directory is in your PATH, or
            echo 2. Manually build the installer by opening installer.iss with Inno Setup Compiler.
            echo.
            echo Press any key to open the download page for Inno Setup...
            pause >nul
            start https://jrsoftware.org/isdl.php
            exit /b 1
        )
    )
)

:: Build the installer
echo Using Inno Setup: %ISCC_CMD%
%ISCC_CMD% installer.iss

:: Check if installer was created
if not exist "Output\KhmerTTSSetup.exe" (
    echo Installer build failed!
    pause
    exit /b 1
)

:: Move installer to the main directory
echo Moving installer to main directory...
if not exist Output mkdir Output
move Output\KhmerTTSSetup.exe KhmerTTSSetup.exe 2>nul

echo Done! Installer created: KhmerTTSSetup.exe
echo.
echo NOTE: To customize the installer, edit installer.iss
echo.
echo Press any key to exit...
pause >nul
