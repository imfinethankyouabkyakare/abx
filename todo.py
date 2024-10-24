import streamlit as st

# Custom CSS styling for a beautiful interface
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    
    .main-heading {
        font-size: 45px;
        color: #2a9d8f;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
    }

    .subheading {
        font-size: 25px;
        color: #264653;
        margin-top: 30px;
        text-align: center;
    }

    .task-container {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 20px;
        margin-top: 10px;
        border: 1px solid #ced4da;
    }

    .task-input {
        font-size: 18px;
        padding: 10px;
        border: none;
        border-radius: 8px;
        background-color: #ffffff;
        width: 100%;
        margin-top: 10px;
    }

    .task-button {
        background-color: #2a9d8f;
        color: white;
        font-size: 18px;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        margin-top: 15px;
    }

    .task-button:hover {
        background-color: #21867a;
    }

    .task-item {
        font-size: 20px;
        padding: 10px;
        background-color: #ffffff;
        margin-top: 10px;
        border: 1px solid #ced4da;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .remove-button {
        background-color: #e76f51;
        color: white;
        border: none;
        padding: 5px 15px;
        border-radius: 5px;
        cursor: pointer;
    }

    .remove-button:hover {
        background-color: #c35441;
    }

    .completed-task {
        text-decoration: line-through;
        color: #6c757d;
    }
    </style>
""", unsafe_allow_html=True)

# Main heading
st.markdown("<h1 class='main-heading'>To-Do List📝</h1>", unsafe_allow_html=True)

# Initialize session state for tasks and completion status
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []
if 'completed' not in st.session_state:
    st.session_state['completed'] = []

# Input task from the user
st.markdown("<h3 class='subheading'>Add a new task:</h3>", unsafe_allow_html=True)
new_task = st.text_input("", key='task_input', placeholder="Enter your task here...", label_visibility="collapsed")

# Function to add task to the list
def add_task():
    if new_task:
        st.session_state['tasks'].append(new_task)
        st.session_state['completed'].append(False)
        st.session_state['task_input'] = ""  # Clear input field

# Function to remove task from the list
def remove_task(index):
    del st.session_state['tasks'][index]
    del st.session_state['completed'][index]

# Button to add task
st.button("Add Task", on_click=add_task, key='add_button', use_container_width=True)

# Display the tasks with checkboxes for completion
st.markdown("<h3 class='subheading'>Your To-Do List:</h3>", unsafe_allow_html=True)
if st.session_state['tasks']:
    for i, task in enumerate(st.session_state['tasks']):
        col1, col2 = st.columns([0.1, 0.9])
        
        # Checkbox to mark task as complete
        with col1:
            completed = st.checkbox("", key=f"check_{i}", value=st.session_state['completed'][i])
            st.session_state['completed'][i] = completed
        
        # Task description with line-through if completed
        with col2:
            task_style = "completed-task" if st.session_state['completed'][i] else ""
            st.markdown(f"<div class='task-item'><span class='{task_style}'>{task}</span>", unsafe_allow_html=True)
            st.button("Remove", key=f"remove_{i}", on_click=remove_task, args=(i,), use_container_width=True)
else:
    st.write("You have no tasks. Add a task to get started!")
