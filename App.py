import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2 as pdf
#from huggingface_hub import upload_file
import os
#from notdiamond.settings import GOOGLE_API_KEY
import json

load_dotenv() #load all the environment variable

#genai.configure(api_key=os.getenv(GOOGLE_API_KEY))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response

def get_gemini_response(input_text):
    model = genai.GenerativeModel('models/gemini-2.5-pro')  # ✅ Correct full model path
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
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



## streamlit app
st.title("Pro ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")
submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        final_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(final_prompt)
        st.subheader(response)


