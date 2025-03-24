# Khmer TTS Installer Guide

This document explains how to build and distribute the Khmer TTS application for Windows 11.

## Prerequisites

To build the installer, you need:

1. Python and all required dependencies (listed in requirements.txt)
2. Pillow library: `pip install pillow`
3. Inno Setup (download from https://jrsoftware.org/isdl.php)
   - Make sure to add Inno Setup to your PATH during installation

## Building the Installer

1. Run the build script:
   ```
   build_installer.bat
   ```

2. If successful, this will create `KhmerTTSSetup.exe` in the main directory.

3. Distribute this installer to users - it contains everything they need to run the application, including Python.

## What the Installer Does

The installer:

1. Bundles Python and all required dependencies with the application
2. Creates start menu and optional desktop shortcuts
3. Optionally adds the application to Windows autostart
4. Registers the application in Windows search
5. Provides a clean uninstaller

## Customizing the Installer

- Edit `installer.iss` to customize the installer settings
- Edit `khmer_tts.spec` to customize how PyInstaller packages the application
- Edit `create_icon.py` to change the application icon

## Troubleshooting

### Common Issues

1. **PyInstaller errors**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Try cleaning the build: `pyinstaller --clean khmer_tts.spec`

2. **Inno Setup not found**:
   - Ensure Inno Setup is installed and in your PATH
   - Alternatively, open `installer.iss` directly with the Inno Setup Compiler

3. **Application crashes after installation**:
   - Look for missing dependencies in the `app.log` file in the installation directory
   - Check that all required files were included in the distribution

## Technical Notes

- The application is packaged using PyInstaller with the `--noconsole` option
- Windows registry entries are created to register the app with Windows Search
- The installer automatically detects the best installation directory
- The application's user data and settings are stored in the user's profile directory

If you encounter any issues not covered here, please refer to the PyInstaller and Inno Setup documentation.
