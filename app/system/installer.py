"""
Installation module for Khmer STT application

This module handles first-run installation of the application:
- Creates application folder in Program Files
- Copies currently running executable there
- Creates Windows start menu entry
- Registers as a proper Windows application
"""

import os
import sys
import shutil
import logging
import winreg
import ctypes
from pathlib import Path
import subprocess
import atexit

logger = logging.getLogger(__name__)

APP_NAME = "KhmerSTT"
INSTALL_DIR = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), APP_NAME)

# Import uninstaller to create uninstall script
# from app.system.uninstaller import create_uninstaller_script

def is_admin():
    """Check if the current process has administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False


def is_installed():
    """
    Check if the application is already installed
    Looks for registry entry in Software\KhmerSTT to determine if app is installed
    """
    try:
        # Check if registry key exists
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\KhmerSTT",
            0, 
            winreg.KEY_READ
        )
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        # Registry key doesn't exist
        return False
    except Exception as e:
        logger.error(f"Error checking installation status: {e}")
        return False


def create_installation_marker():
    """Create registry entry to mark app as installed"""
    try:
        # Create or open the registry key
        key = winreg.CreateKeyEx(
            winreg.HKEY_CURRENT_USER,
            r"Software\KhmerSTT",
            0,
            winreg.KEY_WRITE
        )
        
        # Set installation flag
        winreg.SetValueEx(key, "Installed", 0, winreg.REG_SZ, "true")
        
        # Add current version information if available
        try:
            # Get executable path
            if hasattr(sys, '_MEIPASS'):  # PyInstaller environment
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Try to get version from a version file if it exists
            version_file = os.path.join(base_dir, "version.txt")
            if os.path.exists(version_file):
                with open(version_file, 'r') as f:
                    version = f.read().strip()
                winreg.SetValueEx(key, "Version", 0, winreg.REG_SZ, version)
        except Exception as e:
            logger.warning(f"Could not add version information: {e}")
        
        # Set install path
        winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, INSTALL_DIR)
        
        winreg.CloseKey(key)
        return True
    except Exception as e:
        logger.error(f"Error creating installation marker: {e}")
        return False


def create_desktop_ini():
    """Create desktop.ini file to customize folder appearance"""
    try:
        ini_path = os.path.join(INSTALL_DIR, "desktop.ini")
        exe_name = os.path.basename(sys.executable)
        
        with open(ini_path, 'w') as f:
            f.write("[.ShellClassInfo]\n")
            f.write("ConfirmFileOp=0\n")
            f.write("NoSharing=1\n")
            f.write(f"IconResource={exe_name},0\n")
            f.write("[ViewState]\n")
            f.write("Mode=\n")
            f.write("Vid=\n")
            f.write("FolderType=Generic\n")
        
        # Set file attributes
        subprocess.run(["attrib", "+s", "+h", ini_path], check=False)
        subprocess.run(["attrib", "+s", INSTALL_DIR], check=False)
        
        return True
    except Exception as e:
        logger.error(f"Error creating desktop.ini: {e}")
        return False


def create_start_menu_shortcut(target_path):
    """
    Create Start Menu shortcut to the application executable
    
    Args:
        target_path: Path to the target executable
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Creating Start Menu shortcut for: {target_path}")
        
        # Use PowerShell to create shortcut
        start_menu_dir = os.path.join(
            os.environ.get('APPDATA', ''),
            r"Microsoft\Windows\Start Menu\Programs"
        )
        
        shortcut_path = os.path.join(start_menu_dir, f"{APP_NAME}.lnk")
        
        # PowerShell command to create shortcut - using raw strings to avoid backslash issues
        ps_path = shortcut_path.replace('\\', '\\\\')
        target = target_path.replace('\\', '\\\\')
        
        ps_command = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{ps_path}')
        $Shortcut.TargetPath = '{target}'
        $Shortcut.Description = 'Khmer Speech-to-Text Application'
        $Shortcut.Save()
        """
        
        # Execute PowerShell command
        subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            check=False
        )
        
        return os.path.exists(shortcut_path)
    except Exception as e:
        logger.error(f"Error creating start menu shortcut: {e}")
        return False


def copy_uninstaller():
    """
    Copy the uninstall.bat script to the installation directory
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the source uninstall.bat path
        if hasattr(sys, '_MEIPASS'):  # PyInstaller environment
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        source_uninstaller = os.path.join(base_dir, "uninstall.bat")
        
        # If uninstall.bat exists in the source directory, copy it to installation directory
        if os.path.exists(source_uninstaller):
            target_uninstaller = os.path.join(INSTALL_DIR, "uninstall.bat")
            shutil.copy2(source_uninstaller, target_uninstaller)
            logger.info(f"Copied uninstaller to: {target_uninstaller}")
            return True
        else:
            logger.warning(f"Uninstaller script not found at: {source_uninstaller}")
            return False
    except Exception as e:
        logger.error(f"Error copying uninstaller: {e}")
        return False


def install_application():
    """Perform the installation process"""
    if is_installed():
        logger.info("Application is already installed. Skipping installation.")
        return True
    
    logger.info("Starting application installation")
    
    # Get current executable path
    source_exe = sys.executable
    if not os.path.exists(source_exe):
        logger.error(f"Current executable not found: {source_exe}")
        return False
    
    try:
        # Create installation directory if it doesn't exist
        os.makedirs(INSTALL_DIR, exist_ok=True)
        
        # Copy the executable
        target_exe = os.path.join(INSTALL_DIR, os.path.basename(source_exe))
        shutil.copy2(source_exe, target_exe)
        
        # Create desktop.ini
        create_desktop_ini()
        
        # Create Start Menu shortcut
        create_start_menu_shortcut(target_exe)
        
        # Copy the uninstaller script to installation directory
        copy_uninstaller()
        
        # Create registry entry to mark as installed
        create_installation_marker()
        
        logger.info(f"Installation completed successfully to: {INSTALL_DIR}")
        return True
    except Exception as e:
        logger.error(f"Error during installation: {e}")
        return False


def restart_from_installed_location():
    """
    Restart the application from its installed location
    """
    try:
        installed_exe = os.path.join(INSTALL_DIR, os.path.basename(sys.executable))
        if os.path.exists(installed_exe):
            # Start the installed executable
            subprocess.Popen([installed_exe])
            # Exit the current instance
            atexit.register(lambda: os._exit(0))
            return True
        return False
    except Exception as e:
        logger.error(f"Error restarting from installed location: {e}")
        return False


def needs_installation():
    """
    Check if the application needs to be installed
    
    Returns:
        True if installation is needed, False otherwise
    """
    # If already installed, no need to install again
    if is_installed():
        return False
    
    # If running from Program Files, mark as installed and continue
    if sys.executable.lower().startswith(os.environ.get('PROGRAMFILES', 'C:\\Program Files').lower()):
        create_installation_marker()
        return False
    
    # Otherwise, installation is needed
    return True


def handle_first_run():
    """
    Check if this is the first run and handle installation if needed
    
    Returns:
        True if application can continue normally,
        False if application needs to exit (e.g., after installation)
    """
    if not needs_installation():
        logger.info("No installation needed. Continuing normal startup.")
        return True
    
    logger.info("First run detected. Installation needed.")
    
    # Check if we have admin rights
    if not is_admin():
        # Restart with admin privileges
        logger.info("Requesting elevation to administrator privileges for installation")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                " ".join(sys.argv), 
                None, 
                1
            )
            # Exit the current instance
            sys.exit(0)
            return False
        except Exception as e:
            logger.error(f"Failed to restart with admin privileges: {e}")
            # Continue without admin, installation might fail
    
    # Perform installation
    if install_application():
        # Restart from installed location
        restart_from_installed_location()
        return False
    
    # If installation failed, continue with current executable
    logger.warning("Installation failed. Continuing with current executable.")
    return True
