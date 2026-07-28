import os
import re
import sys
from html.parser import HTMLParser

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

class SEOHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1_count = 0
        self.h1_tags = []
        self.images_total = 0
        self.images_missing_alt = []
        
        self.in_title = False
        self.in_head = True
        
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "body":
            self.in_head = False
            
        attrs_dict = dict(attrs)
        
        if tag == "title" and self.in_head:
            self.in_title = True
            
        elif tag == "meta" and self.in_head:
            name = attrs_dict.get("name", "").lower()
            if name == "description":
                self.description = attrs_dict.get("content", "")
                
        elif tag == "h1":
            self.h1_count += 1
            
        elif tag == "img":
            self.images_total += 1
            src = attrs_dict.get("src", "unknown")
            alt = attrs_dict.get("alt")
            # If alt is missing or empty
            if alt is None or not alt.strip():
                self.images_missing_alt.append(src)
                
    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data

def validate_seo_for_file(filepath):
    parser = SEOHTMLParser()
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()
    parser.feed(html_content)
    
    relative_path = os.path.relpath(filepath, PUBLIC_DIR)
    
    # Calculate score
    deductions = 0
    issues = []
    
    # Title checks
    title_len = len(parser.title.strip())
    if title_len == 0:
        deductions += 30
        issues.append("Missing <title> tag")
    elif title_len < 50 or title_len > 60:
        deductions += 10
        issues.append(f"Title length out of range (50-60): current is {title_len} chars ('{parser.title.strip()}')")
        
    # Description checks
    desc_len = len(parser.description.strip())
    if desc_len == 0:
        deductions += 30
        issues.append("Missing meta description")
    elif desc_len < 120 or desc_len > 160:
        deductions += 10
        issues.append(f"Meta description out of range (120-160): current is {desc_len} chars")
        
    # Heading checks
    if parser.h1_count == 0:
        deductions += 20
        issues.append("No H1 heading found")
    elif parser.h1_count > 1:
        deductions += 20
        issues.append(f"Multiple H1 headings found ({parser.h1_count})")
        
    # Image alt checks
    if parser.images_total > 0:
        missing_count = len(parser.images_missing_alt)
        if missing_count > 0:
            deductions += min(20, missing_count * 5)
            issues.append(f"{missing_count} out of {parser.images_total} images are missing alt text")
            for img_src in parser.images_missing_alt[:3]:
                issues.append(f"  - Missing alt for: {img_src}")
            if missing_count > 3:
                issues.append(f"  - ... and {missing_count - 3} more")
                
    score = max(0, 100 - deductions)
    return {
        "file": relative_path,
        "score": score,
        "issues": issues,
        "title": parser.title.strip(),
        "description": parser.description.strip(),
        "h1_count": parser.h1_count,
        "images_total": parser.images_total,
        "images_missing_alt_count": len(parser.images_missing_alt)
    }

def run_seo_validation():
    if not os.path.exists(PUBLIC_DIR):
        print(f"Public directory not found at {PUBLIC_DIR}")
        sys.exit(1)
        
    reports = []
    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                reports.append(validate_seo_for_file(filepath))
                
    # Sort reports by file name
    reports.sort(key=lambda r: r["file"])
    
    print("=" * 70)
    print("                    SEO VALIDATION REPORT")
    print("=" * 70)
    
    total_score = 0
    passed_count = 0
    
    for r in reports:
        print(f"\nFile: public/{r['file']}")
        print(f"Score: {r['score']}/100")
        total_score += r["score"]
        
        if r["score"] == 100:
            print("  ✓ All checks passed!")
            passed_count += 1
        else:
            for issue in r["issues"]:
                print(f"  ✗ {issue}")
                
    avg_score = total_score / len(reports) if reports else 0
    print("\n" + "=" * 70)
    print(f"OVERALL SUMMARY:")
    print(f"Total HTML pages scanned: {len(reports)}")
    print(f"Fully optimized pages (100/100): {passed_count}/{len(reports)}")
    print(f"Average SEO Score: {avg_score:.2f}/100")
    print("=" * 70)

if __name__ == "__main__":
    run_seo_validation()
