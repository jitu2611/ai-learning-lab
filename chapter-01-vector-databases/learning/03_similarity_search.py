"""Brute-force vector search with three common similarity measures.

Run: python learning/03_similarity_search.py
"""

import numpy as np

DOCUMENTS = {
    "deploy": "Production deployments require approval from the platform team.",
    "password": "Use the Forgot Password link to reset an account password.",
    "incident": "Every incident needs a blameless postmortem.",
}

# Pretend these came from an embedding model. Real embeddings have hundreds of dimensions.
VECTORS = {
    "deploy": np.array([0.90, 0.70, 0.10]),
    "password": np.array([0.10, 0.20, 0.95]),
    "incident": np.array([0.45, 0.85, 0.20]),
}
QUERY = np.array([0.88, 0.64, 0.12])  # pretend embedding for "How do I release changes live?"


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def l2_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


if __name__ == "__main__":
    print("Query vector:", QUERY)
    results = []
    for doc_id, vector in VECTORS.items():
        results.append((doc_id, cosine_similarity(QUERY, vector), dot_product(QUERY, vector), l2_distance(QUERY, vector)))

    print("\nHigher is better for cosine/dot; lower is better for L2.\n")
    for doc_id, cosine, dot, l2 in sorted(results, key=lambda item: item[1], reverse=True):
        print(f"{doc_id:8} cosine={cosine:.3f}  dot={dot:.3f}  l2={l2:.3f}")
        print(f"         {DOCUMENTS[doc_id]}")
