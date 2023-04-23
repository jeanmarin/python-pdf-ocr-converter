"""
converter5.py: A script to convert PDF files to text using OCR
Number 5 in the series of scripts to convert PDF files to text using OCR.

See README.md for more information.
Simple and elegant.
Opens a dialog box to select a PDF file.
Converts the PDF file to text using OCR.
Prints the text to the console.
Adds a page separator to the text file.
Writes the text to a text file in the program folder.
This version has a progress bar in the terminal.

Author: Your Name <AlienAIOverlord@gmail.com>
Copyright (c) 2023, Jean-Louis Marin
License: MIT License
"""

import PyPDF2
import pytesseract
import sys
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


# Function to print a progress bar
def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
      
    percent = ('{0:.1f}').format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

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

    # Open a text file for writing the extracted text
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        # Converting the PDF pages to images and performing OCR
        for page_num in range(num_pages):
            # Convert the PDF page to an image
            images = convert_from_path(file_path, first_page=page_num+1, last_page=page_num+1)

            # Perform OCR on the image
            for image in images:
                text = ocr_image(image)
                # Write the page separator and extracted text to the output file
                output_file.write(f"\n*********** PAGE {page_num + 1} ***********\n")
                output_file.write(text)

            # Update the progress bar
            print_progress_bar(page_num + 1, num_pages, prefix='Processing:', suffix='Complete')

    # Print a newline character to move the cursor to the next line
    print()


