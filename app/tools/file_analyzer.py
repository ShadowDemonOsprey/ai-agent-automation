"""
File analyzer tool.

Analyzes text content and returns useful metrics.

Used by the agent for requests such as
"analyze this text" or "summarize the document stats".

Metrics provided:
- Character, word, line and sentence counts
- Unique word count
- Average word length
- Most common words
- Estimated reading time
"""


import re
from collections import Counter

WORDS_PER_MINUTE = 200


def analyze_text(content: str) -> dict:
    """
    Compute statistics for a block of text.

    Args:
        content (str):
            Text to analyze.

    Returns:
        dict:
            Text metrics.
    """

    content = content.strip()

    if not content:

        return {
            "tool": "file_analyzer",
            "error": "No content provided"
        }

    words = re.findall(
        r"\b[a-zA-Z0-9']+\b",
        content
    )

    sentences = [
        sentence for sentence in re.split(
            r"[.!?]+",
            content
        )
        if sentence.strip()
    ]

    characters = len(content)

    word_lengths = [len(word) for word in words]

    word_counts = Counter(
        word.lower()
        for word in words
    )

    most_common = word_counts.most_common(10)

    reading_minutes = (
        len(words) / WORDS_PER_MINUTE
        if words else 0.0
    )

    return {
        "tool": "file_analyzer",
        "characters": characters,
        "words": len(words),
        "unique_words": len(word_counts),
        "lines": len(content.splitlines()),
        "sentences": len(sentences),
        "average_word_length": (
            round(sum(word_lengths) / len(word_lengths), 2)
            if word_lengths else 0
        ),
        "most_common_words": [
            {"word": word, "count": count}
            for word, count in most_common
        ],
        "estimated_reading_minutes": (
            round(reading_minutes, 2)
            if reading_minutes else 0
        ),
    }
