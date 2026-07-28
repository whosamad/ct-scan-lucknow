import os

INDEX_PATH = "/Users/samad/GITHUB SITES/ctscan-static/public/index.html"

FAQ_SCHEMA = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Are CT scans safe?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "CT scans are generally safe and effective. The radiation exposure is minimal and carefully monitored to ensure patient safety."
      }
    },
    {
      "@type": "Question",
      "name": "How do I prepare for a CT scan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Preparation varies based on the type of CT scan. For abdominal scans, fasting for 4-6 hours is often recommended. Specific instructions will be provided at the time of booking."
      }
    },
    {
      "@type": "Question",
      "name": "How long does a CT scan take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most CT scans take about 10-30 minutes. The duration depends on the area being scanned and whether a contrast dye is used."
      }
    },
    {
      "@type": "Question",
      "name": "What is the cost of a CT scan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "CT scans start at ₹1500. Contact us for detailed pricing and any ongoing offers or packages."
      }
    },
    {
      "@type": "Question",
      "name": "Can I get a CT scan without a doctor’s referral?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, you can book a CT scan without a referral. For specialized scans involving contrast dye, additional precautions may apply. Contact us for assistance."
      }
    }
  ]
}
</script>
"""

def inject_faq_schema():
    if not os.path.exists(INDEX_PATH):
        print("index.html not found!")
        return
        
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "FAQPage" in content:
        print("FAQPage schema already exists in index.html.")
        return
        
    if "</head>" in content:
        content = content.replace("</head>", f"{FAQ_SCHEMA}\n</head>", 1)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully injected FAQPage schema to homepage.")
    else:
        print("Could not find </head> tag to insert schema.")

if __name__ == "__main__":
    inject_faq_schema()
