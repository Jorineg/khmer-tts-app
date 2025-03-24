"""
Script to generate a simple arrow down image for the combo boxes
"""

from PIL import Image, ImageDraw
import os
import math

def generate_arrow_down(width=11, height=6, color=(102, 102, 102), line_width=1):
    """
    Generate a downward-pointing arrow with two diagonal lines
    making the image twice as wide as it is high
    
    Args:
        width (int): Width of the arrow in pixels
        height (int): Height of the arrow in pixels
        color (tuple): RGB color tuple
        line_width (int): Width of the lines in pixels
        
    Returns:
        Image: PIL Image object
    """
    # Create a transparent image with padding
    padding = 1
    img_width = width + padding * 2
    img_height = height + padding * 2
    img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate points for a downward-pointing arrow
    # Center bottom point
    center_x = padding + width // 2
    center_y = padding + height - 1
    
    # Left top point
    left_x = padding
    left_y = padding
    
    # Right top point
    right_x = padding + width - 1
    right_y = padding
    
    # Draw the two diagonal lines
    draw.line([(left_x, left_y), (center_x, center_y)], fill=color, width=line_width)
    draw.line([(right_x, right_y), (center_x, center_y)], fill=color, width=line_width)
    
    return img

if __name__ == "__main__":
    # Save path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(current_dir, "arrow_down.png")
    
    # Generate and save
    arrow = generate_arrow_down()
    arrow.save(save_path)
    
    print(f"Arrow image saved to {save_path}")
