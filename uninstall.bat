@echo off
setlocal enabledelayedexpansion

echo Khmer STT Uninstaller
echo =====================
echo.

:: Set variables
set "APP_NAME=KhmerSTT"
set "INSTALL_DIR=%PROGRAMFILES%\%APP_NAME%"
set "APPDATA_DIR=%APPDATA%\%APP_NAME%"
set "START_MENU_SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP_NAME%.lnk"

:: Check for administrator privileges and self-elevate if needed
echo Checking administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This uninstaller requires administrator privileges.
    echo Requesting elevation...
    
    :: Create a temporary VBS script to elevate privileges
    set "ELEVATE_VBS=%TEMP%\elevate_khmerstt_uninstall.vbs"
    echo Set UAC = CreateObject^("Shell.Application"^) > "%ELEVATE_VBS%"
    echo UAC.ShellExecute "%~f0", "", "", "runas", 1 >> "%ELEVATE_VBS%"
    
    :: Run the VBS script and exit current instance
    wscript.exe "%ELEVATE_VBS%"
    del "%ELEVATE_VBS%"
    exit /b
)

echo Running with administrator privileges.
echo.

:: Confirm uninstallation
echo This will uninstall Khmer STT from your computer.
echo All settings and API keys will be removed.
echo.
set /p CONFIRM="Are you sure you want to continue? (Y/N): "
if /i "%CONFIRM%" neq "Y" (
    echo Uninstallation cancelled.
    pause
    exit /b
)
echo.

:: Stop any running instances of the application
echo Stopping any running instances of Khmer STT...
taskkill /f /im "Khmer STT.exe" >nul 2>&1
timeout /t 2 /nobreak >nul
echo.

:: Remove Windows Credentials (API keys)
echo Removing API keys from Windows Credentials Manager...
:: Using cmdkey to list and delete credentials
for /f "tokens=1" %%a in ('cmdkey /list ^| findstr "KhmerSTTApp"') do (
    set "target=%%a"
    echo Removing credential: !target!
    cmdkey /delete:!target! >nul 2>&1
)
echo API keys removed.
echo.

:: Remove autostart registry entry
echo Removing autostart registry entry...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /f >nul 2>&1
echo Autostart entry removed.
echo.

:: Remove application settings from registry
echo Removing registry settings...
reg delete "HKCU\Software\%APP_NAME%" /f >nul 2>&1
echo Registry settings removed.
echo.

:: Remove AppData directory
echo Removing application data...
if exist "%APPDATA_DIR%" (
    rd /s /q "%APPDATA_DIR%" >nul 2>&1
    echo AppData directory removed.
) else (
    echo No AppData directory found.
)
echo.

:: Remove Start Menu shortcut
echo Removing Start Menu shortcut...
if exist "%START_MENU_SHORTCUT%" (
    del "%START_MENU_SHORTCUT%" >nul 2>&1
    echo Start Menu shortcut removed.
) else (
    echo No Start Menu shortcut found.
)
echo.

:: Remove installation directory (last step)
echo Removing application files...
if exist "%INSTALL_DIR%" (
    :: Create a batch file to delete the installation directory after this script exits
    set "CLEANUP_BAT=%TEMP%\cleanup_khmerstt.bat"
    
    echo @echo off > "%CLEANUP_BAT%"
    echo :check >> "%CLEANUP_BAT%"
    echo timeout /t 1 /nobreak >nul >> "%CLEANUP_BAT%"
    echo if exist "%INSTALL_DIR%" ( >> "%CLEANUP_BAT%"
    echo   rd /s /q "%INSTALL_DIR%" >> "%CLEANUP_BAT%"
    echo   if exist "%INSTALL_DIR%" goto check >> "%CLEANUP_BAT%"
    echo ) >> "%CLEANUP_BAT%"
    echo echo Khmer STT has been completely uninstalled. >> "%CLEANUP_BAT%"
    echo echo Thank you for using Khmer STT! >> "%CLEANUP_BAT%"
    echo echo. >> "%CLEANUP_BAT%"
    echo pause >> "%CLEANUP_BAT%"
    echo del "%CLEANUP_BAT%" >> "%CLEANUP_BAT%"
    
    :: Start the cleanup batch file in a new window
    start "" "%CLEANUP_BAT%"
    
    echo Application files will be removed after this window closes.
) else (
    echo No installation directory found.
    echo.
    echo Khmer STT has been completely uninstalled.
    echo Thank you for using Khmer STT!
    echo.
    pause
)

:: Exit
echo.
echo Uninstallation process completed. This window will close automatically.
timeout /t 3 >nul
exit
