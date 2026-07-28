import os
import sys
from PIL import Image

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
TARGET_DIR = os.path.join(PUBLIC_DIR, "wp-content", "uploads")

def convert_images(quality=82):
    if not os.path.exists(TARGET_DIR):
        print(f"Directory not found: {TARGET_DIR}")
        sys.exit(1)
        
    converted_count = 0
    skipped_count = 0
    total_savings = 0
    
    print(f"Scanning directory: {TARGET_DIR}")
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in (".jpg", ".jpeg", ".png"):
                src_path = os.path.join(root, file)
                dest_path = os.path.splitext(src_path)[0] + ".webp"
                
                try:
                    img = Image.open(src_path)
                    
                    # Skip if already exists and webp is newer/valid
                    if os.path.exists(dest_path):
                        skipped_count += 1
                        continue
                        
                    # Get original file size
                    orig_size = os.path.getsize(src_path)
                    
                    # Convert and save
                    img.save(dest_path, "WEBP", quality=quality)
                    
                    # Get new file size
                    new_size = os.path.getsize(dest_path)
                    savings = orig_size - new_size
                    total_savings += max(0, savings)
                    
                    print(f"Converted: {file} -> {os.path.basename(dest_path)} (Saved {savings/1024:.2f} KB)")
                    converted_count += 1
                except Exception as e:
                    print(f"Failed to convert {file}: {e}")
                    
    print("\n--- Image Optimization Summary ---")
    print(f"Successfully converted: {converted_count} images")
    print(f"Skipped (already exist): {skipped_count} images")
    print(f"Total disk space saved: {total_savings / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    quality_arg = 82
    if len(sys.argv) > 1:
        try:
            quality_arg = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 convert_images.py [quality_percentage]")
            sys.exit(1)
    convert_images(quality=quality_arg)
