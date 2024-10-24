import streamlit as st
import subprocess
import time

# Initialize session state variables
if 'process' not in st.session_state:
    st.session_state.process = None
if 'server_running' not in st.session_state:
    st.session_state.server_running = False

# Title and description
st.title("ASReview Lab Interface")
st.write("Control your ASReview Lab instance from this Streamlit app.")

# Server status indicator
status_placeholder = st.empty()

# Start button
if st.button('Start ASReview Lab', disabled=st.session_state.server_running):
    try:
        # Start the ASReview Lab process
        process = subprocess.Popen(
            ["asreview", "lab"],
            shell=False
        )
        
        # Store the process in session state
        st.session_state.process = process
        st.session_state.server_running = True
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Show success message
        st.success("ASReview Lab has started successfully!")
        
        # Display the link
        st.markdown("[Open ASReview Lab in new tab](http://localhost:5000)", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Failed to start ASReview Lab: {str(e)}")
        st.session_state.server_running = False

# Stop button
if st.button('Stop ASReview Lab', disabled=not st.session_state.server_running):
    if st.session_state.process:
        try:
            # Terminate the process
            st.session_state.process.terminate()
            
            # Wait for the process to terminate
            st.session_state.process.wait(timeout=5)
            
            # Clean up the session state
            st.session_state.process = None
            st.session_state.server_running = False
            
            # Show success message
            st.success("ASReview Lab has been stopped successfully!")
            
        except Exception as e:
            st.error(f"Failed to stop ASReview Lab: {str(e)}")

# Update status indicator
if st.session_state.server_running:
    status_placeholder.success("Status: ASReview Lab is running")
    st.markdown("Access ASReview Lab at: [http://localhost:5000](http://localhost:5000)")
else:
    status_placeholder.info("Status: ASReview Lab is not running")

# Display additional information
with st.expander("How to use ASReview Lab"):
    st.write("""
    1. Click 'Start ASReview Lab' to launch the server
    2. Click the link above or go to http://localhost:5000 in your browser
    3. Use ASReview Lab as normal
    4. When finished, click 'Stop ASReview Lab' to shut down the server
    
    Note: If you encounter any issues, try stopping and restarting the server.
    """)