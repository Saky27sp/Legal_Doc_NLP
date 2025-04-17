import fitz  # PyMuPDF
from collections import Counter, defaultdict
import re

def extract_keywords_contexts(pdf_path, top_n=5, window=40):
    doc = fitz.open(pdf_path)
    keyword_counts = Counter()
    keyword_contexts = defaultdict(list)

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        keyword_counts.update(words)

    stopwords = set([
        'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'for', 'with', 'as',
        'on', 'at', 'by', 'an', 'be', 'this', 'are', 'from', 'or', 'it', 'was',
        'which', 'we', 'not', 'can', 'has', 'have', 'will', 'may', 'shall'
    ])

    for word in list(keyword_counts):
        if word in stopwords or len(word) < 3:
            del keyword_counts[word]

    top_keywords = keyword_counts.most_common(top_n)

    for keyword, _ in top_keywords:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text().lower()
            matches = [m.start() for m in re.finditer(r'\b{}\b'.format(re.escape(keyword)), text)]
            for match in matches:
                start = max(0, match - window)
                end = min(len(text), match + window)
                context = text[start:end]
                cleaned_context = re.sub(r'\s+', ' ', context).strip()
                keyword_contexts[keyword].append({
                    'page': page_num,
                    'context': cleaned_context
                })

    structured_output = []
    for keyword, occurrences in keyword_contexts.items():
        structured_output.append({
            'keyword': keyword,
            'occurrences': occurrences
        })

    return structured_output
