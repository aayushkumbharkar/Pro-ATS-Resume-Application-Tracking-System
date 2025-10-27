import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2 as pdf
import os
import time
from google.api_core.exceptions import ResourceExhausted

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------------------
# Gemini Response Function (Flash default)
# -------------------------------
@st.cache_data
def get_gemini_response(input_text):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = model.generate_content(input_text)
            return response.text
        except ResourceExhausted:
            st.warning("⚠️ Temporary rate limit hit. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return "⚠️ Error occurred while generating response."

    st.error("⚠️ API quota exceeded multiple times. Try again later.")
    return "Quota limit reached. Please wait a bit before retrying."

# -------------------------------
# PDF Text Extraction
# -------------------------------
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# -------------------------------
# Prompt Template
# -------------------------------
input_prompt = """
Act like a highly experienced Applicant Tracking System (ATS) with deep domain knowledge of software engineering, data science, data analytics, and big data roles.

Your task is to evaluate a candidate's resume based on the provided job description in a highly competitive job market.

Provide a detailed evaluation including:
1. An estimated **JD Match percentage** based on relevance and keyword alignment.
2. A list of **important missing keywords** that are in the job description but not mentioned in the resume.
3. A **clear, professional profile summary** that highlights strengths and areas for improvement, including suggestions for enhancing the resume for better alignment.

Avoid JSON or structured formats — instead, present the response in rich, readable text paragraphs.

Resume:
{text}

Job Description:
{jd}
"""

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🧠 Pro ATS — Resume Evaluator (Gemini Flash)")
st.caption("Powered by Gemini 1.5 Flash — optimized for speed and free-tier usage")

jd = st.text_area("📄 Paste the Job Description here")
uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF only)", type="pdf")
submit = st.button("🚀 Submit for Evaluation")

# -------------------------------
# Main Logic
# -------------------------------
if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner("Analyzing resume with Gemini 1.5 Flash..."):
            resume_text = input_pdf_text(uploaded_file)
            final_prompt = input_prompt.format(text=resume_text, jd=jd)
            response = get_gemini_response(final_prompt)
            st.subheader("🔍 ATS Evaluation Report")
            st.write(response)
    else:
        st.error("Please provide both the Job Description and a Resume PDF file.")
