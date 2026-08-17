"""
File analyzer tool tests.
"""


from app.tools.file_analyzer import analyze_text

TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox is fast. "
    "Mathematics powers artificial intelligence."
)


def test_basic_metrics():
    result = analyze_text(TEXT)

    assert result["words"] == 19
    assert result["sentences"] == 3
    assert result["unique_words"] <= result["words"]
    assert result["characters"] > 0
    assert result["estimated_reading_minutes"] > 0


def test_most_common_words():
    result = analyze_text(TEXT)

    top = result["most_common_words"][0]

    assert top["word"] == "the"
    assert top["count"] == 3


def test_empty_content():
    result = analyze_text("   ")
    assert "error" in result


def test_lines_count():
    result = analyze_text("line one\nline two\nline three")
    assert result["lines"] == 3
