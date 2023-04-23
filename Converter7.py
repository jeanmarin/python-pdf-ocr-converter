"""
converter7.py: A script to convert PDF files to text using OCR
Number 7 in the series of scripts to convert PDF files to text using OCR.

See README.md for more information.
Simple and elegant.
Opens a dialog box to select a PDF file.
Converts the PDF file to text using OCR.
Prints the text to the console.
Adds a page separator to the text file.
Writes the text to a text file in the program folder.
Progress bar in the terminal.
Sends the text to ChatGPT for corrections.
Writes the corrected text to a text file in the program folder.
NOTED ChatGPT does not do that good of a job with the formatting.
The more complex the image page is with indents and tables, the worse the results.
I found it was better if I did the corrects manually.
***WARNING*** This script will cost you money as you need a paid OpenAI API KEY.
Expect this to take 3 times as long as the other scripts.
two output files: Output_Raw.txt and Output_Corrected.txt
This version it will do a diff between the raw text and the corrected text.

Author: Your Name <AlienAIOverlord@gmail.com>
Copyright (c) 2023, Jean-Louis Marin
License: MIT License
"""

import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import sys
import openai
import difflib
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog

# Set your OpenAI API key and the path to the tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_executable>'
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def ocr_image(image):
    """
    Perform OCR on an image and return the extracted text.
    """
    return pytesseract.image_to_string(image)


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


def correct_text(text):
    """
    Send the text to ChatGPT for corrections.
    """
    prompt = f"Please correct the following text for grammar, punctuation, and capitalization:\n\n{text}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    corrected_text = response.choices[0].text.strip()
    return corrected_text


def log_differences(raw_text, corrected_text, page_num, output_file):
    """
    Log the differences between the raw text and the corrected text.
    """
    
    differences = list(difflib.ndiff(raw_text.splitlines(), corrected_text.splitlines()))
    output_file.write(f"\n*********** PAGE {page_num + 1} ***********\n")
    for line in differences:
        if line.startswith('+ ') or line.startswith('- '):
            output_file.write(line + '\n')


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
    with open('output_raw.txt', 'w', encoding='utf-8') as raw_output_file, open('output_corrected.txt', 'w', encoding='utf-8') as corrected_output_file, open('output_diff.txt', 'w', encoding='utf-8') as diff_output_file:
        for page_num in range(num_pages):
            images = convert_from_path(file_path, first_page=page_num+1, last_page=page_num+1)

            for image in images:
                text = ocr_image(image)
                raw_output_file.write(f"\n*********** PAGE {page_num + 1} ***********\n")
                raw_output_file.write(text)

                corrected_text = correct_text(text)
                corrected_output_file.write(f"\n*********** PAGE {page_num + 1} ***********\n")
                corrected_output_file.write(corrected_text)

                log_differences(text, corrected_text, page_num, diff_output_file)

            print_progress_bar(page_num + 1, num_pages, prefix='Processing:', suffix='Complete')

    print()


