# AI Learning Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Chapters](https://img.shields.io/badge/chapters-80-7c3aed)](CURRICULUM.md)

**A practical, open-source path for developers who want to build real AI systems—not just call an API.**

AI Learning Lab turns the concepts behind LLM apps, RAG, agents, evaluation, and production AI into progressive chapters with explanations and runnable projects.

## Built for developers

This is for engineers who already know how to code and want to transition into AI engineering. We skip introductory Python syntax and focus on the engineering concepts, system trade-offs, and hands-on implementation work that matter in practice.

## 80-chapter roadmap

| Module | Focus |
|---|---|
| 1 | AI building blocks |
| 2 | LLM application foundations |
| 3 | Retrieval-Augmented Generation (RAG) |
| 4 | AI agents |
| 5 | Models and adaptation |
| 6 | Evaluation, safety, and reliability |
| 7 | Production AI products — including a ChatGPT-style app |
| 8 | Multimodal AI and capstone systems |

Explore the full [80-chapter curriculum →](CURRICULUM.md)

## Start here

**[Chapter 001 — Vector Databases](chapter-001-vector-databases/)** is implemented now. It includes:

- transparent scripts for tokenization, self-attention, pooling, and similarity search;
- a local ChromaDB semantic-search application;
- a detailed guide from text input to retrieved source chunks.

```bash
git clone https://github.com/jitu2611/ai-learning-lab.git
cd ai-learning-lab/chapter-001-vector-databases
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python learning/01_tokenization_and_ids.py
```

## Open source

This project is public and released under the [MIT License](LICENSE). Contributions, corrections, chapter proposals, and practical examples are welcome—see [CONTRIBUTING.md](CONTRIBUTING.md).

If this helps your AI-engineering journey, give the repository a star so other developers can find it.
