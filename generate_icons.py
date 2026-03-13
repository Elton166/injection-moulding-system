"""
Generate unique app icons for Injection Moulding Management System
Run: python generate_icons.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient(width, height):
    """Create a gradient background"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Define gradient colors
    color1 = (102, 126, 234)  # #667eea
    color2 = (118, 75, 162)   # #764ba2
    color3 = (240, 147, 251)  # #f093fb
    
    for y in range(height):
        # Calculate color for this row
        ratio = y / height
        if ratio < 0.5:
            # Blend color1 to color2
            blend_ratio = ratio * 2
            r = int(color1[0] + (color2[0] - color1[0]) * blend_ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * blend_ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * blend_ratio)
        else:
            # Blend color2 to color3
            blend_ratio = (ratio - 0.5) * 2
            r = int(color2[0] + (color3[0] - color2[0]) * blend_ratio)
            g = int(color2[1] + (color3[1] - color2[1]) * blend_ratio)
            b = int(color2[2] + (color3[2] - color2[2]) * blend_ratio)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

def draw_injection_machine(draw, size):
    """Draw stylized injection moulding machine"""
    center = size // 2
    scale = size / 512
    
    # Machine base
    base_color = (255, 255, 255, 240)
    draw.rectangle(
        [center - int(120 * scale), center + int(60 * scale),
         center + int(120 * scale), center + int(100 * scale)],
        fill=base_color
    )
    
    # Injection unit (left)
    draw.rectangle(
        [center - int(140 * scale), center - int(20 * scale),
         center - int(40 * scale), center + int(60 * scale)],
        fill=base_color
    )
    
    # Barrel
    draw.rectangle(
        [center - int(40 * scale), center + int(10 * scale),
         center + int(40 * scale), center + int(30 * scale)],
        fill=base_color
    )
    
    # Clamping unit (right)
    draw.rectangle(
        [center + int(40 * scale), center - int(40 * scale),
         center + int(140 * scale), center + int(60 * scale)],
        fill=base_color
    )
    
    # Mould cavity (center - highlighted)
    mould_color = (255, 193, 7, 230)
    draw.rectangle(
        [center - int(20 * scale), center - int(10 * scale),
         center + int(20 * scale), center + int(30 * scale)],
        fill=mould_color
    )

def draw_decorative_elements(draw, size):
    """Add decorative corner brackets and dots"""
    margin = int(size * 0.04)
    bracket_size = int(size * 0.06)
    line_width = max(2, int(size * 0.006))
    
    bracket_color = (255, 255, 255, 180)
    
    # Top-left bracket
    draw.line([margin + bracket_size, margin, margin, margin], fill=bracket_color, width=line_width)
    draw.line([margin, margin, margin, margin + bracket_size], fill=bracket_color, width=line_width)
    
    # Top-right bracket
    draw.line([size - margin - bracket_size, margin, size - margin, margin], fill=bracket_color, width=line_width)
    draw.line([size - margin, margin, size - margin, margin + bracket_size], fill=bracket_color, width=line_width)
    
    # Bottom-left bracket
    draw.line([margin, size - margin - bracket_size, margin, size - margin], fill=bracket_color, width=line_width)
    draw.line([margin, size - margin, margin + bracket_size, size - margin], fill=bracket_color, width=line_width)
    
    # Bottom-right bracket
    draw.line([size - margin, size - margin - bracket_size, size - margin, size - margin], fill=bracket_color, width=line_width)
    draw.line([size - margin - bracket_size, size - margin, size - margin, size - margin], fill=bracket_color, width=line_width)
    
    # Corner dots
    dot_radius = max(3, int(size * 0.008))
    dot_color = (255, 255, 255, 200)
    center = size // 2
    offset = int(size * 0.29)
    
    positions = [
        (center - offset, center - offset),
        (center + offset, center - offset),
        (center - offset, center + offset),
        (center + offset, center + offset)
    ]
    
    for x, y in positions:
        draw.ellipse([x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius], fill=dot_color)

def create_icon(size):
    """Create a unique icon with the specified size"""
    # Create gradient background
    image = create_gradient(size, size)
    
    # Convert to RGBA for transparency support
    image = image.convert('RGBA')
    
    # Create overlay for drawing
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Draw decorative circles
    center = size // 2
    for i in range(5):
        radius = int(size * (0.2 + i * 0.15))
        circle_color = (255, 255, 255, 25)
        draw.ellipse(
            [center - radius, center - radius, center + radius, center + radius],
            outline=circle_color,
            width=max(1, int(size * 0.01))
        )
    
    # Draw injection machine
    draw_injection_machine(draw, size)
    
    # Add text "IM"
    try:
        # Try to use a bold font
        font_size = int(size * 0.16)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        text = "IM"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = center - text_width // 2
        text_y = center - int(size * 0.2) - text_height // 2
        
        # Draw text with shadow
        shadow_offset = max(2, int(size * 0.004))
        draw.text((text_x + shadow_offset, text_y + shadow_offset), text, 
                 fill=(0, 0, 0, 128), font=font)
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    except Exception as e:
        print(f"Note: Could not add text: {e}")
    
    # Draw decorative elements
    draw_decorative_elements(draw, size)
    
    # Composite overlay onto background
    image = Image.alpha_composite(image, overlay)
    
    # Convert back to RGB for PNG
    final_image = Image.new('RGB', (size, size), (255, 255, 255))
    final_image.paste(image, (0, 0), image)
    
    return final_image

def main():
    """Generate both icon sizes"""
    print("🎨 Generating unique app icons...")
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Generate 192x192 icon
    print("Creating 192x192 icon...")
    icon_192 = create_icon(192)
    icon_192.save('static/icon-192.png', 'PNG', quality=95)
    print("✅ Saved: static/icon-192.png")
    
    # Generate 512x512 icon
    print("Creating 512x512 icon...")
    icon_512 = create_icon(512)
    icon_512.save('static/icon-512.png', 'PNG', quality=95)
    print("✅ Saved: static/icon-512.png")
    
    print("\n🎉 Icons generated successfully!")
    print("\n📱 Your app now has unique, professional icons!")
    print("\nNext steps:")
    print("1. Restart your Django server")
    print("2. Visit http://127.0.0.1:8000/")
    print("3. Check DevTools → Application → Manifest to see icons")
    print("4. Deploy and install on Android to see the new icon!")

if __name__ == '__main__':
    main()
