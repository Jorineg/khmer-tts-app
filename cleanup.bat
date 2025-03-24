@echo off
echo Cleaning up build artifacts for Khmer TTS application...

:: Remove build folders
if exist build (
    echo Removing build folder...
    rmdir /s /q build
)

if exist dist (
    echo Removing dist folder...
    rmdir /s /q dist
)

if exist __pycache__ (
    echo Removing __pycache__ folder...
    rmdir /s /q __pycache__
)

:: Remove PyInstaller artifacts
if exist "Khmer TTS.spec" (
    echo Removing PyInstaller spec file...
    del "Khmer TTS.spec"
)

:: Remove app-level __pycache__ folders
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Removing %%d...
    rmdir /s /q "%%d"
)

:: Remove Output folder from Inno Setup
if exist Output (
    echo Removing Inno Setup output folder...
    rmdir /s /q Output
)

echo.
echo Cleanup complete!
echo.
echo Press any key to exit...
pause >nul
