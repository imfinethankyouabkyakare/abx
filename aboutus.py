import streamlit as st

# Custom CSS for a dark theme About Us page
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e; /* Dark background */
            color: #ffffff; /* Light text */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .title {
            font-size: 3.5em;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            margin-top: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            font-size: 1.8em;
            color: #e0e0e0;
            text-align: center;
            margin-bottom: 25px;
            font-weight: 600;
        }
        .image {
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s;
        }
        .image:hover {
            transform: scale(1.05);
        }
        .disclaimer {
            font-size: 1.2em;
            color: #ffffff;
            background-color: #E74C3C; /* Red background for disclaimer */
            font-weight: bold;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            transition: background-color 0.3s;
        }
        .disclaimer:hover {
            background-color: #C0392B; /* Darker red on hover */
        }
        .about-section {
            margin: 40px auto;
            padding: 30px;
            width: 85%;
            text-align: justify;
            color: #ffffff; /* Light text for about section */
            font-size: 1.2em;
            line-height: 1.8;
            background-color: #2c2c2c; /* Dark background for about section */
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .section-title {
            font-size: 2.5em;
            color: #ffffff;
            font-weight: 800;
            text-align: center;
            margin-bottom: 15px;
            text-decoration: underline;
        }
        .footer {
            font-size: 1em;
            color: #aaaaaa;
            text-align: center;
            margin-top: 40px;
            font-style: italic;
        }
            .h2{
            text-align: right;
            }
    </style>
""", unsafe_allow_html=True)

# Main content
st.markdown("<h1 class='title'>About Us </h1>", unsafe_allow_html=True)
# st.markdown("<h2 class='subtitle'>Your AI Personal Tutor</h2>" , unsafe_allow_html=True)

# Layout for image, disclaimer, and about section
col1, col2 = st.columns([1, 2])  # Adjust the proportions as needed

with col1:
    st.image("1000_F_643686570_jlFaFaXfYNQKfvdnOAAYbY9E4AkUPWDb-removebg-preview.png", use_column_width=True)
    st.markdown("<div class='disclaimer'>SAATHI IS BY YOU , WITH YOU AND FOR YOU!🎯</div>", unsafe_allow_html=True)

with col2:
       st.markdown("""
    <div class='about-section'>
        <h3 class='section-title'>Saathi🎓 </h3>
        <p>
            Saathi is designed to provide personalized learning experiences, helping students to grasp concepts at their own pace.<br> <br>
                        FEATURES : <br> <br>
            💡TO-DO LIST: It is a simple tool for organizing tasks and priorities, helping you manage your daily activities effectively and stay on track. <br>  
            💡ROADMAP : It is a strategic plan that outlines the key milestones, goals, and steps to achieve a vision or objective. It serves as a guide to help track progress and ensure alignment with long-term goals.<br>
            💡CHATBOT : "Chatbot for students offers instant academic support, answering questions and providing resources to enhance learning. It guides students with personalized assistance, making education more accessible and engaging.<br>
            💡PDF ANALYSER :  This allows you to ask questions from PDF and get answer in exact words provided in it.<br>
            💡NOTES GENERATOR : A notes generator extracts key information from PDF files using a URL or Topic name, creating concise and organized notes. It simplifies the process of gathering essential details, saving time and enhancing productivity.<br>
            💡QUIZ GENERATOR : Quiz generator automatically creates quizzes by extracting content from specified PDF Documents,Topic and Url.<br>
            💡CALCULATOR : For conditions, when user wants to perform advance calculations.<br>
            💡STICKY NOTES : Sticky notes are versatile tools used for storing important information.<br><br>
                   Disclaimer : Saathi can make mistakes , please use it wisely!
                   
            
            
            
            
                   







       </p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>© 2024 Saathi AI Tutor. All rights reserved.</div>", unsafe_allow_html=True)
