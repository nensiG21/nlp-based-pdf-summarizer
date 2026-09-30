import re

def extract_citations(text):

    citations = set()

    # -------- IEEE Style --------
    # [1], [2], [15]
    ieee_pattern = r'\[\d+\]'

    # -------- Author-Year Style --------
    # (Smith, 2024)
    author_year_pattern = r'\([A-Za-z]+,\s?\d{4}\)'

    # -------- Multiple Authors --------
    # (Smith et al., 2023)
    etal_pattern = r'\([A-Za-z]+\set\sal\.,\s?\d{4}\)'

    # -------- DOI Pattern --------
    doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'

    patterns = [

        ieee_pattern,

        author_year_pattern,

        etal_pattern,

        doi_pattern
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        citations.update(matches)

    return sorted(citations)