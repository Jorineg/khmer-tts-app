1. translation stings file is not found for exe. Assumption: it is not bundeled, not properly referenced, ... fix this.

2. in windows overview tab there is the text "ti set up your api keys" that seems to be hardcoded. It is the only text that is displayed if translations strings are missing. move to strings.

3. remove installer batch file and instead "install" when first started (from python of python called batch/ps script that is bundeled into the exe). Detect if installed via registry entry or something and do not install if already installed. Settings are already stored in registry. So maybe just detect if settings are present or not. Installation should do the following:
- create application folder in programmfiles
- copy currently running exe there (or create a shortcut there? I don't know what is better) Any way check how autostart setting functionality is implemented and make sure that it works. (correct path)
- create windows start menu entry
- do not create a desktop shortcut
If you do this, please check build.yml installer batch script for everything that is done there. It currently doesn't work properly, but the intent should be clear. We want to do similar things. But no desktop shortcut.
- register as a proper winodows application

4. create an uninstall batch script that does the opposite of the install script. Make sure to also:
- delete appdata\roaming\KhmerSTT. There is a log and lock files created in a directory. delete the directory there. check for proper name of directory.
- delete api keys from windows credentials manager
- delete autostart registry entry
- delete settings from registry (\hkeycurrentuser\software\KhmerSTT)
- delete application folder in programfiles
- delete start menu entry
NOTE: The uninstaller should be a standalone batch or PowerShell script that an end user can double-click without needing Python installed. It should show clear progress messages and confirm successful uninstallation.

5. the transcription model selection is duplicated in settings. It appears once in the general tab and once in the language tab. Remove it from the general tab and ensure the setting is properly handled by the language tab. Check which one is actually used (which setting keys) and make sure that the changes do not break existing functionality.

6. the only reason the transcription models are not loaded is a missing api key. There is a windows notification if trascription fails because no models are available or selected model is not available. Make this more explicit to describe that one needs to add an api key in settings first. Make it easy to understand. (in notification, strings file)
   - Create different error notifications for different kinds of errors:
   - One specifically for no network connection
   - One for server or API errors (such as server errors or when free API limits are exhausted)

7. connected to 6., add a status (ready, recording, transcribing, error) that says "no api key for selected model" and is active if no api key is available for selected model. This should be only shown in main window, not in overlay. Should be shown instead of "ready". There is this text in overview tab that tells the user that they have to add only show this text if no api key is available for selected model. also make this text red. remove this text from visible window if there is an api key for seleted model. So this must be checked everytime api key is changed or model is changed. Check strings file for this message to make sure it makes sense and you don't remove to much/not enough.

8. There seems to be a bug that after application is started the shortcut doesn't work. It seems to not properly register on startup. However if it is changed thorugh settings (even if changed to the same it was before) it immediatly starts working. (until application is quit and reopend again.) fix this.

9. api keys are currently not found. Although something is written to windows credentials manager. I guess there is a mismatch between what key is written and what is read. But please check. Maybe it has a different cause.

10. with new installer created in 3. github artifacts can be a lot simpler. I only need one exe file. no zip, no license. nothing else. Please adjust build.yml accordingly.

11. there is a down arrow that in resources folder. It doesn't appear in application if bundeled as exe. chekck build.yml and backlog regarding strings....

12. overlay window shows old status for short time after being opened. so it might be "transcription" for some time although shortcut was just pressed and it is actually recording. fix this.

13. okay button on x app close is solid and doesnt match active hide button.... (i like this as main button)

14. "Ready" status text is not immedieatly translated on gui langauge change as other strings. But only after app restart. same for red error box in overview if api key for selected model is not set.

15. Text size issue with Khmer characters in the UI. On some screens, Khmer text appears too small and is unreadable, while English text renders properly. This may be because the default Qt font size units are not optimized for non-Latin scripts. Implement a solution to:
    - Identify screens where this issue occurs (mainly the overlay window and potentially others)
    - Create specific font size adjustments for Khmer language when it's selected
    - Consider using a larger default font size for Khmer throughout the application
    - Test with different Qt font size units (pixels, points, etc.) to find the most consistent rendering