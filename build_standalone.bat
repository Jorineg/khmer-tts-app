@echo off
echo Building Khmer TTS Standalone Executable
echo =======================================

:: Create icon
echo Creating application icon...
python create_icon.py

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Create a simple test to find dependency info
echo Creating DLL checker test...
echo import ctypes > dll_check.py
echo import os >> dll_check.py
echo print("_ctypes found at:", ctypes) >> dll_check.py
echo print("DLL search paths:") >> dll_check.py
echo for path in os.environ["PATH"].split(os.pathsep): >> dll_check.py
echo     if os.path.exists(path): >> dll_check.py
echo         print("  ", path) >> dll_check.py
echo         for file in os.listdir(path): >> dll_check.py
echo             if file.lower().startswith("libffi"): >> dll_check.py
echo                 print("    Found:", os.path.join(path, file)) >> dll_check.py

echo Running DLL check...
python dll_check.py

:: Build a standard directory structure first 
echo Building directory-based executable with PyInstaller...
echo This may take a few minutes...

pyinstaller --clean ^
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
  --additional-hooks-dir=. ^
  --copy-metadata=pyaudio ^
  --copy-metadata=elevenlabs ^
  --copy-metadata=google.generativeai ^
  --copy-metadata=pynput ^
  --copy-metadata=wave ^
  --copy-metadata=pyperclip ^
  --paths="C:\Windows\System32;C:\Windows\SysWOW64;C:\ProgramData\miniconda3\envs\khmertts\Lib\site-packages" ^
  --paths="C:\ProgramData\miniconda3\Lib\site-packages" ^
  --paths="C:\Program Files\miniconda3\Lib\site-packages" ^
  --hidden-import=_ctypes ^
  --hidden-import=win32timezone ^
  --console ^
  --name="Khmer TTS" main.py

:: Check if build was successful
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo PyInstaller build failed!
    pause
    exit /b 1
)

:: Find any system DLLs we might need and copy them manually
echo Looking for system DLLs to copy...
set SYSTEM32_DIR=C:\Windows\System32
set DIST_DIR=dist\Khmer TTS

:: List of common DLLs that might be needed
set DLL_LIST=libffi-7.dll libffi-8.dll libffi-6.dll libffi.dll

for %%d in (%DLL_LIST%) do (
    if exist "%SYSTEM32_DIR%\%%d" (
        echo Copying %%d from System32...
        copy "%SYSTEM32_DIR%\%%d" "%DIST_DIR%\" /Y
    )
)

:: Try to test it by running the executable
echo.
echo Build is complete! 
echo.
echo Would you like to test the executable now? (Y/N)
set /p TEST_EXE=

if /i "%TEST_EXE%" EQU "Y" (
    echo Running test...
    cd "%DIST_DIR%"
    "..\Khmer TTS.exe"
    cd ..\..\
)

echo.
echo PyInstaller build completed.
echo The executable is available at: %DIST_DIR%\Khmer TTS.exe
echo.
echo Press any key to exit...
pause >nul
