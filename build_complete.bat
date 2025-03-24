@echo off
echo Advanced Khmer TTS Builder
echo ========================

:: Create icon if needed
echo Creating application icon...
python create_icon.py

:: Run the comprehensive build script
echo Running comprehensive build script...
python build_from_scratch.py

echo.
echo Build process completed!
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
