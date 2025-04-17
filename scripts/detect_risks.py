RISKY_CLAUSES = [
    'Exclusivity Clause',
    'Penalty / Liquidated Damages',
    'Non-compete / Non-solicit',
    'Termination for Convenience',
]

def find(classified_clauses):
    risky = []
    for clause, label in classified_clauses:
        if label in RISKY_CLAUSES:
            risky.append((clause, label))
    return risky
