# Agentic_AI_Skills

A hands-on training repository for **Agentic AI**, **Retrieval-Augmented Generation (RAG)**, multi-agent systems, conversational applications, and production LLM operations. It combines weekly slides, notebooks, workshop code, study guides, and assignments.

## Repository layout

- **[Lectures/](Lectures/)** - Weekly teaching material and nested demo/workshop projects.
- **[Assignments/](Assignments/)** - Assignment implementations, templates, exercise sheets, and reference material.
- **[Capstone/](Capstone/)** - Separate capstone briefs, evaluation material, and project archives.
- **[Blogs/](Blogs/)** - Supporting visual explainers.
- **[Agentic_AI_Tool_links(Sheet1).csv](Agentic_AI_Tool_links%28Sheet1%29.csv)** - Curated tool links.

## How to read this overview

This inventory summarizes the materials present in the local workspace, including nested lecture folders. Virtual environments, credentials, caches, and generated database files are excluded.

- **Assignment numbers are not lecture-week numbers.** In particular, Assignment 5 implements the Week 4 content-writer assignment; it is not the Week 5 multimodal assignment.
- **Available code does not prove completion.** "Implementation available" and "reference solutions available" describe repository contents, not successful execution, grading, or submission.
- **Folder numbering differs from slide numbering.** Week 9 and Week 11 contain slides labeled Week 8. The dedicated Week 8 folder is empty; ADK/A2A examples are inside Week 6.
- **Some scanned projects are local-only at the time of this update:** the [SupportDesk workshop](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/), [AxiomCart demo](Lectures/Week5_Conversational%26MultiModalAgenticAI/axiomcart-ai-assistant/), and [Week 6 Demo folder](Lectures/Week6_MCP/Demo/) are untracked. Their README links will require those folders to be included when sharing or cloning the repository.

## Weekly lectures: topics and material coverage

### Prerequisites / Week 0 - Python and a first data agent

**Folder:** [Week_1_Prerequisites](Lectures/Week_1_Prerequisites/)

- Python types, operators, strings, collections, control flow, and functions; pandas data creation, filtering, and sorting.
- A live-class notebook, slides, learner guide, roadmap, and agentic-AI cheatbook establish the foundations for using LLM SDKs.
- The CSV FAQ starter introduces natural-language questions over tabular data, with sample e-commerce, credit-card, hospital, and SaaS datasets.
- The ungraded mini-project asks for a Streamlit app with multiple CSV uploads, previews, factual lookup/numeric answers, and explicit missing-information responses. It does not require vector retrieval.

**Practice:** [Assignment 0](Assignments/Assignment0_CSVAgent/README.md) supplies the CSV web-app implementation. The lecture notebook remains a starter.

### Week 1 - Agentic AI foundations and tool calling

**Folder:** [Week1_Agentic_AI](Lectures/Week1_Agentic_AI/)

- LLM capabilities and limitations, provider APIs, structured tool schemas, and the think/act/observe execution loop.
- The nested [demo notebooks](Lectures/Week1_Agentic_AI/Demo%20Notebooks-20260719T080450Z-1-001/Demo%20Notebooks/) compare OpenAI, Anthropic, Gemini, and OpenRouter calls.
- The CRM lead-qualification demo combines company/domain lookup, CRM history, and lead scoring through function calling.
- Optional notebooks illustrate simple/model-based reflex, goal-based, and utility-based agents.
- The [lecture assignment notebook](Lectures/Week1_Agentic_AI/Assignment/Assignment_Week1.ipynb) builds an IT first responder: inspect health/logs, restart critical services, and escalate complex failures.

**Practice:** [Assignment 1 solution](Assignments/Assignment_1/Assignment_solution.ipynb) covers tool implementation, schemas, dispatch, and tool-result messages. Server data and actions are simulated.

### Week 2 - RAG foundations: embeddings, chunking, and indexing

**Folder:** [Week2_RAG](Lectures/Week2_RAG/)

- Embeddings, cosine similarity, semantic versus keyword matching, top-K selection, and score thresholds.
- Fixed-size, recursive, semantic, and structure-aware chunking; overlap, Chroma persistence, metadata filters, and retrieval diversity.
- LlamaIndex vector, summary, tree, keyword, and hybrid indexing strategies, including index comparison and tuning.
- The nested [SupportDesk-RAG workshop](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/README.md) uses support tickets and contains **six** modules. Modules 1-3 teach Week 2 foundations; modules 4-6 also support Week 3.
- Each module includes demo code, notes, exercises, and reference solutions. The first three additionally contain dedicated Assignment 2 solution scripts.

**Practice:** [Assignment 2 summary](Assignments/Assignment2/SUMMARY_Week2_Assignment2.md) and answer sheets document the embeddings, chunking, and indexing exercises. The full workshop should not be mistaken for the scope of Assignment 2 alone.

### Week 3 - RAG pipelines, evaluation, and agentic retrieval

**Folder:** [Week3_Agentic_RAG](Lectures/Week3_Agentic_RAG/)

- Retrieve/context/generate pipelines, LangChain LCEL composition, grounding, citations, retrieval tuning, and multi-turn conversations.
- Retrieval Precision@K, Recall@K, and F1; generation groundedness, completeness, and relevance; LLM-as-judge, failure analysis, and A/B comparisons.
- Agentic RAG with tool descriptions, semantic/category/ID lookup, priority support, multi-step requests, conversation memory, and error handling.
- This folder contains slides and a roadmap; runnable practice is shared with the [SupportDesk modules](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/modules/), rather than duplicated here:
  - [Module 4: RAG pipeline exercises](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/modules/4_rag_pipeline/exercises.md) - prompts, citations, fallback, filters, streaming, and history.
  - [Module 5: evaluation exercises](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/modules/5_evaluation/exercises.md) - metrics, judges, latency/cost, and release decisions.
  - [Module 6: agentic RAG exercises](Lectures/Week2_RAG/SupportDesk-RAG-Workshop/modules/6_agentic_rag/exercises.md) - tool routing, multi-step queries, interaction, and memory.

**Practice:** [Assignment 3](Assignments/Assignment3/) holds exercise documents, extracted notes, review slides, and a Financial Bot reference PDF. Reference implementations for modules 4-6 are also available in [Assignment 2's modules](Assignments/Assignment2/modules/); Assignment 3 itself has no standalone application implementation.

### Week 4 - Multi-agent architecture and LangGraph

**Folder:** [Week4_Multi_Agent_AI](Lectures/Week4_Multi_Agent_AI/)

- When specialization, context isolation, parallelism, and coordination justify multiple agents rather than one.
- Coordinator/worker patterns, sequential workflows, conditional routing, and parallel fan-out/fan-in.
- LangGraph shared state, reducers, nodes, edges, graph compilation, checkpoints, and shared memory.
- Slides use travel planning to demonstrate specialist flight, hotel, and research agents; setup material covers search-provider access.
- The roadmap's assignment is a **smart content assistant**, distinct from the travel-planner teaching example.

**Practice:** [Assignment 4](Assignments/Assignment4/README.md) implements the travel example. [Assignment 5](Assignments/Assignment5/) implements the content-writer assignment with routing, tool loops, and conversation persistence.

### Week 5 - Conversational and multimodal systems

**Folder:** [Week5_Conversational&MultiModalAgenticAI](Lectures/Week5_Conversational%26MultiModalAgenticAI/)

- Structured intent routing, conversational state, specialist tool loops, RAG, clarification, human-in-the-loop workflows, and optional multi-agent synthesis.
- Audio material introduces speech input/output alongside text interactions.
- The nested [AxiomCart instructor demo](Lectures/Week5_Conversational%26MultiModalAgenticAI/axiomcart-ai-assistant/README.md) is an e-commerce assistant. Its source separates configuration/data, state, routing nodes, graph orchestration, Chroma retrieval, product/order/escalation tools, and voice handling; an instructor guide accompanies it.
- The [multimodal assignment brief](Lectures/Week5_Conversational%26MultiModalAgenticAI/Multimodal%20Conversational%20System_Assignment.docx) instead specifies **SnackStack**, a food-order assistant: menu retrieval over eight dishes, order lookup by ID/tracking ID/email, structured routing, and missing-identifier clarification using `interrupt()` and `Command(resume=...)`. Parallel synthesis and voice are optional extensions.

**Practice:** The SnackStack brief and supporting references are present, but no matching SnackStack solution code was found. AxiomCart illustrates related techniques; Assignment 5's content writer is a different assignment.

### Week 6 - MCP, Google ADK, and A2A

**Folder:** [Week6_MCP](Lectures/Week6_MCP/)

- Model Context Protocol tools, resources, prompts, initialization, discovery, content types, client/tool loops, and SSE/streamable-HTTP transport.
- Google ADK agents, session state, sequential/parallel/loop workflows, agents as tools, callbacks, and event streams.
- A2A lifecycle, context threading, message parts/artifacts, and networked agent orchestration.
- The nested [real-estate negotiation simulator](Lectures/Week6_MCP/Demo/real-estate-negotiation-simulator/README.md) is organized into:
  - [m1_mcp](Lectures/Week6_MCP/Demo/real-estate-negotiation-simulator/m1_mcp/) - pricing/inventory servers, clients, transport/protocol demos, study notes, exercises, and solutions.
  - [m2_adk_multiagents](Lectures/Week6_MCP/Demo/real-estate-negotiation-simulator/m2_adk_multiagents/) - ADK/A2A demos, buyer/seller negotiation agents, orchestration, notes, exercises, and solutions.

**Practice:** Three MCP exercises cover a walk-score tool, a multi-server agent, and server-failure handling. Nine ADK/A2A exercises cover budget caps, stuck detection, multi-round context, mediation, prompt-injection defense, human approval, parallel sellers, shared market intelligence, and adaptive strategies. Matching reference-solution folders exist; there is no separate numbered assignment under [Assignments](Assignments/).

### Week 7 - Hybrid search and retrieval

**Folder:** [Week7_HybridSearch](Lectures/Week7_HybridSearch/)

- Dense versus sparse retrieval, SPLADE, and why semantic and lexical signals complement each other.
- The [live-class notebook](Lectures/Week7_HybridSearch/Hybrid%20Search%20%26%20Retrieval%20-%20Live%20Class%20Notebook.ipynb) prepares ESCI product-search data, generates embeddings, indexes/searches with Qdrant, fuses results with reciprocal-rank fusion, and evaluates retrieval.
- Later notebook sections expose hybrid retrieval as a LangChain agent tool.

**Practice:** A worked notebook, slides, and roadmap are available. No explicit Week 7 assignment brief or separate solution was found. Assignment 2 touches hybrid indexing, but does not establish coverage of this Qdrant/SPLADE/ESCI workflow.

### Week 8 - Reserved ADK/A2A folder

**Folder:** [Week8_A2A_GoogleADK](Lectures/Week8_A2A_GoogleADK/)

No teaching files or nested projects are present. Do not infer lecture coverage from the folder name: the available ADK/A2A demos and exercises are inside [Week 6](Lectures/Week6_MCP/Demo/real-estate-negotiation-simulator/m2_adk_multiagents/).

### Week 9 - Agent observability, evaluation, and safety

**Folder:** [Week9](Lectures/Week9/) - its slides are labeled **Week 8**.

- Agent tracing/observability, evaluation, input/output guardrails, and production cost optimization.
- LangSmith and Guardrails Hub setup guides accompany the teaching slides.
- The assignment-review deck describes exercises using LangSmith, DeepEval, guardrails, and cost optimization.
- The slides reference an external fintech workshop, but its demo/exercise/solution implementation is not present locally.

**Practice:** Exercise descriptions and setup instructions are available; no corresponding local application or assignment solution was found. The earlier RAG evaluation exercises are related foundations, not substitutes for these observability/safety labs.

### Week 10 - LLMOps and production operation

**Folder:** [Week10_LLMOps](Lectures/Week10_LLMOps/)

- Operating nondeterministic LLM applications, and how LLMOps differs from traditional MLOps.
- [Why LLMOps demo](Lectures/Week10_LLMOps/Demo_Why_LLMOps.ipynb) - model variability, prompt-drift regression, hallucination/grounding, unreliable tools, retries/timeouts, and cost/latency.
- [Integrated Langfuse demo](Lectures/Week10_LLMOps/Integrated_Demo_LLMOps_Langfuse.ipynb) - travel tools, prompt versioning, model routing, LangGraph workflows, exact/semantic caching, guardrails, and tracing.

**Practice:** Demonstration notebooks and slides are available. No dedicated LLMOps assignment brief or submission was found.

### Week 11 - Repeated observability and safety material

**Folder:** [Week11](Lectures/Week11/) - its slides are also labeled **Week 8**.

Contains observability/evaluation/safety slides and LangSmith/Guardrails setup guides, not a distinct new lecture implementation. The main slide PDF and Guardrails guide duplicate Week 9's files; the LangSmith guide covers the same setup topic.

**Practice:** No additional demo, assignment, or solution is present in this folder.

## Assignments: what each project covers

| Assignment | Topic / lecture alignment | What it covers | Available material |
|---|---|---|---|
| [0 - CSV FAQ agent](Assignments/Assignment0_CSVAgent/README.md) | Prerequisites / Week 0 | Streamlit uploads/previews, pandas-based natural-language lookup and calculations, answer-from-data grounding, missing-information responses. | App implementation, requirements, and four sample CSV datasets. |
| [1 - IT incident responder](Assignments/Assignment_1/Assignment_solution.ipynb) | Week 1 | Health/log investigation, restart/escalation tools, function schemas, tool dispatch, and tool-result messages in an agent loop. | Solution notebook and review slides; simulated tools/data rather than real server operations. |
| [2 - RAG foundations](Assignments/Assignment2/SUMMARY_Week2_Assignment2.md) | Week 2, with shared Week 3 workshop material | Query/top-K/threshold experiments, semantic similarity and batching; chunk size/overlap, metadata and persistence; vector/tree/keyword/hybrid index comparison. | [Embeddings](Assignments/Assignment2/1-Embeddings.md), [chunking](Assignments/Assignment2/2-Chunking.md), and [indexing](Assignments/Assignment2/3-Indexing.md) answer sheets plus dedicated solution scripts. All six workshop modules include demos, exercises, and reference solutions. |
| [3 - Advanced RAG materials](Assignments/Assignment3/) | Week 3 | Prompt/retrieval tuning, citations and fallback, retrieval metrics and LLM judges, agent tools, multi-step retrieval, and memory; Financial Bot reference concepts. | DOCX/PDF material and extracted exercise notes. No standalone application code here; shared implementations are in [modules 4-6](Assignments/Assignment2/modules/). |
| [4 - Smart travel planner](Assignments/Assignment4/README.md) | Week 4 teaching example | Flight/hotel specialists using SerpApi, Tavily travel research, parallel LangGraph branches, itinerary synthesis, and concurrent trip requests. | Modular Python implementation and demo. Does not itself implement the content-writer assignment or checkpointed conversation workflow. |
| [5 - Multi-agent content writer](Assignments/Assignment5/Assignment5_Langgraph.ipynb) | Week 4 assignment | SEO/X/general routing, Tavily deep/basic research, specialist tool loops, shared message state, conditional edges, and same-thread follow-ups with `MemorySaver`. | [Template](Assignments/Assignment5/Assignment%20Template%20-%20Multi-Agents%20Systems.ipynb), primary solution, and [alternative solution](Assignments/Assignment5/Assignment5_AlternativeSolution.ipynb). Includes example route/follow-up checks; persistence is in memory, not durable storage across process restarts. |

## Lecture-to-assignment coverage and gaps

**"Not covered" below means missing or not demonstrated in the available assignment material, not that a learner failed or skipped it.** A demo, a reference solution, and a completed/submitted assignment are different artifacts. This table does not invent assignment numbers for later weeks.

| Lecture folder | Available assignment / exercise coverage | Status | Missing assignment or coverage gap |
|---|---|---|---|
| [Prerequisites / Week 0](Lectures/Week_1_Prerequisites/) | [Assignment 0](Assignments/Assignment0_CSVAgent/) implements the CSV FAQ mini-project. | Implementation available | No missing core mini-project identified; the lecture stub itself still has unfinished starter sections. |
| [Week 1](Lectures/Week1_Agentic_AI/) | [Assignment 1](Assignments/Assignment_1/) and the [lecture assignment](Lectures/Week1_Agentic_AI/Assignment/Assignment_Week1.ipynb) cover incident tools and agent loops. | Implementation available | Multi-provider integration, CRM qualification, and optional goal/utility architectures are demos, not separate assignment solutions. Real server integration is not demonstrated. |
| [Week 2](Lectures/Week2_RAG/) | [Assignment 2](Assignments/Assignment2/) covers embeddings, chunking, and indexing, with answer sheets and dedicated scripts. | Core coverage available | Modules 4-6 are Week 3 practice, not additional completed Assignment 2 answers. Supplied reference/bonus material is not evidence of every exercise being executed or submitted. |
| [Week 3](Lectures/Week3_Agentic_RAG/) | [Assignment 3](Assignments/Assignment3/) contains exercise/reference documents; [shared modules 4-6](Assignments/Assignment2/modules/) have runnable reference solutions. | Reference coverage; submission unverified | No consolidated Assignment 3 application or documented exercise-run report; the optional Financial Bot has reference slides but no implementation. |
| [Week 4](Lectures/Week4_Multi_Agent_AI/) | [Assignment 4](Assignments/Assignment4/) covers travel orchestration; [Assignment 5](Assignments/Assignment5/) covers the assigned content assistant. | Both implementations available | Durable checkpoints, cross-thread shared memory, and resumable human-review workflows are not demonstrated by these assignments. Assignment 5 uses an in-memory checkpointer. |
| [Week 5](Lectures/Week5_Conversational%26MultiModalAgenticAI/) | [SnackStack assignment brief](Lectures/Week5_Conversational%26MultiModalAgenticAI/Multimodal%20Conversational%20System_Assignment.docx); related [AxiomCart instructor demo](Lectures/Week5_Conversational%26MultiModalAgenticAI/axiomcart-ai-assistant/). | Brief + related demo; matching solution absent | SnackStack menu/order tools, identifier clarification/resume, and its integrated conversation workflow have no matching local solution. Voice and parallel synthesis are optional, not mandatory missing tasks. |
| [Week 6](Lectures/Week6_MCP/) | [MCP exercises](Lectures/Week6_MCP/Demo/real-estate-negotiation-simulator/m1_mcp/exercises/) and [ADK/A2A exercises](Lectures/Week6_MCP/Demo/real-estate-negotiation-simulator/m2_adk_multiagents/exercises/) have matching supplied solutions. | Workshop reference solutions available | No separate numbered assignment or learner submission/run report; do not label this week uncovered just because it has no folder under Assignments. |
| [Week 7](Lectures/Week7_HybridSearch/) | Worked hybrid-search notebook; Assignment 2 introduces related hybrid-index concepts. | Demo only for this workflow | No explicit assignment/solution for ESCI, Qdrant dense/sparse search, SPLADE, fusion evaluation, or the hybrid agent tool. |
| [Week 8](Lectures/Week8_A2A_GoogleADK/) | No material in this folder; ADK/A2A practice is located in Week 6. | Empty folder | No independent Week 8 lecture or assignment to assess; do not double-count Week 6 protocol exercises. |
| [Week 9](Lectures/Week9/) | Assignment-review exercise descriptions and LangSmith/Guardrails setup guides. | Descriptions only locally | Referenced fintech workshop code is missing: no local LangSmith tracing, DeepEval evaluation, guardrails, or cost-optimization assignment implementation. |
| [Week 10](Lectures/Week10_LLMOps/) | Why-LLMOps and integrated Langfuse teaching demos. | Demo only | No dedicated assignment applying prompt regression/versioning, routing, caching, reliability, and tracing with a documented evaluation. |
| [Week 11](Lectures/Week11/) | Repeated Week 9 observability/safety slides and setup topics. | Repeated references only | No distinct Week 11 assignment or implementation; the same local observability/safety practice gap remains. |

## Getting started

Use each project's own requirements and setup instructions. Most applications need an OpenAI API key; individual demos may additionally need Anthropic, Google, OpenRouter, Tavily, SerpApi, LangSmith, Langfuse, or Guardrails access.

For the SupportDesk RAG workshop, follow its documented **Python 3.12** setup:

```powershell
Set-Location .\Lectures\Week2_RAG\SupportDesk-RAG-Workshop
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Configure OPENAI_API_KEY locally before running a module.
```

Keep API keys out of source control. Run data-execution agents only on trusted inputs, and review external API usage/costs before executing notebooks. Consult project READMEs and module notes rather than assuming every week shares the same environment.
