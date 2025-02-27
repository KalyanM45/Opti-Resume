import streamlit as st
from OptiResume.main import *

# Page Configurations
st.set_page_config(page_title="Opti-Resume: AI-Powered Resume Optimizer", page_icon="⭐")
st.sidebar.title("Opti-Resume - Tools")
page = st.sidebar.selectbox("", ["Resume Optimisation", "Bullet-Point Analysis", "Know the Needed Skills", "ATS Score Analysis", "Metric Analytics"])

# Loading CSS for the app
@st.cache_data
def load_css():
    with open("static/styles.css") as f:
        return f.read()
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

if page == "Resume Optimisation":
    OptimiseResume()
elif page == "Bullet-Point Analysis":
    BulletPointAnalysis()
elif page == "Know the Needed Skills":
    SkillsAnalysis()
elif page == "ATS Score Analysis":
    ATSAnalysis()
elif page == "Metric Analytics":
    MetricAnalysis()