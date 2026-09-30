import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialize tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    # -------- STEP 1: Remove code-like symbols --------
    text = re.sub(r'[#{}()_=<>/\\]', ' ', text)

    # Remove numbers
    text = re.sub(r'\d+', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # -------- STEP 2: Tokenization --------
    words = word_tokenize(text)

    cleaned_words = []

    for word in words:
        word = word.lower()

        # Keep only meaningful words
        if word.isalpha() and word not in stop_words and len(word) > 2:
            lemma = lemmatizer.lemmatize(word)
            cleaned_words.append(lemma)

    # -------- STEP 3: Join back --------
    processed_text = " ".join(cleaned_words)

    return processed_text