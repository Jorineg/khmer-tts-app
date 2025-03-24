"""
Custom hook file for ctypes to ensure proper DLL loading
"""
from PyInstaller.utils.hooks import collect_dynamic_libs

# This collects all the DLL dependencies for the _ctypes module
binaries = collect_dynamic_libs('_ctypes')

# You can also add specific binaries here if needed
# binaries.append(('path/to/your/libffi.dll', '.'))

hiddenimports = ['_ctypes', 'ctypes.wintypes']
