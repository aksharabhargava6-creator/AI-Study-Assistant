from document_processor import process_pdf
from vector_store import create_vector_store
from rag import retrieve_context


pdf_path = "uploads/CloudWise_AI_Zeroth_Review-_1_ (1).pdf"


print("Processing PDF...")

chunks = process_pdf(pdf_path)

print("Total chunks:", len(chunks))


print("\nGenerating embeddings...")

vector_store = create_vector_store(chunks)

print("Embeddings generated:", len(vector_store))


query = "What are the objectives of CloudWise AI?"


print("\nRetrieving relevant context...\n")

context = retrieve_context(
    query,
    vector_store,
    top_k=3
)


for item in context:

    print("Page:", item["page_number"])
    print("Similarity:", item["similarity"])
    print("Text:")
    print(item["text"])
    print("-" * 70)