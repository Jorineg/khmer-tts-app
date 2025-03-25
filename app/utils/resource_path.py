"""
Utility functions for handling resource paths in both development and PyInstaller environments.
"""
import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller
    
    Args:
        relative_path (str): The path relative to the resources directory
        
    Returns:
        str: The resolved absolute path to the resource
    """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # Assume we're running in development
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, relative_path)

def get_resource_url(relative_path):
    """
    Get a Qt-compatible URL to a resource, works for dev and for PyInstaller
    
    Args:
        relative_path (str): The path relative to the resources directory
        
    Returns:
        str: A URL in the format required by Qt stylesheets
    """
    # For PyInstaller bundled app, we need absolute paths with file:// protocol
    if hasattr(sys, '_MEIPASS'):
        # Use forward slashes for Qt stylesheet URLs even on Windows
        path = get_resource_path(relative_path).replace('\\', '/')
        # For stylesheets, we need to use the file:// protocol
        return f"file:///{path}"
    else:
        # In development mode, use the relative path that worked before
        return relative_path
