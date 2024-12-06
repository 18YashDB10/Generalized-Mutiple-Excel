import os
import pandas as pd
import zipfile
from io import BytesIO
from docxtpl import DocxTemplate
import streamlit as st

# Redirect to login if not authenticated
if not st.session_state.get("authenticated", False):
    st.warning("Please log in first.")
    st.stop()

def generate_word_files(template_path, excel_path, output_dir):
    """
    Generate multiple Word files based on a Word template and an Excel file.
    
    Args:
        template_path (str): Path to the Word template.
        excel_path (str): Path to the Excel file.
        output_dir (str): Directory where the generated files will be saved.
    
    Returns:
        List[str]: List of paths to the generated Word files.
    """
    # Load the Word template
    template = DocxTemplate(template_path)

    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List to hold paths of generated files
    generated_files = []

    # Iterate through the rows of the dataframe
    for index, record in df.iterrows():
        # Convert record to a dictionary
        context = record.to_dict()

        # Render the template with the context
        template.render(context)

        # Define the output file path
        output_file_path = os.path.join(output_dir, f"record_{index + 1}.docx")

        # Save the rendered document
        template.save(output_file_path)

        # Add the file path to the list
        generated_files.append(output_file_path)

    return generated_files

def zip_files(file_paths):
    """
    Create a zip file containing the specified files.

    Args:
        file_paths (List[str]): List of file paths to include in the zip.

    Returns:
        BytesIO: A BytesIO object containing the zip file.
    """
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for file_path in file_paths:
            zipf.write(file_path, os.path.basename(file_path))

    zip_buffer.seek(0)
    return zip_buffer

# Streamlit application
st.title("Excel to Word Generator")

# Upload the Word template
word_file = st.file_uploader("Upload Word Template", type="docx")

# Upload the Excel file
excel_file = st.file_uploader("Upload Excel File", type=["xls", "xlsx"])

if word_file and excel_file:
    # Create a temporary directory
    with st.spinner("Processing files..."):
        temp_dir = "temp_output"

        # Save uploaded files to temporary paths
        word_template_path = os.path.join(temp_dir, "template.docx")
        excel_path = os.path.join(temp_dir, "data.xlsx")

        os.makedirs(temp_dir, exist_ok=True)
        with open(word_template_path, "wb") as f:
            f.write(word_file.read())
        with open(excel_path, "wb") as f:
            f.write(excel_file.read())

        # Generate Word files
        generated_files = generate_word_files(word_template_path, excel_path, temp_dir)

        # Create a zip of the generated files
        zip_buffer = zip_files(generated_files)
        
        # Clean up temporary files
        for file_path in generated_files:
            os.remove(file_path)
        os.remove(word_template_path)
        os.remove(excel_path)
        os.rmdir(temp_dir)

        # Provide the zip file for download
        st.success("Word files generated successfully!")
        st.download_button(
            label="Download All Word Files",
            data=zip_buffer,
            file_name="word_files.zip",
            mime="application/zip"
        )

        
        
