"""Small library for basic text analysis."""
import re
from collections import Counter


def count_words(text: str) -> int:
    """Count the number of words in a text."""
    words = re.findall(r"\b\w+\b", text)
    return len(words)


def most_common_words(text: str, top_n: int = 3) -> list[tuple[str, int]]:
    """Return the top_n most frequent words (lowercased)."""
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words).most_common(top_n)


def average_word_length(text: str) -> float:
    """Average word length in a text."""
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)
