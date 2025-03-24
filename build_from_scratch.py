"""
Build script to create a Windows executable for Khmer TTS
with specific handling for _ctypes and libffi DLL issues
"""
import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def ensure_dir(directory):
    """Ensure directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_build_dirs():
    """Clean build directories"""
    print("Cleaning build directories...")
    for dir_to_clean in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean, ignore_errors=True)

def find_dlls():
    """Find key DLLs in the system"""
    print("Searching for key DLLs...")
    dll_info = {}
    
    # DLLs to find
    dll_names = {
        'libffi': ['libffi-7.dll', 'libffi-6.dll', 'libffi.dll', 'ffi.dll'],
        'crypto': ['libcrypto-3-x64.dll', 'libcrypto.dll'],
        'ssl': ['libssl-3-x64.dll', 'libssl.dll'],
        'bz2': ['LIBBZ2.dll', 'libbz2.dll'],
        'lzma': ['liblzma.dll'],
    }
    
    # Search paths
    paths = [
        os.environ.get('WINDIR', 'C:\\Windows'),
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32'),
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'SysWOW64'),
    ]
    
    # Add Python and conda paths
    if 'CONDA_PREFIX' in os.environ:
        paths.extend([
            os.path.join(os.environ['CONDA_PREFIX'], 'DLLs'),
            os.path.join(os.environ['CONDA_PREFIX'], 'Library', 'bin')
        ])
    
    # Python directory
    python_dir = os.path.dirname(sys.executable)
    paths.append(python_dir)
    paths.append(os.path.join(python_dir, 'DLLs'))
    
    # Search for each DLL
    for key, dll_list in dll_names.items():
        dll_info[key] = None
        for path in paths:
            if not os.path.exists(path):
                continue
            
            for dll in dll_list:
                dll_path = os.path.join(path, dll)
                if os.path.exists(dll_path):
                    dll_info[key] = dll_path
                    print(f"Found {key} DLL: {dll_path}")
                    break
            
            if dll_info[key]:
                break
    
    return dll_info

def copy_dlls_to_cache(dll_info):
    """Copy found DLLs to a local cache"""
    dll_cache = 'dll_cache'
    ensure_dir(dll_cache)
    
    for key, dll_path in dll_info.items():
        if dll_path and os.path.exists(dll_path):
            dest = os.path.join(dll_cache, os.path.basename(dll_path))
            shutil.copy2(dll_path, dest)
            print(f"Copied {key} DLL to cache: {dest}")
    
    return dll_cache

def create_spec_file(dll_cache):
    """Create a PyInstaller spec file that includes the DLLs"""
    print("Creating PyInstaller spec file...")
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Get resource files
resource_dir = os.path.join(os.path.abspath('.'), 'resources')
resource_files = [(resource_dir, 'resources')]

# Get DLLs
dll_files = []
dll_dir = os.path.abspath('{dll_cache}')
if os.path.exists(dll_dir):
    for file in os.listdir(dll_dir):
        if file.lower().endswith('.dll'):
            dll_files.append((os.path.join(dll_dir, file), '.'))

# Combine data files
datas = resource_files

# Hidden imports
hidden_imports = [
    'keyring.backends.Windows',
    'pynput.keyboard._win32',
    'pynput.mouse._win32',
    'google.generativeai',
    'elevenlabs',
    '_ctypes',
    'ctypes',
]

# Collect submodules
for pkg in ['pynput', 'keyring', 'google.generativeai', 'elevenlabs']:
    try:
        hidden_imports.extend(collect_submodules(pkg))
    except Exception:
        pass

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=dll_files,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['tensorflow', 'torch', 'pandas', 'matplotlib', 'notebook', 'jupyter', 'IPython', 'tk', 'tcl', 'PyQt6', 'PySide', 'pytest'],
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
    console=True,
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
"""
    
    spec_file = 'khmer_tts_auto.spec'
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    
    return spec_file

def custom_dlls():
    """Create custom DLL files if needed"""
    print("Checking for custom DLLs...")
    dll_dir = 'dll_cache'
    ensure_dir(dll_dir)
    
    # Look for libffi DLL in common locations
    libffi_paths = []
    for root, _, files in os.walk('C:\\'):
        for file in files:
            if file.startswith('libffi') and file.endswith('.dll'):
                libffi_paths.append(os.path.join(root, file))
                break
        if libffi_paths:
            break
    
    if libffi_paths:
        for path in libffi_paths:
            dest = os.path.join(dll_dir, os.path.basename(path))
            shutil.copy2(path, dest)
            print(f"Copied libffi DLL: {dest}")
    else:
        # Create a minimal libffi stub
        print("No libffi DLL found, creating minimal stub...")
        with open(os.path.join(dll_dir, 'libffi-6.dll'), 'wb') as f:
            f.write(b'LIBFFI STUB - REPLACEMENT NEEDED')
    
    return dll_dir

def build_executable(spec_file):
    """Build the executable using PyInstaller"""
    print("Building executable with PyInstaller...")
    try:
        subprocess.run(['pyinstaller', '--clean', spec_file], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error building with PyInstaller.")
        return False

def manual_dll_copy():
    """Copy DLLs manually to dist folder"""
    print("Manually copying DLLs to dist folder...")
    dll_dir = 'dll_cache'
    dist_dir = os.path.join('dist', 'Khmer TTS')
    
    if os.path.exists(dll_dir) and os.path.exists(dist_dir):
        for file in os.listdir(dll_dir):
            if file.lower().endswith('.dll'):
                src = os.path.join(dll_dir, file)
                dst = os.path.join(dist_dir, file)
                shutil.copy2(src, dst)
                print(f"Copied {file} to {dst}")

def create_test_script():
    """Create a test script in the dist folder"""
    print("Creating test script...")
    dist_dir = os.path.join('dist', 'Khmer TTS')
    if os.path.exists(dist_dir):
        test_script = os.path.join(dist_dir, 'test.bat')
        with open(test_script, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Testing Khmer TTS...\n')
            f.write('"Khmer TTS.exe"\n')
            f.write('echo.\n')
            f.write('echo Test complete.\n')
            f.write('pause\n')
        print(f"Created test script at {test_script}")

def main():
    """Main build process"""
    print("=" * 40)
    print("Khmer TTS App Builder")
    print("=" * 40)
    
    # Clean existing build directories
    clean_build_dirs()
    
    # Find system DLLs
    dll_info = find_dlls()
    
    # Setup DLL cache
    dll_cache = copy_dlls_to_cache(dll_info)
    
    # Add custom DLLs if needed
    custom_dlls()
    
    # Create spec file
    spec_file = create_spec_file(dll_cache)
    
    # Build executable
    if build_executable(spec_file):
        # Copy DLLs to dist folder
        manual_dll_copy()
        
        # Create test script
        create_test_script()
        
        print("\nBuild complete!")
        print(f"The executable is available at: {os.path.join('dist', 'Khmer TTS', 'Khmer TTS.exe')}")
        print("A test script is available at: dist\\Khmer TTS\\test.bat")
    else:
        print("\nBuild failed.")

if __name__ == "__main__":
    main()
