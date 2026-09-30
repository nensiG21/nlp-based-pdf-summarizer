import textstat

def analyze_readability(text):

    score = textstat.flesch_reading_ease(text)

    if score >= 90:
        level = "Very Easy"
    elif score >= 70:
        level = "Easy"
    elif score >= 50:
        level = "Medium"
    elif score >= 30:
        level = "Difficult"
    else:
        level = "Very Difficult"

    return score, level