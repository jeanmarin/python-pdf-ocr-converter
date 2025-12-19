"""Convenience entrypoint for the refactored converter.

This keeps a simple `python run_converter.py` workflow while the real logic
lives in `pdf_ocr_converter`.
"""

from __future__ import annotations

from pdf_ocr_converter.cli import main


if __name__ == "__main__":
    raise SystemExit(main())


