@echo off
echo Building Khmer TTS - Simple Version
echo ================================

:: Create resources dir if it doesn't exist
if not exist resources mkdir resources

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Find libffi DLL in system directories
echo Checking for system DLLs...
set FOUND_LIBFFI=0
for %%G in (C:\Windows\System32\libffi*.dll) do (
    echo Found: %%G
    set FOUND_LIBFFI=1
)

if %FOUND_LIBFFI%==0 (
    echo No libffi DLL found in System32.
    echo Checking SysWOW64...
    for %%G in (C:\Windows\SysWOW64\libffi*.dll) do (
        echo Found: %%G
        set FOUND_LIBFFI=1
    )
)

if %FOUND_LIBFFI%==0 (
    echo WARNING: No libffi DLL found. The app may not run correctly.
    echo Consider installing the libffi DLL to your Windows system.
)

:: Build with PyInstaller
echo Building with basic PyInstaller command...
echo This may take a few minutes...

pyinstaller --clean ^
  --name="Khmer TTS" ^
  --icon=resources\icon.ico ^
  --add-data="resources;resources" ^
  --add-binary="C:\Windows\SysWOW64\libffi*.dll;." ^
  --hidden-import=keyring.backends.Windows ^
  --hidden-import=pynput.keyboard._win32 ^
  --hidden-import=pynput.mouse._win32 ^
  --hidden-import=google.generativeai ^
  --hidden-import=elevenlabs ^
  --collect-all=pynput ^
  --collect-all=wave ^
  --collect-all=elevenlabs ^
  --collect-all=pyaudio ^
  --collect-all=pyperclip ^
  --collect-all=google.generativeai ^
  --collect-all=dotenv ^
  --console ^
  main.py

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
