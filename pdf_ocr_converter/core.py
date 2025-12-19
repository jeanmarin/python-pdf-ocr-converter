"""Core conversion pipeline for PDF -> images -> OCR -> (optional) correction/diff.

This module intentionally does not introduce new third-party dependencies; it
reuses the libraries already present in `requirements.txt`.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Callable, Iterator, Optional, Sequence, Tuple

import PyPDF2
from pdf2image import convert_from_path
import pytesseract

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConvertOptions:
    """Options controlling conversion and OCR."""

    dpi: int = 300
    first_page: int = 1
    last_page: Optional[int] = None
    poppler_path: Optional[Path] = None
    tesseract_cmd: Optional[Path] = None
    ocr_lang: Optional[str] = None


def count_pdf_pages(pdf_path: Path) -> int:
    """Return the number of pages in a PDF."""

    with pdf_path.open("rb") as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)


def iter_page_images(
    pdf_path: Path,
    *,
    page_number: int,
    dpi: int,
    poppler_path: Optional[Path],
) -> Sequence[object]:
    """Render a single PDF page as one (or more) images via pdf2image."""

    kwargs = {}
    if poppler_path is not None:
        kwargs["poppler_path"] = str(poppler_path)

    # pdf2image pages are 1-indexed.
    return convert_from_path(
        str(pdf_path),
        dpi=dpi,
        first_page=page_number,
        last_page=page_number,
        **kwargs,
    )


def ocr_image(image, *, lang: Optional[str] = None) -> str:
    """Perform OCR on one image and return extracted text."""

    if lang:
        return pytesseract.image_to_string(image, lang=lang)
    return pytesseract.image_to_string(image)


def iter_ocr_pages(
    pdf_path: Path,
    options: ConvertOptions,
    *,
    progress_cb: Optional[Callable[[int, int], None]] = None,
) -> Iterator[Tuple[int, str]]:
    """Yield `(page_number, text)` for each OCR'd PDF page.

    Page numbers are 1-indexed.
    """

    if options.tesseract_cmd is not None:
        pytesseract.pytesseract.tesseract_cmd = str(options.tesseract_cmd)

    total_pages = count_pdf_pages(pdf_path)
    last_page = options.last_page or total_pages
    if options.first_page < 1 or last_page < options.first_page:
        raise ValueError("Invalid page range: first_page/last_page.")
    if last_page > total_pages:
        raise ValueError(f"PDF only has {total_pages} pages, last_page={last_page}.")

    for page_number in range(options.first_page, last_page + 1):
        images = iter_page_images(
            pdf_path,
            page_number=page_number,
            dpi=options.dpi,
            poppler_path=options.poppler_path,
        )

        # Normally one image per page; keep the loop to match existing scripts.
        page_text_parts = []
        for image in images:
            page_text_parts.append(ocr_image(image, lang=options.ocr_lang))

        yield page_number, "".join(page_text_parts)

        if progress_cb is not None:
            progress_cb(page_number - options.first_page + 1, last_page - options.first_page + 1)


