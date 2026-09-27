"""Shared configuration for the local Chroma semantic-search demo."""

from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT / "chroma_data"
COLLECTION_NAME = "engineering_handbook"
MODEL_NAME = "all-MiniLM-L6-v2"


def get_collection():
    """Open the persisted collection with the same embedding function for reads/writes."""
    client = chromadb.PersistentClient(path=str(DATABASE_PATH))
    embedding_function = SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )
    return client, collection
