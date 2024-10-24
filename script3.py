import streamlit as st
import subprocess
import psutil
import os
import time
from pathlib import Path

def is_port_in_use(port):
    """Check if a port is in use"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    psutil.Process(proc.pid).kill()
                    time.sleep(1)  # Wait for the process to be killed
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

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

# Control buttons columns
col1, col2 = st.columns(2)

with col1:
    # Start button
    if st.button('Start ASReview Lab', disabled=st.session_state.server_running):
        try:
            # First check if port is already in use
            if is_port_in_use(5000):
                kill_process_on_port(5000)
                time.sleep(1)
            
            # Start the ASReview Lab process
            process = subprocess.Popen(
                ["asreview", "lab"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
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

with col2:
    # Stop button
    if st.button('Stop ASReview Lab', disabled=not st.session_state.server_running):
        if st.session_state.process:
            try:
                # Kill the process and its children
                parent = psutil.Process(st.session_state.process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                
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

# Display process output for debugging (optional)
if st.session_state.server_running and st.session_state.process:
    with st.expander("Server Logs"):
        try:
            output, error = st.session_state.process.communicate(timeout=0.1)
            if output:
                st.code(output)
            if error:
                st.error(error)
        except subprocess.TimeoutExpired:
            pass