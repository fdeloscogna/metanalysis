import streamlit as st
import subprocess
import time
import requests
import os
from pathlib import Path

def check_server_running(url="http://localhost:5000"):
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except:
        return False

# Initialize session state variables
if 'process' not in st.session_state:
    st.session_state.process = None
if 'server_running' not in st.session_state:
    st.session_state.server_running = False

# Title and description
st.set_page_config(
    page_title="ASReview Lab Launcher",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 ASReview Lab")
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 3em;
        margin-top: 1em;
    }
</style>
""", unsafe_allow_html=True)

# Server status indicator
status_placeholder = st.empty()

# Main container for the app
main_container = st.container()

with main_container:
    # Start button
    if st.button('▶️ Launch ASReview Lab', disabled=st.session_state.server_running):
        try:
            # Create a data directory if it doesn't exist
            data_dir = Path("asreview_data")
            data_dir.mkdir(exist_ok=True)
            
            # Start the ASReview Lab process
            process = subprocess.Popen(
                [
                    "asreview", "lab",
                    "--host", "0.0.0.0",
                    "--port", "5000"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            st.session_state.process = process
            st.session_state.server_running = True
            
            # Wait for server to start
            with st.spinner('Starting ASReview Lab...'):
                attempts = 0
                while attempts < 10:
                    if check_server_running():
                        break
                    time.sleep(1)
                    attempts += 1
            
            st.success("✅ ASReview Lab is ready!")
            
            # Display the access link
            st.markdown("""
            ### 🌐 Access ASReview Lab
            Click the link below to open ASReview Lab:
            
            [Open ASReview Lab](http://localhost:5000)
            
            Keep this tab open while using ASReview Lab.
            """)
            
        except Exception as e:
            st.error(f"❌ Error starting ASReview Lab: {str(e)}")
            st.session_state.server_running = False

    # Stop button
    if st.button('⏹️ Stop ASReview Lab', disabled=not st.session_state.server_running):
        if st.session_state.process:
            try:
                # Terminate the process
                st.session_state.process.terminate()
                try:
                    st.session_state.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    st.session_state.process.kill()
                
                st.session_state.process = None
                st.session_state.server_running = False
                
                st.success("✅ ASReview Lab has been stopped!")
                
            except Exception as e:
                st.error(f"❌ Error stopping ASReview Lab: {str(e)}")

    # Update status indicator
    if st.session_state.server_running:
        status_placeholder.success("📡 Status: ASReview Lab is running")
    else:
        status_placeholder.info("💤 Status: ASReview Lab is not running")

    # Help section
    with st.expander("ℹ️ Help & Information"):
        st.write("""
        **Quick Guide:**
        1. Click 'Launch ASReview Lab' to start
        2. Wait for the success message
        3. Click the provided link to open ASReview Lab
        4. When finished, return to this page and click 'Stop ASReview Lab'
        
        **Note:**
        - Keep this tab open while using ASReview Lab
        - All your ASReview projects will be saved automatically
        - If you encounter any issues, try stopping and restarting ASReview Lab
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Built with ❤️ using Streamlit and ASReview</p>
        </div>
        """,
        unsafe_allow_html=True
    )

requirements = st.sidebar.expander("📦 Requirements", expanded=False)
with requirements:
    st.code("""
    streamlit==1.31.0
    asreview==1.1.1
    """)