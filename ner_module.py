# import spacy
# import re

# # load spacy model (more stable than transformer for PDFs)
# nlp = spacy.load("en_core_web_sm")

# # ---------------- CLEAN ----------------
# def clean_text(text):
#     text = re.sub(r'\s+', ' ', text)
#     text = re.sub(r'[^a-zA-Z0-9 .,]', ' ', text)
#     return text.strip()

# # ---------------- MAIN ----------------
# def extract_entities(text):

#     text = clean_text(text[:3000])   # limit + clean

#     doc = nlp(text)

#     entities = []
#     seen = set()

#     allowed = {"PERSON", "ORG", "GPE"}

#     for ent in doc.ents:
#         word = ent.text.strip()

#         # ❌ remove junk
#         if len(word) < 3:
#             continue
#         if not any(c.isalpha() for c in word):
#             continue

#         label = ent.label_

#         if label not in allowed:
#             continue

#         key = (word.lower(), label)
#         if key in seen:
#             continue
#         seen.add(key)

#         entities.append({
#             "text": word,
#             "label": label
#         })

#     return entities


import spacy
import re

# ---------------- LOAD MODEL ----------------
nlp = spacy.load("en_core_web_sm")

# ---------------- CLEAN TEXT ----------------
def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(
        r'[^a-zA-Z0-9 .,]',
        ' ',
        text
    )

    return text.strip()

# ---------------- STOP WORDS ----------------
IGNORE_WORDS = {

    "page",
    "figure",
    "table",
    "section",
    "introduction",
    "conclusion",
    "references",
    "paper",
    "study",
    "research",
    "method",
    "result",
    "author",
    "university",
    "supports",
    "secure",
    "sender"
}

# ---------------- MAIN FUNCTION ----------------
def extract_entities(text):

    # -------- CLEAN + LIMIT --------
    text = clean_text(text[:3000])

    doc = nlp(text)

    entities = []

    seen = set()

    allowed = {

        "PERSON",

        "ORG",

        "GPE"
    }

    for ent in doc.ents:

        word = ent.text.strip()

        label = ent.label_

        # -------- REMOVE JUNK --------
        if len(word) < 3:
            continue

        if word.lower() in IGNORE_WORDS:
            continue

        if not any(c.isalpha() for c in word):
            continue

        if label not in allowed:
            continue

        # -------- REMOVE TOO LONG TERMS --------
        if len(word.split()) > 5:
            continue

        # -------- REMOVE DUPLICATES --------
        key = (word.lower(), label)

        if key in seen:
            continue

        seen.add(key)

        entities.append({

            "text": word,

            "label": label
        })

    return entities