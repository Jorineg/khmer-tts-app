"""
Check required dependencies for Khmer TTS application
"""
import importlib
import sys
import subprocess
import os
import pkg_resources

def check_module(module_name):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        # Check version
        try:
            version = pkg_resources.get_distribution(module_name).version
            return True, version
        except pkg_resources.DistributionNotFound:
            return True, "Unknown version"
    except ImportError as e:
        return False, str(e)

def main():
    # Required modules from requirements.txt
    required_modules = [
        # Core
        'dotenv',
        'keyring',
        'PyQt5',
        
        # Audio
        'pyaudio',
        'wave',
        
        # Keyboard and clipboard
        'pynput',
        'pyperclip',
        
        # APIs
        'google.generativeai',
        'elevenlabs',
        
        # Packaging
        'PyInstaller',
    ]
    
    print("Checking required dependencies for Khmer TTS application...")
    print("-" * 60)
    
    all_good = True
    missing = []
    
    for module in required_modules:
        print(f"Checking {module}...", end=" ")
        result, version = check_module(module)
        if result:
            print(f"OK (Version: {version})")
        else:
            all_good = False
            missing.append(module)
            print(f"MISSING ({version})")
    
    print("-" * 60)
    
    if all_good:
        print("All required dependencies are installed!")
    else:
        print("Missing dependencies:")
        for module in missing:
            print(f"  - {module}")
        print("\nTo install missing dependencies:")
        print("pip install -r requirements.txt")
    
    # Check Python version
    print("-" * 60)
    print(f"Python version: {sys.version}")
    
    # Check for any potential conflicts
    print("-" * 60)
    print("Checking for potential conflicts...")
    if 'tensorflow' in sys.modules:
        print("WARNING: TensorFlow is loaded, which might unnecessarily increase package size.")
    else:
        print("OK: TensorFlow is not loaded.")
    
    if 'torch' in sys.modules:
        print("WARNING: PyTorch is loaded, which might unnecessarily increase package size.")
    else:
        print("OK: PyTorch is not loaded.")
    
if __name__ == "__main__":
    main()
    print("\nPress Enter to exit...")
    input()
