"""See a miniature transformer attention calculation, then mean pooling.

Run: python learning/02_self_attention_and_pooling.py

The numbers below are deliberately tiny and fixed for inspection. They were NOT
trained, so this is a mechanics demo rather than a useful language model.
"""

import numpy as np

np.set_printoptions(precision=3, suppress=True)

TOKENS = ["deploy", "changes", "production"]

# In a real model this is a learned lookup table indexed by token ID.
# Each row is the initial vector for one token. Here hidden size = 4, not 384.
X = np.array([
    [0.8, 0.1, 0.2, 0.0],  # deploy
    [0.3, 0.7, 0.1, 0.1],  # changes
    [0.9, 0.2, 0.8, 0.3],  # production
])

# In a trained transformer these are learned matrices. One attention head shown.
W_Q = np.array([[0.4, 0.1], [0.2, 0.5], [0.3, 0.2], [0.1, 0.3]])
W_K = np.array([[0.5, 0.2], [0.1, 0.6], [0.4, 0.1], [0.2, 0.2]])
W_V = np.array([
    [0.6, 0.1, 0.2, 0.3],
    [0.2, 0.7, 0.1, 0.4],
    [0.3, 0.4, 0.8, 0.2],
    [0.1, 0.5, 0.2, 0.6],
])


def softmax(rows: np.ndarray) -> np.ndarray:
    """Stable row-wise softmax: scores become positive weights summing to 1."""
    shifted = rows - rows.max(axis=1, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / exponentials.sum(axis=1, keepdims=True)


if __name__ == "__main__":
    print("Tokens:", TOKENS)
    print("\nInitial token vectors X (one row per token):\n", X)

    queries = X @ W_Q
    keys = X @ W_K
    values = X @ W_V
    print("\nQ (what each token seeks):\n", queries)
    print("\nK (what each token offers):\n", keys)
    print("\nV (information to mix):\n", values)

    # Each row says how strongly one token attends to every token, including itself.
    raw_scores = (queries @ keys.T) / np.sqrt(keys.shape[1])
    attention_weights = softmax(raw_scores)
    contextual_vectors = attention_weights @ values

    print("\nScaled QK^T attention scores:\n", raw_scores)
    print("\nAttention weights (each row sums to 1):\n", attention_weights)
    print("\nContext-aware vectors after attention:\n", contextual_vectors)

    # Mean pooling: average each vector dimension over non-padding tokens.
    sentence_embedding = contextual_vectors.mean(axis=0)
    print("\nMean-pooled sentence embedding:\n", sentence_embedding)
    print("\nShape:", sentence_embedding.shape, "(4 here; all-MiniLM-L6-v2 uses 384)")
