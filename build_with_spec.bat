@echo off
echo Building Khmer TTS with Custom Spec File
echo ====================================

:: Create icon if needed
echo Creating application icon...
python create_icon.py

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Check for VC redist needed DLLs
echo Checking for VC redistributable components...
if exist "C:\Windows\System32\vcruntime140.dll" (
    echo Found vcruntime140.dll
) else (
    echo WARNING: vcruntime140.dll not found, download and install latest VC redistribution package
    echo from https://aka.ms/vs/17/release/vc_redist.x64.exe
    echo.
    echo Install Visual C++ redistributable? (Y/N)
    set /p INSTALL_VC=
    if /i "%INSTALL_VC%" EQU "Y" (
        echo Downloading VC redistributable...
        powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.x64.exe'"
        echo Installing VC redistributable...
        vc_redist.x64.exe /quiet
    )
)

:: Build the executable
echo Building with custom spec file...
pyinstaller --clean khmer_tts.spec

:: Check if build was successful
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo Build failed!
    pause
    exit /b 1
)

:: Run the DLL fix script
echo Running DLL fix script...
call fix_dlls.bat

echo.
echo Build complete!
echo.
echo The executable is available at: dist\Khmer TTS\Khmer TTS.exe
echo.
echo Press any key to exit...
pause >nul
