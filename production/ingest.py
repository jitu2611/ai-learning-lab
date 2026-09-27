"""Split handbook paragraphs, embed them, and upsert into local Chroma.

Run: python production/ingest.py --reset
"""

import argparse
import re
from pathlib import Path

from common import COLLECTION_NAME, ROOT, get_collection

HANDBOOK = ROOT / "data" / "handbook.md"


def read_paragraphs(path: Path) -> list[dict[str, str]]:
    """Keep each non-empty Markdown paragraph and label it with its latest H2 section."""
    section = "Introduction"
    chunks: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.strip() and not line.startswith("#"):
            text = line.strip()
            chunks.append({"section": section, "text": text})
    return chunks


def chunk_id(index: int, section: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", section.lower()).strip("-")
    return f"{index:03d}-{slug}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Delete and rebuild the local collection.")
    args = parser.parse_args()

    client, collection = get_collection()
    if args.reset:
        client.delete_collection(COLLECTION_NAME)
        _, collection = get_collection()

    chunks = read_paragraphs(HANDBOOK)
    collection.upsert(
        ids=[chunk_id(i, chunk["section"]) for i, chunk in enumerate(chunks)],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[{"section": chunk["section"], "source": HANDBOOK.name} for chunk in chunks],
    )

    print(f"Upserted {len(chunks)} chunks into {COLLECTION_NAME!r}.")
    print(f"Database directory: {ROOT / 'chroma_data'}")
    print("Each chunk was embedded by all-MiniLM-L6-v2 and persisted with its text/metadata.")


if __name__ == "__main__":
    main()
