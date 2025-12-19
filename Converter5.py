"""Converter5 (refactored wrapper).

Adds a terminal progress bar and writes to `output.txt`.
The maintained implementation lives in `pdf_ocr_converter`.
"""

from __future__ import annotations

from pdf_ocr_converter.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["--mode", "raw", "--raw-out", "output.txt"]))
