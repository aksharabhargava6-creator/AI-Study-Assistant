from vector_store import create_vector_store
from search import search


chunks = [
    {
        "chunk_number": 1,
        "page_number": 1,
        "text": "Cloud computing provides on-demand access to computing resources."
    },
    {
        "chunk_number": 2,
        "page_number": 2,
        "text": "Cloud cost optimization focuses on reducing unnecessary infrastructure spending."
    },
    {
        "chunk_number": 3,
        "page_number": 3,
        "text": "Machine learning models can identify patterns in large datasets."
    }
]


vector_store = create_vector_store(chunks)


query = "How can I reduce cloud costs?"


results = search(
    query,
    vector_store,
    top_k=2
)


print("Query:", query)

print("\nMost relevant chunks:\n")


for result in results:

    print("Chunk:", result["chunk_number"])
    print("Page:", result["page_number"])
    print("Similarity:", result["similarity"])
    print("Text:", result["text"])
    print("-" * 60)