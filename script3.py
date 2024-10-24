import streamlit as st
import subprocess
import time
import socket
import requests

def check_server_running(url="http://localhost:5000"):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

def get_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "localhost"

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
        # Start the ASReview Lab process with specific host binding
        process = subprocess.Popen(
            [
                "asreview", "lab",
                "--host", "0.0.0.0",  # Bind to all interfaces
                "--port", "5000"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Store the process in session state
        st.session_state.process = process
        st.session_state.server_running = True
        
        # Wait a moment for the server to start
        time.sleep(5)  # Increased wait time
        
        # Check if server is actually running
        if check_server_running():
            st.success("ASReview Lab has started successfully!")
        else:
            st.warning("Server started but might not be accessible yet. Please wait a few moments and try the link below.")
        
        # Display connection information
        ip_address = get_ip()
        st.markdown("### Connection Information")
        st.markdown(f"""
        Try accessing ASReview Lab using any of these links:
        - [Local Access (localhost)](http://localhost:5000)
        - [Network Access (IP)](http://{ip_address}:5000)
        
        If the links don't work immediately, please wait a few seconds and refresh the page.
        """)
        
        # Display debug information in expander
        with st.expander("Debug Information"):
            st.write(f"Server IP: {ip_address}")
            st.write("Server Port: 5000")
            st.write(f"Full URL: http://{ip_address}:5000")
            
            # Try to get process output
            try:
                out, err = process.communicate(timeout=0.1)
                if out:
                    st.write("Server Output:", out.decode())
                if err:
                    st.write("Server Errors:", err.decode())
            except subprocess.TimeoutExpired:
                process.stdout.close()
                process.stderr.close()
                
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
else:
    status_placeholder.info("Status: ASReview Lab is not running")

# Display additional information
with st.expander("How to use ASReview Lab"):
    st.write("""
    1. Click 'Start ASReview Lab' to launch the server
    2. Wait a few moments for the server to fully start
    3. Try both the localhost and IP address links provided above
    4. If the links don't work immediately, wait a few seconds and refresh the page
    5. When finished, click 'Stop ASReview Lab' to shut down the server
    
    Troubleshooting:
    - If you can't connect, try waiting 10-15 seconds and refreshing the page
    - Make sure no other service is using port 5000
    - Check the Debug Information section for more details
    """)