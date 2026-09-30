# from nltk.corpus import wordnet as wn

# def get_word_meanings(words):

#     meanings = []

#     for word in words:

#         synsets = wn.synsets(word)

#         if synsets:
#             definition = synsets[0].definition()
#         else:
#             definition = "Meaning not found"

#         meanings.append({
#             "word": word,
#             "meaning": definition
#         })

#     return meanings


# from nltk.corpus import wordnet as wn
# from nltk.tokenize import sent_tokenize

# def get_word_meanings(words, text):

#     meanings = []

#     sentences = sent_tokenize(text)

#     for word in words:

#         definition = None

#         # ---------- Try context from PDF ----------
#         matching_sentences = []

#         for sentence in sentences:

#             if word.lower() in sentence.lower():

#                 matching_sentences.append(sentence.strip())

#         # Use shortest relevant sentence
#         if matching_sentences:

#             definition = min(
#                 matching_sentences,
#                 key=len
#             )

#         # ---------- Fallback to WordNet ----------
#         else:

#             synsets = wn.synsets(word)

#             if synsets:

#                 definition = synsets[0].definition()

#             else:

#                 definition = "Meaning not found"

#         meanings.append({

#             "word": word,

#             "meaning": definition
#         })

#     return meanings




# from nltk.corpus import wordnet as wn
# from nltk.tokenize import sent_tokenize

# # ==================================================
# # WORD MEANING FUNCTION
# # ==================================================
# def get_word_meanings(words, text):

#     meanings = []

#     # -------- SPLIT INTO SENTENCES --------
#     sentences = sent_tokenize(text)

#     for word in words:

#         definition = None

#         # ==================================================
#         # TRY TO GET CONTEXT FROM PDF
#         # ==================================================
#         matching_sentences = []

#         for sentence in sentences:

#             if word.lower() in sentence.lower():

#                 matching_sentences.append(
#                     sentence.strip()
#                 )

#         # ==================================================
#         # USE SHORTEST RELEVANT SENTENCE
#         # ==================================================
#         if matching_sentences:

#             definition = min(

#                 matching_sentences,

#                 key=len
#             )

#         # ==================================================
#         # FALLBACK TO WORDNET
#         # ==================================================
#         else:

#             synsets = wn.synsets(word)

#             if synsets:

#                 definition = synsets[0].definition()

#             else:

#                 definition = "Meaning not found"

#         # ==================================================
#         # SHORTEN VERY LONG DEFINITIONS
#         # ==================================================
#         if len(definition) > 180:

#             definition = definition[:180] + "..."

#         # ==================================================
#         # STORE RESULT
#         # ==================================================
#         meanings.append({

#             "word": word,

#             "meaning": definition
#         })

#     return meanings



from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize

# ==================================================
# WORD MEANING FUNCTION
# ==================================================
def get_word_meanings(words, text):

    meanings = []

    sentences = sent_tokenize(text)

    for word in words:

        definition = None

        matching_sentences = []

        # ==================================================
        # FIND RELEVANT SENTENCES
        # ==================================================
        for sentence in sentences:

            clean_sentence = sentence.strip()

            # sentence contains word
            if word.lower() in clean_sentence.lower():

                # remove bad short headings
                if len(clean_sentence.split()) < 5:
                    continue

                # remove noisy titles
                if "experiment" in clean_sentence.lower():
                    continue

                if "theory" in clean_sentence.lower():
                    continue

                if "introduction" in clean_sentence.lower():
                    continue

                matching_sentences.append(
                    clean_sentence
                )

        # ==================================================
        # CHOOSE BEST SENTENCE
        # ==================================================
        if matching_sentences:

            # choose medium informative sentence
            definition = min(

                matching_sentences,

                key=lambda s: abs(len(s.split()) - 12)
            )

        # ==================================================
        # WORDNET FALLBACK
        # ==================================================
        else:

            synsets = wn.synsets(word)

            if synsets:

                definition = synsets[0].definition()

            else:

                definition = "Meaning not found"

        # ==================================================
        # SHORTEN VERY LONG TEXT
        # ==================================================
        if len(definition) > 180:

            definition = definition[:180] + "..."

        meanings.append({

            "word": word,

            "meaning": definition
        })

    return meanings