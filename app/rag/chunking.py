"""
Text chunking.

Splits long documents into overlapping chunks so they
can be embedded and searched by the vector store.

Strategy:
- Split the text into sentences.
- Group sentences into chunks up to chunk_size characters.
- Carry an overlap (tail) of the previous chunk into the
  next one so boundary context is preserved.
"""


import re


def _split_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    parts = re.split(
        r"(?<=[.!?])\s+|\n\s*\n",
        text.strip()
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]



def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text:
            Document text.
        chunk_size:
            Maximum characters per chunk.
        overlap:
            Characters of overlap between chunks.

    Returns:
        list of chunk strings.
    """

    if not text or not text.strip():
        return []

    sentences = _split_sentences(text)

    chunks: list[str] = []

    current: list[str] = []

    current_size = 0

    for sentence in sentences:

        sentence = sentence.strip()

        # A single sentence larger than the chunk size
        # is split by brute force.
        if len(sentence) > chunk_size:

            # Flush what we have.
            if current:

                chunks.append(" ".join(current))

                current = []

                current_size = 0

            for start in range(0, len(sentence), chunk_size):

                chunks.append(
                    sentence[start:start + chunk_size]
                )

            continue

        projected = current_size + len(sentence)

        # Include separator space.
        if current:

            projected += 1

        if projected <= chunk_size:

            current.append(sentence)

            current_size = projected

        else:

            chunks.append(" ".join(current))

            # Carry overlap from the finished chunk.
            tail = " ".join(current)

            overlap_text = tail[-overlap:] if len(tail) > overlap else tail

            current = []

            current_size = 0

            if overlap_text.strip():

                current.append(overlap_text)

                current_size = len(overlap_text) + 1

            current.append(sentence)

            current_size += len(sentence)

    if current:

        chunks.append(" ".join(current))

    return chunks
