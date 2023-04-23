"""
converter3.py: A script to convert PDF files to text using OCR
Number 3 in the series of scripts to convert PDF files to text using OCR.

See README.md for more information.
Simple and elegant.
Opens a dialog box to select a PDF file.
Converts the PDF file to text using OCR.
Prints the text to the console.
Writes the text to a text file in the program folder.

Author: Your Name <AlienAIOverlord@gmail.com>
Copyright (c) 2023, Jean-Louis Marin
License: MIT License
"""

import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import tkinter as tk
from tkinter import filedialog


# Set the path to the tesseract executable, if needed
# pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_executable>'


def ocr_image(image):
    """
    Perform OCR on an image and return the extracted text.
    """
    return pytesseract.image_to_string(image)



# User input for the file name of the PDF to be converted
# Open a file dialog to select the PDF file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])

if not file_path:
    print("no file selected. Exiting...")
    exit()

# Creating a pdf file object
#pdfFileObj = open('example.pdf', 'rb')
with open(file_path, 'rb') as pdfFileObj:
    # Creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # Printing number of pages in pdf file
    num_pages = len(pdfReader.pages)
    print("Number of pages:", num_pages)

    # Converting the PDF pages to images and performing OCR
    for page_num in range(num_pages):
        # Convert the PDF page to an image
        images = convert_from_path(file_path, first_page=page_num+1, last_page=page_num+1)

        # Perform OCR on the image
        for image in images:
            text = ocr_image(image)
            print(f"Text from page {page_num + 1}:\n{text}")
