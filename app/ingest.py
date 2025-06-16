import os
from pathlib import Path
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuration
CURRENT_DIR = Path(__file__).parent
DATA_DIR = CURRENT_DIR / "../data"
OUTPUT_FILE = CURRENT_DIR / "../chunks/chunks.txt"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_pdfs_from_folder(folder_path):
    """Load text from all PDFs in the given folder."""
    all_text = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            try:
                reader = PdfReader(path)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                all_text.append(text)
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return all_text

def chunk_documents(documents):
    """Split documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = []
    for doc in documents:
        chunks.extend(splitter.split_text(doc))
    print(f"Total chunks created: {len(chunks)}")
    return chunks

def save_chunks(chunks, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n---\n")
    print(f"Chunks saved to {output_path}")

if __name__ == "__main__":
    raw_texts = load_pdfs_from_folder(DATA_DIR)
    all_chunks = chunk_documents(raw_texts)
    save_chunks(all_chunks, OUTPUT_FILE)
