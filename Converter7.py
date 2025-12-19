"""Converter7 (refactored wrapper).

Performs OCR, corrects via OpenAI, and writes a diff of added/removed lines.
Outputs: `output_raw.txt`, `output_corrected.txt`, `output_diff.txt`.

The maintained implementation lives in `pdf_ocr_converter`.
"""

from __future__ import annotations

from pdf_ocr_converter.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["--mode", "all"]))