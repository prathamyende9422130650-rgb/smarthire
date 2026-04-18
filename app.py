import streamlit as st
import plotly.express as px
from parser import parse_resume
from analyzer import analyze_resume, get_resume_score, generate_cover_letter, generate_interview_questions
from recommender import recommend_jobs
from report import generate_pdf_report

st.set_page_config(page_title="SmartHire", page_icon="🤖", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* Background */
.stApp {
    background: radial-gradient(ellipse at top left, #1a1040 0%, #0a0a0f 50%, #0d1a2e 100%);
    min-height: 100vh;
}

/* Title */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    background: linear-gradient(135deg, #a78bfa, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #c4b5fd !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: rgba(167, 139, 250, 0.05);
    border: 2px dashed rgba(167, 139, 250, 0.4);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #a78bfa;
    background: rgba(167, 139, 250, 0.1);
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(167, 139, 250, 0.2);
    border-radius: 16px;
    padding: 20px !important;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(167, 139, 250, 0.5);
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #a78bfa !important;
    background: rgba(167, 139, 250, 0.1) !important;
    border-bottom: 2px solid #a78bfa !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5) !important;
}

/* Link Button (Apply on LinkedIn) */
.stLinkButton > a {
    background: linear-gradient(135deg, #0077b5, #00a0dc) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 119, 181, 0.3) !important;
}
.stLinkButton > a:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 119, 181, 0.5) !important;
}

/* Container / Job Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(167, 139, 250, 0.15) !important;
    border-radius: 20px !important;
    padding: 8px !important;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(167, 139, 250, 0.4) !important;
    background: rgba(167, 139, 250, 0.05) !important;
    transform: translateY(-2px);
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #7c3aed, #38bdf8) !important;
    border-radius: 10px !important;
}
.stProgress > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}

/* Text Input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(167, 139, 250, 0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #a78bfa !important;
}

/* Divider */
hr {
    border-color: rgba(167, 139, 250, 0.15) !important;
}

/* Success / Warning / Error */
.stSuccess {
    background: rgba(52, 211, 153, 0.1) !important;
    border: 1px solid rgba(52, 211, 153, 0.3) !important;
    border-radius: 12px !important;
}
.stWarning {
    background: rgba(251, 191, 36, 0.1) !important;
    border: 1px solid rgba(251, 191, 36, 0.3) !important;
    border-radius: 12px !important;
}
.stError {
    background: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)
# Login System
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Login Page
if not st.session_state.logged_in:
    st.title("🤖 SmartHire")
    st.subheader("Please Login to Continue")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    if "users" not in st.session_state:
        st.session_state.users = {"admin": "admin123"}

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Incorrect username or password!")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Sign Up", use_container_width=True):
            if new_user and new_pass:
                st.session_state.users[new_user] = new_pass
                st.success("Account created! Please login now.")
            else:
                st.error("Please fill in both username and password!")

# Main App
else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 SmartHire — AI Resume Analyzer")
    with col2:
        st.write(f"👤 {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

    if uploaded_file:
        resume_data = parse_resume(uploaded_file)

        # Candidate Info
        st.subheader("👤 Candidate Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Name", resume_data["name"])
        col2.metric("Email", resume_data["email"])
        col3.metric("Experience", resume_data["experience"] + " Years")

        st.divider()

        # Skills Chart
        st.subheader("🛠️ Skills Detected")
        if resume_data["skills"]:
            fig = px.pie(names=resume_data["skills"], title="Skills Distribution")
            st.plotly_chart(fig)
        else:
            st.warning("No skills found in resume!")

        st.divider()

        # Feature Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 AI Analysis",
            "🏆 Resume Score",
            "✉️ Cover Letter",
            "🎯 Interview Questions",
            "💼 Job Recommendations"
        ])

        # Tab 1 - AI Analysis
        with tab1:
            st.subheader("📊 AI Resume Analysis")
            with st.spinner("AI is analyzing your resume..."):
                analysis = analyze_resume(resume_data["text"])
            st.write(analysis)

        # Tab 2 - Resume Score
        with tab2:
            st.subheader("🏆 Resume Score")
            with st.spinner("Calculating your score..."):
                score_text = get_resume_score(resume_data["text"])
            st.write(score_text)
            try:
                for line in score_text.split('\n'):
                    if 'Total:' in line:
                        total = int(''.join(filter(str.isdigit, line)))
                        st.metric("Total Score", f"{total}/100")
                        st.progress(total)
                        break
            except:
                pass

        # Tab 3 - Cover Letter
        with tab3:
            st.subheader("✉️ Cover Letter Generator")
            job_title = st.text_input("Enter Job Title (e.g. Python Developer)")
            company_name = st.text_input("Enter Company Name (e.g. TCS)")

            if st.button("Generate Cover Letter") and job_title and company_name:
                with st.spinner("Writing your cover letter..."):
                    cover_letter = generate_cover_letter(
                        resume_data["text"], job_title, company_name
                    )
                st.write(cover_letter)
                st.session_state.cover_letter = cover_letter
            elif "cover_letter" not in st.session_state:
                st.session_state.cover_letter = ""

        # Tab 4 - Interview Questions
        with tab4:
            st.subheader("🎯 Interview Questions Generator")
            job_for_interview = st.text_input("Enter Job Title for Interview Prep")

            if st.button("Generate Questions") and job_for_interview:
                with st.spinner("Generating interview questions..."):
                    interview_qs = generate_interview_questions(
                        resume_data["text"], job_for_interview
                    )
                st.write(interview_qs)
                st.session_state.interview_qs = interview_qs
            elif "interview_qs" not in st.session_state:
                st.session_state.interview_qs = ""

        # Tab 5 - Job Recommendations
        with tab5:
            st.subheader("💼 LinkedIn Job Recommendations")
            jobs = recommend_jobs(resume_data["skills"])

            if jobs:
                for job in jobs:
                    with st.container(border=True):
                        st.markdown(f"### {job['title']}")
                        st.write(f"🏢 **Company:** {job['company']}")
                        st.write(f"📍 **Location:** {job['location']}")
                        st.write(f"💰 **Salary:** {job['salary']}")
                        st.write(f"✅ **Match Score:** {job['match_score']}%")
                        st.progress(job['match_score'])
                        st.link_button(
                            "🔗 Apply on LinkedIn",
                            job['linkedin_url'],
                            use_container_width=True
                        )
            else:
                st.warning("No matching jobs found. Try adding more skills to your resume.")

        st.divider()

        # PDF Report
        st.subheader("📄 Download Full Report")
        if st.button("📥 Generate PDF Report", use_container_width=True):
            with st.spinner("Creating your PDF report..."):
                score_text = get_resume_score(resume_data["text"])
                analysis = analyze_resume(resume_data["text"])
                cover = st.session_state.get("cover_letter", "Cover letter not generated")
                interview = st.session_state.get("interview_qs", "Interview questions not generated")

                pdf_path = generate_pdf_report(
                    resume_data, analysis, score_text, cover, interview
                )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Report",
                    data=f,
                    file_name="SmartHire_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )