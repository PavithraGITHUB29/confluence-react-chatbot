import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

def store_pages_in_faiss(pages: dict):
    titles, contents = list(pages.keys()), list(pages.values())
    embeddings = model.encode(contents)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, titles, contents

def search_relevant_page(query, index, titles, contents):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), 1)
    if I[0][0] >= len(titles):
        return None, None
    return titles[I[0][0]], contents[I[0][0]]
