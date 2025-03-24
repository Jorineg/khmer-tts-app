# NSIS Script for Khmer TTS Installer

!include "MUI2.nsh"
!include "LogicLib.nsh"

# General settings
Name "Khmer TTS"
OutFile "KhmerTTSSetup.exe"
Unicode True
InstallDir "$PROGRAMFILES\Khmer TTS"
InstallDirRegKey HKCU "Software\Khmer TTS" ""
RequestExecutionLevel admin

# Interface settings
!define MUI_ICON "resources\icon.ico"
!define MUI_UNICON "resources\icon.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"
!define MUI_ABORTWARNING

# Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES

# Finish page with option to launch app
!define MUI_FINISHPAGE_RUN "$INSTDIR\Khmer TTS.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Khmer TTS now"
!insertmacro MUI_PAGE_FINISH

# Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Language
!insertmacro MUI_LANGUAGE "English"

# Installer sections
Section "Khmer TTS" SecMain
  SectionIn RO
  
  # Set output directory
  SetOutPath "$INSTDIR"
  
  # Include all files from the dist\Khmer TTS directory
  File /r "dist\Khmer TTS\*.*"
  
  # Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  # Create shortcuts
  CreateDirectory "$SMPROGRAMS\Khmer TTS"
  CreateShortcut "$SMPROGRAMS\Khmer TTS\Khmer TTS.lnk" "$INSTDIR\Khmer TTS.exe"
  CreateShortcut "$SMPROGRAMS\Khmer TTS\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  
  # Write registry
  WriteRegStr HKCU "Software\Khmer TTS" "" $INSTDIR
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\App Paths\Khmer TTS.exe" "" "$INSTDIR\Khmer TTS.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Khmer TTS" "DisplayName" "Khmer TTS"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Khmer TTS" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Khmer TTS" "DisplayIcon" "$INSTDIR\Khmer TTS.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Khmer TTS" "DisplayVersion" "1.0.0"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Khmer TTS" "Publisher" "Khmer TTS"
SectionEnd

Section "Desktop Shortcut" SecDesktop
  CreateShortcut "$DESKTOP\Khmer TTS.lnk" "$INSTDIR\Khmer TTS.exe"
SectionEnd

Section "Start with Windows" SecStartup
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Khmer TTS" '"$INSTDIR\Khmer TTS.exe"'
SectionEnd

# Descriptions
LangString DESC_SecMain ${LANG_ENGLISH} "The main application files."
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create a shortcut on the desktop."
LangString DESC_SecStartup ${LANG_ENGLISH} "Start Khmer TTS automatically when Windows starts."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartup} $(DESC_SecStartup)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

# Uninstaller section
Section "Uninstall"
  # Remove registry keys
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Khmer TTS"
  DeleteRegKey HKCU "Software\Khmer TTS"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\App Paths\Khmer TTS.exe"
  DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Khmer TTS"
  
  # Remove shortcuts
  Delete "$SMPROGRAMS\Khmer TTS\*.*"
  RMDir "$SMPROGRAMS\Khmer TTS"
  Delete "$DESKTOP\Khmer TTS.lnk"
  
  # Remove files and folders
  RMDir /r "$INSTDIR"
SectionEnd
