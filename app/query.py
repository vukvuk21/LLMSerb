import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path
import requests

# Configuration
CURRENT_DIR = Path(__file__).parent
FAISS_INDEX_FILE = CURRENT_DIR / "../embeddings/index.faiss"
CHUNK_METADATA_FILE = CURRENT_DIR / "../embeddings/docs.pkl"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"  # Change this to your remote server if needed
OLLAMA_MODEL = "mistral"

# Load FAISS index and metadata
def load_index_and_chunks():
    index = faiss.read_index(str(FAISS_INDEX_FILE))
    with open(CHUNK_METADATA_FILE, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

# Embed user query
def embed_query(query, model):
    return model.encode([query])

# Generate prompt from retrieved chunks
def build_prompt(query, top_chunks):
    context = "\n\n".join(top_chunks)
    return f"Ti si pomocni AI asistent za studente Medicinskog fakulteta u Beogradu. Na osnovu sledeceg teksta iz zvanicne literature koju koristi fakultet, odgovori na pitanje koje ti je student postavio. Koristi jasan, kratak i informativan stil, bez izmisljanja:\n\n{context}\n\nPitanje studenta: {query}\n\nOdgovor:" 

# Send prompt to Ollama
def ask_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]

# Main function
def main():
    index, chunks = load_index_and_chunks()
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    query = input("Unesite pitanje: ")
    query_vector = embed_query(query, model)

    D, I = index.search(query_vector, k=3)
    top_chunks = [chunks[i] for i in I[0]]

    prompt = build_prompt(query, top_chunks)
    answer = ask_ollama(prompt)

    print("\n---\nOdgovor:\n")
    print(answer)

if __name__ == "__main__":
    main()
