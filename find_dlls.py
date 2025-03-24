"""
Script to find important DLLs in the system
"""
import os
import sys
import ctypes
import glob

def find_dll(dll_name):
    """Find a DLL in various system locations"""
    print(f"\nSearching for {dll_name}...")
    
    # Common locations
    search_paths = [
        os.environ.get("WINDIR", "C:\\Windows"),
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "System32"),
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "SysWOW64"),
        os.environ.get("PATH", "").split(os.pathsep)
    ]
    
    # Flatten the list
    paths = []
    for path in search_paths:
        if isinstance(path, list):
            paths.extend(path)
        else:
            paths.append(path)
    
    found_dlls = []
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        
        try:
            # Using glob to handle wildcards
            for dll_path in glob.glob(os.path.join(path, dll_name)):
                if os.path.isfile(dll_path):
                    found_dlls.append(dll_path)
                    print(f"  Found at: {dll_path}")
        except Exception as e:
            print(f"  Error searching in {path}: {e}")
    
    if not found_dlls:
        print(f"  {dll_name} NOT FOUND in common system locations")
    
    return found_dlls

def main():
    """Main function"""
    print("DLL Finder Utility")
    print("=================")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Python Executable: {sys.executable}")
    
    # Check ctypes location
    try:
        print(f"\nCtypes information:")
        print(f"  Module location: {ctypes.__file__}")
        
        # Try to load _ctypes
        try:
            import _ctypes
            print(f"  _ctypes module location: {_ctypes.__file__}")
        except ImportError as e:
            print(f"  Error importing _ctypes: {e}")
        
        # Get loaded DLLs
        print("\nCurrently loaded DLLs:")
        loaded_dlls = [dll._name for dll in ctypes.cdll.items if dll._name]
        for dll in loaded_dlls:
            print(f"  {dll}")
    except Exception as e:
        print(f"  Error getting ctypes info: {e}")
    
    # Search for specific DLLs
    dlls_to_find = [
        "libffi*.dll", 
        "ffi.dll",
        "libcrypto*.dll", 
        "libssl*.dll",
        "LIBBZ2.dll", 
        "liblzma.dll",
        "python*.dll"
    ]
    
    for dll_name in dlls_to_find:
        find_dll(dll_name)
    
    # If in a conda environment, check conda paths
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        print(f"\nSearching in Conda environment ({conda_prefix})...")
        conda_paths = [
            os.path.join(conda_prefix, "DLLs"),
            os.path.join(conda_prefix, "Library", "bin")
        ]
        
        for dll_name in dlls_to_find:
            for path in conda_paths:
                if os.path.exists(path):
                    try:
                        for dll_path in glob.glob(os.path.join(path, dll_name)):
                            if os.path.isfile(dll_path):
                                print(f"  Found {dll_name} at: {dll_path}")
                    except Exception as e:
                        print(f"  Error searching in {path}: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
