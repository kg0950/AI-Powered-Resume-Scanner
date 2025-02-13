from flask import Flask, request, jsonify
import pdfplumber
import spacy
import os
from fuzzywuzzy import fuzz
from werkzeug.utils import secure_filename
from transformers import pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Load NLP models
nlp = spacy.load("en_core_web_sm")
classifier = pipeline("zero-shot-classification")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Skills list (expandable)
SKILLS = ["Python", "Machine Learning", "C++", "Java", "Deep Learning", "SQL", "TensorFlow", "NLP"]

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def extract_resume_details(text):
    doc = nlp(text)
    extracted_skills = [skill for skill in SKILLS if any(fuzz.partial_ratio(skill, token.text) > 80 for token in doc)]
    return {"skills": extracted_skills}

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    text = extract_text_from_pdf(filepath)
    resume_data = extract_resume_details(text)
    return jsonify(resume_data)

@app.route('/match', methods=['POST'])
def match_resume():
    data = request.json
    job_description = data.get("job_description", "")
    resume_skills = data.get("skills", [])
    result = classifier(job_description, resume_skills)
    return jsonify({"match_scores": result})

if __name__ == '__main__':
    app.run(debug=True)
