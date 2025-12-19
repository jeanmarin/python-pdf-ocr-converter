"""Diff utilities for comparing OCR output vs corrected output."""

from __future__ import annotations

import difflib
from typing import Iterable, Iterator, List


def iter_changed_lines(raw_text: str, corrected_text: str) -> Iterator[str]:
    """Yield only added/removed lines from a unified ndiff.

    `difflib.ndiff()` yields:
    - "  " unchanged lines
    - "- " removed lines
    - "+ " added lines
    - "? " intraline hints

    For the repo's use-case (reviewing changes), we keep only "+ " and "- ".
    """

    for line in difflib.ndiff(raw_text.splitlines(), corrected_text.splitlines()):
        if line.startswith("+ ") or line.startswith("- "):
            yield line


def changed_lines(raw_text: str, corrected_text: str) -> List[str]:
    """Return changed lines as a list (wrapper around `iter_changed_lines`)."""

    return list(iter_changed_lines(raw_text=raw_text, corrected_text=corrected_text))


def format_page_header(page_number: int) -> str:
    """Return the standard page header used across scripts."""

    return f"*********** PAGE {page_number} ***********"


def write_page_block(output_file, page_number: int, lines: Iterable[str]) -> None:
    """Write a header + the given lines to an open text file."""

    output_file.write("\n" + format_page_header(page_number) + "\n")
    for line in lines:
        output_file.write(line + "\n")


