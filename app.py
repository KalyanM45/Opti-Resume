import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from OptiResume.utils import ExtractPDF, SendRequest, CreatePDF

st.set_page_config(page_title="Opti-Resume: AI-Powered Resume Optimization", page_icon="📝")

# Sidebar for pages
st.sidebar.title("Opti-Resume - Tools")
page = st.sidebar.selectbox("", ["Optimise Your Resume", "Bullet-Point Analysis", "Know the Needed Skills", "ATS Score Analysis", "Metric Analytics"])

# Read the external CSS file
with open("static/styles.css") as f:  # Adjust the file path as needed
    css = f.read()

# Inject the CSS into the Streamlit app
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Main page functionality for resume optimization
if page == "Optimise Your Resume":
    st.title("Opti-Resume: AI-Powered Resume Optimization")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    if uploaded_file is not None:
        resume_text = ExtractPDF(uploaded_file)
        if st.button("Optimize"):
            optimized_text = SendRequest("Prompt.txt", resume_text)
            st.text_area("Optimized Resume", optimized_text, height=300)
            input_filename = uploaded_file.name.split('.')[0]  # Get the original filename without extension
            optimized_filename = CreatePDF(optimized_text, input_filename)
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
            analysis_result = SendRequest("Keyword_Prompt.txt", job_description)
            st.subheader("Skills Categorized from Job Description")
            st.text_area("", analysis_result, height=200)
        else:
            st.error("Please enter a job description to analyze.")

# Bullet Analysis page
elif page == "Bullet-Point Analysis":
    st.title("Opti-Resume: Bullet Point Optimization")
    bullet_ = st.text_area("Enter Your Bullet Point", height=100)   
        
    if st.button("Analyze Bullet Points"):
        if bullet_:
            bullet_analysis = SendRequest("Bullet_Prompt.txt", bullet_)
            st.text_area("Optimized Bullet Points", bullet_analysis, height=150)
        else:
            st.error("Please Enter a Bullet Point to Analyze.")

# Keyword Analysis page
elif page == "Metric Analytics":
    st.title("Opti-Resume: Metric Analysis")
    bullet = st.text_area("Enter Your Bullet Point", height=100)
    if st.button("Analyze"):
        if bullet:
            metric_result = SendRequest("Metric_Prompt.txt", bullet)
            st.text_area("Metric Result", metric_result, height=300)