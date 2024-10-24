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
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Configure credentials and API key
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "C:\\Users\\asus\\Downloads\\saathi-439108-2866ecb350dc.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# --- Utility Functions ---
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return "\n".join(p.get_text() for p in paragraphs)

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain(prompt_template):
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def generate_notes_from_chunks(text_chunks):
    chain = get_conversational_chain("Generate concise notes based on the following content:\n{context}\nNotes:")
    all_notes = [chain({"input_documents": [Document(page_content=chunk)]})["output_text"] for chunk in text_chunks]
    return "\n".join(all_notes)

def generate_notes_from_topic(topic):
    chain = get_conversational_chain("Generate detailed notes on the following topic:\n{context}\nNotes:")
    response = chain({"input_documents": [Document(page_content=topic)]})
    return response["output_text"]

# Save notes with clean formatting using asterisks
def save_notes_as_pdf(notes, main_topic, filename="generated_notes.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Title: Main Topic (Bold + Underlined + Green)
    pdf.set_font("Arial", style="BU", size=16)
    pdf.set_text_color(0, 128, 0)  # Green color
    pdf.cell(0, 10, txt=main_topic.upper(), ln=True, align='C')

    pdf.ln(10)  # Add space after the title

    # Configure font settings for general text
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Black text for general content

    # Iterate through notes and format them with asterisks
    for line in notes.split('\n'):
        line = line.strip()  # Clean extra whitespace

        if len(line) < 50 and not any(punct in line for punct in ".!?"):
            # Short lines without punctuation are treated as headings
            pdf.set_font("Arial", style="B", size=14)  # Bold for headings
            pdf.set_text_color(0, 0, 0)  # Black
            pdf.cell(0, 10, txt=line.upper(), ln=True, align='L')
            pdf.ln(5)  # Space below the heading

        elif line:  # Normal content lines
            pdf.set_font("Arial", size=12)  # Standard font
            pdf.set_text_color(0, 0, 255)  # Blue text for content
            pdf.cell(5)  # Indent
            pdf.cell(0, 10, txt=f"* {line.capitalize()}", ln=True, align='L')  # Asterisk instead of bullet

        else:
            pdf.ln(5)  # Add space between sections

    pdf.output(filename)
    return filename

# --- Streamlit App UI ---
def main():
    st.set_page_config("AI Notes Generator", layout="wide", page_icon="📝")
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'>Notes Generator 💡</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px;'>Generate clean and concise notes from PDFs, Topics, or URLs with ease.</p>", 
        unsafe_allow_html=True
    )

    # Option selection menu with icons
    option = st.selectbox(
        "Select Input Type:",
        ("📄 Upload PDF", "💬 Enter Topic", "🔗 Enter URL")
    )

    if option == "📄 Upload PDF":
        pdf_docs = st.file_uploader("Upload one or more PDFs:", accept_multiple_files=True)
        if st.button("Generate Notes from PDF"):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    notes = generate_notes_from_chunks(text_chunks)

                    st.success("Notes generated successfully!")
                    st.write(notes)

                    pdf_path = save_notes_as_pdf(notes, "Generated Notes from PDF")
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            "📥 Download Notes as PDF",
                            data=pdf_file,
                            file_name="notes_from_pdf.pdf",
                            mime="application/pdf"
                        )

    elif option == "💬 Enter Topic":
        topic = st.text_area("Enter the topic:")
        if st.button("Generate Notes"):
            if topic.strip():
                with st.spinner("Generating notes..."):
                    notes = generate_notes_from_topic(topic)

                    st.success("Notes generated successfully!")
                    st.write(notes)

                    pdf_path = save_notes_as_pdf(notes, topic)
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            "📥 Download Notes as PDF",
                            data=pdf_file,
                            file_name="notes_from_topic.pdf",
                            mime="application/pdf"
                        )

    elif option == "🔗 Enter URL":
        url = st.text_input("Enter the URL:")
        if st.button("Generate Notes"):
            if url.strip():
                with st.spinner("Fetching content..."):
                    raw_text = get_text_from_url(url)
                    text_chunks = get_text_chunks(raw_text)
                    notes = generate_notes_from_chunks(text_chunks)

                    st.success("Notes generated successfully!")
                    st.write(notes)

                    pdf_path = save_notes_as_pdf(notes, "Generated Notes from URL")
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            "📥 Download Notes as PDF",
                            data=pdf_file,
                            file_name="notes_from_url.pdf",
                            mime="application/pdf"
                        )

if __name__ == "__main__":
    main()