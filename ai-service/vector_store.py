import json
import os

from embedding_service import generate_embedding


VECTOR_STORE_FOLDER = "vector_stores"


def create_vector_store(chunks, document_id):

    vector_store = []

    for chunk in chunks:

        embedding = generate_embedding(
            chunk["text"]
        )

        vector_store.append({

            "chunk_number": chunk["chunk_number"],

            "page_number": chunk["page_number"],

            "text": chunk["text"],

            "embedding": embedding

        })

    save_vector_store(
        vector_store,
        document_id
    )

    return vector_store


def save_vector_store(
    vector_store,
    document_id
):

    os.makedirs(
        VECTOR_STORE_FOLDER,
        exist_ok=True
    )

    file_path = os.path.join(
        VECTOR_STORE_FOLDER,
        f"{document_id}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            vector_store,
            file
        )


def load_vector_store(document_id):

    file_path = os.path.join(
        VECTOR_STORE_FOLDER,
        f"{document_id}.json"
    )

    if not os.path.exists(file_path):

        return None

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)