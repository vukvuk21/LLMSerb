import os
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

# Configuration
CURRENT_DIR = Path(__file__).parent
CHUNKS_FILE = CURRENT_DIR / "../chunks/chunks.txt"
FAISS_INDEX_FILE = CURRENT_DIR / "../embeddings/index.faiss"
CHUNK_METADATA_FILE = CURRENT_DIR / "../embeddings/docs.pkl"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Load chunks
def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        chunks = [chunk.strip() for chunk in content.split("---") if chunk.strip()]
    print(f"Loaded {len(chunks)} chunks.")
    return chunks

# Embed chunks and save FAISS index
def embed_and_index(chunks):
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = model.encode(chunks, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save FAISS index and chunk metadata
    FAISS_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_FILE))

    with open(CHUNK_METADATA_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"Saved FAISS index to {FAISS_INDEX_FILE}")
    print(f"Saved chunk metadata to {CHUNK_METADATA_FILE}")

if __name__ == "__main__":
    chunks = load_chunks(CHUNKS_FILE)
    embed_and_index(chunks)
