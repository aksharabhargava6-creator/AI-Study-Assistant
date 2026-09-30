import numpy as np

from embedding_service import generate_embedding


def cosine_similarity(vector1, vector2):

    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    similarity = np.dot(vector1, vector2) / (
        np.linalg.norm(vector1) * np.linalg.norm(vector2)
    )

    return float(similarity)


def search(query, vector_store, top_k=3):

    query_embedding = generate_embedding(query)

    results = []

    for item in vector_store:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "chunk_number": item["chunk_number"],
            "page_number": item["page_number"],
            "text": item["text"],
            "similarity": similarity
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]