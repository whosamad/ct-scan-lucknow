import os
import re

PUBLIC_DIR = "/Users/samad/GITHUB SITES/ctscan-static/public"
DOMAIN = "https://ctscanlucknow.com"

def fix_sitemap_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace relative path locations with absolute domain URLs
    # For <loc>/path</loc> or <image:loc>/path</image:loc>
    def make_absolute(match):
        tag_open = match.group(1)
        path = match.group(2)
        tag_close = match.group(3)
        
        # Avoid prepending if already absolute
        if path.startswith("http"):
            return match.group(0)
            
        # Ensure correct slash joining
        if not path.startswith("/"):
            path = "/" + path
            
        # Update image extensions to .webp in sitemap locs
        path = re.sub(r'\.(jpg|jpeg|png)$', '.webp', path, flags=re.IGNORECASE)
        
        return f"{tag_open}{DOMAIN}{path}{tag_close}"
        
    # Locate all <loc>...</loc> and <image:loc>...</image:loc> tags
    # Using non-capturing groups (?:...) to keep group indexing clean:
    # group 1 = opening tag, group 2 = content, group 3 = closing tag
    loc_pattern = re.compile(r'(<(?:image:)?loc>)([^<]*)(</(?:image:)?loc>)', re.IGNORECASE)
    content = loc_pattern.sub(make_absolute, content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Fixed sitemap URLs and image extensions in: {filepath}")

def main():
    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith(".xml"):
                fix_sitemap_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
