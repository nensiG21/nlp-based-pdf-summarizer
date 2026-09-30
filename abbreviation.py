import re

def extract_abbreviations(text):

    abbreviations = []

    # normalize dash characters
    text = text.replace("–", " ")
    text = text.replace("-", " ")

    text = re.sub(r'\s+', ' ', text)

    # Pattern 1: ABC (Full Form)
    pattern1 = r'\b([A-Z]{2,})\s*\(([A-Za-z ]{3,})\)'

    # Pattern 2: Full Form (ABC)
    pattern2 = r'([A-Za-z ]{3,})\s*\(([A-Z]{2,})\)'

    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)

    for short, full in matches1:
        abbreviations.append({
            "short": short.strip(),
            "long": full.strip()
        })

    for full, short in matches2:
        abbreviations.append({
            "short": short.strip(),
            "long": full.strip()
        })

    return abbreviations