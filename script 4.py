import streamlit as st
import subprocess
import time
import requests
import os
from pathlib import Path

st.set_page_config(
    page_title="ASReview Lab Launcher",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 ASReview Lab")

st.warning("""
### Important Note
Due to Streamlit Cloud's security restrictions, we cannot run ASReview Lab directly on this platform. 

Instead, you have two options:

1. **Run locally on your computer:**
```bash
pip install asreview
asreview lab
```
Then open http://localhost:5000 in your browser.

2. **Use ASReview Cloud:**
Visit [ASReview LAB](https://asreview.nl/asreview-lab/) to use the cloud version directly.

For more information, visit the [ASReview documentation](https://asreview.readthedocs.io/).
""")

st.markdown("---")

with st.expander("ℹ️ Why can't this run on Streamlit Cloud?"):
    st.markdown("""
    Streamlit Cloud has certain limitations that prevent running ASReview Lab directly:
    
    1. **Port Access**: Streamlit Cloud doesn't allow opening additional ports needed by ASReview Lab
    2. **Process Management**: Long-running processes are not supported
    3. **Security Restrictions**: Direct network access is limited
    
    For the best experience, we recommend running ASReview Lab locally or using their cloud version.
    """)

with st.expander("📚 Quick Guide to Local Installation"):
    st.markdown("""
    1. **Install Python** if you haven't already
    2. **Open your terminal/command prompt**
    3. **Install ASReview:**
       ```bash
       pip install asreview
       ```
    4. **Start ASReview Lab:**
       ```bash
       asreview lab
       ```
    5. **Open in browser:**
       - Go to http://localhost:5000
    """)