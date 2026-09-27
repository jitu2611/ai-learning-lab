"""Generate the developer-focused AI Learning Lab curriculum."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
modules = [
("01 AI Building Blocks", ["Vector Databases", "Embedding Models", "Production Tokenization", "Attention Mechanisms", "Transformer Architecture", "LLM Inference", "Similarity Metrics", "Approximate Nearest Neighbour Search", "Context Windows", "GPU Computing for AI"]),
("02 LLM Application Foundations", ["Choosing an LLM", "Calling Model APIs", "Prompt Engineering", "System Prompts and Context Design", "Structured Outputs", "Function Calling", "Streaming Responses", "Caching LLM Requests", "Rate Limits and Retries", "Build a Minimal LLM Application"]),
("03 Retrieval-Augmented Generation", ["Document Ingestion Pipelines", "Chunking Strategies", "Metadata and Access Filters", "Hybrid Search", "Reranking", "Query Rewriting", "RAG Prompt Construction", "Citations and Grounding", "Conversational RAG", "Build a RAG Application"]),
("04 AI Agents", ["Agent Loops and Planning", "Tool Design", "Tool Schemas and Validation", "Tool Error Handling", "Agent State Machines", "Short-Term Memory", "Long-Term Memory", "Agentic RAG", "Human-in-the-Loop Workflows", "Build an AI Agent"]),
("05 Models and Adaptation", ["Open-Source Model Inference", "Model Quantization", "Instruction Tuning", "Fine-Tuning Datasets", "LoRA and PEFT", "Synthetic Data Generation", "Preference Optimization", "Fine-Tuning Evaluation", "Model Distillation", "Build a Domain Assistant"]),
("06 Evaluation, Safety, and Reliability", ["Evaluation Dataset Design", "Retrieval Metrics", "LLM-as-a-Judge", "Tracing and Observability", "Hallucination Reduction", "Prompt Injection Defense", "Data Privacy and Access Control", "Safety Guardrails", "Latency and Cost Optimization", "Build a Reliable AI System"]),
("07 Production AI Products", ["ChatGPT-Style Application Architecture", "Streaming Chat UI", "Conversation Persistence", "User Authentication and Multi-Tenancy", "File Upload and Chat With Documents", "Tool-Enabled Chat", "Feedback and Product Analytics", "Background Jobs and Queues", "Deploying an AI Application", "Build a ChatGPT-Style Application"]),
("08 Multimodal and Capstone Systems", ["Vision Language Models", "Image Embeddings and Search", "Speech-to-Text and Text-to-Speech", "Multimodal RAG", "AI System Architecture", "Security Threat Modeling", "Cost Architecture", "Open-Source AI Contributions", "Capstone Architecture", "Capstone: Production AI Assistant"]),
]

practices = [
"Build a focused, runnable developer tool or service that exposes the concept through a CLI or API.",
"Implement a small baseline, measure it, then document one trade-off or failure mode.",
"Integrate the concept into a minimal application and add an automated check for its expected behavior.",
"Use a realistic sample workload and record latency, cost, quality, or safety observations.",
"Create a reproducible example with configuration, sample inputs, and an explanation of operational limits.",
]

chapter = 1
curriculum = ["# AI Learning Lab Curriculum\n", "An 80-chapter, developer-focused path from AI foundations to production applications. Chapter 001 is implemented; further chapters are developed progressively with a concrete build target.\n"]
for module_title, titles in modules:
    curriculum.append(f"## {module_title}\n")
    for title in titles:
        slug = "".join(c.lower() if c.isalnum() else "-" for c in title).strip("-")
        while "--" in slug:
            slug = slug.replace("--", "-")
        folder = ROOT / f"chapter-{chapter:03d}-{slug}"
        if chapter != 1:
            folder.mkdir(exist_ok=True)
            (folder / "README.md").write_text(f"""# Chapter {chapter:03d} — {title}

**Status:** Planned

## Why this matters

Developers use **{title}** to build AI features that are useful, observable, and maintainable.

## Practical implementation

{practices[(chapter - 1) % len(practices)]}

## Done when

- You can explain the design trade-off in your own words.
- The example runs from a clean environment.
- You documented one limitation, failure mode, or safety concern.

> Detailed lesson content and production-quality runnable code will be added as this chapter is developed.
""", encoding="utf-8")
        curriculum.append(f"- [{chapter:03d}. {title}](chapter-{chapter:03d}-{slug}/)\n")
        chapter += 1
(ROOT / "CURRICULUM.md").write_text("\n".join(curriculum), encoding="utf-8")
print(f"Generated curriculum for {chapter - 1} chapters.")
