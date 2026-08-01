# -*- coding: utf-8 -*-
"""
================================================================================
ASSIGNMENT 2 - MODULE 3 SOLUTION: Indexing Strategies (LlamaIndex)
================================================================================

WHAT THIS FILE IS
-----------------
Completed solution for the exercises in
Assignments/Assignment2/3-Indexing.md. Each exercise is a function headed with
an "ASSIGNMENT 2 - Exercise N" banner for easy debugging and execution.

HOW TO RUN (from this folder: modules/3_indexing/)
--------------------------------------------------
    python assignment2_solution.py            # run every exercise
    python assignment2_solution.py 5          # run only Exercise 5

WARNING ON COST/TIME
--------------------
Tree and Keyword indexes make MANY LLM calls to build. Exercises use small
document subsets where possible to keep runtime and cost low.

REQUIREMENTS
------------
- .env at workshop root with OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_CHAT_MODEL
- ../../data/synthetic_tickets.json
"""

# =============================================================================
# ASSIGNMENT 2 - Shared setup: configure LlamaIndex Settings once.
# =============================================================================
import json
import os
import sys
import time

from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SummaryIndex,
    TreeIndex,
    KeywordTableIndex,
    Document,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

load_dotenv()

Settings.embed_model = OpenAIEmbedding(
    model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
Settings.llm = OpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

DATA_PATH = "../../data/synthetic_tickets.json"


def load_documents(limit=None):
    """ASSIGNMENT 2 helper: build LlamaIndex Documents (optionally a subset)."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        tickets = json.load(f)
    if limit:
        tickets = tickets[:limit]  # ASSIGNMENT 2: cap docs to limit LLM calls
    documents = []
    for t in tickets:
        content = (
            f"Ticket ID: {t['ticket_id']}\nTitle: {t['title']}\n"
            f"Description: {t['description']}\nResolution: {t['resolution']}\n"
            f"Category: {t['category']}\nPriority: {t['priority']}"
        )
        documents.append(
            Document(
                text=content,
                metadata={
                    "ticket_id": t["ticket_id"],
                    "category": t["category"],
                    "priority": t["priority"],
                    "title": t["title"],
                },
            )
        )
    return documents


# =============================================================================
# ASSIGNMENT 2 - Exercise 1: Change the Query (Easy)
# =============================================================================
def exercise_1():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 1: Change the Query")
    print("=" * 80)

    documents = load_documents()
    vector_index = VectorStoreIndex.from_documents(documents)
    engine = vector_index.as_query_engine(similarity_top_k=3)

    query = "Database connection is timing out"  # ASSIGNMENT 2: the new query
    response = engine.query(query)
    print(f"Query: '{query}'")
    print(f"Answer: {str(response)[:200]}")
    for i, node in enumerate(response.source_nodes, 1):
        print(f"  #{i} {node.metadata.get('ticket_id')} score={node.score:.4f}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 2: Adjust the Number of Results (Easy)
# =============================================================================
def exercise_2():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 2: similarity_top_k = 5")
    print("=" * 80)

    documents = load_documents()
    vector_index = VectorStoreIndex.from_documents(documents)
    engine = vector_index.as_query_engine(similarity_top_k=5)  # ASSIGNMENT 2

    query = "How do I fix authentication issues after password reset?"
    response = engine.query(query)
    print(f"Query: '{query}'")
    print(f"Answer: {str(response)[:200]}")
    print(f"Retrieved {len(response.source_nodes)} source documents")


# =============================================================================
# ASSIGNMENT 2 - Exercise 3: Change the Tree Index Branch Factor (Easy)
# =============================================================================
def exercise_3():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 3: Tree Index child_branch_factor")
    print("=" * 80)

    documents = load_documents(limit=10)  # ASSIGNMENT 2: small subset - tree is slow
    print("Building Tree Index (this makes several LLM calls)...")
    tree_index = TreeIndex.from_documents(documents)

    query = "How do I fix authentication issues after password reset?"
    for factor in [1, 3]:  # ASSIGNMENT 2: focused vs broader traversal
        start = time.time()
        engine = tree_index.as_query_engine(child_branch_factor=factor)
        response = engine.query(query)
        print(f"\nchild_branch_factor={factor} ({time.time() - start:.1f}s)")
        print(f"  {str(response)[:180]}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 4: Test a Keyword-Specific Query (Easy)
# =============================================================================
def exercise_4():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 4: Keyword-specific query (exact ID)")
    print("=" * 80)

    documents = load_documents(limit=10)
    print("Building Keyword Index (LLM extracts keywords)...")
    keyword_index = KeywordTableIndex.from_documents(documents)
    engine = keyword_index.as_query_engine()

    keyword_query = "TICK-001"  # ASSIGNMENT 2: exact ID lookup
    response = engine.query(keyword_query)
    print(f"Query: '{keyword_query}'")
    print(f"Result: {str(response)[:200]}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 5: Compare Index Types Side-by-Side (Medium)
# =============================================================================
def exercise_5():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 5: Vector vs Keyword side-by-side")
    print("=" * 80)

    documents = load_documents()
    print("Building indexes...")
    vector_idx = VectorStoreIndex.from_documents(documents)
    keyword_idx = KeywordTableIndex.from_documents(documents)

    # ASSIGNMENT 2: semantic query vs exact-ID query highlights each index's strength
    for query in ["authentication login problem", "database timeout error", "TICK-005"]:
        print("\n" + "-" * 60)
        print(f"Query: '{query}'")
        vec = vector_idx.as_query_engine(similarity_top_k=3).query(query)
        print(f"  Vector : {str(vec)[:120]}")
        kw = keyword_idx.as_query_engine().query(query)
        print(f"  Keyword: {str(kw)[:120]}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 6: Save and Load an Index (Medium)
# =============================================================================
def exercise_6():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 6: Persist and reload a Vector Index")
    print("=" * 80)

    documents = load_documents()
    persist_dir = "./assignment2_saved_index"  # ASSIGNMENT 2: on-disk location

    print("Building and saving index...")
    vector_index = VectorStoreIndex.from_documents(documents)
    vector_index.storage_context.persist(persist_dir=persist_dir)
    print(f"  Saved to {persist_dir}")

    print("Loading index from disk...")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    loaded_index = load_index_from_storage(storage_context)

    response = loaded_index.as_query_engine().query("login problem")
    print(f"  Query result: {str(response)[:180]}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 7: Add Metadata Filtering (Medium)
# =============================================================================
def exercise_7():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 7: Metadata Filtering by category")
    print("=" * 80)

    documents = load_documents()
    vector_index = VectorStoreIndex.from_documents(documents)

    print("Without filter:")
    response = vector_index.as_query_engine(similarity_top_k=3).query("system problem")
    print(f"  {str(response)[:160]}")

    # ASSIGNMENT 2: restrict retrieval to a single category
    for category in ["Authentication", "Database"]:
        filters = MetadataFilters(filters=[ExactMatchFilter(key="category", value=category)])
        engine = vector_index.as_query_engine(similarity_top_k=3, filters=filters)
        response = engine.query("system problem")
        print(f"\nWith '{category}' filter:")
        print(f"  {str(response)[:160]}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 8: Benchmark Index Build Time (Medium)
# =============================================================================
def exercise_8():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 8: Benchmark index build time")
    print("=" * 80)

    documents = load_documents()
    print(f"Building indexes for {len(documents)} documents...\n")

    start = time.time()
    VectorStoreIndex.from_documents(documents)
    print(f"Vector Index : {time.time() - start:.2f}s (embeds every document)")

    start = time.time()
    KeywordTableIndex.from_documents(documents)
    print(f"Keyword Index: {time.time() - start:.2f}s (LLM extracts keywords)")

    start = time.time()
    SummaryIndex.from_documents(documents)
    print(f"Summary Index: {time.time() - start:.2f}s (just stores docs; work at query time)")


# =============================================================================
# ASSIGNMENT 2 - Bonus: Simple Hybrid Search (Challenge)
# =============================================================================
def exercise_bonus():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Bonus: Simple Hybrid (Vector + Keyword) Search")
    print("=" * 80)

    documents = load_documents()
    vector_index = VectorStoreIndex.from_documents(documents)
    keyword_index = KeywordTableIndex.from_documents(documents)

    query = "authentication timeout error"
    vector_nodes = vector_index.as_retriever(similarity_top_k=5).retrieve(query)
    keyword_nodes = keyword_index.as_retriever().retrieve(query)

    print(f"Query: '{query}'")
    print("Vector results:", [n.node.metadata.get("ticket_id") for n in vector_nodes[:3]])
    print("Keyword results:", [n.node.metadata.get("ticket_id") for n in keyword_nodes[:3]])

    # ASSIGNMENT 2: combine both lists and de-duplicate while keeping order
    seen, hybrid = set(), []
    for node in vector_nodes + keyword_nodes:
        tid = node.node.metadata.get("ticket_id")
        if tid and tid not in seen:
            seen.add(tid)
            hybrid.append(tid)
    print(f"Hybrid (combined, deduped): {hybrid[:5]}")


# =============================================================================
# ASSIGNMENT 2 - Runner
# =============================================================================
EXERCISES = {
    "1": exercise_1,
    "2": exercise_2,
    "3": exercise_3,
    "4": exercise_4,
    "5": exercise_5,
    "6": exercise_6,
    "7": exercise_7,
    "8": exercise_8,
    "bonus": exercise_bonus,
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in EXERCISES:
        EXERCISES[sys.argv[1]]()
    else:
        for fn in EXERCISES.values():
            fn()
    print("\nASSIGNMENT 2 - Module 3 solution complete.")
