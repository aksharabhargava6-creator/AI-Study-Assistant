from vector_store import load_vector_store
from search import search
from llm_service import generate_answer


def retrieve_context(
    query,
    document_id,
    top_k=3
):

    vector_store = load_vector_store(
        document_id
    )

    if vector_store is None:

        return []

    results = search(
        query,
        vector_store,
        top_k=top_k
    )

    context = []

    for result in results:

        context.append({

            "page_number":
                result["page_number"],

            "text":
                result["text"],

            "similarity":
                result["similarity"]

        })

    return context


def answer_question(
    question,
    document_id
):

    context = retrieve_context(
        question,
        document_id
    )

    if not context:

        return {

            "answer":
                "I could not find relevant information in the selected document.",

            "sources":
                []

        }

    answer = generate_answer(
        context,
        question
    )

    return {

        "answer":
            answer,

        "sources":
            context

    }