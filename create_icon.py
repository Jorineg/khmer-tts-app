"""
Create a simple icon for the Khmer TTS application.
This will be used by the installer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Create the resources directory if it doesn't exist
resources_dir = "resources"
if not os.path.exists(resources_dir):
    os.makedirs(resources_dir)

# Create a 256x256 icon
icon_size = 256
image = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a background circle
bg_color = (65, 105, 225)  # Royal blue
draw.ellipse([(10, 10), (icon_size-10, icon_size-10)], fill=bg_color)

# Try to add text (if we have a font)
try:
    # Try to get a font
    font_size = 120
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # Draw text
    text = "KH"
    # Use getbbox or getsize based on Pillow version
    text_bbox = None
    try:
        # For newer Pillow versions
        text_bbox = font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        # For older Pillow versions
        try:
            text_width, text_height = font.getsize(text)
        except:
            # Fallback to a hardcoded estimate if both methods fail
            text_width, text_height = icon_size // 2, icon_size // 2
    
    position = ((icon_size - text_width) // 2, (icon_size - text_height) // 2 - 10)
    draw.text(position, text, fill=(255, 255, 255), font=font)
except Exception as e:
    print(f"Could not add text to icon: {e}")
    # Draw a simple symbol if text fails
    draw.rectangle([(icon_size//3, icon_size//3), (2*icon_size//3, 2*icon_size//3)], fill=(255, 255, 255))

# Save as PNG
png_path = os.path.join(resources_dir, "icon.png")
image.save(png_path)
print(f"Created icon at {png_path}")

# Save as ICO for Windows
try:
    ico_path = os.path.join(resources_dir, "icon.ico")
    # Create multiple sizes for the ICO file
    image.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"Created ICO at {ico_path}")
except Exception as e:
    print(f"Could not create ICO file: {e}")
    # Try another method
    try:
        image.save(ico_path, format='ICO')
        print(f"Created basic ICO at {ico_path}")
    except:
        print("Failed to create ICO file completely.")
