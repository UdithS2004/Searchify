import re

_TOKEN_RE = re.compile(r"[a-z]+")

def tokenize(text: str) -> list[str]:
    """Lowercase and split text into alphabetic tokens."""
    if not text:
        return []
    return _TOKEN_RE.findall(text.lower())