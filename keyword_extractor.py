import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, num_keywords=10):

    doc = nlp(text)

    keywords = []

    ignore_words = ["page"]

    for token in doc:

        if (
            token.pos_ in ["NOUN", "PROPN"] 
            and not token.is_stop
            and token.text.lower() not in ignore_words
            and len(token.text) > 2
        ):
            keywords.append(token.text.lower())

    keyword_freq = Counter(keywords)

    return [word for word, freq in keyword_freq.most_common(num_keywords)]