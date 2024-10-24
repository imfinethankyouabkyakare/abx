import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Use Streamlit session state to keep track of Firebase initialization
if "firebase_initialized" not in st.session_state:
    cred = credentials.Certificate("saathi-439108-2866ecb350dc - Copy.json")
    
    # Only initialize Firebase if not already initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    st.session_state["firebase_initialized"] = True

# Function to log in a user
def login_user(email, password):
    try:
        # Firebase Admin SDK can't verify password directly, so this is an example.
        user = auth.get_user_by_email(email)
        return user
    except auth.UserNotFoundError:
        st.error("User not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to register a new user
def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success(f"User {email} successfully registered.")
        return user
    except Exception as e:
        st.error(f"Error registering: {e}")
        return None

# Streamlit UI for login and registration
st.title("Welcome to Saathi📚")

# Enhanced Custom CSS for styling
# Enhanced Custom CSS for styling the heading
st.markdown("""
    <style>
    /* Global Body Styles */
    body {
        background-color: #f3f4f6; /* Light theme background */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: black;
    }

    /* Header Styles */
    .stMarkdown h1 {
        text-align: center;
        color: #fff;
        padding: 20px;
        border-radius: 15px;
        font-size: 2.5em;
        # border: 3px solid #FFFFFF;  
        # text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        # box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
        width: fit-content;
        margin: 20px auto;
    }

    .stSubheader {
        text-align: center;
        color: #333;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }

    /* Form Container Styles */
    .stForm {
        background: linear-gradient(to bottom right, #ffffff, #f0f4f8);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin: 50px auto;
        transition: all 0.3s ease;
    }
    .stForm:hover {
        box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.2);
        transform: scale(1.02);
    }

    /* Input Fields Styles */
    .stTextInput label {
        font-weight: bold;
    }
    .stTextInput input {
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #2980b9;
        color: #333;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border: 2px solid #ff6f61;
        box-shadow: 0px 4px 12px rgba(255, 111, 97, 0.2);
        outline: none;
    }

    /* Dropdown Styles */
    .stSelectbox label {
        font-weight: bold;
    }

    /* Button Styles */
    .stButton button {
        background-color: #ff6f61;
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 50px;
        cursor: pointer;
        margin-top: 20px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #ff7b6f;
        box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.4);
        transform: translateY(-5px);
    }

    </style>

    """, unsafe_allow_html=True)
    


# Layout container for forms
with st.container():
    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login to Your Account")

        with st.form("login_form", clear_on_submit=True):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")
            
            if submit_button:
                user = login_user(email, password)
                if user:
                    st.success(f"Logged in as {email}")

    elif choice == "Sign Up":
        st.subheader("Create a New Account")

        with st.form("signup_form", clear_on_submit=True):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Sign Up")
            
            if submit_button:
                user = register_user(new_email, new_password)
                if user:
                    st.success("You have successfully created an account.")
