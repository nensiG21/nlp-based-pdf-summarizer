from langdetect import detect

def detect_language(text):

    try:
        language = detect(text)
    except:
        language = "unknown"

    return language