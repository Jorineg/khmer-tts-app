@echo off
echo Installing Auto-Py-To-Exe
echo =======================

:: Install auto-py-to-exe
echo Installing auto-py-to-exe...
pip install auto-py-to-exe

echo.
echo Installation complete!
echo.
echo Auto-Py-To-Exe provides a simple graphical interface for creating Windows executables.
echo.
echo Starting Auto-Py-To-Exe...
auto-py-to-exe

echo.
echo When the GUI opens:
echo 1. Set "Script Location" to "main.py"
echo 2. Select "One Directory" or "One File" (One File is recommended for simpler deployment)
echo 3. Check "Window Based" to hide the console window
echo 4. Under "Additional Files" add your "resources" folder
echo 5. Under "Advanced" add these hidden imports:
echo    - keyring.backends.Windows
echo    - pynput.keyboard._win32
echo    - pynput.mouse._win32
echo    - google.generativeai
echo    - elevenlabs
echo 6. Click "Convert .py to .exe"
echo.
echo After the build completes, you'll find your .exe in the "output" folder
echo.
pause
