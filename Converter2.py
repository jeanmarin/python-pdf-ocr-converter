"""
converter2.py: A script to convert PDF files to text using OCR
Number 2 in the series of scripts to convert PDF files to text using OCR.

See README.md for more information.
Early attempt but calling the pageObj throws an error. 

Author: Your Name <AlienAIOverlord@gmail.com>
Copyright (c) 2023, Jean-Louis Marin
License: MIT License
"""

# importing required modules
import PyPDF2

# creating a pdf file object
pdfFileObj = open('example.pdf', 'rb')

# creating a pdf reader object
PdfReader = PyPDF2.PdfReader(pdfFileObj)

# printing number of pages in pdf file
print(PdfReader.pages)

# creating a page object
pageObj = PdfReader.pages(0)

# extracting text from page
print(pageObj.extractText())

# closing the pdf file object
pdfFileObj.close()
