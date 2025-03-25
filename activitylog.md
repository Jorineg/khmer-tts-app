## March 25, 2025
### Fixed resource loading for bundled executable (backlog task #11)
- Created new utility module `app/utils/resource_path.py` to handle resource paths consistently
- Implemented `get_resource_path()` and `get_resource_url()` functions for PyInstaller compatibility
- Modified stylesheet in `app/gui/styles/app_stylesheet.py` to use the new utility for loading arrow_down.png
- Ensures resources (especially the down arrow icon for combo boxes) properly appear in bundled exe
- Files changed: Added `app/utils/resource_path.py`, `app/utils/__init__.py`, Modified `app/gui/styles/app_stylesheet.py`

## March 25, 2025
### Simplified GitHub artifacts for easier distribution (backlog task #10)
- Modified `.github/workflows/build.yml` to streamline the build process
- Removed creation of additional files (install.bat, README.txt, LICENSE.txt)
- Eliminated zip packaging step and simplified artifact structure
- Now only the standalone executable is uploaded as the GitHub artifact
- This change supports the new self-installer functionality added in task #3
- Files changed: `.github/workflows/build.yml`

## March 25, 2025
### Improved UI layout by placing language selector and buttons side by side
- Modified the main window layout to place language selector and button container in a horizontal arrangement
- Removed vertical stacking to save space and create a more compact UI
- Aligned language selector to the left and buttons to the right
- Files changed: app/gui/main_window.py, app/gui/language_selector.py

## March 25, 2025
### Fixed initial language setting at application startup
- Fixed issue where GUI language wasn't properly applied at startup when set to Khmer
- Modified `LanguageSelector.set_language()` method to also update the TranslationManager
- Ensures that when application starts, the saved UI language preference is properly applied
- Removed need to switch between languages to get Khmer UI to work
- Files changed: app/gui/language_selector.py

## March 25, 2025
### Fixed language switching with TranslationManager singleton pattern
- Implemented singleton pattern for TranslationManager to ensure only one instance is used throughout the app
- Fixed TranslationManager's get_string method to properly handle the JSON structure
- Added has_string method to TranslationManager to check if translation keys exist
- Updated MainWindow to use the singleton instead of creating its own instance
- Updated overview_tab.py to handle feature_list translations properly when language changes
- Modified tab initialization to stop passing redundant translation_manager instances
- Files changed: app/i18n/translation_manager.py, app/gui/main_window.py, app/gui/tabs/overview_tab.py

### Fixed model switching functionality
- Fixed bug where switching transcription models would cause an AttributeError
- Added missing `update_transcription_model` method to `TranscriptionManager` class in `app/transcription/transcription_manager.py`
- Method handles model switching including error checking for missing API keys and model availability
- Ensures settings are properly updated when switching between transcription models

### Improved translation system for real-time language switching
- Implemented a centralized translation component registry in `TranslationManager` class
- Added auto-registration of UI components with the translation manager
- Fixed issue where app title, "current shortcut" and "status" labels weren't updated during language change
- Updated `OverviewTab`, `MainWindow`, and `TrayManager` classes to use new translation system
- Created a more consistent approach for UI language updates with central coordination
- All UI components now register themselves with the translation manager, allowing centralized updates
- UI now properly updates ALL text elements when language is changed without requiring app restart
- Additional tabs now use the improved translation system:
  - Updated `GeneralTab`, `ApiKeysTab`, and `LanguageTab` to use the registry system
  - Each component tracks its own translatable elements for more consistent updates
  - Refactored `MainWindow` translation handling to use a dictionary-based approach for cleaner code
  - Ensures all UI elements are properly updated when language changes

### Fixed translation issues (backlog tasks #1 and #2)
- **Task #1**: Fixed translation strings file not being found in executable
  - Modified the PyInstaller command in `.github/workflows/build.yml` to include the app/i18n directory in the executable bundle
  - Enhanced `TranslationManager` in `app/i18n/translation_manager.py` to better handle PyInstaller environment with proper fallback paths
- **Task #2**: Removed hardcoded text in overview tab
  - Removed hardcoded text "to set up your API keys" from `app/gui/tabs/overview_tab.py`
  - Replaced it with the proper translation string variable `api_keys_info2`

### Fixed duplicate settings functionality
- Identified and fixed multiple instances of redundant settings-saving operations:
  - Fixed autostart settings being saved twice - once in `GeneralTab.on_run_on_startup_changed()` and again in `MainWindow.on_autostart_changed()`
  - Removed redundant shortcut signal connection in `MainWindow.connect_tab_signals()` that bypassed the tab's handler
  - Fixed model selection settings being saved twice - once in `LanguageTab.on_model_selection_changed()` and again in `MainWindow.on_model_changed()`
  - Removed redundant language setting save in the `stop_recording()` method
- Main changes were in `app/gui/main_window.py` to remove duplicate settings operations
- This prevents unnecessary operations and potential race conditions when changing settings

### Implemented self-installation (backlog task #3)
- **Task #3**: Implemented self-installation on first run
  - Created new module `app/system/installer.py` to handle installation process
  - Updated `main.py` to check on startup if installation is needed
  - Added registry-based installation detection
  - Application now self-installs to Program Files on first run with admin privileges
  - Creates Start Menu entry (no desktop shortcut per requirements)
  - Makes sure autostart registry setting points to installed executable

### Created standalone uninstaller (backlog task #4)
- **Task #4**: Created standalone uninstaller batch script
  - Created `uninstall.bat` as a self-contained script that handles all uninstallation steps
  - The uninstaller requires no Python dependencies and can be double-clicked by end users
  - Updated installer to copy this uninstaller to the installation directory
  - Uninstaller removes API keys, registry entries, AppData directory, Start Menu shortcut, and installation directory
  - Added clear user feedback throughout the uninstallation process

### Removed duplicated model selection from settings (backlog task #5)
- **Task #5**: Removed duplicated transcription model selection from settings
  - Removed model selection group from the General tab in `app/gui/tabs/general_tab.py`
  - Updated Language tab's model selection handling in `app/gui/tabs/language_tab.py` to set both `model_selection` and `default_model` settings
  - Modified Language tab to load model selection based on `default_model` setting for consistency
  - Ensured backwards compatibility with existing code that may rely on the `default_model` setting

### Improved API key error notifications (backlog task #6)
- **Task #6**: Implemented more explicit error messages when transcription fails due to missing API keys
  - Added new translation strings for various error notifications in `app/i18n/strings.json`
  - Enhanced `TranscriptionManager` in `app/transcription/transcription_manager.py` to detect and report different error types:
    - Missing API key errors
    - Network connection errors
    - API service errors (server issues or quota exceeded)
  - Updated `MainWindow` to handle specific error types with detailed notifications
  - Added visible warning in the Overview tab to alert users about missing API keys
  - Implemented API key checking when starting the app and when changing transcription models
  - Added signal connections to update the UI when API keys are changed in the settings
  - Highlighted API key setup instructions in the Overview tab when keys are missing

### Added explicit API key status indicator (backlog task #7)
- **Task #7**: Added a status indicator for missing API keys
  - Added new translation string for "No API key for {model_name}" status in `app/i18n/strings.json`
  - Enhanced `OverviewTab.set_status()` to handle different status types with appropriate styling
  - Updated status text to show a bold red warning when API keys are missing
  - Modified `OverviewTab.update_api_key_warning()` to change the status to "no_api_key" when needed
  - Ensured API key setup instructions are only shown in red when an API key is missing
  - Made sure the status reverts to "Ready" when API keys are available

## March 25, 2025
### Fixed language switching functionality - Implemented Singleton Pattern
- Converted TranslationManager to use a proper singleton pattern with a static get_instance() method
- Fixed critical issue where multiple instances of TranslationManager were being created, causing language changes to not propagate
- Modified MainWindow, LanguageSelector, and all Tab classes to use the singleton instance rather than creating their own instances
- This ensures that when language is changed in one part of the application, it affects all other parts consistently
- Files modified:
  - app/i18n/translation_manager.py
  - app/gui/main_window.py
  - app/gui/language_selector.py
  - app/gui/tabs/language_tab.py
  - app/gui/tabs/api_keys_tab.py
  - app/gui/tabs/general_tab.py
  - app/gui/tabs/overview_tab.py

## March 25, 2025
### Refactored UI tabs to use new translatable widgets
- Created and implemented a comprehensive system of translatable widgets to simplify UI translation
- Converted TranslationManager to a singleton instance for easier access throughout the application
- Implemented embedded translation keys using <<key>> template syntax for more flexible translations
- Changed inheritance order for translatable widgets to fix initialization issues
- Simplified the TranslationManager by removing unnecessary methods and properties
- Added TranslatableQAction for system tray menu items to ensure they update when language changes
- Modified files: app/gui/widgets/translatable.py, app/i18n/translation_manager.py, app/gui/tray_manager.py

### Files Changed:
- `app/i18n/translation_manager.py`
- `app/gui/widgets/translatable.py`
- `app/gui/tabs/api_keys_tab.py`
- `app/gui/tabs/general_tab.py`
- `app/gui/tabs/language_tab.py`
- `app/gui/tabs/overview_tab.py`

### Benefits:
- More maintainable code with less boilerplate for translations
- Consistent approach to UI translations across the entire application
- UI components automatically update when language changes without manual management
- Simpler tab implementations with clear separation between UI and translation logic
- Reduced code duplication for translation-related functionality

## March 25, 2025
### Enhanced translation system with template strings
- Implemented a flexible template-based translation system using `<<key>>` syntax
- Simplified TranslatableMixin by removing prefix/suffix parameters
- Now any translatable widget can have rich text with embedded translation keys
- Example: `"<b><<overview_tab.title>></b> - <a href='#'><<buttons.click_here>></a>"`
- Refactored API Keys tab to use the new template approach
- All translatable widgets now support template strings with embedded translation keys
- Greatly simplified complex UI elements that mix static content with translated strings
- Added regex-based translation key extraction from templates

### Files Changed:
- `app/gui/widgets/translatable.py`
- `app/i18n/translation_manager.py`
- `app/gui/tabs/api_keys_tab.py`
- `app/gui/tabs/overview_tab.py`

### Benefits:
- More powerful and flexible translation integration in complex UI elements
- No need for separate prefix/suffix or manual string concatenation
- HTML and rich text can now easily include translatable components
- Cleaner code with less string manipulation for mixed content

## March 25, 2025
### Identified text size issue with Khmer characters in UI
- Documented an issue where Khmer text appears too small and unreadable on some screens
- The problem appears to be related to Qt font size units not being optimized for non-Latin scripts
- Added this to the backlog as item #15 with several proposed approaches to fix
- This will require testing different font sizing approaches to find the best solution for Khmer text
- Files changed: `backlog.md`

## March 25, 2025
### Fixed text size issue for Khmer characters (backlog task #15)
- Improved text readability for Khmer characters on screens with different resolutions
- Changed font size specifications from pixel units to point units (pt) in the application stylesheet
- Added explicit font-size: 10pt to all UI elements in the stylesheet for better cross-resolution display
- Changed the status label in the overlay window to use pointSize() instead of direct pixel size
- These changes ensure consistent text sizing across different screen resolutions
- Files changed: `app/gui/styles/app_stylesheet.py`, `app/gui/overlay.py`

## March 25, 2025
### Fixed missing translation key and typo in overview tab
- Added missing "shortcut" translation key in `app/i18n/strings.json` that was causing warning: "Translation key not found: overview_tab.shortcut, error: 'shortcut'"
- Fixed typo in the overview tab title from "Spech To Text" to "Speech To Text" in `app/gui/tabs/overview_tab.py`
- Replaced hardcoded app title with translation string reference using `self.get_string('overview_tab.title')` to follow localization best practices
- Updated translations for app_name, window_title, and overview_tab.title to be consistent

## March 25, 2025
### Fixed shortcut registration and display issues
- Fixed issue where the global shortcut was not working when configured
- Fixed overview tab not showing the correct shortcut
- Added proper notification from GeneralTab to MainWindow when shortcut is changed
- Improved MainWindow.update_shortcut_label to safely update the overview tab display
- Files changed: app/gui/tabs/general_tab.py, app/gui/main_window.py

## March 26, 2025
### Fixed shortcut persistence across application restarts
- Fixed issue where shortcuts weren't persisting correctly across application restarts
- Enhanced MainWindow.load_settings to properly initialize all shortcut-related components
- Added keyboard_thread initialization in MainWindow constructor for better state management
- Improved update_global_shortcut method to handle shortcut changes more robustly
- Ensured shortcut is correctly loaded into the General tab and keyboard listener on app startup
- Files changed: app/gui/main_window.py

## March 25, 2025
### Fixed translation widget updates on language change
- Fixed issue where UI widgets weren't properly updating when language was changed
- Added more robust signal connection mechanism in `app/gui/widgets/translatable.py`
- Implemented failsafe disconnection and reconnection logic to ensure signal is properly connected
- Translatable widgets now properly respond to language change events
- Added proper error handling for translation signal connection

## 2023-06-11: Refactoring Settings Management and Transcription Handling

### Changes Made:
- Created new `TranscriptionHandler` class to encapsulate recording and transcription logic
- Enhanced `SettingsManager` with specialized methods for updating shortcuts, languages, and models
- Simplified `MainWindow` by moving recording and transcription functionality to the new handler
- Updated tabs to use the enhanced SettingsManager methods, reducing redundancy
- Fixed duplication issues in settings handling across tabs

### Files Changed:
- `app/transcription/transcription_handler.py` (new file)
- `app/settings/settings_manager.py`
- `app/gui/main_window.py`
- `app/gui/tabs/language_tab.py`
- `app/gui/tabs/general_tab.py`

### Benefits:
- Improved code organization with clearer separation of responsibilities
- Reduced MainWindow code size and complexity
- Better encapsulation of functionality in appropriate classes
- Eliminated redundant settings operations

## 2023-06-12: UI Styling and Signal Handling Improvements

### Changes Made:
- Created a dedicated stylesheet module to separate styling from application logic
- Moved all CSS styles from MainWindow to the new app_stylesheet.py file
- Further simplified signal handling in MainWindow
- Removed redundant methods that were no longer needed
- Improved documentation explaining why certain methods remain in MainWindow
- Connected some tab signals directly to the TranscriptionHandler to reduce message passing

### Files Changed:
- Created new: `app/gui/styles/app_stylesheet.py`
- Updated: `app/gui/main_window.py`

### Benefits:
- Improved separation of concerns (styling vs. application logic)
- Further reduced code size and complexity in MainWindow
- More direct signal handling with less redundant methods

## 2023-06-12: Extended Stylesheet System to All Tabs

### Changes Made:
- Expanded the stylesheet module with additional component styles
- Moved all inline CSS from tab files to the central stylesheet
- Created specialized functions for different UI components:
  - Group boxes, combo boxes, labels, checkboxes, warning labels, etc.
- Standardized similar styles that were duplicated across files
- Fixed styling inconsistencies between tabs

### Files Changed:
- Enhanced: `app/gui/styles/app_stylesheet.py` 
- Updated: 
  - `app/gui/tabs/overview_tab.py`
  - `app/gui/tabs/language_tab.py`
  - `app/gui/tabs/general_tab.py`
  - `app/gui/tabs/api_keys_tab.py`

### Benefits:
- Better style consistency across all UI components
- Easier theme changes (all styles in one place)
- Reduced code duplication (approximately 150 lines removed)
- Simpler tab implementations with focus on functionality, not styling
- Improved maintainability for future UI changes

## March 25, 2025
### Fixed API keys not being found in Windows credentials manager (backlog task #9)
- Fixed mismatch between service names used when saving and retrieving API keys
- The API keys tab was saving keys with "google_api_key" and "elevenlabs_api_key" service names
- But config.py was retrieving with "google" and "elevenlabs" service names
- Updated app/gui/tabs/api_keys_tab.py to use consistent service names
- Also added missing winreg import in app/settings/settings_manager.py
- Files changed: 
  - app/gui/tabs/api_keys_tab.py
  - app/settings/settings_manager.py

## March 25, 2025
### Fixed uninstaller batch file bundling and Windows uninstaller registration
- Modified `.github/workflows/build.yml` to include uninstall.bat in the PyInstaller bundle
- Enhanced `app/system/installer.py` to register the uninstaller with Windows Add/Remove Programs
- Added `register_uninstaller()` function to create proper registry entries for uninstallation
- This ensures the uninstaller script is available in the packaged executable and appears in Windows' Add/Remove Programs
- Files changed: `.github/workflows/build.yml`, `app/system/installer.py`