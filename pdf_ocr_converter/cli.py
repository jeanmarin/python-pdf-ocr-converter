"""Command-line interface for the OCR converter."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from pdf_ocr_converter.core import ConvertOptions, iter_ocr_pages
from pdf_ocr_converter.diffing import changed_lines, write_page_block
from pdf_ocr_converter.openai_corrector import correct_text_via_openai
from pdf_ocr_converter.progress import print_progress_bar
from pdf_ocr_converter.ui import select_pdf_file_via_dialog

logger = logging.getLogger(__name__)


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-ocr-converter",
        description="Convert a PDF to text using OCR (optionally correct via OpenAI, optionally diff).",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to a PDF file. If omitted, a file dialog is shown.",
    )
    parser.add_argument("--dpi", type=int, default=300, help="DPI for PDF rendering (default: 300).")
    parser.add_argument("--first-page", type=int, default=1, help="First page to process (1-indexed).")
    parser.add_argument("--last-page", type=int, default=None, help="Last page to process (1-indexed).")
    parser.add_argument(
        "--poppler-path",
        type=str,
        default=None,
        help="Poppler bin folder (Windows). If set, passed to pdf2image.",
    )
    parser.add_argument(
        "--tesseract-cmd",
        type=str,
        default=None,
        help="Path to tesseract.exe (Windows). If set, passed to pytesseract.",
    )
    parser.add_argument(
        "--ocr-lang",
        type=str,
        default=None,
        help="Tesseract language code (e.g. 'eng').",
    )
    parser.add_argument(
        "--mode",
        choices=("raw", "corrected", "diff", "all"),
        default="raw",
        help="Output mode.",
    )
    parser.add_argument("--raw-out", default="output_raw.txt", help="Raw text output file.")
    parser.add_argument("--corrected-out", default="output_corrected.txt", help="Corrected text output file.")
    parser.add_argument("--diff-out", default="output_diff.txt", help="Diff output file.")
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable terminal progress bar.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logs.",
    )
    return parser


def _resolve_input_path(input_arg: Optional[str]) -> Path:
    if input_arg:
        return Path(input_arg)

    selected = select_pdf_file_via_dialog()
    if selected is None:
        raise SystemExit("No file selected. Exiting...")
    return selected


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    _configure_logging(args.verbose)
    load_dotenv()  # allow OPENAI_API_KEY from a local .env

    pdf_path = _resolve_input_path(args.input)
    if not pdf_path.exists():
        raise SystemExit(f"Input PDF does not exist: {pdf_path}")

    options = ConvertOptions(
        dpi=args.dpi,
        first_page=args.first_page,
        last_page=args.last_page,
        poppler_path=Path(args.poppler_path) if args.poppler_path else None,
        tesseract_cmd=Path(args.tesseract_cmd) if args.tesseract_cmd else None,
        ocr_lang=args.ocr_lang,
    )

    want_raw = args.mode in ("raw", "all")
    want_corrected = args.mode in ("corrected", "all")
    want_diff = args.mode in ("diff", "all")

    # Open outputs only as needed.
    raw_fp = open(args.raw_out, "w", encoding="utf-8") if want_raw else None
    corrected_fp = open(args.corrected_out, "w", encoding="utf-8") if want_corrected else None
    diff_fp = open(args.diff_out, "w", encoding="utf-8") if want_diff else None

    try:
        def _progress(i: int, total: int) -> None:
            if not args.no_progress:
                print_progress_bar(i, total)

        api_key = os.getenv("OPENAI_API_KEY", "")

        for page_number, raw_text in iter_ocr_pages(pdf_path, options, progress_cb=_progress):
            if want_raw and raw_fp is not None:
                raw_fp.write(f"\n*********** PAGE {page_number} ***********\n")
                raw_fp.write(raw_text)

            corrected_text = None
            if want_corrected or want_diff:
                corrected_text = correct_text_via_openai(raw_text, api_key=api_key)

            if want_corrected and corrected_fp is not None and corrected_text is not None:
                corrected_fp.write(f"\n*********** PAGE {page_number} ***********\n")
                corrected_fp.write(corrected_text)

            if want_diff and diff_fp is not None and corrected_text is not None:
                lines = changed_lines(raw_text, corrected_text)
                write_page_block(diff_fp, page_number, lines)

        if not args.no_progress:
            print()  # newline after progress bar
        return 0
    finally:
        for fp in (raw_fp, corrected_fp, diff_fp):
            if fp is not None:
                fp.close()


if __name__ == "__main__":
    raise SystemExit(main())


