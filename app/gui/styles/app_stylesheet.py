"""
Application stylesheet definitions
"""

import os
from app.utils.resource_path import get_resource_url
from PyQt5.QtWidgets import QApplication

def get_main_stylesheet():
    """
    Return the main application stylesheet
    
    Returns:
        str: The stylesheet as a string
    """
    # Get the URL for the arrow down image
    arrow_down_url = get_resource_url('resources/arrow_down.png')
    
    return """
        QMainWindow, QDialog {
            background-color: #f5f5f7;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
            font-size: 10pt;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #1c6ea4;
        }
        
        QTabWidget::pane {
            border: 1px solid #d0d0d0;
            background-color: white;
            border-radius: 5px;
        }
        
        QTabBar::tab {
            background-color: #e6e6e6;
            color: #555555;
            padding: 8px 16px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border: 1px solid #d0d0d0;
            border-bottom: none;
            min-width: 80px;
            font-size: 10pt;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom-color: white;
            color: #3498db;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 1px solid #d0d0d0;
            border-radius: 5px;
            margin-top: 12px;
            padding-top: 10px;
            font-size: 10pt;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        
        QLabel {
            color: #333333;
            font-size: 10pt;
        }
        
        /* Define styles for input widgets */
        QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit {
            border: 1px solid #d0d0d0;
            border-radius: 3px;
            padding: 5px;
            background-color: #ffffff;
            selection-background-color: #3498db;
            selection-color: #ffffff;
            height: 16px;
            font-size: 10pt;
        }
        
        /* Custom dropdown arrow using the arrow image */
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #d0d0d0;
        }
        
        QComboBox::down-arrow {
            image: url(%s);
            width: 16px;
            height: 16px;
        }
    """ % arrow_down_url


def get_subtle_button_style():
    """
    Return style for subtle buttons
    
    Returns:
        str: The stylesheet as a string
    """
    return """
        QPushButton {
            background-color: transparent;
            color: #555555;
            border: 1px solid #d0d0d0;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 10pt;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
        QPushButton:pressed {
            background-color: #e0e0e0;
        }
    """


def get_accent_button_style():
    """
    Return style for accent buttons
    
    Returns:
        str: The stylesheet as a string
    """
    return """
        QPushButton {
            background-color: white;
            color: #3498db;
            border: 1px solid #3498db;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }
        QPushButton:hover {
            background-color: #ecf0f1;
        }
        QPushButton:pressed {
            background-color: #d6e9f8;
        }
    """


def get_group_box_style(color="#2980b9"):
    """
    Return style for QGroupBox
    
    Args:
        color: Color for the group box title, default is blue
        
    Returns:
        str: The stylesheet as a string
    """
    return f"""
        QGroupBox {{
            font-weight: bold;
            border: 1px solid #d0d0d0;
            border-radius: 5px;
            margin-top: 12px;
            padding-top: 10px;
            font-size: 10pt;
            color: {color};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
    """


def get_features_group_box_style():
    """
    Return style for features group box (used in overview tab)
    
    Returns:
        str: The stylesheet as a string
    """
    return """
        QGroupBox {
            font-weight: bold;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 10px;
            font-size: 10pt;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #2980b9;
        }
    """


def get_combo_box_style():
    """
    Return style for QComboBox
    
    Returns:
        str: The stylesheet as a string
    """
    return """
        QComboBox {
            border: 1px solid #d0d0d0;
            border-radius: 3px;
            padding: 5px;
            background-color: #ffffff;
            height: 16px;
            font-size: 10pt;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #d0d0d0;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
    """


def get_description_label_style():
    """
    Return style for description labels
    
    Returns:
        str: The stylesheet as a string
    """
    return "color: #34495e; line-height: 1.4; margin-bottom: 10px; font-size: 10pt;"


def get_feature_label_style():
    """
    Return style for feature list labels
    
    Returns:
        str: The stylesheet as a string
    """
    return "color: #34495e; padding-left: 5px; font-size: 10pt;"


def get_note_label_style():
    """
    Return style for note/hint labels
    
    Returns:
        str: The stylesheet as a string
    """
    return "font-style: italic; color: #7f8c8d; margin-top: 10px; font-size: 10pt;"


def get_warning_label_style():
    """
    Return style for warning/error labels
    
    Returns:
        str: The stylesheet as a string
    """
    return "color: #e74c3c; font-weight: bold; background-color: #ffeeee; padding: 10px; border-radius: 5px; font-size: 10pt;"


def get_label_style():
    """
    Return style for standard labels with bold formatting
    
    Returns:
        str: The stylesheet as a string
    """
    return "font-weight: bold; margin-right: 10px; font-size: 10pt;"


def get_checkbox_style():
    """
    Return style for checkboxes
    
    Returns:
        str: The stylesheet as a string
    """
    return "margin-bottom: 5px; font-size: 10pt;"


def get_link_style():
    """
    Return style for hyperlink labels
    
    Returns:
        str: The stylesheet as a string
    """
    return "margin-top: 5px; margin-bottom: 10px; color: #2980b9; font-size: 10pt;"


def get_status_label_style():
    """
    Return style for status labels
    
    Returns:
        str: The stylesheet as a string
    """
    return "color: #7f8c8d; margin-top: 5px; font-size: 10pt;"
