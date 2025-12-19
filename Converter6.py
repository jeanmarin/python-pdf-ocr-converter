"""Converter6 (refactored wrapper).

Performs OCR and then sends each page's text to OpenAI for basic correction.
Writes `output_raw.txt` and `output_corrected.txt`.

The maintained implementation lives in `pdf_ocr_converter`.
"""

from __future__ import annotations

from pdf_ocr_converter.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["--mode", "corrected"]))