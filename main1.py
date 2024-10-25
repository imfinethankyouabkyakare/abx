%%writefile app.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import os
import numpy as np
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
api_key = os.getenv("GOOGLE_API_KEY")  # Set your Google API key in .env
if api_key:
    import google.generativeai as genai
    genai.configure(api_key=api_key)

# File to store saved notes
NOTES_FILE = "saved_notes.json"

# Function to load notes from a JSON file
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

# Function to save notes to a JSON file
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

# Function to delete a specific note by its ID
def delete_note(notes, note_id):
    if note_id in notes:
        del notes[note_id]
        save_notes(notes)
        return True
    return False

# Login page for authentication
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":  # Simple login validation
            st.session_state['authenticated'] = True
        else:
            st.error("Invalid credentials")

# Notes page
def notes():
    st.title("Notes Writing Pad 📝")
    st.write("Easily create, edit, save, and delete notes.")
    notes = load_notes()
    selected_note_id = "new_note"
    selected_note = {"title": "", "text": "", "drawing": None}

    # Sidebar for saved notes
    st.sidebar.subheader("📋 Your Notes")
    if st.sidebar.button("New Note", key="new_note"):
        selected_note_id = "new_note"

    for key, note in notes.items():
        if st.sidebar.button(note["title"], key=key):
            selected_note_id = key
            selected_note = note

    # Note title and text inputs
    note_title = st.text_input("Note Title", value=selected_note["title"])
    note_text = st.text_area("Write your note here:", value=selected_note["text"], height=200)

    # Handwriting pad
    st.subheader("✍ Handwriting Pad")
    drawing_mode = st.selectbox("Drawing mode:", ("freedraw", "line", "rect", "circle", "transform"))
    stroke_width = st.slider("Stroke width:", 1, 10, 2)
    stroke_color = st.color_picker("Stroke color:", "#000000")
    bg_color = st.color_picker("Background color:", "#FFFFFF")

    initial_drawing = np.array(selected_note["drawing"], dtype=np.uint8) if selected_note["drawing"] else None
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=True,
        drawing_mode=drawing_mode,
        height=300,
        width=600,
        key="canvas",
        initial_drawing=initial_drawing,
    )

    if st.button("Save Note"):
        if note_title and (note_text or (canvas_result.image_data is not None and canvas_result.image_data.any())):
            note_id = str(len(notes) + 1) if selected_note_id == "new_note" else selected_note_id
            notes[note_id] = {
                "title": note_title,
                "text": note_text,
                "drawing": canvas_result.image_data.tolist() if canvas_result.image_data is not None else None,
            }
            save_notes(notes)
            st.success("Note saved successfully!")
            st.experimental_rerun()

    if selected_note_id != "new_note" and st.button("Delete Note"):
        if delete_note(notes, selected_note_id):
            st.success("Note deleted successfully!")
            st.experimental_rerun()

# To-do list page
def todo():
    st.title("To-Do List📝")
    if 'tasks' not in st.session_state:
        st.session_state['tasks'] = []
    if 'completed' not in st.session_state:
        st.session_state['completed'] = []

    new_task = st.text_input("Enter a new task")
    if st.button("Add Task"):
        if new_task:
            st.session_state['tasks'].append(new_task)
            st.session_state['completed'].append(False)

    st.write("### Your Tasks")
    for i, task in enumerate(st.session_state['tasks']):
        completed = st.checkbox("Complete", key=f"check_{i}", value=st.session_state['completed'][i])
        st.session_state['completed'][i] = completed
        if completed:
            st.write(f"~~{task}~~")
        else:
            st.write(task)
        if st.button("Remove", key=f"remove_{i}"):
            del st.session_state['tasks'][i]
            del st.session_state['completed'][i]
            st.experimental_rerun()

# Sticky notes page
def sticky_notes():
    st.title("Sticky Notes")
    st.write("Create and store important information here.")

# PDF analyzer page
def pdf_analyzer():
    st.title("PDF Analyzer")
    st.write("Upload PDF files to analyze content.")
    pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True, type="pdf")
    if pdf_docs and st.button("Analyze PDFs"):
        st.write("PDF analysis is a placeholder; full analysis feature to be added.")

# Roadmap page
def roadmap():
    st.title("Roadmap")
    roadmap_text = st.text_area("Enter your roadmap:")
    if st.button("Save Roadmap"):
        st.session_state["roadmap"] = roadmap_text
        st.success("Roadmap saved!")
    st.write("### Your Roadmap")
    st.write(st.session_state.get("roadmap", ""))

# Calculator page
def calculator():
    st.title("Calculator")
    num1 = st.number_input("Enter first number", value=0.0)
    operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
    num2 = st.number_input("Enter second number", value=0.0)

    if st.button("Calculate"):
        if operation == "Add":
            result = num1 + num2
        elif operation == "Subtract":
            result = num1 - num2
        elif operation == "Multiply":
            result = num1 * num2
        elif operation == "Divide":
            result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
        st.write("Result:", result)

# Quiz generator page
def get_pdf_text(pdf_docs):
    """Extract text from PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
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
    A. [Option A]\n
    B. [Option B]\n
    C. [Option C]\n
    D. [Option D]\n

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

def quiz_generator():
    st.title("AI Quiz Generator 🎓")
    st.write("Generate quiz questions from PDFs, Topics, or URLs")
    
    option = st.selectbox("Select Input Type:", ("📄 Upload PDF", "💬 Enter Topic", "🔗 Enter URL"))
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

def main():
    st.sidebar.title("Self Tutor App")
    menu = st.sidebar.selectbox("Select an Option", ["About Us", "Notes", "Sticky Notes", "PDF Analyzer", 
                                                     "Roadmap", "Calculator", "Todo", "Quiz Generator"])

    if menu == "About Us":
        st.title("About Us")
        st.write("This app helps students with various academic tasks and organization.")
    elif menu == "Notes":
        notes()
    elif menu == "Sticky Notes":
        sticky_notes()
    elif menu == "PDF Analyzer":
        pdf_analyzer()
    elif menu == "Roadmap":
        roadmap()
    elif menu == "Calculator":
        calculator()
    elif menu == "Todo":
        todo()
    elif menu == "Quiz Generator":
        quiz_generator()

if __name__ == "__main__":
    main()
