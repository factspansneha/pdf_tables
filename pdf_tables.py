import streamlit as st # data app development
import subprocess # process in the os
from subprocess import STDOUT, check_call #os process manipuation
import os #os process manipuation
import base64 # byte object into a pdf file 
import camelot as cam # extracting tables from PDFs 

# to run this only once and it's cached
#@st.cache_resource

import subprocess
import os

def gh():
    """Install Ghostscript on the Windows machine"""
    # Path to the Ghostscript installer
    installer_path = "path/to/ghostscript-installer.exe"  # Replace this with the actual path

    # Check if the installer file exists
    if not os.path.exists(installer_path):
        print("Ghostscript installer not found at specified path.")
        return

    # Command to run the installer silently
    command = f'"{installer_path}" /S'

    # Launching the subprocess to execute the command
    proc = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Wait for the process to finish
    stdout, stderr = proc.communicate()

    # Check if the installation was successful
    if proc.returncode == 0:
        print("Ghostscript installation successful.")
    else:
        print("Failed to install Ghostscript.")
        print("Error message:", stderr)

# Call the function to install Ghostscript
gh()





st.title("PDF Table Extractor")
st.subheader("with `Camelot` Python library")

st.image("https://raw.githubusercontent.com/camelot-dev/camelot/master/docs/_static/camelot.png", width=200)


# file uploader on streamlit 

input_pdf = st.file_uploader(label = "upload your pdf here", type = 'pdf')

st.markdown("### Page Number")

page_number = st.text_input("Enter the page # from where you want to extract the PDF eg: 3", value = 1)

# run this only when a PDF is uploaded

if input_pdf is not None:
    # byte object into a PDF file 
    with open("input.pdf", "wb") as f:
        base64_pdf = base64.b64encode(input_pdf.read()).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))
    f.close()

    # read the pdf and parse it using stream
    table = cam.read_pdf("input.pdf", pages = page_number, flavor = 'stream')

    st.markdown("### Number of Tables")

    # display the output after parsing 
    st.write(table)

    # display the table

    if len(table) > 0:

        # extract the index value of the table
        
        option = st.selectbox(label = "Select the Table to be displayed", options = range(len(table) + 1))

        st.markdown('### Output Table')

        # display the dataframe
        
        st.dataframe(table[int(option)-1].df)