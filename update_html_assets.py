import os
import re

PUBLIC_DIR = "/Users/samad/GITHUB SITES/ctscan-static/public"

def generate_alt_from_filename(filename):
    # Remove extension and dimensions (e.g. -300x300, -1024x683)
    base = os.path.splitext(filename)[0]
    base = re.sub(r'-\d+x\d+$', '', base)
    base = re.sub(r'-scaled$', '', base)
    words = base.replace('-', ' ').replace('_', ' ').split()
    
    # Capitalize and make it descriptive
    cleaned = " ".join(words)
    if "ct" not in cleaned.lower() and "scan" not in cleaned.lower():
        cleaned += " CT Scan Lucknow"
    else:
        # capitalize CT and Scan correctly
        cleaned = re.sub(r'(?i)\bct\b', 'CT', cleaned)
        cleaned = re.sub(r'(?i)\bscan\b', 'Scan', cleaned)
        
    return cleaned.title()

def process_html_file(filepath):
    is_homepage = os.path.basename(filepath) == "index.html" and os.path.dirname(filepath) == PUBLIC_DIR
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Update image src/srcset extensions to .webp for local uploads
    # Target strings inside wp-content/uploads/
    def replace_extensions(match):
        val = match.group(0)
        # replace .jpg, .jpeg, .png with .webp
        val = re.sub(r'\.(jpg|jpeg|png)(?=[?\s"\'\d,])', '.webp', val, flags=re.IGNORECASE)
        return val
        
    content = re.sub(r'(?:/wp-content/uploads/[^\s"\'>]+)', replace_extensions, content)
    
    # 2. Inject loading="lazy" and descriptive alt texts
    # We will find all <img> tags and parse/update them
    img_tag_pattern = re.compile(r'<img\b([^>]*)>', re.IGNORECASE)
    
    def update_img_tag(match):
        attrs_str = match.group(1)
        
        # Parse attributes
        attrs = {}
        # Simple attribute parser
        attr_pairs = re.findall(r'(\b[a-zA-Z\-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', attrs_str)
        for key, val1, val2, val3 in attr_pairs:
            attrs[key.lower()] = val1 or val2 or val3
            
        src = attrs.get('src', '')
        
        # Check if logo or hero image (should NOT be lazy loaded)
        is_logo = "logo" in src.lower() or "ct-scan-lucknow.webp" in src.lower() or "ct-scan-lucknow.png" in src.lower()
        is_hero = is_homepage and ("machine-scaled" in src.lower() or "machine.webp" in src.lower())
        
        # Rebuild attributes string
        new_attrs = []
        
        # Keep track of updated loading and alt
        has_loading = False
        has_alt = False
        
        for key, val1, val2, val3 in attr_pairs:
            k = key.lower()
            v = val1 or val2 or val3
            
            # Update source in attributes if it wasn't captured by the glob block (e.g. relative src)
            if k == 'src' or k == 'srcset':
                v = re.sub(r'\.(jpg|jpeg|png)\b', '.webp', v, flags=re.IGNORECASE)
                
            if k == 'loading':
                has_loading = True
                if is_logo or is_hero:
                    # Remove lazy loading for logo or hero
                    continue
                v = "lazy"
                
            if k == 'alt':
                has_alt = True
                # If alt is empty, generate a descriptive alt text
                if not v.strip():
                    filename = os.path.basename(src.split('?')[0]) if src else ""
                    v = generate_alt_from_filename(filename) if filename else "CT Scan Lucknow"
                    
            new_attrs.append(f'{key}="{v}"')
            
        # Add loading="lazy" if not present
        if not has_loading and not (is_logo or is_hero):
            new_attrs.append('loading="lazy"')
            
        # Add alt if not present
        if not has_alt:
            filename = os.path.basename(src.split('?')[0]) if src else ""
            alt_text = generate_alt_from_filename(filename) if filename else "CT Scan Lucknow"
            new_attrs.append(f'alt="{alt_text}"')
            
        return f'<img {" ".join(new_attrs)}>'
        
    content = img_tag_pattern.sub(update_img_tag, content)
    
    # 3. Preload hero image on homepage
    if is_homepage:
        preload_tag = '\n<link rel="preload" as="image" href="/wp-content/uploads/2025/01/machine-scaled.webp">\n'
        # Insert inside head
        if "</head>" in content and "rel=\"preload\" as=\"image\"" not in content:
            content = content.replace("</head>", f"{preload_tag}</head>", 1)
            print("Preloaded hero image on homepage.")
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Processed HTML assets and alt texts for: {filepath}")

def main():
    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith(".html"):
                process_html_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
