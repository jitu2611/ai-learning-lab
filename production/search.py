"""Retrieve semantically similar handbook paragraphs.

Run: python production/search.py "How can I deploy changes to production?"
"""

import argparse

from common import get_collection


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Natural-language question to search for.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve.")
    parser.add_argument("--section", help="Optional exact section metadata filter, e.g. Accounts.")
    args = parser.parse_args()

    _, collection = get_collection()
    if collection.count() == 0:
        raise SystemExit("Collection is empty. Run: python production/ingest.py --reset")

    results = collection.query(
        query_texts=[args.query],
        n_results=min(args.top_k, collection.count()),
        where={"section": args.section} if args.section else None,
        include=["documents", "metadatas", "distances"],
    )

    print(f"\nQuery: {args.query!r}\n")
    for rank, (document, metadata, distance) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), start=1
    ):
        print(f"{rank}. id={results['ids'][0][rank - 1]}  distance={distance:.4f}")
        print(f"   source={metadata['source']}  section={metadata['section']}")
        print(f"   {document}\n")

    print("Lower distance means nearer under this collection's configured distance metric.")
    print("These are retrieved source chunks, not LLM-generated answers.")


if __name__ == "__main__":
    main()
