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
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
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

# Function to extract text from PDF files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

# Function to split text into manageable chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create and store the vector index
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Function to load a conversational chain for question answering
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not available, say,
    "Answer is not available in the context." Avoid providing incorrect answers.

    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user input and search for answers
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply: ", response["output_text"])

# PDF analyzer page
def pdf_analyzer():
    st.title("PDF Analyzer")
    st.write("Upload PDF files to analyze content and ask questions.")
    user_question = st.text_input("Ask a Question from the PDF Files:")
    
    pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True, type="pdf")
    
    if pdf_docs and st.button("Submit & Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            st.success("Processing complete! You can now ask questions.")
    
    if user_question:
        with st.spinner("Retrieving the answer..."):
            user_input(user_question)

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
            result = num1 / num2 if num2 != 0 else "Cannot divide by zero!"
        st.write(f"Result: {result}")

# Quiz generator page
def quiz_generator():
    st.title("Quiz Generator")
    st.write("Generate quizzes from provided content.")

# Main function
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
        pdf_analyzer()  # Updated PDF Analyzer function
    elif menu == "Roadmap":
        roadmap()
    elif menu == "Calculator":
        calculator()
    elif menu == "Todo":
        todo()
    elif menu == "Quiz Generator":
        quiz_generator()
        
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login()
else:
    main()

