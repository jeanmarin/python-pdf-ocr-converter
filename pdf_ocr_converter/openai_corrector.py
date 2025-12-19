"""Optional OpenAI-based post-processing for OCR text.

This keeps the existing repo behavior (Converter6/7) but isolates it so the
core OCR logic does not require network access and stays testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OpenAICorrectOptions:
    """Options for OpenAI completion-based correction (legacy OpenAI SDK)."""

    engine: str = "text-davinci-002"
    max_tokens: int = 2048
    temperature: float = 0.5


def correct_text_via_openai(
    text: str,
    *,
    api_key: str,
    options: Optional[OpenAICorrectOptions] = None,
) -> str:
    """Send text to OpenAI for basic grammar/punctuation correction."""

    if not api_key:
        raise ValueError("OpenAI API key is required for correction.")

    if options is None:
        options = OpenAICorrectOptions()

    import openai

    openai.api_key = api_key

    prompt = (
        "Please correct the following text for grammar, punctuation, and capitalization:\n\n"
        f"{text}"
    )

    response = openai.Completion.create(
        engine=options.engine,
        prompt=prompt,
        max_tokens=options.max_tokens,
        n=1,
        stop=None,
        temperature=options.temperature,
    )

    return response.choices[0].text.strip()


