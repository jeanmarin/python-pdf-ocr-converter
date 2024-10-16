<img src="images/OCR_Chimp.png" alt="OCR Chimp going at it!" width="900px">
<small><i>OCR Chimp going at it!</i></small>
<img src="https://img.shields.io/badge/Status-works%20after%20lot%20of%20debugging-red"> <img src="https://img.shields.io/badge/Python%20Skill-intermediate%20-brightgreen"> 
# PDF-to-Text OCR Converter Series

A series of scripts to convert PDF files to text using Optical Character Recognition (OCR). Each script in the series provides different functionality and improvements over previous versions.

## Overview of Scripts

1. `converter1.py`: Initial attempt with errors; converts a PDF to a series of images and then uses OCR to convert the images to text.
2. `converter2.py`: Early attempt; calling the `pageObj` throws an error.
3. `converter3.py`: Simple and elegant script; opens a dialog box to select a PDF file, converts it to text using OCR, prints the text to the console, and writes the text to a text file in the program folder.
4. `converter4.py`: Improved version of `converter3.py` with added page separators in the text file.
5. `converter5.py`: Further improvement of `converter4.py` with a progress bar in the terminal.
6. `converter6.py`: Builds on `converter5.py` by sending the text to ChatGPT for corrections and writing the corrected text to a separate text file in the program folder. **Warning**: This script requires a paid OpenAI API key and may take up to three times longer than the other scripts. It generates two output files: `Output_Raw.txt` and `Output_Corrected.txt`.
7. `converter7.py`: Enhances `converter6.py` by performing a diff between the raw text and the corrected text.

## Requirements

- Python 3.6 or higher
- Libraries: PyPDF2, pytesseract, pdf2image, PIL, tkinter, dotenv (for `converter6.py` and `converter7.py`)

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone this repository or download the scripts individually.
2. Install the required libraries (if not already installed).
3. Run the desired script from the command line or your favorite Python IDE:

```bash
python converterX.py
```

Replace `X` with the number of the script version you want to run.

4. For `converter3.py` and later versions, the script will open a file dialog to select a PDF file.
5. The script will then convert the PDF file to text using OCR, printing the text to the console and writing it to a text file in the program folder. Later versions will have additional features as described in the overview above.

## Notes

- For Windows users, you may need to install the Tesseract OCR engine and set the path to the Tesseract executable in the scripts. For more information, visit [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract).
- The performance and accuracy of the OCR conversion may vary depending on the quality of the input PDF file and the OCR engine used.
- **IMPORTANT**: Never share your ChatGPT API key. When using `converter6.py` or `converter7.py`, add your API key to a `.env` file based on the provided `.env.template` file.

## Test Files

Two sample PDF files are included for testing:

1. `Poem1.PDF`: A one-page poem for quick testing.
2. `The_Art_of_War_by_Sun_Tzu.PDF`: A longer text for more extensive testing.

## License

MIT License. See `LICENSE` for more information.
