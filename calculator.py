import streamlit as st
import math

# Setting the page configuration
st.set_page_config(
    page_title="Advanced Calculator",
    layout="centered",
    initial_sidebar_state="auto",
)

# Injecting CSS styles for a modern look
st.markdown("""
    <style>
    /* Overall page styling */
    body {
        background-color: #f3f4f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }

    /* Header styling */
    .header h1 {
        text-align: center;
        color: #fff;
        background: #4CAF50;
        padding: 15px;
        border-radius: 10px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        width: fit-content;
        margin: auto;
        margin-top: 20px;
        border-bottom: none; /* Remove the default line under heading */
    }

    /* Input box and results styling */
    .input-box, .result-box {
        background: var(--background-color, linear-gradient(to bottom right, #000000, #f0f4f8));
        padding: 20px;
        border-radius: 15px;
        max-width: 450px;
        margin: 20px auto;
        color: var(--text-color, #000000);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
    }
    .input-box:hover, .result-box:hover {
        box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.2);
        transform: scale(1.02);
    }

    .stTextInput label, .stNumberInput label {
        font-weight: bold;
        font-size: 1.1em;
    }

    /* Button Styling */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 16px;
        border-radius: 12px;
        cursor: pointer;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45a049;
        box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.2);
        transform: translateY(-5px);
    }   
    </style>
""", unsafe_allow_html=True)

# Setting up the header
st.markdown('<div class="header"><h1>Advanced Calculator </h1></div>', unsafe_allow_html=True)

# Setting up the calculator functionality
st.markdown('<div class="input-box">', unsafe_allow_html=True)

# Dropdown for selecting calculation type
operation = st.selectbox(
    "Choose an operation",
    ["Basic Arithmetic", "Trigonometric", "Logarithmic", "Square Root", "Factorial", "Power", "Evaluate Expression"]
)

# Input handling and calculation logic
if operation == "Basic Arithmetic":
    st.markdown("### Basic Arithmetic Operations")
    num1 = st.number_input("Enter first number", value=None, step=1)
    num2 = st.number_input("Enter second number", value=None, step=1)
    operation_type = st.selectbox("Select operation", ["Addition", "Subtraction", "Multiplication", "Division"])

    if st.button("Calculate"):
        if operation_type == "Addition":
            result = num1 + num2
        elif operation_type == "Subtraction":
            result = num1 - num2
        elif operation_type == "Multiplication":
            result = num1 * num2
        elif operation_type == "Division":
            result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
        st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)

elif operation == "Trigonometric":
    st.markdown("### Trigonometric Operations")
    angle = st.number_input("Enter angle (in degrees)", value=0.0, step=0.1)
    trig_func = st.selectbox("Select trigonometric function", ["Sine", "Cosine", "Tangent"])

    if st.button("Calculate"):
        radian_angle = math.radians(angle)
        if trig_func == "Sine":
            result = math.sin(radian_angle)
        elif trig_func == "Cosine":
            result = math.cos(radian_angle)
        elif trig_func == "Tangent":
            result = math.tan(radian_angle)
        st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)

elif operation == "Logarithmic":
    st.markdown("### Logarithmic Operations")
    num = st.number_input("Enter a number", value=1.0, step=0.1)
    log_base = st.number_input("Enter base (default is e)", value=math.e, step=0.1)

    if st.button("Calculate"):
        result = math.log(num, log_base) if num > 0 else "Number must be greater than zero"
        st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)

elif operation == "Square Root":
    st.markdown("### Square Root Calculation")
    num = st.number_input("Enter a number", value=0.0, step=0.1)

    if st.button("Calculate"):
        result = math.sqrt(num) if num >= 0 else "Cannot calculate square root of negative number"
        st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)

elif operation == "Factorial":
    st.markdown("### Factorial Calculation")
    num = st.number_input("Enter a number (integer)", value=0, step=1)

    if st.button("Calculate"):
        result = math.factorial(int(num)) if num >= 0 else "Cannot calculate factorial of negative number"
        st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)

elif operation == "Power":
    st.markdown("### Power Calculation")
    base = st.number_input("Enter the base number", value=0.0, step=0.1)
    exponent = st.number_input("Enter the exponent", value=1.0, step=0.1)

    if st.button("Calculate"):
        result = math.pow(base, exponent)
        st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)

elif operation == "Evaluate Expression":
    st.markdown("### Evaluate Complex Expression")
    expression = st.text_input("Enter the expression (use Python syntax)")

    if st.button("Calculate"):
        try:
            result = eval(expression)
            st.markdown(f'<div class="result-box"><h3>Result: {result}</h3></div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="result-box"><h3>Error: {str(e)}</h3></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
