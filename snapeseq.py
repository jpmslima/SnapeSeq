import streamlit as st
from Bio import SeqIO
import os

st.title("SeverusSnapSequences")
st.write("Upload a multifasta file and search for a sequence by its complete or partial name.")

# Upload the multifasta file:
uploaded_file = st.file_uploader("Upload your multifasta file", type=["fasta"])

# Field for search the sequences using name:
search_term = st.text_input("Enter the sequence name (complete or partial):")

def retrieve_fasta(input_file, output_file, search_term):

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        found = False
        for record in SeqIO.parse(infile, "fasta"):
            if search_term in record.id or search_term in record.description:
                SeqIO.write(record, outfile, "fasta")
                found = True
                break
        return found
    
    if uploaded_file and search_term:
        # Save the uploaded file temporarily
        input_file_path = "uploaded_file.fasta"
        with open(input_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
        # Define the output file path
        output_file_path = "output.fasta"
    
        # Call the retrieve_fasta function
        if retrieve_fasta(input_file_path, output_file_path, search_term):
            st.success(f"Sequence found and saved to {output_file_path}!")
            
            # Provide a download link for the output file
            with open(output_file_path, "rb") as f:
                st.download_button(
                    label="Download Output Fasta File",
                    data=f,
                    file_name="output.fasta",
                    mime="text/plain"
                )
        else:
            st.error("No matching sequence found.")
    
        # Clean up temporary files
        os.remove(input_file_path)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)