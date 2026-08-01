# -*- coding: utf-8 -*-
"""
================================================================================
ASSIGNMENT 2 - MODULE 2 SOLUTION: Chunking & Vector Stores
================================================================================

WHAT THIS FILE IS
-----------------
Completed solution for the Hour 2 exercises in
Assignments/Assignment2/2-Chunking.md. Each exercise is a function headed with
an "ASSIGNMENT 2 - Exercise N" banner for easy debugging and execution.

HOW TO RUN (from this folder: modules/2_chunking/)
--------------------------------------------------
    python assignment2_solution.py            # run every exercise
    python assignment2_solution.py 5          # run only Exercise 5 (no API cost)

REQUIREMENTS
------------
- .env at workshop root with OPENAI_API_KEY + OPENAI_EMBEDDING_MODEL
- ../../data/synthetic_tickets.json
- bs4 + lxml installed (needed by the HTML splitter demo)
"""

# =============================================================================
# ASSIGNMENT 2 - Shared setup. Imports used across the chunking exercises.
# =============================================================================
import json
import os
import sys

from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DATA_PATH = "../../data/synthetic_tickets.json"


def load_tickets():
    """ASSIGNMENT 2 helper: load the synthetic support tickets."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_documents():
    """ASSIGNMENT 2 helper: build LangChain Documents with metadata."""
    tickets = load_tickets()
    documents = []
    for t in tickets:
        full_text = f"""
Ticket ID: {t['ticket_id']}
Title: {t['title']}
Category: {t['category']}
Priority: {t['priority']}
Description: {t['description']}
Resolution: {t['resolution']}
        """.strip()
        documents.append(
            Document(
                page_content=full_text,
                metadata={
                    "ticket_id": t["ticket_id"],
                    "category": t["category"],
                    "priority": t["priority"],
                },
            )
        )
    return documents


# =============================================================================
# ASSIGNMENT 2 - Exercise 1: Change the Chunk Size (Easy)
# =============================================================================
# Instruction: compare chunk_size 200/overlap 20 vs 500/50 and observe how the
# chunk count and meaningfulness change.
def exercise_1():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 1: Change the Chunk Size")
    print("=" * 80)

    documents = build_documents()
    for size, overlap in [(200, 20), (500, 50)]:  # ASSIGNMENT 2: before vs after
        splitter = CharacterTextSplitter(
            chunk_size=size, chunk_overlap=overlap, separator="\n"
        )
        chunks = splitter.split_documents(documents)
        print(f"  chunk_size={size}, overlap={overlap} -> {len(chunks)} chunks")


# =============================================================================
# ASSIGNMENT 2 - Exercise 2: Change the Search Query (Easy)
# =============================================================================
def exercise_2():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 2: Change the Search Query")
    print("=" * 80)

    documents = build_documents()
    embeddings = OpenAIEmbeddings(model=MODEL)
    store = Chroma.from_documents(documents, embeddings, collection_name="a2_ex2")

    query = "Database is timing out frequently"  # ASSIGNMENT 2: the new query
    results = store.similarity_search(query, k=3)
    print(f"Query: '{query}'")
    for i, doc in enumerate(results, 1):
        print(f"  #{i} [{doc.metadata['category']}] {doc.metadata['ticket_id']}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 3: Adjust Number of Results (Easy)
# =============================================================================
def exercise_3():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 3: Adjust Number of Results (k=5)")
    print("=" * 80)

    documents = build_documents()
    embeddings = OpenAIEmbeddings(model=MODEL)
    store = Chroma.from_documents(documents, embeddings, collection_name="a2_ex3")

    query = "Authentication problems after password reset"
    k = 5  # ASSIGNMENT 2: changed from 3 to 5
    for i, doc in enumerate(store.similarity_search(query, k=k), 1):
        marker = "  (extra result)" if i > 3 else ""
        print(f"  #{i} [{doc.metadata['category']}] {doc.metadata['ticket_id']}{marker}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 4: Try Different Metadata Filters (Easy)
# =============================================================================
def exercise_4():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 4: Different Metadata Filters")
    print("=" * 80)

    documents = build_documents()
    embeddings = OpenAIEmbeddings(model=MODEL)
    store = Chroma.from_documents(documents, embeddings, collection_name="a2_ex4")

    query = "system not working"
    for category in ["Database", "Performance", "Authentication"]:  # ASSIGNMENT 2
        results = store.similarity_search(query, k=3, filter={"category": category})
        print(f"\nFilter category='{category}' -> {len(results)} results")
        for doc in results:
            print(f"  [{doc.metadata['category']}] {doc.metadata['ticket_id']}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 5: Compare Chunk Sizes (Medium) - NO API COST
# =============================================================================
# Instruction: build a table of chunk_size vs #chunks vs avg length, then find
# which size makes the most chunks and which yields ~1 chunk per ticket.
def exercise_5():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 5: Compare Chunk Sizes")
    print("=" * 80)

    tickets = load_tickets()
    documents = [
        Document(
            page_content=(
                f"Ticket ID: {t['ticket_id']}\nTitle: {t['title']}\n"
                f"Description: {t['description']}\nResolution: {t['resolution']}"
            ).strip()
        )
        for t in tickets
    ]

    avg_doc = sum(len(d.page_content) for d in documents) // len(documents)
    print(f"Total documents: {len(documents)}")
    print(f"Avg document length: {avg_doc} chars\n")
    print("Chunk Size | # Chunks | Avg Chunk Length")
    print("-" * 45)

    best_size, best_count = None, -1
    for size in [100, 200, 300, 500, 1000]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size, chunk_overlap=size // 10
        )
        chunks = splitter.split_documents(documents)
        avg_len = sum(len(c.page_content) for c in chunks) // len(chunks) if chunks else 0
        print(f"{size:>10} | {len(chunks):>8} | {avg_len:>16}")
        if len(chunks) > best_count:  # ASSIGNMENT 2: track the most chunks
            best_size, best_count = size, len(chunks)

    print(f"\n  Most chunks: chunk_size={best_size} ({best_count} chunks)")
    print(f"  ~1 chunk per ticket happens once chunk_size >= the avg doc length")


# =============================================================================
# ASSIGNMENT 2 - Exercise 6: Add Similarity Scores to Results (Medium)
# =============================================================================
# Note: Chroma returns L2 DISTANCE, so LOWER = more similar.
def exercise_6():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 6: Add Similarity Scores (distance)")
    print("=" * 80)

    documents = build_documents()
    embeddings = OpenAIEmbeddings(model=MODEL)
    store = Chroma.from_documents(documents, embeddings, collection_name="a2_ex6")

    query = "Authentication problems after password reset"
    results_with_scores = store.similarity_search_with_score(query, k=3)
    print(f"Query: '{query}'  (lower distance = more similar)")
    for i, (doc, score) in enumerate(results_with_scores, 1):
        print(f"  #{i} distance={score:.4f} [{doc.metadata['category']}] "
              f"{doc.metadata['ticket_id']}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 7: Filter by Multiple Conditions (Medium)
# =============================================================================
def exercise_7():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 7: Combined Filters (category AND priority)")
    print("=" * 80)

    tickets = load_tickets()
    documents = [
        Document(
            page_content=f"{t['title']}. {t['description']}",
            metadata={
                "ticket_id": t["ticket_id"],
                "category": t["category"],
                "priority": t["priority"],
            },
        )
        for t in tickets
    ]
    embeddings = OpenAIEmbeddings(model=MODEL)
    store = Chroma.from_documents(documents, embeddings, collection_name="a2_ex7")

    query = "system not working"
    # ASSIGNMENT 2: Chroma requires $and for multiple conditions
    combos = [
        ("Authentication", "High"),
        ("Database", "Critical"),
        ("Performance", "Medium"),
    ]
    for category, priority in combos:
        f = {"$and": [{"category": category}, {"priority": priority}]}
        results = store.similarity_search(query, k=3, filter=f)
        print(f"\nFilter: {priority} priority + {category} -> {len(results)} results")
        for doc in results:
            print(f"  [{doc.metadata['priority']}] [{doc.metadata['category']}] "
                  f"{doc.metadata['ticket_id']}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 8: Save and Load Vector Store (Medium)
# =============================================================================
def exercise_8():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 8: Save and Load a Vector Store")
    print("=" * 80)

    tickets = load_tickets()
    documents = [
        Document(
            page_content=f"{t['title']}. {t['description']}",
            metadata={"ticket_id": t["ticket_id"], "category": t["category"]},
        )
        for t in tickets
    ]
    embeddings = OpenAIEmbeddings(model=MODEL)

    persist_dir = "./assignment2_chroma_db"  # ASSIGNMENT 2: on-disk location
    print("Building and persisting vector store...")
    Chroma.from_documents(
        documents,
        embeddings,
        collection_name="a2_persist",
        persist_directory=persist_dir,
    )
    print(f"  Saved to {persist_dir}")

    print("Loading vector store back from disk...")
    loaded = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="a2_persist",
    )
    for doc in loaded.similarity_search("login problem", k=3):
        print(f"  {doc.metadata['ticket_id']}: {doc.page_content[:50]}...")


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
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in EXERCISES:
        EXERCISES[sys.argv[1]]()
    else:
        for fn in EXERCISES.values():
            fn()
    print("\nASSIGNMENT 2 - Module 2 solution complete.")
