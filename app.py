import base64
import re
import streamlit as st
from nltk.tokenize import sent_tokenize

from abbreviation import extract_abbreviations
from citation_extractor import extract_citations
from export_pdf import summary_to_pdf
from image_summary import extract_image_summaries
from keyword_extractor import extract_keywords
from language_detector import detect_language
from ner_module import extract_entities
from pdf_extractor import extract_text_from_pdf
from readability import analyze_readability
from reference_extractor import extract_references
from summarizer import generate_summary
from translator import translate_text
from word_meaning import get_word_meanings

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI PDF NLP Summarizer",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("📄 AI PDF NLP Summarizer")

# Initialize Session State
if "summary" not in st.session_state:
    st.session_state.summary = None
if "image_results" not in st.session_state:
    st.session_state.image_results = None

# ==========================================
# HELPER FUNCTIONS & CACHING
# ==========================================
@st.cache_data(show_spinner=False)
def load_pdf_text(file_bytes):
    """Extract raw text from PDF bytes with caching."""
    return extract_text_from_pdf(file_bytes)

def clean_pdf_text(text: str) -> str:
    """Sanitize extracted text while preserving technical content."""
    text = re.sub(r'[^\w\s.,:;!?()\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ==========================================
# SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.title("⚙ Configuration")

summary_length = st.sidebar.selectbox(
    "Select Summary Length",
    ["Short", "Medium", "Long"]
)

languages = {
    "Hindi": "hi",
    "Marathi": "mr",
    "French": "fr",
    "German": "de"
}

language_name = st.sidebar.selectbox(
    "Translation Language",
    list(languages.keys())
)
language = languages[language_name]

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================
if uploaded_file is not None:
    col1, col2 = st.columns([1.1, 1])

    # Left Column: PDF Viewer
    with col1:
        st.subheader("📑 Uploaded PDF")
        file_bytes = uploaded_file.getvalue()
        base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
        
        pdf_display = f"""
            <iframe
                src="data:application/pdf;base64,{base64_pdf}#toolbar=1&zoom=page-width"
                width="100%"
                height="800px"
                style="border: none;">
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Right Column: Analysis Tabs
    with col2:

        # -----------------------------------------
        # Extract PDF text
        # -----------------------------------------
        raw_text = load_pdf_text(file_bytes)
        clean_text = clean_pdf_text(raw_text)

        # -----------------------------------------
        # Text extraction status
        # -----------------------------------------
        if clean_text:
            word_count = len(clean_text.split())
            st.success(
                f"✅ Text extracted successfully ({word_count:,} words)"
            )
            text_to_use = clean_text

            try:
                detected_lang = detect_language(raw_text)
                st.info(
                    f"🌍 Detected Language: **{detected_lang.upper()}**"
                )
            except Exception:
                detected_lang = "en"
        else:
            st.warning(
                "⚠️ No normal text was extracted. You can still use Image OCR."
            )
            text_to_use = ""
            detected_lang = "en"

        # -----------------------------------------
        # ALWAYS CREATE THE TABS
        # -----------------------------------------
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Summary & Translate",
            "Insights",
            "Keywords",
            "Text & Stats",
            "Citations",
            "References"
        ])

        # =================================================
        # TAB 1: SUMMARY & TRANSLATE
        # =================================================
        with tab1:

            if st.button("🚀 Generate Summary", type="primary"):

                # -----------------------------------------
                # Generate normal text summary
                # -----------------------------------------
                if text_to_use:
                    with st.spinner("⚡ Generating AI Summary..."):
                        try:
                            st.session_state.summary = generate_summary(
                                text_to_use, summary_length
                            )
                        except Exception as e:
                            st.error(f"❌ Summary Error: {e}")
                            st.session_state.summary = None
                else:
                    st.warning(
                        "⚠️ No document text is available for normal text summarization."
                    )

                # -----------------------------------------
                # ALWAYS TRY IMAGE OCR
                # -----------------------------------------
                with st.spinner("📷 Extracting images and running PaddleOCR..."):
                    try:
                        st.session_state.image_results = extract_image_summaries(
                            uploaded_file, summary_length
                        )
                    except Exception as e:
                        st.error(f"⚠️ Image OCR Error: {e}")
                        st.session_state.image_results = []

            # =================================================
            # DISPLAY NORMAL SUMMARY
            # =================================================
            if st.session_state.summary:
                st.success("✅ Summary Generated Successfully")
                st.subheader("📌 Summary")
                st.text_area(
                    "Summary Output",
                    st.session_state.summary,
                    height=220,
                    label_visibility="collapsed"
                )

            # =================================================
            # DISPLAY IMAGE OCR SUMMARY
            # =================================================
            st.subheader("🖼 Image OCR Summary")

            if st.session_state.image_results:
                for result in st.session_state.image_results:
                    st.divider()
                    st.markdown(f"#### 📷 Image {result['image_no']}")
                    st.image(result["image"], use_container_width=True)

                    with st.expander("📄 OCR Extracted Text"):
                        st.write(result["ocr_text"])

                    st.markdown("### 🤖 Image Summary")

                    # -----------------------------------------
                    # DIAGNOSTIC PRINT
                    # -----------------------------------------
                    print("========== UI SUMMARY ==========")
                    print(result["summary"])
                    print("===============================")

                    st.success(result["summary"])
            else:
                st.caption(
                    "No meaningful images with readable text found in this PDF."
                )

            # =================================================
            # DOWNLOAD NORMAL SUMMARY & TRANSLATION
            # =================================================
            if st.session_state.summary:
                pdf_file = summary_to_pdf(st.session_state.summary)
                st.download_button(
                    label="⬇ Download Summary PDF",
                    data=pdf_file,
                    file_name="summary.pdf",
                    mime="application/pdf"
                )

                st.subheader(f"🌍 Translated Summary ({language_name})")
                try:
                    translated = translate_text(st.session_state.summary, language)
                    st.text_area(
                        "Translated Output",
                        translated,
                        height=220,
                        label_visibility="collapsed"
                    )
                except Exception as e:
                    st.error(f"❌ Translation Error: {e}")

        # =================================================
        # TAB 2: INSIGHTS
        # =================================================
        with tab2:
            st.subheader("🔍 Named Entity Recognition")
            if clean_text:
                try:
                    entities = extract_entities(clean_text)
                    if entities:
                        for e in entities:
                            st.write(f"• **{e['text']}** → `{e['label']}`")
                    else:
                        st.info("No entities found.")
                except Exception as e:
                    st.error(f"NER Error: {e}")
            else:
                st.info("No text available for NER.")

            st.subheader("📖 Abbreviations")
            if raw_text:
                try:
                    abrv = extract_abbreviations(raw_text)
                    if abrv:
                        for a in abrv:
                            st.write(f"• **{a['short']}** → {a['long']}")
                    else:
                        st.info("No abbreviations found.")
                except Exception as e:
                    st.error(f"Abbreviation Error: {e}")
            else:
                st.info("No text available.")

        # =================================================
        # TAB 3: KEYWORDS
        # =================================================
        with tab3:
            st.subheader("🔑 Key Phrases")
            if raw_text:
                try:
                    keywords = extract_keywords(raw_text)
                    if keywords:
                        st.write(", ".join([f"`{kw}`" for kw in keywords]))

                        st.subheader("📘 Word Meanings")
                        meanings = get_word_meanings(keywords, raw_text)
                        if meanings:
                            for m in meanings:
                                st.write(f"• **{m['word']}**: {m['meaning']}")
                        else:
                            st.info("No definitions found.")
                    else:
                        st.info("No keywords found.")
                except Exception as e:
                    st.error(f"Keyword Error: {e}")
            else:
                st.info("No text available for keywords.")

        # =================================================
        # TAB 4: TEXT & STATS
        # =================================================
        with tab4:
            colA, colB = st.columns(2)

            with colA:
                st.subheader("📊 Statistics")
                if raw_text:
                    try:
                        sentences = sent_tokenize(raw_text)
                        st.metric("Total Sentences", len(sentences))
                        st.metric("Total Words", len(raw_text.split()))
                    except Exception as e:
                        st.error(f"Statistics Error: {e}")
                else:
                    st.info("No text available.")

            with colB:
                st.subheader("📚 Readability")
                if raw_text:
                    try:
                        score, level = analyze_readability(raw_text)
                        st.metric("Readability Score", score)
                        st.metric("Grade Level", level)
                    except Exception as e:
                        st.error(f"Readability Error: {e}")
                else:
                    st.info("No text available.")

            st.subheader("📄 Full Extracted Text")
            st.text_area(
                "Extracted Text",
                raw_text,
                height=300,
                label_visibility="collapsed"
            )

        # =================================================
        # TAB 5: CITATIONS
        # =================================================
        with tab5:
            st.subheader("📌 Extracted Citations")
            if raw_text:
                try:
                    citations = extract_citations(raw_text)
                    if citations:
                        for citation in citations:
                            st.write(f"• {citation}")
                    else:
                        st.info("No inline citations detected.")
                except Exception as e:
                    st.error(f"Citation Error: {e}")
            else:
                st.info("No text available.")

        # =================================================
        # TAB 6: REFERENCES
        # =================================================
        with tab6:
            st.subheader("📚 Extracted References")
            if raw_text:
                try:
                    refs = extract_references(raw_text)
                    if refs:
                        for ref in refs:
                            st.write(f"• {ref}")
                    else:
                        st.info("No reference section entries detected.")
                except Exception as e:
                    st.error(f"Reference Error: {e}")
            else:
                st.info("No text available.")
else:
    st.info("👈 Upload a PDF file from the sidebar to begin analysis.")