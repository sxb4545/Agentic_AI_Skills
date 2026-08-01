# SUMMARY — Week 2 Concept Refresh & Assignment 2

Prepared for the **Week 3 SupportDesk RAG** live session. This captures the three
Week 2 foundations (Embeddings, Chunking, Indexing), the results of running the
module demos, and the completed Assignment 2 answers.

---

## 1. How to run everything

All demos and solutions live under the workshop and read `../../data/synthetic_tickets.json`.
They require a `.env` at the workshop root with `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`,
`OPENAI_CHAT_MODEL` (already present).

```powershell
# From each module folder:
python demo.py                     # the teaching demo
python assignment2_solution.py     # all Assignment 2 exercises
python assignment2_solution.py 5   # a single exercise (here #5)
```

> Set `$env:MPLBACKEND='Agg'` before running the embeddings demo so plots save to
> file instead of opening a blocking window.
> One-time dependency added for the chunking HTML splitter: `pip install bs4 lxml`.

Solution files created in this workspace (each exercise is headed with an
`ASSIGNMENT 2 - Exercise N` comment banner for easy debugging):

- [modules/1_embeddings/assignment2_solution.py](modules/1_embeddings/assignment2_solution.py)
- [modules/2_chunking/assignment2_solution.py](modules/2_chunking/assignment2_solution.py)
- [modules/3_indexing/assignment2_solution.py](modules/3_indexing/assignment2_solution.py)

---

## 2. Embeddings (Module 1)

**Concept.** Text → dense vector (1536 dims for `text-embedding-3-small`). Similar
meaning ⇒ vectors point the same way. Compare with **cosine similarity** (range −1..1;
OpenAI vectors are normalized so cosine ≈ dot product).

**Pipeline:** `Query → embed → cosine vs all docs → sort → top-K`.

**Demo / solution findings (query `"Database is running very slowly"`):**
- Similarity range across 20 tickets: **[0.15, 0.52]**.
- Top hit `TICK-010 Dashboard loading extremely slowly` (0.52) — a Performance
  ticket found *by meaning*, not shared keywords.
- Score drops below 0.5 already at **rank #2** → a high `top_k` returns weak tail
  results; pair it with a similarity threshold.
- Semantic proof: `"User authentication failed"` vs `"Login credentials rejected"`
  = **0.778** (paraphrase) vs `"Database connection timeout"` = **0.447** (off-topic).
- **Batching is ~2.9x faster** than one call per text (and the gap grows with volume).

**Rules that carry into Week 3:** same model for query + docs; keep chunks ~100–500
tokens; batch; cache by text hash; add a score threshold to drop junk.

---

## 3. Chunking (Module 2)

**Concept.** Break documents into self-contained units — the "Goldilocks" balance of
completeness vs specificity vs cost.

| Strategy | Best for |
|---|---|
| Fixed-size (`CharacterTextSplitter`) | quick prototypes, unstructured text |
| **Recursive** (`RecursiveCharacterTextSplitter`) | general default (splits `\n\n → \n → . → space`) |
| Semantic (`SemanticChunker`) | high-accuracy, topic-aware (costs embeddings) |
| Markdown / HTML header | structured docs, wikis, scraped pages |
| Whole document | already-short docs (like these tickets) |

**Demo / solution findings:**
- `CharacterTextSplitter`: `200/20` → **60 chunks**; `500/50` → **39 chunks**
  (bigger chunks = fewer, more coherent pieces, lower precision).
- Recursive chunk-size sweep (avg doc ≈ 508 chars): 100→130 chunks, 200→82,
  300→41, 500→32, 1000→20. **~1 chunk/ticket at chunk_size ≈ avg doc length (1000).**
- Chroma extras that matter for the assistant: **persistence**, **metadata
  filtering** (`category`, `priority`, and combined `$and`), and **MMR** for diverse
  results. Chroma returns **L2 distance → lower is more similar**.

**Guidance:** recursive splitter, ~200–500 tokens, 15–20% overlap, count **tokens
not characters**.

---

## 4. Indexing (Module 3)

**Key distinction:** *RAG-level* indexing (how knowledge is organized — your job)
vs *DB-level* ANN indexing (HNSW/IVF — the vector DB's job). **Storage is flat;
retrieval is smart** — most "index types" are really different retrieval strategies.

| Index | Retrieval logic | Best for | Speed | Accuracy |
|---|---|---|---|---|
| **Vector (flat)** | cosine top-K | general semantic search (default) | Fast | High |
| Summary | LLM scans all docs (O(n)) | small sets, high-level Qs | Slow | Medium |
| Tree | hierarchical traversal (O(log n)) | large hierarchical corpora | Medium | High |
| Keyword | LLM-extracted keyword match | exact terms/codes | Fast | Medium |
| Hybrid | vector + keyword, fused | production | Medium | Highest |

**Demo / solution findings:**
- Vector top hit `TICK-001` (score 0.63) with a grounded synthesized answer.
- Keyword index extracted **250 keywords** from the tickets.
- **Exact-ID gap:** querying bare `"TICK-005"` failed on *both* Vector
  ("no information available") and Keyword ("Empty Response"). Lesson: use
  **metadata filtering on `ticket_id`** for exact lookups — not free-text search.
- **Tree `child_branch_factor`:** 1 = fast single path (may miss branches);
  3 = broader recall but more LLM calls (slower). 2 is a good default.

**Production best practice:** Vector + Keyword + Reciprocal Rank Fusion, plus
metadata filters for IDs/codes.

---

## 5. Why this matters for Week 3

The SupportDesk assistant chains these directly:

```
Ingest tickets → CHUNK (recursive, ~400 tok, ~20% overlap)
             → EMBED (text-embedding-3-small, batched)
             → INDEX (vector + metadata; hybrid for production)
             → retrieve top-K → assemble prompt context → LLM generates answer
```

Everything measured in Week 3 — **Precision@K, Recall@K, Groundedness,
Completeness, Relevance** — is only as good as these three foundations. Weak
chunking or a bad `top_k`/threshold shows up immediately as low precision and
ungrounded answers.

**Week 3 build order:** baseline retrieval+generation → multi-turn history
(ground each turn in retrieved evidence) → evaluation harness → A/B iteration →
agentic RAG (ReAct: Reason → Tool → Observe) with LangChain tool routing.

---

## 6. Assignment 2 — status

Answers written back into the assignment sheets (each answer grounded in a real run):

- [Assignments/Assignment2/1-Embeddings.md](../../../Assignments/Assignment2/1-Embeddings.md)
- [Assignments/Assignment2/2-Chunking.md](../../../Assignments/Assignment2/2-Chunking.md)
- [Assignments/Assignment2/3-Indexing.md](../../../Assignments/Assignment2/3-Indexing.md)

Solution code (with `ASSIGNMENT 2` comment banners) lives beside each module demo,
listed in section 1 above.
