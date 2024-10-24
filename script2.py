import streamlit as st
import subprocess
import webbrowser
import time
import asreview

# Title of the app
st.title("ASReview Interface")

# Description
st.write("This is your ASReview application. Click the button below to start.")

# A button to trigger the ASReview Lab app
if st.button('Start ASReview'):
    try:
        # Run the 'asreview lab' command in the background
        process = subprocess.Popen(["asreview", "lab"])
        
        # Wait a moment to ensure the server starts
        time.sleep(3)

        # Automatically open ASReview in a new browser tab
        webbrowser.open('http://localhost:5000')

        st.write("ASReview has started! If the app didn't open, click [here](http://localhost:5000).")
    except Exception as e:
        st.write(f"An error occurred: {e}")
