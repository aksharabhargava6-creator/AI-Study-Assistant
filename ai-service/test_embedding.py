from embedding_service import generate_embedding


text = "Cloud cost optimization"

embedding = generate_embedding(text)

print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])