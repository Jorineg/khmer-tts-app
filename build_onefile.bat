@echo off
echo Building Khmer TTS Single-File Executable
echo =======================================

:: Create icon
echo Creating application icon...
python create_icon.py

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Locate the libffi.dll in the system
echo Checking for required system DLLs...
set LIBFFI_PATH=
for %%G in (C:\Windows\System32\libffi*.dll) do (
    set LIBFFI_PATH=%%G
    echo Found: %%G
)

:: Create a lighter version for debugging
echo Building single-file executable with PyInstaller...
echo This may take a few minutes...

:: Build a one-file executable with more debug info and binaries
pyinstaller --clean --onefile ^
  --icon=resources\icon.ico ^
  --exclude=tensorflow ^
  --exclude=torch ^
  --exclude=pandas ^
  --exclude=matplotlib ^
  --exclude=notebook ^
  --exclude=jupyter ^
  --exclude=IPython ^
  --exclude=tk ^
  --exclude=tcl ^
  --exclude=PyQt6 ^
  --exclude=PySide ^
  --exclude=pytest ^
  --add-binary="C:\ProgramData\miniconda3\Library\bin\libffi-8.dll;." ^
  --console ^
  --name="Khmer TTS" main.py

:: Check if build was successful
if not exist "dist\Khmer TTS.exe" (
    echo PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo PyInstaller build successful!
echo.
echo One-file executable created at: dist\Khmer TTS.exe
echo.
echo Press any key to exit...
pause >nul
