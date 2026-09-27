"""A tiny WordPiece-like tokenizer for learning only.

Run: python learning/01_tokenization_and_ids.py

Real tokenizers use a much larger vocabulary and model-specific rules.
"""

import re

# IDs are arbitrary labels assigned by a tokenizer vocabulary.
VOCABULARY = {
    "[PAD]": 0,
    "[UNK]": 1,
    "[CLS]": 2,
    "[SEP]": 3,
    "how": 4,
    "do": 5,
    "i": 6,
    "deploy": 7,
    "changes": 8,
    "to": 9,
    "production": 10,
    "vector": 11,
    "##ization": 12,
    "?": 13,
}


def basic_tokenize(text: str) -> list[str]:
    """Lowercase and separate words/punctuation. This is intentionally simple."""
    return re.findall(r"[a-z]+|[^\w\s]", text.lower())


def wordpiece(word: str) -> list[str]:
    """Split a word into known vocabulary pieces, else return [UNK]."""
    if word in VOCABULARY:
        return [word]

    pieces: list[str] = []
    start = 0
    while start < len(word):
        end = len(word)
        found = None
        while end > start:
            candidate = word[start:end] if start == 0 else "##" + word[start:end]
            if candidate in VOCABULARY:
                found = candidate
                break
            end -= 1
        if found is None:
            return ["[UNK]"]
        pieces.append(found)
        start = end
    return pieces


def encode(text: str) -> tuple[list[str], list[int]]:
    pieces = [piece for word in basic_tokenize(text) for piece in wordpiece(word)]
    tokens = ["[CLS]", *pieces, "[SEP]"]
    return tokens, [VOCABULARY[token] for token in tokens]


if __name__ == "__main__":
    for sentence in ["How do I deploy changes to production?", "vectorization", "deployinator"]:
        tokens, ids = encode(sentence)
        print(f"\nSentence: {sentence!r}")
        print("Tokens:  ", tokens)
        print("Token IDs:", ids)
