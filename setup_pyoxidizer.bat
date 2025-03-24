@echo off
echo Setting up PyOxidizer for Khmer TTS
echo ==============================

:: Install PyOxidizer
echo Installing PyOxidizer...
pip install pyoxidizer

:: Create a PyOxidizer configuration
echo Creating PyOxidizer configuration...
echo # This is a PyOxidizer configuration file > pyoxidizer.bzl
echo def make_exe(dist): >> pyoxidizer.bzl
echo     python_config = dist.make_python_interpreter_config() >> pyoxidizer.bzl
echo     python_config.run_mode = "run-module" >> pyoxidizer.bzl
echo     python_config.module_name = "main" >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     python_config.resources_policy = "prefer-in-memory-over-filesystem" >> pyoxidizer.bzl
echo     python_config.include_sources = True >> pyoxidizer.bzl
echo     python_config.include_resources = True >> pyoxidizer.bzl
echo     python_config.include_test = False >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     dist.add_python_resource("main") >> pyoxidizer.bzl
echo     dist.add_python_resources("resources") >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     # Add required packages >> pyoxidizer.bzl
echo     for pkg in ["keyring", "PyQt5", "pyaudio", "pynput", "google.generativeai", "elevenlabs", "dotenv", "pyperclip"]: >> pyoxidizer.bzl
echo         dist.pip_install([pkg]) >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     # Exclude unneeded packages >> pyoxidizer.bzl
echo     for pkg in ["tensorflow", "torch", "pandas", "matplotlib"]: >> pyoxidizer.bzl
echo         dist.pip_exclude([pkg]) >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     exe = dist.to_python_executable( >> pyoxidizer.bzl
echo         name="Khmer TTS", >> pyoxidizer.bzl
echo         packaging_policy=dist.default_packaging_policy(), >> pyoxidizer.bzl
echo         config=python_config, >> pyoxidizer.bzl
echo     ) >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     exe.windows_runtime_dlls_mode = "always" >> pyoxidizer.bzl
echo     exe.windows_subsystem = "windows" >> pyoxidizer.bzl
echo     exe.resource_policies = {"resources": "prefer-in-memory-over-filesystem"} >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo     return exe >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo def make_install(exe): >> pyoxidizer.bzl
echo     return exe.to_install() >> pyoxidizer.bzl
echo. >> pyoxidizer.bzl
echo register_target("exe", make_exe) >> pyoxidizer.bzl
echo register_target("install", make_install, depends=["exe"], default=True) >> pyoxidizer.bzl
echo resolve_targets() >> pyoxidizer.bzl

echo.
echo Setup complete! You can now run:
echo.
echo   pyoxidizer build    - To build the application
echo   pyoxidizer run      - To run the application
echo.
echo Press any key to exit...
pause >nul
