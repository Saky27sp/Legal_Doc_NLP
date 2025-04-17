# scripts/classify_clauses.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the pre-trained Legal-BERT model
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("nlpaueb/legal-bert-base-uncased", num_labels=10)  # Adjust num_labels as per your classification needs

# Define your clause labels
LABELS = [
    "Confidentiality",
    "Indemnity",
    "Termination",
    "Payment Terms",
    "Governing Law",
    "Intellectual Property",
    "Arbitration",
    "Exclusivity",
    "Non-compete",
    "Other"
]

def classify_clause(clause_text):
    inputs = tokenizer(clause_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    return LABELS[predicted_class_id]

def predict(clauses):
    return [(clause, classify_clause(clause)) for clause in clauses]
