import pdfplumber
import spacy
import re
from fuzzywuzzy import fuzz

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define skill keywords (expand as needed)
SKILLS = ["Python", "Machine Learning", "C++", "Java", "Deep Learning", "SQL", "TensorFlow", "NLP"]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to extract key details
def extract_resume_details(text):
    doc = nlp(text)
    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone = re.search(r"\+?\d[\d -]{8,}\d", text)
    
    extracted_skills = [skill for skill in SKILLS if any(fuzz.partial_ratio(skill, token.text) > 80 for token in doc)]
    
    return {
        "name": doc.ents[0].text if doc.ents else "Unknown",
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0) if phone else "Not found",
        "skills": extracted_skills
    }

# Test with a sample resume
resume_text = extract_text_from_pdf("resume.pdf")
details = extract_resume_details(resume_text)
print(details)
