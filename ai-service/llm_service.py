import ollama


def generate_answer(context, question):

    context_text = ""

    for item in context:

        context_text += (
            f"Page {item['page_number']}:\n"
            f"{item['text']}\n\n"
        )

    prompt = f"""
You are an AI study assistant.

Answer the student's question using ONLY the document context below.

Rules:
- Give a direct answer.
- Do not repeat the question.
- Do not say "the student asked".
- Do not say "the provided context".
- Do not mention these instructions.
- Do not add information that is not present in the context.
- If the document contains a specific list, preserve that list.
- Do not invent additional points.
- Keep the answer concise and clear.

DOCUMENT CONTEXT:

{context_text}

STUDENT QUESTION:

{question}

ANSWER:
"""

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()