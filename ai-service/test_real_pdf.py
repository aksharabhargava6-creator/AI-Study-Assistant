from document_processor import process_pdf
from vector_store import create_vector_store
from search import search


pdf_path = "uploads/CloudWise_AI_Zeroth_Review-_1_ (1).pdf"


print("Processing PDF...")

chunks = process_pdf(pdf_path)

print("Total chunks:", len(chunks))


print("\nGenerating embeddings...")

vector_store = create_vector_store(chunks)

print("Embeddings generated:", len(vector_store))


query = "What are the objectives of CloudWise AI?"


print("\nSearching for:", query)

results = search(
    query,
    vector_store,
    top_k=5
)


print("\nMost relevant results:\n")


for result in results:

    print("Chunk:", result["chunk_number"])
    print("Page:", result["page_number"])
    print("Similarity:", result["similarity"])
    print("Text:")
    print(result["text"])
    print("-" * 70)