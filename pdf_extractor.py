import re
import fitz


# =================================================
# CLEAN PDF TEXT
# =================================================

def clean_pdf_text(text):

    if not text:
        return ""

    # Remove page markers
    text = re.sub(
        r"-*\s*Page\s*\d+\s*-*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove dashed lines
    text = re.sub(
        r"-{2,}",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =================================================
# EXTRACT NORMAL TEXT FROM PDF
# =================================================

def extract_text_from_pdf(file_bytes):

    if not file_bytes:
        return ""

    try:

        # Open PDF directly from bytes
        doc = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        all_text = []

        # -----------------------------------------
        # Extract normal PDF text
        # -----------------------------------------

        for page_number in range(
            len(doc)
        ):

            page = doc.load_page(
                page_number
            )

            text = page.get_text(
                "text"
            )

            if text:

                all_text.append(
                    text
                )

        doc.close()

        # -----------------------------------------
        # Combine text
        # -----------------------------------------

        final_text = "\n".join(
            all_text
        )

        # -----------------------------------------
        # Clean text
        # -----------------------------------------

        final_text = clean_pdf_text(
            final_text
        )

        print(
            "Normal PDF text extraction completed."
        )

        print(
            "Extracted words:",
            len(final_text.split())
        )

        return final_text

    except Exception as e:

        print(
            "PDF extraction error:",
            e
        )

        return ""