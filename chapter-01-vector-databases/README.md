# Chapter 1 — Vector Databases

This chapter explains the path from a sentence to semantic search:

```text
text → tokens → token IDs → contextual token vectors → pooled embedding
     → vector database → nearest-neighbour search → source chunks
```

This chapter contains two tracks:

- **`learning/`** — transparent, tiny implementations. They illustrate the algorithms; they are not trained language models.
- **`production/`** — a practical local semantic-search application using Sentence Transformers and ChromaDB.

> A vector database retrieves stored source text. It does not generate the next word. Add an LLM after retrieval to make a RAG application.

## Setup

Requires Python 3.10+.

```bash
git clone <YOUR-GITHUB-URL>
cd vector-db-learning-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The learning scripts need only NumPy. The production scripts also install ChromaDB and Sentence Transformers. On the first production command, the embedding model is downloaded once and cached locally.

## Run in this order

```bash
python learning/01_tokenization_and_ids.py
python learning/02_self_attention_and_pooling.py
python learning/03_similarity_search.py
python production/ingest.py --reset
python production/search.py "How can I deploy changes to production?"
```

## The complete pipeline

### 1. Tokenization

A tokenizer breaks text into tokens. Real tokenizers typically use **subwords**, so unfamiliar words can be represented as pieces.

```text
"deployinator" → ["deploy", "##in", "##ator"]
```

`learning/01_tokenization_and_ids.py` uses a deliberately small WordPiece-like tokenizer. A production tokenizer has a much larger learned vocabulary and more sophisticated normalization rules.

### 2. Token IDs

Each vocabulary token has a fixed integer ID.

```text
["deploy", "production"] → [6, 11]
```

This is a dictionary lookup, not an AI decision. IDs are labels; `11` is not more meaningful than `6`.

### 3. Initial token vectors and transformer layers

A neural model has a learned embedding table. It looks up an initial vector for every token ID. Transformer layers then use **self-attention** to mix information from other tokens.

For each token vector `x`, one attention head computes:

```text
Q = XWq       (what each token is looking for)
K = XWk       (what each token offers)
V = XWv       (information each token contributes)
attention = softmax(QKᵀ / √d)
output = attention × V
```

This lets `bank` take different context from `money` versus `river`. Actual sentence-transformer models have several layers, multiple attention heads, residual connections, normalization, feed-forward networks, positional information, and trained weights. The learning script shows only the essential attention calculation with tiny, fixed numbers.

For `all-MiniLM-L6-v2`, `L6` means six transformer layers and the hidden-vector width is **384**.

### 4. Pooling

After the transformer, there is still one contextual vector per input token. A vector DB needs one vector per searchable chunk. Sentence Transformers commonly use **mean pooling** over real tokens:

```text
sentence_vector = average(contextual_token_vectors)
```

Averaging 384-dimensional token vectors produces another 384-dimensional vector. Padding and special tokens are excluded using an attention mask.

### 5. Store chunks

Documents are split into chunks before embedding. The production demo stores each paragraph from `data/handbook.md` together with:

```text
id + original text + 384-dimensional vector + metadata
```

Chunking matters: a very large chunk can dilute meaning; a tiny chunk may lack context. Start around 200–500 tokens with a small overlap, then evaluate on real questions.

### 6. Search

The incoming question goes through the **same embedding model**. Its vector is compared with stored vectors and the nearest chunks are returned.

Common measures:

- **Cosine similarity:** angle between vectors; ignores length after normalization.
- **Dot product:** sum of element-wise products; equivalent to cosine for unit-normalized vectors.
- **L2/Euclidean distance:** geometric distance between vectors.

The learning search uses brute force: calculate every score and sort. Production vector indexes use approximate-nearest-neighbor algorithms (commonly HNSW) to avoid checking every vector at huge scale. Approximate search trades a tiny amount of recall for much lower latency.

## Learning track

| Script | What it teaches |
|---|---|
| `01_tokenization_and_ids.py` | normalization, simple wordpiece splitting, vocabulary IDs, `[UNK]` |
| `02_self_attention_and_pooling.py` | initial lookup vectors, Q/K/V, scaled dot-product attention, contextual vectors, mean pooling |
| `03_similarity_search.py` | cosine, dot product, L2 distance, brute-force top-k retrieval |

The vectors and transformer weights in these scripts are intentionally made up. Training those weights is a separate, expensive process. During inference we only use learned weights.

## Production track

```bash
# Embed paragraphs and persist a local Chroma collection
python production/ingest.py --reset

# Retrieve the most relevant stored paragraphs
python production/search.py "Who must approve a production release?" --top-k 3

# Filter on metadata (each handbook paragraph has a section)
python production/search.py "How are passwords reset?" --section Accounts
```

Files created locally:

```text
chroma_data/                 # persisted database; ignored by git
```

`production/ingest.py` uses `all-MiniLM-L6-v2`, a compact, free, general-English embedding model. It is a good local default, not a universal best model. Choose a model based on language, domain, recall/latency requirements, privacy, and cost.

## Retrieval versus RAG

This repository implements retrieval:

```text
question → nearest stored paragraphs
```

A RAG system adds a generation step:

```text
question + retrieved paragraphs → LLM → grounded answer
```

A safe RAG prompt should require the LLM to answer only from retrieved context and cite chunk IDs. Retrieval quality still needs testing: semantic similarity is not proof that a chunk is correct, current, or authorized for a user to see.

## Production considerations

Before calling a system production-ready, add:

- evaluations with real user queries and expected chunks;
- hybrid retrieval (keyword/BM25 + vector) and reranking for harder corpora;
- metadata/access-control filtering **before** exposing retrieved text;
- chunking and update/delete policies;
- document versioning, freshness, and source citations;
- observability for retrieval scores, latency, and empty/poor results;
- a proper managed database, backups, and capacity testing when data grows.

Chroma is excellent for local development and smaller deployments. Postgres + pgvector, Qdrant, Weaviate, Milvus, or a managed provider may fit larger operational needs.
