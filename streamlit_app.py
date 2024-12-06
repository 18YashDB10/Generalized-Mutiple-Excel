import streamlit as st
from dotenv import load_dotenv
import os
import shutil


try:
    shutil.rmtree(os.path.join(os.getcwd(),"temp_output"))
except Exception as e:
    print(e)
    pass

# Load environment variables
load_dotenv()

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Redirect to login if not authenticated
if not st.session_state.authenticated:
    st.sidebar.warning("Please log in to access the application.")
    st.sidebar.write("[Login Page](Login)")
