import os 
from PyInstaller.utils.hooks import collect_dynamic_libs 
 
# Collect DLLs 
binaries = collect_dynamic_libs('_ctypes') 
 
# Add our downloaded DLLs 
dll_dir = os.path.join(os.path.abspath('.'), 'dlls') 
for file in os.listdir(dll_dir): 
    if file.lower().endswith('.dll'): 
        binaries.append((os.path.join(dll_dir, file), '.')) 
 
hiddenimports = ['_ctypes'] 
