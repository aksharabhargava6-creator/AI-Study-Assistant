from vector_store import create_vector_store


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
    }
]


vector_store = create_vector_store(chunks)


print("Total chunks:", len(vector_store))

print("First chunk number:", vector_store[0]["chunk_number"])

print("First chunk page:", vector_store[0]["page_number"])

print("Embedding length:", len(vector_store[0]["embedding"]))

print("First 5 embedding values:")
print(vector_store[0]["embedding"][:5])