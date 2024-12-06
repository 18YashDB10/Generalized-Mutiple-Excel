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

# Get credentials from environment variables
EMAIL = st.secrets['EMAIL']
PASSWORD = st.secrets['PASSWORD']


st.title("Login")

# Input fields for login
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    if email == EMAIL and password == PASSWORD:
        st.success("Login successful!")
        st.session_state.authenticated = True
        st.write("[Go to Excel to Word Converter](Excel_to_Word)")
    else:
        st.error("Invalid email or password.")
