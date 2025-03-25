"""
Uninstallation module for Khmer STT application

This module contains functions to uninstall the application:
- Delete application folder in Program Files
- Remove Windows start menu entry
- Remove registry settings
- Remove API keys from Windows Credentials Manager
- Remove autostart registry entry
- Clean up AppData directory
"""

import os
import sys
import shutil
import logging
import winreg
import ctypes
import subprocess
from pathlib import Path
import keyring

logger = logging.getLogger(__name__)

APP_NAME = "KhmerSTT"
INSTALL_DIR = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), APP_NAME)
API_KEY_SERVICE = "KhmerSTTApp"


def is_admin():
    """Check if the current process has administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False


def remove_api_keys():
    """Remove API keys from Windows Credentials Manager"""
    try:
        # Remove all known service API keys
        keyring.delete_password(API_KEY_SERVICE, "google")
        logger.info("Removed Google API key")
    except keyring.errors.PasswordDeleteError:
        # Key doesn't exist, ignore
        pass
    except Exception as e:
        logger.error(f"Error removing Google API key: {e}")

    try:
        keyring.delete_password(API_KEY_SERVICE, "elevenlabs")
        logger.info("Removed ElevenLabs API key")
    except keyring.errors.PasswordDeleteError:
        # Key doesn't exist, ignore
        pass
    except Exception as e:
        logger.error(f"Error removing ElevenLabs API key: {e}")


def remove_registry_settings():
    """Remove registry settings"""
    try:
        # Remove autostart entry
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )
            winreg.DeleteValue(key, APP_NAME)
            winreg.CloseKey(key)
            logger.info("Removed autostart registry entry")
        except FileNotFoundError:
            # Entry doesn't exist, ignore
            pass
        except Exception as e:
            logger.error(f"Error removing autostart registry entry: {e}")

        # Remove application settings
        try:
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\KhmerSTT"
            )
            logger.info("Removed application registry settings")
        except FileNotFoundError:
            # Key doesn't exist, ignore
            pass
        except Exception as e:
            logger.error(f"Error removing application registry settings: {e}")

        return True
    except Exception as e:
        logger.error(f"Error removing registry settings: {e}")
        return False


def remove_appdata_directory():
    """Remove AppData directory"""
    try:
        app_data_dir = os.path.join(os.environ.get('APPDATA', '.'), APP_NAME)
        if os.path.exists(app_data_dir):
            shutil.rmtree(app_data_dir, ignore_errors=True)
            logger.info(f"Removed AppData directory: {app_data_dir}")
        return True
    except Exception as e:
        logger.error(f"Error removing AppData directory: {e}")
        return False


def remove_start_menu_shortcut():
    """Remove start menu shortcut"""
    try:
        start_menu_dir = os.path.join(
            os.environ.get('APPDATA', ''),
            r"Microsoft\Windows\Start Menu\Programs"
        )
        
        shortcut_path = os.path.join(start_menu_dir, f"{APP_NAME}.lnk")
        
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            logger.info(f"Removed Start Menu shortcut: {shortcut_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error removing Start Menu shortcut: {e}")
        return False


def uninstall_application():
    """
    Perform the uninstallation process
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting uninstallation process")
    
    # First remove API keys
    remove_api_keys()
    
    # Remove registry settings
    remove_registry_settings()
    
    # Remove AppData directory
    remove_appdata_directory()
    
    # Remove Start Menu shortcut
    remove_start_menu_shortcut()
    
    # Finally, remove installation directory
    # This should be done last as it might contain the running executable
    try:
        if os.path.exists(INSTALL_DIR):
            # Create a batch file to delete the directory after the process exits
            temp_dir = os.environ.get('TEMP')
            batch_path = os.path.join(temp_dir, f"uninstall_{APP_NAME}.bat")
            
            with open(batch_path, 'w') as f:
                f.write('@echo off\n')
                f.write('echo Removing application files...\n')
                f.write(f'timeout /t 2 /nobreak >nul\n')
                f.write(f'rmdir /s /q "{INSTALL_DIR}"\n')
                f.write(f'del "%~f0"\n')
            
            # Execute the batch file
            subprocess.Popen(['cmd', '/c', batch_path], 
                            creationflags=subprocess.CREATE_NEW_CONSOLE | 
                                        subprocess.DETACHED_PROCESS)
            
            logger.info(f"Created cleanup batch file to remove installation directory: {INSTALL_DIR}")
        
        return True
    except Exception as e:
        logger.error(f"Error during uninstallation: {e}")
        return False


def create_uninstaller_script():
    """Create uninstaller batch script in installation directory"""
    try:
        # Create uninstall.bat in installation directory
        uninstall_path = os.path.join(INSTALL_DIR, "uninstall.bat")
        
        with open(uninstall_path, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Uninstalling Khmer Speech-to-Text...\n\n')
            
            # Check for administrator privileges
            f.write('net session >nul 2>&1\n')
            f.write('if %errorlevel% neq 0 (\n')
            f.write('    echo This uninstaller requires administrator privileges.\n')
            f.write('    echo Please right-click on this batch file and select "Run as administrator".\n')
            f.write('    pause\n')
            f.write('    exit /b 1\n')
            f.write(')\n\n')
            
            # Get the Python executable path
            exe_path = os.path.join(INSTALL_DIR, os.path.basename(sys.executable))
            
            # Run Python code to handle uninstallation
            f.write(f'"{exe_path}" -c "import sys; sys.path.append(\'{INSTALL_DIR}\'); from app.system.uninstaller import uninstall_application; uninstall_application()"\n\n')
            
            f.write('echo.\n')
            f.write('echo Uninstallation completed!\n')
            f.write('echo.\n')
            f.write('pause\n')
        
        logger.info(f"Created uninstaller script: {uninstall_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating uninstaller script: {e}")
        return False
