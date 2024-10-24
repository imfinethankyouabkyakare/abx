import streamlit as st
import calculator
import stickynotes
import aboutus
import notes
import quiz
import pdf_analyser
import roadmap
import todo
import login
import chatbot


# Create tabs for navigation
tab1, tab2, tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10 = st.tabs(["About Us","Login","Notes","Pdf_analyser"])

with tab1:
    aboutus.run()
with tab2:
    login.run()
with tab3:
    notes.run()
with tab4:
    pdf_analyser.run()


