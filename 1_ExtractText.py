'''
Just Text (Works)
Tabulart Text (Works) but Table Information also

'''


import fitz
import os
import numpy as np
import json
def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    mypdf = fitz.open(pdf_path)
    all_text = ""  # Initialize an empty string to store the extracted text

    # Iterate through each page in the PDF
    for page_num in range(mypdf.page_count):
        page = mypdf[page_num]  # Get the page
        text = page.get_text("text")  # Extract text from the page
        all_text += text  # Append the extracted text to the all_text string

    return all_text  # Return the extracted text


# Define the path to the PDF file
pdf_path = "data/AboutBangladesh.pdf"
# Extract text from the PDF file
extracted_text = extract_text_from_pdf(pdf_path)
print("Extracted text from PDF:")
print(extracted_text)  # Print the first 1000 characters of the extracted text
