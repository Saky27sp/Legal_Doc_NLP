# Legal_Doc_NLP
# Contract Review and Legal Document Analysis Using NLP 🧠📄
LegalDocNLP is an NLP-powered system for automated legal contract analysis. It uses domain-specific transformer models (Legal-BERT and LegalT5) to identify, label, and summarize risky contractual clauses and extract key parties and obligations — all through a Flask-based web interface.

# 🔍 Features
* Extracts legal clauses from uploaded contracts
* Classifies risky clauses using Legal-BERT
* Labels each clause (e.g., Termination, Indemnity)
* Summarizes clauses using LegalT5
* Extracts parties and keyword contexts
* Displays all results in a structured web interface

# 🧭 Code Flow
→ app.py

│

├── Upload PDF → route: "/"

├── Process file using: summarize_contract.generate(pdf_path)

│

├── summarize_contract.py:

│ ├─ Uses Legal-BERT for clause classification

│ ├─ Applies rule-based clause labeling

│ ├─ Generates summaries using LegalT5

│

├── pdf_processor.py:

│ ├─ Extracts full text from PDF

│ ├─ Extracts keywords and their contextual windows

│

→ Results rendered in templates/results.html

# 📂 Code Breakdown
app.py

→ Flask web server that handles file upload, invokes summarization and renders results.

scripts/summarize_contract.py

→ Core NLP logic:

• Clause classification using Legal-BERT

• Clause labeling via keyword rules

• Clause summarization using LegalT5

• Party & obligation extraction

pdf_processor.py

→ PDF parsing using fitz (PyMuPDF)

→ Keyword frequency calculation

→ Context window extraction

templates/upload.html

→ Front-end file uploader

templates/results.html

→ Displays summary, risky clauses, keyword contexts

# 🛠️ Requirements
  Install dependencies:
  
  pip install -r requirements.txt
  
  Example contents of requirements.txt:
* flask
* transformers
* torch
* nltk
* fpdf
* pymupdf

# 🚀 How to Run
1. Clone the repo

    git clone https://github.com/your-username/Legal_Doc_NLP.git
    cd Legal_Doc_NLP

2. Install dependencies:

    pip install -r requirements.txt

3. Run the app:

    python app.py

4. Open in browser:
    http://127.0.0.1:5000/

# 📎 Sample Files Included
* SampleContract.pdf
* LegalDocNLP_Report.docx
* LegalDocNLP_BasePaper.docx
* LegalDocNLP_Presentation.pptx

# 🧠 Models Used
* Legal-BERT: For clause classification
* LegalT5: For abstractive clause summarization
* CUAD Dataset: Inspired the clause types

# 📌 Future Improvements
* OCR for scanned PDFs
* Clause comparison and templating
* Severity scoring for risks
* Export to structured JSON/PDF (optional)


