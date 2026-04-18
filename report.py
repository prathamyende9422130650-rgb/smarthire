from fpdf import FPDF
import datetime

def generate_pdf_report(resume_data, analysis, score_text, cover_letter, interview_questions):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 15, "SmartHire - Resume Analysis Report", ln=True, align="C")

    # Date
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, f"Generated: {datetime.datetime.now().strftime('%d %B %Y')}", ln=True, align="C")
    pdf.ln(5)

    # Candidate Info
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Candidate Information", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Name: {resume_data['name']}", ln=True)
    pdf.cell(0, 8, f"Email: {resume_data['email']}", ln=True)
    pdf.cell(0, 8, f"Experience: {resume_data['experience']} Years", ln=True)
    pdf.cell(0, 8, f"Skills: {', '.join(resume_data['skills'])}", ln=True)
    pdf.ln(5)

    # AI Analysis
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "AI Analysis", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, analysis)
    pdf.ln(5)

    # Resume Score
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "Resume Score", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, score_text)
    pdf.ln(5)

    # Cover Letter
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "Generated Cover Letter", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, cover_letter)
    pdf.ln(5)

    # Interview Questions
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "Interview Questions", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, interview_questions)

    path = "/tmp/resume_report.pdf"
    pdf.output(path)
    return path