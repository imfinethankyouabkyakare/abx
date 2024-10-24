import google.generativeai as genai
import os
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# Configure the API key
genai.configure(api_key="AIzaSyCi2IUi0gm_sSxEn6_QZZvi5okfgrFkyI8")

# Set page configuration for a wide layout and page icon
st.set_page_config("AI Roadmap Generator", layout="wide", page_icon="🗺")

# Custom title and description with centered alignment and color styling
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>Roadmap Generator 🪜 </h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Generate structured learning paths for any domain</p>", 
    unsafe_allow_html=True
)

# User input: Domain name and difficulty level
domain_name = st.text_input("Enter the domain name (e.g., Machine Learning, Data Science):")
difficulty_level = st.selectbox("Select difficulty level:", ["Basic", "Intermediate", "Advanced"])

# Function to generate roadmap using Gemini Pro API
def generate_roadmap(domain, difficulty):
    # Create the prompt based on user input
    prompt_text = f"Generate a {difficulty} roadmap for learning {domain}. Include essential topics, skills, and tools."

    # Use GenerativeModel to generate the content
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt_text)

    # Return the generated roadmap as text
    return response.text

# Function to visualize the roadmap as a tree using matplotlib and networkx
def visualize_roadmap(roadmap_text):
    # Split the roadmap into topics
    topics = roadmap_text.split("\n")
    topics = [topic.strip() for topic in topics if topic.strip()]

    # Create a directed graph
    G = nx.DiGraph()

    # Add the root node and connect topics as edges
    root_node = f"{domain_name} ({difficulty_level})"
    G.add_node(root_node)
    for topic in topics:
        G.add_edge(root_node, topic)

    # Plot the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", 
        node_size=3000, font_size=10, font_weight="bold", arrows=False
    )
    plt.title(f"{domain_name} - {difficulty_level} Roadmap")
    st.pyplot(plt.gcf())  # Render the graph in Streamlit

# Button to generate the roadmap
if st.button("Generate Roadmap"):
    if domain_name.strip():
        with st.spinner("Generating roadmap..."):
            # Generate the roadmap and display it
            roadmap = generate_roadmap(domain_name, difficulty_level)
            st.subheader("Generated Roadmap:")
            st.write(roadmap)
            
    else:
        st.warning("Please enter a domain name.")