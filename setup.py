"""
Setup script for building a Windows installer using cx_Freeze
"""
import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "os", "sys", "ctypes", "logging", "keyring", "PyQt5", 
        "pyaudio", "wave", "pynput", "pyperclip", 
        "google.generativeai", "elevenlabs", "dotenv"
    ],
    "excludes": [
        "tensorflow", "torch", "numpy.random", "matplotlib", "pandas",
        "scipy", "notebook", "jupyter", "IPython", "h5py", "tkinter",
        "PySide", "PySide2", "PyQt6", "PyQt4", "wx", "FixTk",
        "tcl", "tk", "_tkinter", "botocore", "boto3", "pytest", "sklearn"
    ],
    "include_files": [
        ("resources", "resources")
    ],
    "include_msvcr": True,
}

# GUI applications require a different base on Windows
base = "Win32GUI" if sys.platform == "win32" else None

exe = Executable(
    script="main.py",
    base=base,
    target_name="Khmer TTS.exe",
    shortcut_name="Khmer TTS",
    shortcut_dir="DesktopFolder",
    icon="resources/icon.ico" if os.path.exists("resources/icon.ico") else None
)

setup(
    name="Khmer TTS",
    version="1.0.0",
    description="Khmer TTS Application",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
