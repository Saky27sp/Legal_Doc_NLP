import spacy
import re
nlp = spacy.load("en_core_web_sm")

def parse(clauses):
    obligations = []
    for clause in clauses:
        if "shall" in clause or "must" in clause or "agrees to" in clause:
            doc = nlp(clause)
            parties = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON"]]
            obligations.append({
                "clause": clause,
                "parties": parties,
                "obligation": clause
            })
    return obligations
