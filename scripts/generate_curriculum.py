"""Generate planned chapter READMEs for the AI Learning Lab curriculum."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
modules = [
("01 Foundations and Vector Search", [
"Vector Databases", "Python Environment and CLI Tools", "Python Data Types and Control Flow", "Functions, Modules, and Packages", "Files, JSON, and CSV", "NumPy Arrays and Vectorization", "Linear Algebra for AI", "Probability and Statistics", "Optimization Intuition", "Similarity Search and ANN Indexes"]),
("02 Classical Machine Learning", [
"Data Collection and Dataset Splits", "Data Cleaning and Feature Engineering", "Linear Regression", "Logistic Regression", "Loss Functions and Gradient Descent", "Regularization", "Decision Trees", "Random Forests and Gradient Boosting", "Clustering with K-Means", "Model Metrics and Cross Validation"]),
("03 Neural Network Fundamentals", [
"Perceptrons and Activation Functions", "Neural Network Forward Pass", "Backpropagation", "PyTorch Tensors and Autograd", "Training Loops and Optimizers", "Overfitting and Dropout", "Batch Normalization", "Learning Rate Schedules", "Convolutional Neural Networks", "Image Classification Project"]),
("04 Natural Language Processing", [
"Text Normalization and Tokenization", "Subword Tokenizers", "Bag of Words and TF-IDF", "Word Embeddings", "Sequence Models and RNNs", "Attention Mechanisms", "Transformer Architecture", "Self Attention from Scratch", "Positional Encodings", "Text Classification Project"]),
("05 Large Language Models", [
"Language Modeling and Next Token Prediction", "Pretraining Data and Objectives", "Decoder Only Transformers", "Sampling: Temperature Top-K and Top-P", "Prompt Engineering", "System Prompts and Context Windows", "Structured Outputs", "Function and Tool Calling", "Open Source Model Inference", "LLM Application Project"]),
("06 Embeddings and RAG", [
"Embedding Models and Dimensions", "Document Chunking Strategies", "Metadata and Filters", "Hybrid Search: BM25 and Vectors", "Reranking", "Retrieval Evaluation", "RAG Prompt Construction", "Citation and Grounding", "Conversational RAG", "RAG Application Project"]),
("07 Adapting Models", [
"Instruction Tuning", "Supervised Fine Tuning Data", "LoRA and Parameter Efficient Fine Tuning", "Quantization", "Preference Optimization", "Synthetic Data Generation", "Fine Tuning Evaluation", "Model Distillation", "Domain Adaptation", "Fine Tuned Assistant Project"]),
("08 Agents and Memory", [
"Agent Loops and Planning", "Tool Design", "Tool Error Handling", "Agent State Machines", "Short Term Memory", "Long Term Memory", "Agentic RAG", "Multi Agent Collaboration", "Human in the Loop", "Agent Project"]),
("09 Reliability and Safety", [
"LLM Evaluation Design", "Automated Evaluators", "Tracing and Observability", "Prompt Injection", "Data Privacy and Access Control", "Hallucination Reduction", "Bias and Fairness", "Red Teaming", "Latency and Cost Optimization", "Reliable AI System Project"]),
("10 Production and Advanced AI", [
"API Design for AI Services", "Async Jobs and Queues", "Caching", "Deployment with Containers", "Model Serving", "Monitoring and Incident Response", "Multimodal Models", "Speech and Vision Applications", "Capstone Architecture", "Capstone: Production AI Assistant"]),
]

practices = [
"Build a minimal, runnable example; record inputs, outputs, and what changed when you alter one parameter.",
"Implement the core operation in a small Python script and add a testable example input.",
"Compare a baseline with an improved version and report one measurable result.",
"Create a command-line demo that makes the concept observable rather than hidden behind a library.",
"Use a real or small synthetic dataset, then document assumptions and failure cases.",
]

chapter = 1
curriculum = ["# AI Learning Lab Curriculum\n", "One hundred progressive chapters. Chapter 1 is implemented; later chapters are planned with a concrete build target.\n"]
for module_title, titles in modules:
    curriculum.append(f"## {module_title}\n")
    for title in titles:
        slug = "".join(c.lower() if c.isalnum() else "-" for c in title).strip("-")
        while "--" in slug:
            slug = slug.replace("--", "-")
        folder = ROOT / f"chapter-{chapter:03d}-{slug}"
        if chapter != 1:
            folder.mkdir(exist_ok=True)
            readme = f"""# Chapter {chapter:03d} — {title}

**Status:** Planned

## Goal

Learn the core idea of **{title}**, when it is useful, and its important trade-offs.

## Practical implementation

{practices[(chapter - 1) % len(practices)]}

## Completion criteria

- Explain the concept in your own words.
- Run the example and inspect its output.
- Add a short note describing one limitation or failure case.

> This chapter is scaffolded in the curriculum. Its detailed lesson and runnable implementation will be added when the chapter is developed.
"""
            (folder / "README.md").write_text(readme, encoding="utf-8")
        curriculum.append(f"- [{chapter:03d}. {title}](chapter-{chapter:03d}-{slug}/)\n")
        chapter += 1

(ROOT / "CURRICULUM.md").write_text("\n".join(curriculum), encoding="utf-8")
print(f"Generated curriculum for {chapter - 1} chapters.")
