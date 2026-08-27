from src.retrieval.kb_loader import load_kb_chunks


chunks = load_kb_chunks("knowledge-base")

assert chunks, "Knowledge base should contain chunks."

first = chunks[0]

assert "text" in first
assert "source" in first
assert "section" in first
assert "document_type" in first

assert first["text"]
assert first["source"]
assert first["section"]
assert first["document_type"]

print("=" * 70)
print("KB LOADER TEST")
print("=" * 70)
print(f"Total chunks: {len(chunks)}")
print("Required fields: PASS")
print("KB loader: PASS")
