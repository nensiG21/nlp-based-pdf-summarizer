import os

# =========================================================
# PADDLEPADDLE COMPATIBILITY FIX
# =========================================================
os.environ["FLAGS_enable_pir_api"] = "0"

import re
import cv2
import fitz
import numpy as np

from PIL import Image
from paddleocr import PaddleOCR

from summarizer import generate_summary


# =========================================================
# PADDLEOCR INITIALIZATION
# =========================================================
print("Loading PaddleOCR...")

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    text_det_limit_side_len=2000,
    text_det_limit_type="max",
    text_det_thresh=0.2,
    text_det_box_thresh=0.4,
    text_det_unclip_ratio=1.5,
    enable_mkldnn=False
)

print("PaddleOCR loaded successfully.")


# =========================================================
# CLEAN OCR TEXT
# =========================================================
def clean_ocr_text(text):

    if not text:
        return ""

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Normalize line breaks
    text = re.sub(
        r"\n{2,}",
        "\n",
        text
    )

    # Remove spaces before punctuation
    text = re.sub(
        r"\s+([.,!?;:])",
        r"\1",
        text
    )

    # Remove obvious OCR garbage
    text = re.sub(
        r"[|]{2,}",
        " ",
        text
    )

    # Remove isolated symbols
    text = re.sub(
        r"(?m)^\s*[+×÷|~_^]+\s*$",
        "",
        text
    )

    # Remove BloSum triplet prefix noise
    text = re.sub(
        r"<H>\s*<R>\s*<T>",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Remove repeated spaces again
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# CHECK OCR TEXT
# =========================================================
def is_meaningful_text(text):

    if not text:
        return False

    words = text.split()

    if len(words) < 5:
        return False

    alphabetic_chars = sum(
        c.isalpha()
        for c in text
    )

    return alphabetic_chars >= 20


# =========================================================
# OCR ONE IMAGE REGION
# =========================================================
def extract_image_ocr(image):

    if image is None:
        return "", None

    print(
        "========== PADDLEOCR STARTED =========="
    )

    # -----------------------------------------------------
    # RUN PADDLEOCR
    # -----------------------------------------------------
    results = ocr.predict(
        input=image
    )

    extracted_lines = []

    # -----------------------------------------------------
    # READ OCR RESULTS
    # -----------------------------------------------------
    for result in results:

        try:
            result_json = result.json

            if callable(result_json):
                result_json = result_json()

        except Exception as e:

            print(
                "Could not read PaddleOCR JSON:",
                e
            )

            continue

        if not isinstance(
            result_json,
            dict
        ):
            continue

        res = result_json.get(
            "res",
            result_json
        )

        if not isinstance(
            res,
            dict
        ):
            continue

        texts = res.get(
            "rec_texts",
            []
        )

        scores = res.get(
            "rec_scores",
            []
        )

        boxes = res.get(
            "rec_boxes",
            []
        )

        # -------------------------------------------------
        # COLLECT OCR TEXT
        # -------------------------------------------------
        for i, text in enumerate(texts):

            if not text:
                continue

            text = str(
                text
            ).strip()

            # ---------------------------------------------
            # CONFIDENCE
            # ---------------------------------------------
            score = 1.0

            if i < len(scores):

                try:
                    score = float(
                        scores[i]
                    )

                except:
                    score = 1.0

            if score < 0.35:
                continue

            # ---------------------------------------------
            # POSITION
            # ---------------------------------------------
            x_position = 0
            y_position = 0

            if i < len(boxes):

                try:

                    box = boxes[i]

                    x_position = (
                        float(box[0])
                        + float(box[2])
                    ) / 2

                    y_position = (
                        float(box[1])
                        + float(box[3])
                    ) / 2

                except:

                    x_position = 0
                    y_position = 0

            extracted_lines.append(
                (
                    x_position,
                    y_position,
                    text,
                    score
                )
            )

    # -----------------------------------------------------
    # SORT TOP TO BOTTOM
    # -----------------------------------------------------
    extracted_lines.sort(
        key=lambda x: (
            x[1],
            x[0]
        )
    )

    # -----------------------------------------------------
    # COMBINE OCR TEXT
    # -----------------------------------------------------
    extracted_text = "\n".join(
        item[2]
        for item in extracted_lines
    )

    extracted_text = clean_ocr_text(
        extracted_text
    )

    print(
        "========== PADDLEOCR FINISHED =========="
    )

    print(
        "OCR TEXT:"
    )

    print(
        extracted_text
    )

    print(
        "OCR WORDS:",
        len(
            extracted_text.split()
        )
    )

    # -----------------------------------------------------
    # RGB IMAGE
    # -----------------------------------------------------
    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return extracted_text, rgb


# =========================================================
# FIND MULTIPLE IMAGE REGIONS ON A PDF PAGE
# =========================================================
def detect_image_regions(page):

    print(
        "Detecting image regions..."
    )

    # -----------------------------------------------------
    # RENDER PAGE
    # -----------------------------------------------------
    pix = page.get_pixmap(
        dpi=250,
        alpha=False
    )

    image_bytes = pix.tobytes(
        "png"
    )

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    page_image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if page_image is None:
        return []

    height, width = page_image.shape[:2]

    # -----------------------------------------------------
    # GRAYSCALE
    # -----------------------------------------------------
    gray = cv2.cvtColor(
        page_image,
        cv2.COLOR_BGR2GRAY
    )

    # -----------------------------------------------------
    # FIND NON-WHITE CONTENT
    # -----------------------------------------------------
    _, threshold = cv2.threshold(
        gray,
        245,
        255,
        cv2.THRESH_BINARY_INV
    )

    # -----------------------------------------------------
    # REMOVE SMALL NOISE
    # -----------------------------------------------------
    kernel = np.ones(
        (15, 15),
        np.uint8
    )

    threshold = cv2.morphologyEx(
        threshold,
        cv2.MORPH_CLOSE,
        kernel
    )

    # -----------------------------------------------------
    # FIND CONTOURS
    # -----------------------------------------------------
    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    regions = []

    page_area = width * height

    for contour in contours:

        x, y, w, h = cv2.boundingRect(
            contour
        )

        area = w * h

        # Ignore very small objects
        if area < page_area * 0.01:
            continue

        # Ignore almost entire page
        if area > page_area * 0.90:
            continue

        # Ignore very small width/height
        if w < width * 0.10:
            continue

        if h < height * 0.05:
            continue

        regions.append(
            (
                x,
                y,
                w,
                h
            )
        )

    # -----------------------------------------------------
    # SORT TOP TO BOTTOM / LEFT TO RIGHT
    # -----------------------------------------------------
    regions.sort(
        key=lambda r: (
            r[1],
            r[0]
        )
    )

    # -----------------------------------------------------
    # MERGE OVERLAPPING REGIONS
    # -----------------------------------------------------
    merged = []

    for region in regions:

        x, y, w, h = region

        merged_region = False

        for i, existing in enumerate(merged):

            ex, ey, ew, eh = existing

            # Calculate intersection
            ix1 = max(
                x,
                ex
            )

            iy1 = max(
                y,
                ey
            )

            ix2 = min(
                x + w,
                ex + ew
            )

            iy2 = min(
                y + h,
                ey + eh
            )

            if ix2 > ix1 and iy2 > iy1:

                nx1 = min(
                    x,
                    ex
                )

                ny1 = min(
                    y,
                    ey
                )

                nx2 = max(
                    x + w,
                    ex + ew
                )

                ny2 = max(
                    y + h,
                    ey + eh
                )

                merged[i] = (
                    nx1,
                    ny1,
                    nx2 - nx1,
                    ny2 - ny1
                )

                merged_region = True

                break

        if not merged_region:

            merged.append(
                region
            )

    # -----------------------------------------------------
    # FINAL SORT
    # -----------------------------------------------------
    merged.sort(
        key=lambda r: (
            r[1],
            r[0]
        )
    )

    print(
        "Detected regions:",
        len(merged)
    )

    return [
        (
            page_image[
                y:y + h,
                x:x + w
            ]
        )
        for x, y, w, h in merged
    ]


# =========================================================
# IMAGE OCR + SUMMARY
# =========================================================
def extract_image_summaries(
    uploaded_file,
    summary_length
):

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.getvalue()

    if not pdf_bytes:
        return []

    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    output = []

    image_number = 1

    # =====================================================
    # PROCESS EACH PAGE
    # =====================================================
    for page_index in range(
        len(doc)
    ):

        print(
            f"Processing PDF page {page_index + 1}"
        )

        page = doc.load_page(
            page_index
        )

        # -------------------------------------------------
        # DETECT MULTIPLE REGIONS
        # -------------------------------------------------
        try:

            image_regions = detect_image_regions(
                page
            )

        except Exception as e:

            print(
                "Region detection error:",
                e
            )

            continue

        # -------------------------------------------------
        # PROCESS EACH IMAGE REGION
        # -------------------------------------------------
        for region_index, image in enumerate(
            image_regions,
            start=1
        ):

            print(
                f"Processing image {image_number} "
                f"from page {page_index + 1}"
            )

            # ---------------------------------------------
            # OCR
            # ---------------------------------------------
            try:

                extracted_text, rgb_image = (
                    extract_image_ocr(
                        image
                    )
                )

            except Exception as e:

                print(
                    "OCR error:",
                    e
                )

                continue

            # ---------------------------------------------
            # CHECK OCR
            # ---------------------------------------------
            if not is_meaningful_text(
                extracted_text
            ):

                print(
                    "OCR text is not meaningful."
                )

                continue

            # ---------------------------------------------
            # GENERATE SUMMARY
            # ---------------------------------------------
            try:

                print(
                    "Generating image summary..."
                )

                summary = generate_summary(
                    extracted_text,
                    summary_length
                )

                print(
                    "Image summary generated successfully."
                )

            except Exception as e:

                print(
                    "========== SUMMARY ERROR =========="
                )

                print(
                    type(e).__name__
                )

                print(
                    str(e)
                )

                print(
                    "==================================="
                )

                summary = ""

            # ---------------------------------------------
            # CREATE PIL IMAGE
            # ---------------------------------------------
            pil_image = Image.fromarray(
                rgb_image
            )

            # ---------------------------------------------
            # SAVE RESULT
            # ---------------------------------------------
            output.append(
                {
                    "image_no": image_number,
                    "page_no": page_index + 1,
                    "image": pil_image,
                    "ocr_text": extracted_text,
                    "summary": summary
                }
            )

            image_number += 1

    doc.close()

    uploaded_file.seek(0)

    print(
        "Image OCR processing completed."
    )

    print(
        "Total images processed:",
        len(output)
    )

    return output