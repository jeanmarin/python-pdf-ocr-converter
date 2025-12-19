"""Progress utilities (no third-party deps)."""

from __future__ import annotations

import sys


def print_progress_bar(
    iteration: int,
    total: int,
    *,
    prefix: str = "Processing:",
    suffix: str = "Complete",
    length: int = 50,
    fill: str = "█",
) -> None:
    """Print a simple terminal progress bar (in-place)."""

    if total <= 0:
        return
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r{prefix} |{bar}| {percent}% {suffix}")
    sys.stdout.flush()


