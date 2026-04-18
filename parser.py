import pdfplumber
import re

def parse_resume(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    lines = text.strip().split('\n')
    
    skip_words = ["curriculum", "vitae", "resume", "cv", "curriculum vitae"]
    name = "Not Found"
    for line in lines:
        clean = line.strip().lower()
        if clean and not any(word in clean for word in skip_words):
            name = line.strip()
            break

    email = re.findall(r'[\w.-]+@[\w.-]+', text)
    email = email[0] if email else "Not Found"

    phone = re.findall(r'[\+\(]?[1-9][0-9\s\-\(\)]{7,}[0-9]', text)
    phone = phone[0] if phone else "Not Found"

    skills_list = [
        "Python", "Java", "JavaScript", "SQL", "React",
        "Machine Learning", "Excel", "Communication",
        "Leadership", "TensorFlow", "Docker", "AWS",
        "Node.js", "MongoDB", "Git", "C++", "HTML", "CSS"
    ]
    found_skills = [s for s in skills_list if s.lower() in text.lower()]

    experience_years = re.findall(r'(\d+)\+?\s*(?:year|yr)', text.lower())
    if not experience_years:
        experience_years = re.findall(r'20(\d\d)\s*[-–]\s*(?:20(\d\d)|present)', text.lower())
    exp = experience_years[0] if experience_years else "Fresher"

    return {
        "text": text,
        "name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills,
        "experience": exp
    }