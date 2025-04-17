from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pdf_processor import extract_keywords_contexts
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from summarize_contract import generate

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "No file part"
        file = request.files['pdf_file']
        if file.filename == '':
            return "No selected file"
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process PDF
        summary, risky_clauses, parties, obligations = generate(filepath)
        keyword_contexts = extract_keywords_contexts(filepath)

        return render_template('results.html',
                               summary=summary,
                               risky_clauses=risky_clauses,
                               parties=sorted(set(parties)),
                               obligations=obligations,
                               keyword_contexts=keyword_contexts)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
