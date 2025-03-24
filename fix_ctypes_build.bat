@echo off
echo Fixing _ctypes Issue and Building Khmer TTS
echo ======================================

:: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

:: Create a directory to store DLLs
if not exist dlls mkdir dlls

:: Download libffi DLL from the web
echo Downloading libffi DLL...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/liberodark/libffi-dll/raw/master/win64/libffi-6.dll' -OutFile 'dlls\libffi-6.dll'}"
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/liberodark/libffi-dll/raw/master/win64/libffi-7.dll' -OutFile 'dlls\libffi-7.dll'}"

:: Create hook file for _ctypes
echo Creating _ctypes hook file...
echo import os > hook-_ctypes.py
echo from PyInstaller.utils.hooks import collect_dynamic_libs >> hook-_ctypes.py
echo. >> hook-_ctypes.py
echo # Collect DLLs >> hook-_ctypes.py
echo binaries = collect_dynamic_libs('_ctypes') >> hook-_ctypes.py
echo. >> hook-_ctypes.py
echo # Add our downloaded DLLs >> hook-_ctypes.py
echo dll_dir = os.path.join(os.path.abspath('.'), 'dlls') >> hook-_ctypes.py
echo for file in os.listdir(dll_dir): >> hook-_ctypes.py
echo     if file.lower().endswith('.dll'): >> hook-_ctypes.py
echo         binaries.append((os.path.join(dll_dir, file), '.')) >> hook-_ctypes.py
echo. >> hook-_ctypes.py
echo hiddenimports = ['_ctypes'] >> hook-_ctypes.py

:: Create a dummy DLL if download fails
if not exist dlls\libffi-6.dll if not exist dlls\libffi-7.dll (
    echo Fallback: Creating dummy file for libffi DLL...
    copy NUL dlls\libffi-6.dll
)

:: Build with PyInstaller
echo Building with PyInstaller...
pyinstaller --clean ^
  --icon=resources\icon.ico ^
  --add-data="resources;resources" ^
  --add-binary="dlls\*.dll;." ^
  --hidden-import=keyring.backends.Windows ^
  --hidden-import=pynput.keyboard._win32 ^
  --hidden-import=pynput.mouse._win32 ^
  --hidden-import=google.generativeai ^
  --hidden-import=elevenlabs ^
  --hidden-import=_ctypes ^
  --additional-hooks-dir=. ^
  --collect-all=pynput ^
  --collect-all=elevenlabs ^
  --collect-all=pyaudio ^
  --collect-all=keyring ^
  --collect-all=google.generativeai ^
  --console ^
  --name="Khmer TTS" main.py

:: Check if build was successful
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo Build failed!
    pause
    exit /b 1
)

:: Copy our DLLs to the dist directory
echo Copying DLLs to distribution folder...
copy dlls\*.dll "dist\Khmer TTS\"

:: Copy libffi DLL from our manually downloaded files
if exist dlls\libffi-6.dll copy dlls\libffi-6.dll "dist\Khmer TTS\"
if exist dlls\libffi-7.dll copy dlls\libffi-7.dll "dist\Khmer TTS\"
if exist C:\Windows\System32\libffi*.dll copy C:\Windows\System32\libffi*.dll "dist\Khmer TTS\"

:: Create a test script
echo Creating test script...
echo @echo off > "dist\Khmer TTS\test.bat"
echo echo Testing Khmer TTS... >> "dist\Khmer TTS\test.bat"
echo "Khmer TTS.exe" >> "dist\Khmer TTS\test.bat"
echo pause >> "dist\Khmer TTS\test.bat"

echo.
echo Build complete!
echo.
echo The executable is available at: dist\Khmer TTS\Khmer TTS.exe
echo A test script is available at: dist\Khmer TTS\test.bat
echo.
echo Would you like to test the application now? (Y/N)
set /p TEST_APP=

if /i "%TEST_APP%" EQU "Y" (
    echo.
    echo Running test.bat...
    cd "dist\Khmer TTS"
    call test.bat
    cd ..\..\
)

echo.
echo Done!
echo.
echo Press any key to exit...
pause >nul
