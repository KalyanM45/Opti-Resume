import streamlit as st
from OptiResume.utils import ExtractPDF, SendRequest, CreatePDF

def OptimiseResume():
    st.title("Opti-Resume: AI-Powered Resume Optimization")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        resume_text = ExtractPDF(uploaded_file)

        if st.button("Optimize"):
            optimized_text = SendRequest("Optimisation-Prompt.txt", resume_text)
            st.text_area("Optimized Resume", optimized_text, height=300)
            input_filename = f'Artifacts/{uploaded_file.name.split('.')[0]}'
            optimized_filename = CreatePDF(optimized_text, input_filename)
            if optimized_filename:
                with open(optimized_filename, "rb") as file:
                    st.download_button("Download Optimized Resume", file, file_name=optimized_filename)
            else:
                st.error("There was an issue generating the optimized resume.")

def ATSAnalysis():
    st.title("Opti-Resume: ATS Score Analysis")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    job_description = st.text_area("Enter the Job Description", height=200)
    
    if uploaded_file is not None and job_description:
        if st.button("Analyze ATS Score"):
            resume_data = ExtractPDF(uploaded_file)
            req_text = "Resume: " + resume_data + "\nJob Description: " + job_description
            ats_result = SendRequest("ATS_Check.txt", req_text)
            st.text_area("ATS Score Result", ats_result, height=500)


def SkillsAnalysis():
    st.title("Opti-Resume: Skills Analysis")
    job_description = st.text_area("Enter the Job Description", height=200)
    if st.button("Analyze Keywords"):
        if job_description:
            analysis_result = SendRequest("Keyword_Prompt.txt", job_description)
            st.subheader("Skills Categorized from Job Description")
            st.text_area("", analysis_result, height=200)
        else:
            st.error("Please enter a job description to analyze.")

def BulletPointAnalysis():
    st.title("Opti-Resume: Bullet Point Optimization")
    bullet_ = st.text_area("Enter Your Bullet Point", height=100)   
        
    if st.button("Analyze Bullet Points"):
        if bullet_:
            bullet_analysis = SendRequest("Bullet_Prompt.txt", bullet_)
            st.text_area("Optimized Bullet Points", bullet_analysis, height=150)
        else:
            st.error("Please Enter a Bullet Point to Analyze.")

def MetricAnalysis():
    st.title("Opti-Resume: Metric Analysis")
    bullet = st.text_area("Enter Your Bullet Point", height=100)
    if st.button("Analyze"):
        if bullet:
            metric_result = SendRequest("Metric_Prompt.txt", bullet)
            st.text_area("Metric Result", metric_result, height=300)