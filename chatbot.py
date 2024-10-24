import streamlit as st  # For UI
import os
from dotenv import load_dotenv  # To load environment variables
import google.generativeai as genai  # Google Gemini API

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Function to generate a response from Gemini
def get_gemini_response(ques):
    resp = model.generate_content(ques)
    return resp.text

# Set up the Streamlit app with a wide layout and expanded sidebar
st.set_page_config(
    page_title="Gemini Pro Q/A Project", layout="wide", initial_sidebar_state="expanded"
)

# Centered title and description with custom styling
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>SAATHI CHATBOT🤖</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Ask questions and get response instantly</p>", 
    unsafe_allow_html=True
)

# User input for questions
question = st.text_input("Ask a question:")

# Submit button with response handling
if st.button("Submit"):
    if question:
        with st.spinner("Generating response..."):
            response = get_gemini_response(question)
            st.write(f"*User:* {question}")
            st.write(f"*Bot:* {response}")
    else:
        st.warning("Please enter a question.")