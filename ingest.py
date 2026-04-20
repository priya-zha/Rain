"""
ingest.py — Run ONCE to process the docs and save the vector index.
Creates a storage/ folder with embeddings saved to disk.

Before running:
  export ANTHROPIC_API_KEY=sk-ant-your-key-here
  python ingest.py
"""

import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# ── Load API key from terminal ────────────────────────────────────────────────

api_key = os.environ.get("ANTHROPIC_API_KEY")
# Reads the key you set with: export ANTHROPIC_API_KEY=sk-ant-...

if not api_key:
    raise ValueError(
        "ANTHROPIC_API_KEY not found.\n"
        "Run this first:\n"
        "  export ANTHROPIC_API_KEY=sk-ant-your-key-here"
    )


# ── Configure LlamaIndex ──────────────────────────────────────────────────────

Settings.llm = Anthropic(
    model="claude-sonnet-4-5",
    api_key=api_key,
    max_tokens=1024,
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
    # Free local model, downloads automatically (~130MB on first run).
    # Converts text into vectors that capture meaning numerically.
)


# ── Load docs ─────────────────────────────────────────────────────────────────

print("Loading documents from docs/...")
documents = SimpleDirectoryReader("docs/").load_data()
# Reads every file in the docs/ folder.
# Supports .txt, .pdf, .md automatically.
print(f"  {len(documents)} documents loaded.")


# ── Create vector index ───────────────────────────────────────────────────────

print("Creating index (first run downloads embedding model ~130MB)...")
index = VectorStoreIndex.from_documents(documents)
# LlamaIndex does three things here automatically:
#   1. CHUNKING  — splits each doc into ~500 character overlapping pieces
#   2. EMBEDDING — converts each chunk into a vector using the model above
#   3. INDEXING  — organises vectors for fast similarity search
print("  Index created.")


# ── Save to disk ──────────────────────────────────────────────────────────────

index.storage_context.persist(persist_dir="storage/")
# Saves everything to storage/ folder as JSON files.
# Next time app.py starts, it loads from here instantly.
# No need to re-embed — that's the whole point.
print("  Saved to storage/")
print()
print("Done. Now run:  streamlit run app.py")
