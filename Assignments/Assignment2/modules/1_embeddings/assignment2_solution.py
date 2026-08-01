# -*- coding: utf-8 -*-
"""
================================================================================
ASSIGNMENT 2 - MODULE 1 SOLUTION: Embeddings & Similarity Search
================================================================================

WHAT THIS FILE IS
-----------------
This is the completed solution for the Hour 1 exercises in
Assignments/Assignment2/1-Embeddings.md. Every exercise is implemented as its
own function, each headed with an "ASSIGNMENT 2 - Exercise N" banner so it is
easy to find, debug, and run individually.

HOW TO RUN (from this folder: modules/1_embeddings/)
----------------------------------------------------
    python assignment2_solution.py            # runs every exercise in order
    python assignment2_solution.py 5          # runs only Exercise 5

REQUIREMENTS
------------
- .env at the workshop root with OPENAI_API_KEY and OPENAI_EMBEDDING_MODEL
- Data file at ../../data/synthetic_tickets.json
"""

# =============================================================================
# ASSIGNMENT 2 - Shared setup (imports, client, data). Reused by all exercises.
# =============================================================================
import json
import os
import sys
import time

import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()  # Loads OPENAI_API_KEY from the workshop-root .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DATA_PATH = "../../data/synthetic_tickets.json"


def load_tickets():
    """ASSIGNMENT 2 helper: load the synthetic support tickets from disk."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def embed_tickets(tickets):
    """ASSIGNMENT 2 helper: batch-embed 'title. description' for every ticket."""
    texts = [f"{t['title']}. {t['description']}" for t in tickets]
    response = client.embeddings.create(input=texts, model=MODEL)
    return np.array([d.embedding for d in response.data])


# =============================================================================
# ASSIGNMENT 2 - Exercise 1: Change the Search Query (Easy)
# =============================================================================
# Instruction: swap the query to "Database is running very slowly" and observe
# whether the top results match and which categories they belong to.
def exercise_1():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 1: Change the Search Query")
    print("=" * 80)

    tickets = load_tickets()
    embeddings = embed_tickets(tickets)

    query = "Database is running very slowly"  # ASSIGNMENT 2: the new query
    q_resp = client.embeddings.create(input=[query], model=MODEL)
    q_emb = np.array([q_resp.data[0].embedding])

    similarities = cosine_similarity(q_emb, embeddings)[0]
    top_idx = np.argsort(similarities)[::-1][:5]

    print(f"Query: '{query}'")
    for rank, idx in enumerate(top_idx, 1):
        t = tickets[idx]
        print(f"  #{rank} {similarities[idx]:.4f} [{t['category']}] {t['title']}")

    # ASSIGNMENT 2 answer note: top matches are Performance/Database tickets,
    # confirming the query lands in the right topic area.


# =============================================================================
# ASSIGNMENT 2 - Exercise 2: Adjust the Number of Results (Easy)
# =============================================================================
# Instruction: set top_k = 10 and report where similarity drops below 0.5,
# whether results #8-#10 are still relevant, and the score of result #10.
def exercise_2():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 2: Adjust the Number of Results (top_k=10)")
    print("=" * 80)

    tickets = load_tickets()
    embeddings = embed_tickets(tickets)

    query = "Database is running very slowly"
    q_resp = client.embeddings.create(input=[query], model=MODEL)
    q_emb = np.array([q_resp.data[0].embedding])
    similarities = cosine_similarity(q_emb, embeddings)[0]

    top_k = 10  # ASSIGNMENT 2: changed from 5 to 10
    top_idx = np.argsort(similarities)[::-1][:top_k]

    drop_rank = None
    for rank, idx in enumerate(top_idx, 1):
        score = similarities[idx]
        # ASSIGNMENT 2: record the first rank whose score falls below 0.5
        if drop_rank is None and score < 0.5:
            drop_rank = rank
        print(f"  #{rank} {score:.4f} [{tickets[idx]['category']}] {tickets[idx]['title']}")

    print(f"\n  Similarity first drops below 0.5 at rank #{drop_rank}")
    print(f"  Score of result #10: {similarities[top_idx[-1]]:.4f}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 3: Add a Similarity Threshold (Easy)
# =============================================================================
# Instruction: skip results below a 0.5 threshold; compare a relevant query
# with an unrelated one ("How to make pizza").
def exercise_3():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 3: Add a Similarity Threshold (>= 0.5)")
    print("=" * 80)

    tickets = load_tickets()
    embeddings = embed_tickets(tickets)
    threshold = 0.5  # ASSIGNMENT 2: only show confident matches

    for query in ["Database is running very slowly", "How to make pizza"]:
        q_resp = client.embeddings.create(input=[query], model=MODEL)
        q_emb = np.array([q_resp.data[0].embedding])
        similarities = cosine_similarity(q_emb, embeddings)[0]
        top_idx = np.argsort(similarities)[::-1][:10]

        print(f"\nQuery: '{query}'")
        shown = 0
        for rank, idx in enumerate(top_idx, 1):
            score = similarities[idx]
            if score < threshold:  # ASSIGNMENT 2: the added skip line
                continue
            shown += 1
            print(f"  #{rank} {score:.4f} {tickets[idx]['title']}")
        if shown == 0:
            print("  (no results above threshold - query is unrelated to the tickets)")


# =============================================================================
# ASSIGNMENT 2 - Exercise 4: Compare Two Queries (Easy)
# =============================================================================
def exercise_4():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 4: Compare Two Queries")
    print("=" * 80)

    tickets = load_tickets()
    embeddings = embed_tickets(tickets)

    for q in ["Login authentication failed", "Slow database performance"]:
        response = client.embeddings.create(input=[q], model=MODEL)
        q_emb = np.array([response.data[0].embedding])
        sims = cosine_similarity(q_emb, embeddings)[0]
        top_idx = int(np.argmax(sims))
        print(f"\nQuery: '{q}'")
        print(f"  Best match: {tickets[top_idx]['title']}")
        print(f"  Score: {sims[top_idx]:.4f}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 5: Test Semantic Understanding (Medium)
# =============================================================================
# Instruction: prove embeddings capture meaning, not keywords, by comparing
# paraphrases against an unrelated sentence.
def exercise_5():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 5: Test Semantic Understanding")
    print("=" * 80)

    texts = [
        "User authentication failed",   # Original
        "Login credentials rejected",   # Same meaning, different words
        "Cannot sign in to account",    # Same meaning, different words
        "Database connection timeout",  # DIFFERENT topic
    ]
    response = client.embeddings.create(input=texts, model=MODEL)
    embeddings = np.array([d.embedding for d in response.data])
    sim = cosine_similarity(embeddings)

    print("Similarity Matrix (upper triangle):")
    for i in range(len(texts)):
        for j in range(len(texts)):
            if i < j:
                print(f"  {sim[i][j]:.3f}  '{texts[i]}' vs '{texts[j]}'")

    # ASSIGNMENT 2: paraphrases (rows 0-2) score much higher than the
    # unrelated database sentence (row 3) -> embeddings encode meaning.


# =============================================================================
# ASSIGNMENT 2 - Exercise 6: Filter by Category (Medium)
# =============================================================================
# Instruction: complete the category-filter skip line inside the search loop.
def exercise_6():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 6: Filter by Category")
    print("=" * 80)

    tickets = load_tickets()
    embeddings = embed_tickets(tickets)

    def search_with_category(query, category_filter=None, top_k=5):
        response = client.embeddings.create(input=[query], model=MODEL)
        query_emb = np.array([response.data[0].embedding])
        similarities = cosine_similarity(query_emb, embeddings)[0]

        results = []
        for idx in np.argsort(similarities)[::-1]:
            ticket = tickets[idx]
            # ASSIGNMENT 2: the completed line - skip non-matching categories
            if category_filter and ticket["category"] != category_filter:
                continue
            results.append((ticket, similarities[idx]))
            if len(results) >= top_k:
                break
        return results

    print("All categories:")
    for ticket, score in search_with_category("login problem"):
        print(f"  {score:.3f} [{ticket['category']}] {ticket['title']}")

    print("\nOnly 'Authentication' category:")
    for ticket, score in search_with_category("login problem", category_filter="Authentication"):
        print(f"  {score:.3f} [{ticket['category']}] {ticket['title']}")


# =============================================================================
# ASSIGNMENT 2 - Exercise 7: Batch vs Single Embedding (Medium)
# =============================================================================
# Instruction: measure how much faster one batched call is vs one call per text.
def exercise_7():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Exercise 7: Batch vs Single Embedding")
    print("=" * 80)

    texts = [
        "Password reset not working",
        "Database connection timeout",
        "App crashes on startup",
        "Payment declined error",
        "Email notifications delayed",
    ]

    print("Method 1: Single API calls...")
    start = time.time()
    for text in texts:
        client.embeddings.create(input=[text], model=MODEL)
    time_slow = time.time() - start
    print(f"  Time: {time_slow:.2f} seconds")

    print("\nMethod 2: Batch API call...")
    start = time.time()
    client.embeddings.create(input=texts, model=MODEL)
    time_fast = time.time() - start
    print(f"  Time: {time_fast:.2f} seconds")

    print(f"\n  Batch is {time_slow / time_fast:.1f}x faster for {len(texts)} texts!")


# =============================================================================
# ASSIGNMENT 2 - Bonus: Similarity Matrix Heatmap (Challenge)
# =============================================================================
# Saves a heatmap PNG for the first 10 tickets. Uses the Agg backend so it
# runs headless without popping a window.
def exercise_bonus():
    print("\n" + "=" * 80)
    print("ASSIGNMENT 2 - Bonus: Similarity Matrix Heatmap")
    print("=" * 80)

    import matplotlib
    matplotlib.use("Agg")  # ASSIGNMENT 2: headless backend, save to file
    import matplotlib.pyplot as plt

    tickets = load_tickets()[:10]
    texts = [t["title"] for t in tickets]
    response = client.embeddings.create(input=texts, model=MODEL)
    embeddings = np.array([d.embedding for d in response.data])
    sim_matrix = cosine_similarity(embeddings)

    plt.figure(figsize=(10, 8))
    plt.imshow(sim_matrix, cmap="RdYlGn", vmin=0, vmax=1)
    plt.colorbar(label="Cosine Similarity")
    plt.xticks(range(10), [t["ticket_id"] for t in tickets], rotation=45, ha="right")
    plt.yticks(range(10), [t["ticket_id"] for t in tickets])
    plt.title("Ticket Similarity Matrix")
    plt.tight_layout()
    plt.savefig("assignment2_similarity_heatmap.png")
    print("  Saved as assignment2_similarity_heatmap.png")


# =============================================================================
# ASSIGNMENT 2 - Runner: run all exercises, or a single one via CLI argument.
# =============================================================================
EXERCISES = {
    "1": exercise_1,
    "2": exercise_2,
    "3": exercise_3,
    "4": exercise_4,
    "5": exercise_5,
    "6": exercise_6,
    "7": exercise_7,
    "bonus": exercise_bonus,
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in EXERCISES:
        EXERCISES[sys.argv[1]]()
    else:
        for fn in EXERCISES.values():
            fn()
    print("\nASSIGNMENT 2 - Module 1 solution complete.")
