@echo off
echo DLL Fix Utility for Khmer TTS
echo ===========================

:: Check if executable exists
if not exist "dist\Khmer TTS\Khmer TTS.exe" (
    echo Error: Executable not found at dist\Khmer TTS\Khmer TTS.exe
    echo Please run the build_with_system_python.bat script first.
    pause
    exit /b 1
)

echo Found executable at dist\Khmer TTS\Khmer TTS.exe

:: Create a directory for DLLs if it doesn't exist
if not exist "dll_cache" mkdir dll_cache

:: List of DLLs to search for and copy
echo Searching for required DLLs...
set DLL_LIST=libffi-7.dll libffi-8.dll libffi-6.dll libffi.dll ffi.dll LIBBZ2.dll liblzma.dll libcrypto-3-x64.dll libssl-3-x64.dll

:: Search paths
set SEARCH_PATHS=C:\Windows\System32 C:\Windows\SysWOW64 C:\ProgramData\miniconda3\DLLs C:\ProgramData\miniconda3\Library\bin

:: Try to find DLLs from Anaconda/Miniconda locations
echo Searching in Miniconda locations...
for %%d in (%DLL_LIST%) do (
    for %%p in (%SEARCH_PATHS%) do (
        if exist "%%p\%%d" (
            echo Found %%d in %%p
            copy "%%p\%%d" "dll_cache\" /Y
            copy "%%p\%%d" "dist\Khmer TTS\" /Y
        )
    )
)

:: Try to find DLLs from Python installation
echo Searching in system Python locations...
for %%d in (%DLL_LIST%) do (
    for /f "tokens=*" %%i in ('where %%d 2^>nul') do (
        echo Found %%d at %%i
        copy "%%i" "dll_cache\" /Y
        copy "%%i" "dist\Khmer TTS\" /Y
    )
)

:: Search in the Python directory
echo Searching in Python directory...
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_DIR=%%~dpi
)

if defined PYTHON_DIR (
    echo Checking in %PYTHON_DIR% and subdirectories
    for %%d in (%DLL_LIST%) do (
        for /f "tokens=*" %%i in ('dir /b /s "%PYTHON_DIR%\%%d" 2^>nul') do (
            echo Found %%d at %%i
            copy "%%i" "dll_cache\" /Y 
            copy "%%i" "dist\Khmer TTS\" /Y
        )
    )
)

:: Check if libffi DLL was found
set FOUND_LIBFFI=0
for %%f in (dll_cache\libffi*.dll dll_cache\ffi.dll) do (
    if exist "%%f" set FOUND_LIBFFI=1
)

if %FOUND_LIBFFI%==0 (
    echo WARNING: No libffi DLL was found. Creating a dummy DLL.
    echo This is just for testing - we'll need to find the real DLL.
    echo If the app still doesn't work, we'll try another approach.
    
    :: Create a simple python script to generate a dummy DLL
    echo import ctypes > create_dummy_dll.py
    echo import os >> create_dummy_dll.py
    echo print("_ctypes path:", ctypes.__file__) >> create_dummy_dll.py
    echo print("Looking for dependencies...") >> create_dummy_dll.py
    echo os.system("dumpbin /dependents " + ctypes.__file__) >> create_dummy_dll.py
    
    python create_dummy_dll.py
)

echo.
echo DLL fix process completed.
echo The following DLLs were copied to dist\Khmer TTS:
dir "dist\Khmer TTS\*.dll"

echo.
echo Would you like to test the executable now? (Y/N)
set /p TEST_EXE=

if /i "%TEST_EXE%" EQU "Y" (
    echo Running test...
    cd "dist\Khmer TTS"
    "Khmer TTS.exe"
    cd ..\..\
)

echo.
echo Done!
echo.
echo Press any key to exit...
pause >nul
