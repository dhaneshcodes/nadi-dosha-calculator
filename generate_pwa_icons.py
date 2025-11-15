#!/usr/bin/env python3
"""
Generate PWA icons from og-image.png
Requires: pip install Pillow
"""

try:
    from PIL import Image
except ImportError:
    print("❌ Pillow not installed. Install with: pip install Pillow")
    exit(1)

import os
from pathlib import Path

# Icon sizes required for PWA
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def generate_icons():
    """Generate all PWA icon sizes from og-image.png"""
    
    # Source image
    source_path = Path('og-image.png')
    
    if not source_path.exists():
        print(f"❌ Source image not found: {source_path}")
        print("💡 Please upload og-image.png first, or create it from:")
        print("   D:/DOWNLOADS-CHROME/Gemini_Generated_Image_ub2dikub2dikub2d.png")
        return False
    
    try:
        # Open source image
        print(f"📸 Opening source image: {source_path}")
        source_img = Image.open(source_path)
        
        # Convert to RGB if RGBA (for better compatibility)
        if source_img.mode == 'RGBA':
            # Create white background
            rgb_img = Image.new('RGB', source_img.size, (255, 255, 255))
            rgb_img.paste(source_img, mask=source_img.split()[3])  # Use alpha channel as mask
            source_img = rgb_img
        elif source_img.mode != 'RGB':
            source_img = source_img.convert('RGB')
        
        print(f"✅ Source image: {source_img.size[0]}x{source_img.size[1]}, mode: {source_img.mode}")
        
        # Generate icons
        generated = 0
        for size in ICON_SIZES:
            output_path = Path(f'icon-{size}x{size}.png')
            
            # Resize with high-quality resampling
            resized = source_img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save
            resized.save(output_path, 'PNG', optimize=True)
            print(f"✅ Generated: {output_path} ({size}x{size})")
            generated += 1
        
        print(f"\n🎉 Successfully generated {generated} icon files!")
        print(f"📁 Location: {Path.cwd()}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating icons: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("PWA Icon Generator")
    print("=" * 60)
    print()
    
    if generate_icons():
        print("\n📤 Next steps:")
        print("1. Review the generated icons")
        print("2. Upload to server: scp -i deploy_key -P 22 icon-*.png root@159.89.161.170:/var/www/nadi-dosha-calculator/")
        print("3. Test PWA installation on mobile/desktop")
    else:
        print("\n💡 Alternative: Use online tool at https://www.pwabuilder.com/imageGenerator")

