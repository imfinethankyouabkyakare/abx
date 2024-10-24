import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Set up Google Application Credentials
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "C:\\Users\\asus\\Downloads\\saathi-439108-2866ecb350dc.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Configure Google Generative AI with API Key
genai.configure(api_key=os.getenv("AIzaSyCpzURfYqs9TbCw7yncdMt09dsj0bsvkW0"))

def get_pdf_text(pdf_docs):
    """Extract text from PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def fetch_url_content(url):
    """Fetch and extract text from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    else:
        st.error("Failed to retrieve content. Please check the URL.")
        return ""

def generate_quiz_questions_from_text(text, noq):
    """Generate quiz questions from text using Google Generative AI."""
    prompt_template = """
    Generate {NOQ} quiz questions based on the following content:\n{context}\n
For each question, provide 4 answer options labeled A, B, C, and D, with one correct answer. Format the output as follows:

Question 1: [Your question here]\n
\n A. [Option A]\n
\n B. [Option B]\n
\n C. [Option C]\n
\n D. [Option D]\n

...and so on.

Answer Key:\n
1. [Question 1 number] - [Correct option]\n
2. [Question 2 number] - [Correct option]\n
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "NOQ"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    document = Document(page_content=text)
    response = chain({"input_documents": [document], "NOQ": noq})
    return response["output_text"]

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config("AI Quiz Generator", layout="wide", page_icon="🎓")
    
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'> Quiz Generator 🎓</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px;'>Generate quiz questions from PDFs, Topics, or URLs </p>",
        unsafe_allow_html=True
    )

    # Option selection with icons
    option = st.selectbox(
        "Select Input Type:",
        ("📄 Upload PDF", "💬 Enter Topic", "🔗 Enter URL")
    )

    noq = st.number_input("Enter the Number of Questions to Generate:", min_value=1, max_value=50, value=5)

    if option == "📄 Upload PDF":
        pdf_docs = st.file_uploader("Upload your PDF Files:", accept_multiple_files=True)

        if st.button("Generate Quiz Questions from PDF"):
            if pdf_docs:
                with st.spinner("Processing PDF..."):
                    raw_text = get_pdf_text(pdf_docs)
                    questions = generate_quiz_questions_from_text(raw_text, noq)
                    st.success("Quiz Questions Generated!")
                    st.write(questions)
            else:
                st.warning("Please upload at least one PDF file.")

    elif option == "💬 Enter Topic":
        topic = st.text_area("Enter the Topic:")

        if st.button("Generate Quiz Questions from Topic"):
            if topic.strip():
                with st.spinner("Generating Questions..."):
                    questions = generate_quiz_questions_from_text(topic, noq)
                    st.success("Quiz Questions Generated!")
                    st.write(questions)
            else:
                st.warning("Please enter a valid topic.")

    elif option == "🔗 Enter URL":
        url = st.text_input("Enter the URL:")

        if st.button("Generate Quiz Questions from URL"):
            if url.strip():
                with st.spinner("Fetching URL Content..."):
                    content = fetch_url_content(url)
                    if content:
                        questions = generate_quiz_questions_from_text(content, noq)
                        st.success("Quiz Questions Generated!")
                        st.write(questions)
            else:
                st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()