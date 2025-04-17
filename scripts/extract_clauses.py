import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def segment_clauses(text):
    # Simple segmentation by paragraph or sentence
    paragraphs = text.split('\n\n')
    clauses = [p.strip() for p in paragraphs if len(p.strip()) > 30]
    return clauses
