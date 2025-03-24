"""
Copy all required DLLs to the distribution directory
to ensure the executable works properly
"""
import os
import sys
import shutil
import glob
import ctypes

def main():
    """Main function to copy DLLs to dist directory"""
    # Target directory
    target_dir = os.path.join("dist", "Khmer TTS")
    if not os.path.exists(target_dir):
        print(f"Error: Target directory {target_dir} does not exist.")
        print("Please run the build script first.")
        return False
    
    # Create a list of DLLs we need
    dlls_to_copy = [
        "libffi*.dll", 
        "ffi.dll",
        "libcrypto*.dll", 
        "libssl*.dll",
        "LIBBZ2.dll", 
        "liblzma.dll",
        "python*.dll",
        "vcruntime*.dll",
        "msvcp*.dll",
        "api-ms-win*.dll"
    ]
    
    # Search paths
    search_paths = [
        os.environ.get("WINDIR", "C:\\Windows"),
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "System32"),
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "SysWOW64")
    ]
    
    # Add Conda paths if in Conda environment
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        search_paths.extend([
            os.path.join(conda_prefix, "DLLs"),
            os.path.join(conda_prefix, "Library", "bin")
        ])
    
    # Add Python directory
    python_dir = os.path.dirname(sys.executable)
    search_paths.append(python_dir)
    
    # Get directory of the ctypes module
    try:
        ctypes_dir = os.path.dirname(ctypes.__file__)
        search_paths.append(ctypes_dir)
    except:
        pass
    
    # Search for and copy DLLs
    copied_dlls = []
    for dll_pattern in dlls_to_copy:
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            try:
                # Find all matching DLLs
                matches = glob.glob(os.path.join(search_path, dll_pattern))
                for dll_path in matches:
                    if os.path.isfile(dll_path):
                        dll_name = os.path.basename(dll_path)
                        target_path = os.path.join(target_dir, dll_name)
                        
                        # Copy if not already copied
                        if dll_name not in copied_dlls:
                            try:
                                shutil.copy2(dll_path, target_path)
                                copied_dlls.append(dll_name)
                                print(f"Copied {dll_name} from {dll_path}")
                            except Exception as e:
                                print(f"Error copying {dll_path}: {e}")
            except Exception as e:
                print(f"Error searching in {search_path}: {e}")
    
    print(f"\nSuccessfully copied {len(copied_dlls)} DLLs to {target_dir}")
    print("List of copied DLLs:")
    for dll in copied_dlls:
        print(f"  {dll}")
    
    return True

if __name__ == "__main__":
    main()
