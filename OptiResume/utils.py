import os
import openai
from fpdf import FPDF
from PyPDF2 import PdfReader
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='../.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to Extract Text from PDF
def ExtractPDF(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to Optimize Resume Text using OpenAI API
def SendRequest(filename, text):
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
def CreatePDF(text, input_filename):
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