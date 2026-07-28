import os
import re

PUBLIC_DIR = "/Users/samad/GITHUB SITES/ctscan-static/public"

METADATA_MAP = {
    "about-us/index.html": {
        "title": "About Us | CT Scan Lucknow Best Diagnostic Centre In UP",
        "description": "Learn more about CT Scan Lucknow, our state-of-the-art 128-slice CT scanner, our expert radiologists, and our commitment to affordable diagnostic care."
    },
    "contact-us/index.html": {
        "title": "Contact CT Scan Lucknow | Book Diagnostic Scan Appointment",
        "description": "Get in touch with CT Scan Lucknow. Book your appointment for CT Scan, X-Ray, and Ultrasound online or call us directly at +91-7266985519."
    },
    "privacy-policy/index.html": {
        "title": "Privacy Policy | CT Scan Lucknow Diagnostic Centre",
        "description": "Read the privacy policy of CT Scan Lucknow. Learn how we collect, protect, and use your personal information and diagnostic data securely."
    },
    "category/queries/index.html": {
        "title": "CT Scan Lucknow Queries | Patient Information & FAQs",
        "description": "Browse queries and FAQs about CT scans, X-rays, ultrasounds, and diagnostic procedures at CT Scan Lucknow. Find expert patient guides here."
    },
    "author/admlnlx/index.html": {
        "title": "admlnlx | Author at CT Scan Lucknow Diagnostic Centre",
        "description": "Read articles and expert guides published by admlnlx on CT Scan Lucknow. Find helpful tips about CT scans, safety, pricing, and procedures."
    },
    "author/teamctl/index.html": {
        "title": "TeamCTL | Author at CT Scan Lucknow Diagnostic Centre",
        "description": "Read diagnostic articles and guides written by TeamCTL at CT Scan Lucknow. Learn about CT scan safety, comparison guides, and Lucknow centres."
    },
    "can-cancer-be-detected-in-ct-scan/index.html": {
        "title": "Can Cancer Be Detected in CT Scan? Risks & Accuracy",
        "description": "Can cancer be detected in a CT scan? Learn about the accuracy of CT scans for diagnosing cancer, scan types, potential risks, and safety guidelines."
    },
    "ct-scan-vs-pet-scan-difference/index.html": {
        "title": "CT Scan vs PET Scan: What is the Difference? | Guide",
        "description": "Compare CT scan vs PET scan to understand their key differences in technology, uses, diagnostic accuracy, radiation risks, and pricing in Lucknow."
    },
    "government-hospital-ct-scan-price-vs-private-in-lucknow/index.html": {
        "title": "Government vs Private Hospital CT Scan Price in Lucknow",
        "description": "Compare CT scan prices between private and government hospitals in Lucknow. Find pricing for brain, chest, abdominal, and contrast CT scans."
    },
    "is-ct-scan-contrast-dangerous/index.html": {
        "title": "Is CT Scan Contrast Dangerous? Side Effects & Safety",
        "description": "Is CT scan contrast dangerous? Learn about the risks, common side effects, allergic reactions, and safety precautions for contrast CT scans."
    },
    "is-ct-scan-safe/index.html": {
        "title": "Is CT Scan Safe? Radiation Risks & Patient Safety Info",
        "description": "Is a CT scan safe? Understand the radiation dose, health risks, benefit-to-risk ratio, and precautions for pregnant patients and children."
    },
    "what-is-the-difference-between-mri-and-ct-scan/index.html": {
        "title": "MRI vs CT Scan: What is the Difference? | Safety Guide",
        "description": "Discover the difference between MRI and CT scan. Compare diagnostic accuracy, imaging technology, scan duration, safety profiles, and costs."
    }
}

def set_meta_tag(content, name, value):
    # Check if exists
    pattern = re.compile(rf'<meta\s+name="{name}"\s+content="[^"]*"[^>]*>', re.IGNORECASE)
    if pattern.search(content):
        # Replace
        return pattern.sub(f'<meta name="{name}" content="{value}">', content)
    else:
        # Insert after <head> or <title>
        title_pattern = re.compile(r'<title>.*?</title>', re.IGNORECASE)
        if title_pattern.search(content):
            return title_pattern.sub(lambda m: m.group(0) + f'\n<meta name="{name}" content="{value}">', content, count=1)
        else:
            return content.replace("<head>", f"<head>\n<meta name=\"{name}\" content=\"{value}\">", 1)

def set_og_tag(content, property_name, value):
    pattern = re.compile(rf'<meta\s+property="{property_name}"\s+content="[^"]*"[^>]*>', re.IGNORECASE)
    if pattern.search(content):
        return pattern.sub(f'<meta property="{property_name}" content="{value}">', content)
    else:
        title_pattern = re.compile(r'<title>.*?</title>', re.IGNORECASE)
        if title_pattern.search(content):
            return title_pattern.sub(lambda m: m.group(0) + f'\n<meta property="{property_name}" content="{value}">', content, count=1)
        else:
            return content.replace("<head>", f"<head>\n<meta property=\"{property_name}\" content=\"{value}\">", 1)

def optimize_metadata():
    for rel_path, meta in METADATA_MAP.items():
        filepath = os.path.join(PUBLIC_DIR, rel_path)
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Optimize title
        content = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', content)
        
        # Set meta tags (inserting if missing)
        content = set_meta_tag(content, "description", meta["description"])
        content = set_og_tag(content, "og:title", meta["title"])
        content = set_og_tag(content, "og:description", meta["description"])
        content = set_meta_tag(content, "twitter:title", meta["title"])
        content = set_meta_tag(content, "twitter:description", meta["description"])
        
        # Optimize Rank Math schema if exists
        schema_pattern = re.compile(r'<script type="application/ld\+json" class="rank-math-schema">.*?</script>', re.DOTALL)
        def replace_schema_meta(match):
            schema_text = match.group(0)
            schema_text = re.sub(r'"description":"[^"]*"', f'"description":"{meta["description"]}"', schema_text)
            schema_text = re.sub(r'"headline":"[^"]*"', f'"headline":"{meta["title"]}"', schema_text)
            schema_text = re.sub(r'"name":"[^"]*"', f'"name":"{meta["title"]}"', schema_text, count=1)
            return schema_text
            
        content = schema_pattern.sub(replace_schema_meta, content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Optimized metadata (robust) for: {rel_path}")

if __name__ == "__main__":
    optimize_metadata()
