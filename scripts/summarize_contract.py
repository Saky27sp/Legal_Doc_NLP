from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import nltk
import fitz  # PyMuPDF

nltk.download('punkt')

# Load models and tokenizers
summarizer_tokenizer = T5Tokenizer.from_pretrained("SEBIS/legal_t5_small_summ_en", use_fast=False)
summarizer_model = T5ForConditionalGeneration.from_pretrained("SEBIS/legal_t5_small_summ_en")

bert_tokenizer = BertTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
bert_model = BertForSequenceClassification.from_pretrained("nlpaueb/legal-bert-base-uncased", num_labels=2)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_text(text):
    input_text = "summarize: " + text.strip().replace("\n", " ")
    input_ids = summarizer_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = summarizer_model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def detect_risky_clauses(text):
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text)
    risky_clauses = []
    for sentence in sentences:
        inputs = bert_tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)
        outputs = bert_model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
        if prediction == 1:
            clean = sentence.replace("\n", " ").strip()
            if len(clean.split()) > 4:  # Ignore short or fragment-like matches
                risky_clauses.append(clean)

    return risky_clauses

def extract_parties_and_obligations(text):
    words = text.split()
    raw_parties = [w.strip(",.():;-") for w in words if w.isupper() and len(w) > 3]

    # Common noise words to ignore
    stopwords = {
        'AGREEMENT', 'CONTRACT', 'ACTION', 'INFORMATION', 'COMPETITION',
        'OTHER', 'RESULT', 'PROPERTIES', 'PENALTIES', 'AND', 'OR', 'THE',
        'SHALL', 'THIS', 'SECTION', 'CLAUSE', 'SUBSECTION'
    }

    parties = [p for p in raw_parties if p not in stopwords and not p.isdigit()]

    # Optional: remove duplicates and sort
    parties = sorted(set(parties))

    obligations = "Obligation text placeholder. You can extract obligation logic here later."
    return parties, obligations


def generate(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(raw_text)
    risky_clauses = detect_risky_clauses(raw_text)
    parties, obligations = extract_parties_and_obligations(raw_text)
    return summary, risky_clauses, parties, obligations
