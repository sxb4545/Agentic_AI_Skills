# Agentic_AI_Skills

A hands-on training repository for building **Agentic AI** and **Retrieval-Augmented Generation (RAG)** applications. It collects the lecture material, demo notebooks, workshops, and assignments used across a multi-week course that takes you from Python foundations to production-style agent and RAG systems.

## What this repo is about

The goal is to teach the practical engineering skills needed to build LLM-powered agents: calling models programmatically, giving them tools via function calling, grounding them in your own data with RAG, and evaluating the results. Each week builds on the previous one, mixing slides, runnable notebooks/scripts, sample datasets, and exercises.

## Repository layout

- **[Lectures/](Lectures)** — Weekly teaching material (slides, notebooks, demos, datasets).
- **[Assignments/](Assignments)** — Practice projects and solution notebooks.
- **[Blogs/](Blogs)** — Supporting write-ups and visual explainers (images/GIFs).
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

### Week 3 — Agentic RAG ([Lectures/Week3_Agentic_RAG](Lectures/Week3_Agentic_RAG))

Extends the Week 2 RAG foundations toward fully agentic, RAG-powered knowledge agents. Currently provides the lecture slide decks (PDF) for RAG-Powered Knowledge Agents.

**Covers:** Bringing agents and RAG together into multi-step, tool-using knowledge assistants.

### Week 4 — Multi-Agent AI ([Lectures/Week4_Multi_Agent_AI](Lectures/Week4_Multi_Agent_AI))

Introduces multi-agent systems for coordinating specialized agents across complex, stateful workflows. The live class focuses on when multi-agent designs are useful, including context isolation, parallel execution, domain specialization, strict workflow sequencing, scalability, and fault recovery. It also emphasizes that coordination overhead should be justified: a single agent is often preferable for simple tasks or workflows that require all intermediate context to remain shared.

- **Context engineering and quarantine** — Give each worker only the information, tools, and instructions needed for its responsibility; return focused results to the coordinator instead of exposing every intermediate step.
- **Common coordination patterns** — Specialized worker agents, coordinator/orchestrator agents, sequential pipelines, conditional routing, and parallel fan-out/fan-in workflows.
- **LangGraph implementation model** — Define typed state, implement node functions, connect nodes with normal or conditional edges, use reducers to merge updates, compile the graph, and test each route.
- **Production workflow capabilities** — Checkpointing and persistence allow workflows to resume, support human review, recover from failures, and retain state across turns. Shared stores can retain user preferences across execution threads, while tracing, streaming, and state inspection support observability.
- **Reference implementation** — The lecture's travel-planner example coordinates flight, hotel, and research agents, using SerpApi for travel searches and Tavily for web research.

See the [Live Class Slides](Lectures/Week4_Multi_Agent_AI/Live%20Class%20Slides_Multi-Agent%20Systems_SWEs%20(1).pdf) and [Week 4 Roadmap](Lectures/Week4_Multi_Agent_AI/Roadmap_Week%204_SWEs.pdf) for the complete lecture material.

## Assignments overview

Hands-on practice projects that reinforce each week's material ([Assignments/](Assignments)):

- **[Assignment0_CSVAgent](Assignments/Assignment0_CSVAgent)** — A Streamlit web app that answers natural-language questions over uploaded CSV files using a LangChain pandas DataFrame agent (`gpt-4o-mini`), with bundled sample data and strict "answer from data only" grounding.

- **[Assignment_1](Assignments/Assignment_1)** — Agentic AI foundations & reflex agents assignment review, with a solution notebook and slides.

- **[Assignment2](Assignments/Assignment2)** — A self-contained copy of the SupportDesk-RAG workshop (six modules plus concept guides) for completing the Week 2 RAG assignment. See [Assignment2/README.md](Assignments/Assignment2/README.md).

- **[Assignment3](Assignments/Assignment3)** — Deep-dive study materials for the advanced RAG and Agentic RAG topics from Week 2/3. Contains the original slide decks (`.docx` and `.pdf`) plus two sets of extracted notes for each topic:
  - **RAG Pipeline** — Prompt-template engineering, retrieval parameter tuning (`k`, MMR), chain construction, and anti-hallucination grounding strategies.
  - **Evaluation** — Two-layer evaluation (retrieval: Precision@K / Recall@K / F1; generation: groundedness, completeness) and LLM-as-judge scoring patterns.
  - **Agentic RAG** — ReAct-style tool-calling agents, tool description quality, priority/category search tools, and conversational memory across agent turns.
  - Also includes a **Financial Bot with LLMs** reference PDF covering LLM-powered financial Q&A patterns.

  **Concepts covered:** advanced prompt engineering, retrieval quality evaluation, LLM-as-judge, building and extending LangChain agent tools, agentic reasoning traces.

- **[Assignment4](Assignments/Assignment4)** — A production-style **Smart Travel Planning Multi-Agent System** orchestrated with **LangGraph**. Four specialized agents collaborate to plan a complete trip end-to-end:
  - **FlightSearchAgent** — Queries SerpApi (Google Flights engine); summarizes best-value, premium, and budget-conscious flight options.
  - **HotelSearchAgent** — Queries SerpApi (Google Hotels engine); summarizes location/value, comfort, and budget hotel picks.
  - **ResearchAgent** — Uses Tavily deep search to answer traveler questions (visa rules, transit passes, weather, local tips) in parallel.
  - **ItineraryPlannerAgent** — Merges all specialist outputs into a day-by-day itinerary with a risk checklist and booking-priority order.
  - **TravelPlannerMultiAgentSystem** (coordinator) — Builds a `LangGraph StateGraph` where flight, hotel, and research nodes run as parallel branches, then feed into the itinerary planner node. Also exposes `plan_multiple_trips()` to handle batches of user requests concurrently.

  **Concepts covered:** LangGraph `StateGraph` workflow design, parallel agent node execution, typed state (`TypedDict`), external API tool adapters (SerpApi + Tavily), multi-agent fan-out/fan-in patterns, and unified result aggregation.

  **External keys required:** `OPENAI_API_KEY` (required), `SERPAPI_API_KEY` and `TAVILY_API_KEY` (recommended; agents degrade gracefully without them). See [Assignment4/README.md](Assignments/Assignment4/README.md) for full setup.

- **[Assignment5](Assignments/Assignment5)** — A **Multi-Agent Content Writer** built with LangGraph. The system routes each request to one of three specialized paths:
  - **SEO Blog Writer** — Uses Tavily deep research for background and a quick Tavily search for SEO keywords or current examples, then produces a structured article with headings, FAQ content, citations when available, and a call to action.
  - **X/Twitter Writer** — Uses the internet-search tool for trends and hashtags, then creates concise posts under 280 characters.
  - **General Handler** — Answers greetings, questions, and follow-ups using the persisted conversation history.

  The implementation defines a typed shared state with an `add_messages` reducer, a model-based router, tool-calling loops with LangGraph `ToolNode`s, conditional edges, and a `MemorySaver` checkpointer. The notebook loads `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL`, `TAVILY_API_KEY`, and `SERPAPI_API_KEY` from the local `Assignments/Assignment5/.env` file. Tavily powers both research tools, with advanced search used for deeper research and basic search used for lighter SEO/trend lookups. Ready-to-run tests cover all three routes and a same-thread persistence follow-up such as “What was my last request?”. See [Assignment5_Langgraph.ipynb](Assignments/Assignment5/Assignment5_Langgraph.ipynb).

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
