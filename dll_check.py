import ctypes 
import os 
print("_ctypes found at:", ctypes) 
print("DLL search paths:") 
for path in os.environ["PATH"].split(os.pathsep): 
    if os.path.exists(path): 
        print("  ", path) 
        for file in os.listdir(path): 
            if file.lower().startswith("libffi"): 
                print("    Found:", os.path.join(path, file)) 
