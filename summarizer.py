from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

# =========================================================
# SUMMARIZATION MODEL
# =========================================================

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

print("Loading summarization model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Summarization model loaded.")


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# GENERATE SUMMARY
# =========================================================

def generate_summary(text, summary_length):

    if not text:
        return ""

    # -----------------------------------------------------
    # Clean input text
    # -----------------------------------------------------

    text = clean_text(text)

    if not text:
        return ""

    # -----------------------------------------------------
    # Select summary length
    # -----------------------------------------------------

    if summary_length == "Short":

        max_new_tokens = 100
        min_new_tokens = 25

    elif summary_length == "Medium":

        max_new_tokens = 180
        min_new_tokens = 40

    else:

        max_new_tokens = 280
        min_new_tokens = 60

    # -----------------------------------------------------
    # Tokenize input
    # -----------------------------------------------------

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    # -----------------------------------------------------
    # Generate summary
    # -----------------------------------------------------

    outputs = model.generate(
        **inputs,

        max_new_tokens=max_new_tokens,

        min_new_tokens=min_new_tokens,

        num_beams=4,

        do_sample=False,

        length_penalty=1.0,

        no_repeat_ngram_size=3,

        repetition_penalty=1.15
    )

    # -----------------------------------------------------
    # Decode summary
    # -----------------------------------------------------

    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    summary = summary.strip()

    # -----------------------------------------------------
    # Print result in terminal
    # -----------------------------------------------------

    print(
        "========== FINAL SUMMARY =========="
    )

    print(summary)

    print(
        "==================================="
    )

    return summary