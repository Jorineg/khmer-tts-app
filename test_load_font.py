import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

print("--- Minimal Font Load Test ---")

# --- Configuration ---
# !!! IMPORTANT: Make absolutely sure this path is correct !!!
# Use the full, absolute path to your Roboto-Regular.ttf file
FONT_FILE_PATH = r"D:\programming\khmer stt app\resources\fonts\Roboto-Regular.ttf"
# --- End Configuration ---

print(f"Python executable: {sys.executable}")
print(f"Attempting to load font file: {FONT_FILE_PATH}")

# 1. Check if file exists using Python's check
if not os.path.exists(FONT_FILE_PATH):
    print(f"[ERROR] Font file not found at: {FONT_FILE_PATH}")
    sys.exit(1) # Exit if file doesn't exist
else:
    print("[INFO] Font file found by os.path.exists.")

# 2. Create QApplication instance (required for some Qt functionalities)
#    We create it *before* calling QFontDatabase methods just in case.
print("[INFO] Creating QApplication instance...")
try:
    app = QApplication(sys.argv)
    print("[INFO] QApplication instance created successfully.")
except Exception as e:
    print(f"[ERROR] Failed to create QApplication: {e}")
    sys.exit(1)

# 3. Attempt to load the font
print("[INFO] Calling QFontDatabase.addApplicationFont...")
font_id = -1 # Initialize to failure state
try:
    # --- THIS IS THE CRITICAL CALL ---
    font_id = QFontDatabase.addApplicationFont(FONT_FILE_PATH)
    # --- END CRITICAL CALL ---

    print(f"[INFO] QFontDatabase.addApplicationFont returned: {font_id}")

    if font_id != -1:
        print("[SUCCESS] Font seems to have been loaded (ID >= 0).")
        # Optional: Try getting family names
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            print(f"[INFO] Found font families: {families}")
        else:
            print("[WARNING] Font loaded (ID >= 0), but couldn't get family names.")
    else:
        print("[ERROR] Font loading failed (ID == -1).")

except Exception as e:
    # This probably won't catch a silent C++ crash, but include it anyway
    print(f"[ERROR] Caught Python exception during addApplicationFont: {e}")

print("[INFO] Script execution finished.")

# Optional: Keep the app running briefly to see if it crashes later
# print("Starting event loop briefly...")
# app.exec_() # Usually not needed just for font loading, but can sometimes reveal issues
# sys.exit(0) # Exit cleanly if app.exec_() is used and finishes