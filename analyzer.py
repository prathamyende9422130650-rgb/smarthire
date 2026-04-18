import requests
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")


def call_groq(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000
            }
        )
        data = response.json()
        
        # Error check karo
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"API Error: {data['error']['message']}"
        else:
            return f"Unexpected response: {str(data)}"
            
    except Exception as e:
        return f"Connection Error: {str(e)}"

def analyze_resume(resume_text):
    return call_groq(f"""Analyze this resume and provide:
1. 3 Strengths of the resume
2. 2 Weaknesses of the resume
3. ATS Score (out of 100)
4. 3 Improvement suggestions

Resume:
{resume_text}""")


def get_resume_score(resume_text):
    return call_groq(f"""Rate this resume on these 5 criteria, give score out of 20 each:
1. Skills (out of 20)
2. Experience (out of 20)
3. Education (out of 20)
4. Formatting (out of 20)
5. Keywords/ATS (out of 20)

Give response in this exact format:
Skills: X
Experience: X
Education: X
Formatting: X
Keywords: X
Total: X
Feedback: (2 lines)

Resume:
{resume_text}""")


def generate_cover_letter(resume_text, job_title, company_name):
    return call_groq(f"""Write a professional cover letter for:
Job Title: {job_title}
Company: {company_name}

Based on this resume:
{resume_text}

Write a 3 paragraph cover letter. Keep it professional and concise.""")


def generate_interview_questions(resume_text, job_title):
    return call_groq(f"""Based on this resume and job title "{job_title}", generate:
1. 5 Technical Interview Questions
2. 3 HR Interview Questions
3. 2 Situational Questions

For each question also give a short tip on how to answer it.

Resume:
{resume_text}""")