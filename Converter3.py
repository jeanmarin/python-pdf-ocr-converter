"""Converter3 (refactored wrapper).

Historically, `Converter3.py` was the first "simple and elegant" script in the
series. The maintained implementation now lives in `pdf_ocr_converter`.

This wrapper keeps the same workflow (file dialog if no input) and produces a
raw OCR output file with page separators.
"""

from __future__ import annotations

from pdf_ocr_converter.cli import main


if __name__ == "__main__":
    # Raw-only mode, written to output_raw.txt (matches the rest of the series).
    raise SystemExit(main(["--mode", "raw", "--raw-out", "output_raw.txt"]))
