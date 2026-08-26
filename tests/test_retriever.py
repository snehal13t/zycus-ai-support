from src.retrieval.retriever import KBRetriever


retriever = KBRetriever()

query = """
New users cannot authenticate through SSO.
Existing users can log in, but new joiners are unable to access the platform.
"""

results = retriever.search(query, top_k=3)

print(f"Found {len(results)} results:\n")

for i, result in enumerate(results, start=1):
    print("=" * 70)
    print(f"RESULT {i}")
    print("Score:", result["score"])
    print("Source:", result["source"])
    print("Section:", result["section"])
    print("Type:", result["document_type"])
    print("\nText:")
    print(result["text"][:500])