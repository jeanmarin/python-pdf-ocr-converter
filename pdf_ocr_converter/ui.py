"""UI helpers (optional).

We keep UI concerns (file dialog) isolated so the core logic stays testable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def select_pdf_file_via_dialog() -> Optional[Path]:
    """Open a file dialog to select a PDF file.

    Returns:
        The selected file path, or None if the user cancels.
    """

    # Tkinter is part of the Python stdlib on Windows, but may not be present
    # in minimal installs. We import lazily so `pdf_ocr_converter` can still be
    # used in headless environments when an explicit input path is provided.
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    selected = filedialog.askopenfilename(
        title="Select a PDF file", filetypes=[("PDF files", "*.pdf")]
    )
    return Path(selected) if selected else None


