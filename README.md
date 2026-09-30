# 📄 NLP-Based PDF Summarizer

An NLP-based PDF summarization and analysis application built using Python and Streamlit.

The application allows users to upload PDF documents and perform multiple NLP-based analysis tasks such as AI-powered summarization, keyword extraction, Named Entity Recognition, language detection, translation, readability analysis, citation extraction, reference extraction, and image-based OCR analysis.

---

## 🚀 Overview

Reading and understanding long PDF documents can be time-consuming, especially for research papers, technical documents, reports, and academic material.

The **NLP-Based PDF Summarizer** provides an interactive interface where users can upload a PDF and analyze its content using Natural Language Processing and OCR techniques.

The application extracts text from the uploaded PDF, processes the extracted content, generates an AI-based summary, and provides additional insights about the document.

It also supports image-based text extraction using OCR for PDFs containing meaningful images or scanned content.

---

## ✨ Features

### 📄 1. PDF Text Extraction

The application extracts text directly from PDF documents.

It uses PyMuPDF to open the PDF and extract text from each page.

The extracted text is cleaned before being passed to the NLP processing modules.

---

### 🤖 2. AI-Based PDF Summarization

The application generates an automatic summary of the extracted PDF content.

The summarization module uses the Hugging Face:

`sshleifer/distilbart-cnn-12-6`

model for sequence-to-sequence summarization.

Users can select:

- Short
- Medium
- Long

summary lengths.

The application adjusts the generated token range according to the selected summary length.

---

### 📷 3. Image OCR and Image Summarization

The application can detect meaningful image regions inside PDF pages.

It uses:

- PaddleOCR
- OpenCV
- PyMuPDF
- PIL

to process images and extract text.

The extracted OCR text is then passed to the summarization module to generate an image-based summary.

This makes the application useful for PDFs containing diagrams, screenshots, scanned content, or images containing readable text.

---

### 🧠 4. Named Entity Recognition

The application performs Named Entity Recognition using spaCy.

It extracts entities such as:

- PERSON
- ORG
- GPE

The extracted entities are displayed along with their entity labels.

---

### 🔤 5. Abbreviation Extraction

The application identifies abbreviations and their corresponding full forms.

It supports patterns such as:

`ABC (Full Form)`

and:

`Full Form (ABC)`

The extracted abbreviations are displayed in the Insights section.

---

### 🔑 6. Keyword Extraction

The application extracts important keywords from the PDF.

spaCy is used for linguistic processing and noun/proper-noun based keyword extraction.

The system filters stop words and irrelevant terms and returns frequently occurring keywords.

---

### 📖 7. Word Meaning / Context Analysis

The application provides meanings for extracted keywords.

It first attempts to identify relevant sentences from the uploaded document containing the keyword.

If suitable contextual information is unavailable, WordNet is used as a fallback for word definitions.

---

### 🌍 8. Language Detection

The application automatically detects the language of the extracted PDF text.

The `langdetect` library is used for language detection.

The detected language is displayed in the application.

---

### 🌐 9. Translation

The generated summary can be translated into different languages.

Currently supported translation options include:

- Hindi
- Marathi
- French
- German

Translation is performed using `deep-translator` and Google Translator.

---

### 📊 10. Text Statistics

The application provides basic document statistics such as:

- Total number of sentences
- Total number of words

NLTK sentence tokenization is used for sentence-level analysis.

---

### 📚 11. Readability Analysis

The application calculates a readability score using the Flesch Reading Ease metric.

The result is classified into levels such as:

- Very Easy
- Easy
- Medium
- Difficult
- Very Difficult

---

### 📌 12. Citation Extraction

The application detects citations from the extracted PDF text.

It supports patterns including:

- IEEE-style citations

`[1]`

- Author-year citations

`(Smith, 2024)`

- Multiple-author citations

`(Smith et al., 2023)`

- DOI patterns

This helps users identify citations present within academic documents.

---

### 📑 13. Reference Extraction

The application attempts to identify the reference section of a document.

It supports reference headings such as:

- REFERENCES
- References
- BIBLIOGRAPHY
- Bibliography
- WORKS CITED
- Works Cited

It supports extraction of IEEE-style references and author-year style references.

---

### 📥 14. Download Summary as PDF

Users can download the generated summary as a PDF file.

The application uses ReportLab to create the downloadable summary document.

---

## 🖥️ Application Interface

The application provides the following main sections:

1. **Summary & Translate**
2. **Insights**
3. **Keywords**
4. **Text & Stats**
5. **Citations**
6. **References**

The application also provides a sidebar where users can:

- Select summary length
- Select translation language
- Upload a PDF

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    │    Uploads PDF      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Streamlit      │
                    │       app.py        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ PDF Text         │        │ Image Detection  │
       │ Extraction       │        │ + OCR            │
       │                  │        │                  │
       │ pdf_extractor.py │        │ image_summary.py │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └────────────┬──────────────┘
                             │
                             ▼
                   ┌─────────────────────┐
                   │  Text Processing    │
                   └──────────┬──────────┘
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Summarizer  │    │ NER         │    │ Keywords    │
   │             │    │             │    │             │
   │ Transformers│    │ spaCy       │    │ spaCy       │
   └─────────────┘    └─────────────┘    └─────────────┘
          │
          ├──────────────► Translation
          │
          ├──────────────► Readability
          │
          ├──────────────► Citations
          │
          ├──────────────► References
          │
          └──────────────► PDF Export



nlp-based-pdf-summarizer/
│
├── app.py
│
├── abbreviation.py
├── citation_extractor.py
├── export_pdf.py
├── image_summary.py
├── keyword_extractor.py
├── language_detector.py
├── ner_module.py
├── pdf_extractor.py
├── preprocessing.py
├── readability.py
├── reference_extractor.py
├── summarizer.py
├── translator.py
├── word_meaning.py
│
├── .agents/
│   └── skills/
│
├── .gitignore
└── requirements.txt


Installation
1. Clone the Repository
git clone https://github.com/nensiG21/nlp-based-pdf-summarizer.git

Move into the project directory:

cd nlp-based-pdf-summarizer
2. Create a Virtual Environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Install the spaCy English Model

The project uses:

en_core_web_sm

Install it using:

python -m spacy download en_core_web_sm
5. Download Required NLTK Resources

The application uses NLTK functionality for sentence tokenization and WordNet-based word meanings.

Make sure the required NLTK resources are available in your environment.

▶️ Run the Application

Start the Streamlit application using:

streamlit run app.py

The application will open in your browser.

📖 How to Use
Step 1

Launch the Streamlit application.

Step 2

Upload a PDF using the sidebar.

Step 3

Select the desired summary length:

Short
Medium
Long
Step 4

Click:

Generate Summary

Step 5

Explore the generated results through the available tabs:

Summary & Translate
Insights
Keywords
Text & Stats
Citations
References
Step 6

Download the generated summary as a PDF if required.

🔄 Application Workflow
PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Cleaning
    ↓
Language Detection
    ↓
       ┌─────────────────────────────┐
       │                             │
       ▼                             ▼
Normal PDF Text                Image Regions
       │                             │
       ▼                             ▼
NLP Processing                  PaddleOCR
       │                             │
       └──────────────┬──────────────┘
                      │
                      ▼
              Content Analysis
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
   Summary          Keywords        NER
       │
       ├── Translation
       ├── Readability
       ├── Citations
       ├── References
       └── PDF Export
🧩 Individual Modules
File	Purpose
app.py	Main Streamlit application
pdf_extractor.py	Extracts and cleans text from PDFs
summarizer.py	Generates AI-based summaries
image_summary.py	Detects image regions, performs OCR and summarizes image text
ner_module.py	Performs Named Entity Recognition
keyword_extractor.py	Extracts important keywords
abbreviation.py	Extracts abbreviations and full forms
language_detector.py	Detects document language
translator.py	Translates generated summaries
readability.py	Calculates readability score
citation_extractor.py	Extracts citation patterns
reference_extractor.py	Extracts reference entries
word_meaning.py	Provides contextual/fallback word meanings
export_pdf.py	Generates downloadable summary PDFs
preprocessing.py	Performs text preprocessing
