"""
PyInstaller spec file for Khmer TTS application
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# Get the absolute path to the resources directory
resources_dir = os.path.join(os.path.abspath('.'), 'resources')
resource_files = [(resources_dir, 'resources')]

# Collect all data files for the packages we need
datas = resource_files + []
datas += collect_data_files('pynput')
datas += collect_data_files('google.generativeai')
datas += collect_data_files('elevenlabs')
datas += collect_data_files('keyring')

# Define binaries to include (DLLs)
binaries = []

# Search for DLLs in common locations
dll_names = ['libffi-7.dll', 'libffi-8.dll', 'libffi-6.dll', 'libffi.dll', 
             'ffi.dll', 'LIBBZ2.dll', 'liblzma.dll', 'libcrypto-3-x64.dll', 
             'libssl-3-x64.dll']
dll_locations = ['C:\\Windows\\System32', 'C:\\Windows\\SysWOW64', 
                 'C:\\ProgramData\\miniconda3\\DLLs', 
                 'C:\\ProgramData\\miniconda3\\Library\\bin']

for dll_location in dll_locations:
    if os.path.exists(dll_location):
        for dll_name in dll_names:
            dll_path = os.path.join(dll_location, dll_name)
            if os.path.exists(dll_path):
                binaries.append((dll_path, '.'))

# Add dynamic libraries for _ctypes
binaries += collect_dynamic_libs('_ctypes')

# Get hidden imports for our packages
hidden_imports = collect_submodules('pynput') + \
                collect_submodules('keyring') + \
                collect_submodules('google.generativeai') + \
                collect_submodules('elevenlabs') + \
                ['_ctypes', 'win32timezone', 'keyring.backends.Windows',
                 'pynput.keyboard._win32', 'pynput.mouse._win32']

# List of modules to explicitly exclude
excludes = [
    'tensorflow', 'torch', 'pandas', 'matplotlib', 
    'notebook', 'jupyter', 'IPython', 'tk', 'tcl', 
    'PyQt6', 'PySide', 'pytest'
]

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Khmer TTS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Khmer TTS',
)
