import re


# ==================================================
# EXTRACT REFERENCES
# ==================================================
def extract_references(text):

    if not text:
        return []

    # ==================================================
    # FIND REFERENCE SECTION
    # ==================================================
    patterns = [
        r'\bREFERENCES\b',
        r'\bReferences\b',
        r'\bBIBLIOGRAPHY\b',
        r'\bBibliography\b',
        r'\bWORKS CITED\b',
        r'\bWorks Cited\b'
    ]

    reference_start = None

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            reference_start = match.end()
            break

    # ==================================================
    # NO REFERENCES FOUND
    # ==================================================
    if reference_start is None:
        return []

    reference_text = text[reference_start:]

    # ==================================================
    # REMOVE COMMON PAGE ARTIFACTS
    # ==================================================
    reference_text = re.sub(
        r'\n?\s*\d+\s*\n',
        '\n',
        reference_text
    )

    # ==================================================
    # NORMALIZE WHITESPACE
    # ==================================================
    reference_text = re.sub(
        r'[ \t]+',
        ' ',
        reference_text
    )

    reference_text = re.sub(
        r'\n{2,}',
        '\n',
        reference_text
    )

    reference_text = reference_text.strip()

    if not reference_text:
        return []

    # ==================================================
    # 1. IEEE STYLE REFERENCES
    # Example:
    # [1] Author...
    # [2] Author...
    # ==================================================
    ieee_refs = re.findall(
        r'(?:^|\n)\s*\[\d+\]\s*(.*?)(?=\n\s*\[\d+\]|\Z)',
        reference_text,
        re.DOTALL
    )

    # ==================================================
    # 2. AUTHOR + YEAR STYLE
    #
    # Example:
    # Harsh Agrawal, Peter Anderson, ...
    # 2019. nocaps: novel object captioning...
    # ==================================================

    year_pattern = re.compile(
        r'(?P<authors>'
        r'[A-Z][A-Za-zÀ-ÿ\'\-]+'
        r'(?:\s+[A-Z][A-Za-zÀ-ÿ\'\-]+)*'
        r'(?:,\s*|\s+and\s+)'
        r'.*?'
        r')'
        r'(?P<year>'
        r'\b(?:19|20)\d{2}\b'
        r')'
        r'\.\s*'
        r'(?P<title>.*?)(?='
        r'\n\s*[A-Z][A-Za-zÀ-ÿ\'\-]+'
        r'(?:\s+[A-Z][A-Za-zÀ-ÿ\'\-]+)*'
        r'(?:,|\s+and\s+)'
        r'.*?\b(?:19|20)\d{2}\b\.'
        r'|\Z'
        r')',
        re.DOTALL
    )

    author_year_refs = []

    for match in year_pattern.finditer(reference_text):

        ref = match.group(0)

        ref = re.sub(
            r'\s+',
            ' ',
            ref
        ).strip()

        if len(ref) > 40:
            author_year_refs.append(ref)

    # ==================================================
    # 3. FALLBACK: SPLIT USING YEAR
    # ==================================================

    if not author_year_refs:

        year_positions = list(
            re.finditer(
                r'\b(?:19|20)\d{2}\.',
                reference_text
            )
        )

        for i, match in enumerate(year_positions):

            if i == 0:
                start = 0
            else:
                start = year_positions[i - 1].end()

            end = (
                year_positions[i + 1].start()
                if i + 1 < len(year_positions)
                else len(reference_text)
            )

            ref = reference_text[start:end]

            ref = re.sub(
                r'\s+',
                ' ',
                ref
            ).strip()

            if len(ref) > 40:
                author_year_refs.append(ref)

    # ==================================================
    # COMBINE ALL REFERENCE TYPES
    # ==================================================
    all_refs = []

    all_refs.extend(ieee_refs)
    all_refs.extend(author_year_refs)

    # ==================================================
    # CLEAN REFERENCES
    # ==================================================
    cleaned_refs = []

    for ref in all_refs:

        ref = re.sub(
            r'\s+',
            ' ',
            ref
        ).strip()

        ref = re.sub(
            r'^[\-\•\*]\s*',
            '',
            ref
        )

        if len(ref) > 25:
            cleaned_refs.append(ref)

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================
    unique_refs = []

    seen = set()

    for ref in cleaned_refs:

        key = ref.lower()

        if key not in seen:

            seen.add(key)

            unique_refs.append(ref)

    # ==================================================
    # RETURN REFERENCES
    # ==================================================
    return unique_refs[:50]