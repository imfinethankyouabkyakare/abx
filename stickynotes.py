import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import os
import numpy as np  # Ensure NumPy is imported

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
        del notes[note_id]  # Remove the note
        save_notes(notes)   # Save changes to file
        return True
    return False

def main():
    """Main function for the Notes Writing Pad app."""
    st.set_page_config(page_title="Notes Writing Pad", layout="wide", page_icon="📝")

    # Centered title and description
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'>Notes Writing Pad 📝</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px;'>Easily create, edit, save, and delete notes. Use the handwriting pad if you're on a touchscreen device!</p>", 
        unsafe_allow_html=True
    )

    # Load notes from the JSON file
    notes = load_notes()

    # Sidebar to display saved notes and an option to create a new note
    st.sidebar.subheader("📋 Your Notes")
    selected_note_id = "new_note"
    selected_note = {"title": "", "text": "", "drawing": None}  # Default empty note

    if st.sidebar.button("New Note", key="new_note"):
        selected_note_id = "new_note"

    # Display existing notes as buttons in the sidebar
    for key, note in notes.items():
        if st.sidebar.button(note["title"], key=key):
            selected_note_id = key
            selected_note = note

    # Input fields for note title and text
    note_title = st.text_input("Note Title", value=selected_note["title"])
    note_text = st.text_area("Write your note here:", value=selected_note["text"], height=200)

    # Handwriting pad section
    st.subheader("✍ Handwriting Pad")
    drawing_mode = st.selectbox("Drawing mode:", ("freedraw", "line", "rect", "circle", "transform"))
    stroke_width = st.slider("Stroke width:", 1, 10, 2)
    stroke_color = st.color_picker("Stroke color:", "#000000")
    bg_color = st.color_picker("Background color:", "#FFFFFF")

    # Prepare initial drawing if it exists
    initial_drawing = selected_note["drawing"]
    if initial_drawing:
        try:
            # Convert back to NumPy array
            initial_drawing = np.array(initial_drawing, dtype=np.uint8)
        except Exception as e:
            st.error(f"Error loading drawing: {e}")
            initial_drawing = None  # Fallback to None if there's an issue
    else:
        initial_drawing = None  # No drawing available

    # Drawing canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",  # Transparent background
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=True,
        drawing_mode=drawing_mode,
        height=300,
        width=600,
        key="canvas",
        initial_drawing=initial_drawing,  # Load drawing if it exists
    )

    # Save or update the note
    if st.button("Save Note"):
        if note_title and (note_text or (canvas_result.image_data is not None and canvas_result.image_data.any())):
            with st.spinner("Saving note..."):
                note_id = str(len(notes) + 1) if selected_note_id == "new_note" else selected_note_id

                notes[note_id] = {
                    "title": note_title,
                    "text": note_text,
                    "drawing": canvas_result.image_data.tolist() if canvas_result.image_data is not None else None,
                }
                save_notes(notes)
                st.success("Note saved successfully!")
                st.experimental_rerun()  # Reload the app to reflect changes
        else:
            st.warning("Please provide a title and either text or a drawing.")

    # Delete the selected note and show confirmation message
    if selected_note_id != "new_note":
        if st.button("Delete Note"):
            if delete_note(notes, selected_note_id):
                st.success("Note deleted successfully!")
                st.experimental_rerun()  # Reload the app to reflect changes

# Run the app
if __name__ == "__main__":
    main()