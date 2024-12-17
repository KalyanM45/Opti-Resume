import streamlit as st
from PyPDF2 import PdfReader
import openai
from fpdf import FPDF
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to Extract Text from PDF
def ExtractPDF(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to Optimize Resume Text using OpenAI API
def send_request(filename, text):
    with open(f"Prompts/{filename}", 'r') as file:
        prompt = file.read()
    prompt = prompt + text
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0
    )
    result = response.choices[0].message.content.strip()
    return result.replace('*', '')

# Function to create a PDF with optimized resume
def create_pdf(text, input_filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_margins(10, 10, 10)  # Set narrower margins to 10 mm
    pdf.set_font("Courier", size=10)
    for line in text.split("\n"):
        # Ensure that the line is encoded in latin-1
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), align='L')
    # Generate the timestamped filename with format ddmmyyyyhhmmss
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    file_name = f"{input_filename}_Optimized_{timestamp}.pdf"
    pdf.output(file_name, 'F')
    return file_name if os.path.exists(file_name) else None


# Sidebar for pages
st.sidebar.title("Opti-Resume")
page = st.sidebar.selectbox("Choose a page", ["Optimise Your Resume", "Bullet-Point Analysis", "Know the Needed Skills", "ATS Score Analysis", "Metric Analytics"])

# Main page functionality for resume optimization
if page == "Optimise Your Resume":
    st.title("Opti-Resume: AI-Powered Resume Optimization")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    if uploaded_file is not None:
        resume_text = ExtractPDF(uploaded_file)
        if st.button("Optimize"):
            optimized_text = send_request("Prompt.txt", resume_text)
            st.text_area("Optimized Resume", optimized_text, height=300)
            input_filename = uploaded_file.name.split('.')[0]  # Get the original filename without extension
            optimized_filename = create_pdf(optimized_text, input_filename)
            if optimized_filename:
                with open(optimized_filename, "rb") as file:
                    st.download_button("Download Optimized Resume", file, file_name=optimized_filename)
            else:
                st.error("There was an issue generating the optimized resume.")

# Keyword Analysis page
elif page == "Know the Needed Skills":
    st.title("Opti-Resume: Skills Analysis")
    job_description = st.text_area("Enter the Job Description", height=200)
    if st.button("Analyze Keywords"):
        if job_description:
            analysis_result = send_request("Keyword_Prompt.txt", job_description)
            st.subheader("Skills Categorized from Resume and Job Description")
            st.text_area("Analysis Result", analysis_result, height=300)
        else:
            st.error("Please enter a job description to analyze.")

# Bullet Analysis page
elif page == "Bullet-Point Analysis":
    st.title("Opti-Resume: Bullet Point Optimization")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    
    if uploaded_file is not None:
        resume_text = ExtractPDF(uploaded_file)
        
        if st.button("Analyze Bullet Points"):
            if resume_text:
                bullet_analysis = send_request(resume_text)
                st.subheader("Optimized Bullet Points")
                st.text_area("Optimized Bullet Points", bullet_analysis, height=300)
            else:
                st.error("No bullet points found. Please upload a valid PDF.")

# Keyword Analysis page
elif page == "Metric Analytics":
    st.title("Opti-Resume: Metric Analysis")
    bullet = st.text_area("Enter Your Bullet Point", height=100)
    if st.button("Analyze"):
        if bullet:
            metric_result = send_request("Metric_Prompt.txt", bullet)
            st.text_area("Metric Result", metric_result, height=300)