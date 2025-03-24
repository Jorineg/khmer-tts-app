@echo off
echo Khmer TTS - Inno Setup Installer
echo ==============================
echo.
echo This script will download and install Inno Setup for creating the Windows installer.
echo.

:: Check if Inno Setup is already installed
set ISCC_CMD=iscc
where %ISCC_CMD% >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Inno Setup is already installed and available in PATH.
    echo You can now run build_installer.bat to create the installer.
    goto :end
)

set ISCC_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist %ISCC_PATH% (
    echo Inno Setup is already installed at %ISCC_PATH%.
    echo You can now run build_installer.bat to create the installer.
    goto :end
)

set ISCC_PATH="C:\Program Files\Inno Setup 6\ISCC.exe"
if exist %ISCC_PATH% (
    echo Inno Setup is already installed at %ISCC_PATH%.
    echo You can now run build_installer.bat to create the installer.
    goto :end
)

echo Inno Setup is not installed or not found.
echo.
echo Would you like to download and install Inno Setup now? (Y/N)
set /p CONFIRM=

if /i "%CONFIRM%" NEQ "Y" (
    echo Installation canceled.
    goto :end
)

:: Create a temporary directory for the download
set TEMP_DIR=%TEMP%\innosetup_download
mkdir %TEMP_DIR% 2>nul

:: Download Inno Setup using PowerShell
echo Downloading Inno Setup installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://jrsoftware.org/download.php/is.exe' -OutFile '%TEMP_DIR%\innosetup.exe'}"

if not exist "%TEMP_DIR%\innosetup.exe" (
    echo Failed to download Inno Setup.
    echo Please download and install Inno Setup manually from https://jrsoftware.org/isdl.php
    start https://jrsoftware.org/isdl.php
    goto :end
)

:: Run the installer
echo Installing Inno Setup...
echo Please follow the installation instructions in the Inno Setup installer window.
echo.
echo IMPORTANT: Make sure to select the option to add Inno Setup to PATH during installation!
echo.
start /wait %TEMP_DIR%\innosetup.exe

:: Clean up
rmdir /s /q %TEMP_DIR% 2>nul

echo.
echo Inno Setup installation completed.
echo You can now run build_installer.bat to create the installer.

:end
echo.
echo Press any key to exit...
pause >nul
