# Agentic_AI_Skills

A hands-on training repository for building **Agentic AI** and **Retrieval-Augmented Generation (RAG)** applications. It collects the lecture material, demo notebooks, workshops, and assignments used across a multi-week course that takes you from Python foundations to production-style agent and RAG systems.

## What this repo is about

The goal is to teach the practical engineering skills needed to build LLM-powered agents: calling models programmatically, giving them tools via function calling, grounding them in your own data with RAG, and evaluating the results. Each week builds on the previous one, mixing slides, runnable notebooks/scripts, sample datasets, and exercises.

## Repository layout

- **[Lectures/](Lectures)** — Weekly teaching material (slides, notebooks, demos, datasets).
- **[Assignments/](Assignments)** — Practice projects and solution notebooks.
- **[Blogs/](Blogs)** — Supporting write-ups.
- **[Agentic_AI_Tool_links(Sheet1).csv](Agentic_AI_Tool_links(Sheet1).csv)** — Curated list of agentic AI tools and links.

## Lectures overview

### Week 0 — Prerequisites: Python for GenAI ([Lectures/Week_1_Prerequisites](Lectures/Week_1_Prerequisites))

Foundational material to get everyone ready before the agentic content begins.

- **Python for GenAI** — Core Python refresher (variables, data types, control flow) delivered through a live-class notebook and slides, aimed at the level needed to work with LLM SDKs.
- **Hello Agent — CSV FAQ Agent (stub)** — A first "hello world" agent that uses LangChain's `create_pandas_dataframe_agent` to answer natural-language questions over CSV knowledge bases (credit card terms, e-commerce FAQs, hospital policy, SaaS docs), including auto-downloading the sample data.
- **Roadmap & study guides** — Course overview, learner guide, an "Agentic AI cheatbook," and a Week 0 mini-project.

**Covers:** Python essentials, working with tabular data via pandas, and your first taste of an LLM-driven data agent.

### Week 1 — Agentic AI Foundations ([Lectures/Week1_Agentic_AI](Lectures/Week1_Agentic_AI))

Introduces the core concepts of AI agents and how to build them with LLMs and tools.

- **Calling LLMs programmatically** — Connect to major LLM providers two ways: directly via official SDKs (OpenAI, Anthropic Claude, Google Gemini) and through a unified aggregator (OpenRouter). Explains message formats, system prompts, and provider differences, with keys loaded from a local `.env` file.
- **CRM Lead Qualifier Agent** — An end-to-end agent that enriches a sales lead from an email address: extracts the company domain, looks up (mocked) company data, checks CRM history, and computes a lead score. Built with **OpenAI function calling** to bridge the LLM to real Python "tools" in a structured loop.
- **Additional (optional) notebooks** — Classic agent architectures for context:
  - *Reflex Agents* — Simple condition–action (rule-based) reactive agents.
  - *Goal-based Agents* — Agents that plan actions toward an explicit goal.
  - *Utility Agents* — Agents that choose actions by maximizing a utility/score function.
- **Slides, roadmap, and a CRM agent README** round out the material.

**Covers:** What makes an LLM an "agent," function/tool calling, multi-provider integration, and foundational agent design patterns (reflex, goal-based, utility).

### Week 2 — RAG-Powered Knowledge Agents ([Lectures/Week2_RAG](Lectures/Week2_RAG))

A full hands-on RAG workshop — **SupportDesk-RAG** — that builds a support-ticket retrieval and troubleshooting assistant with strong anti-hallucination safeguards. See [SupportDesk-RAG-Workshop/README.md](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/README.md) for setup.

The workshop is organized into six runnable modules under `modules/`:

1. **Embeddings** — Generate OpenAI embeddings, compute semantic similarity, and visualize relationships.
2. **Chunking** — Fixed-size vs. recursive vs. semantic chunking, structure-aware splitting, and building a Chroma vector store.
3. **Indexing Strategies** — Compare Vector, Summary, Tree, Keyword Table, and Hybrid indexes using LlamaIndex.
4. **RAG Pipeline** — A complete RAG architecture with LangChain, prompt engineering for grounded responses, and anti-hallucination strategies.
5. **Evaluation** — Two-layer evaluation: retrieval metrics (Precision@K, Recall@K, F1) and generation metrics (groundedness, completeness) using FAISS and LLM-as-judge.
6. **Agentic RAG** — Custom LangChain tools, agents with OpenAI function calling, conversation memory, and multi-step reasoning that compares agentic vs. direct RAG.

**Covers:** The end-to-end RAG lifecycle — embeddings, chunking, indexing, retrieval-augmented generation, evaluation, and combining RAG with agents.

## Getting started

Most notebooks and demos require an **OpenAI API key** (some also use Anthropic, Google, or OpenRouter keys), typically supplied via a local `.env` file.

For the Week 2 RAG workshop specifically:

```powershell
# From Lectures/Week2_RAG/SupportDesk-RAG-Workshop
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env   # then add your OPENAI_API_KEY
```

> Note: The RAG workshop requires **Python 3.12** (`chromadb` does not support 3.13+).

See each module's `README.md` / `notes.md` and the workshop README for detailed, per-topic instructions.
