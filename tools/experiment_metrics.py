"""Simple measurable metrics for experiment output quality."""

from __future__ import annotations

import re

_URL_PATTERN = re.compile(r"https?://\S+")


def compute_response_metrics(response_text: str) -> dict[str, int]:
    normalized = response_text.strip()
    url_count = len(_URL_PATTERN.findall(normalized))
    return {
        "response_length_chars": len(normalized),
        "non_empty_response": int(bool(normalized)),
        "url_count": url_count,
        "contains_url": int(url_count > 0),
    }
