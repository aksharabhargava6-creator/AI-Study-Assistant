from document_processor import process_pdf
from vector_store import create_vector_store
from rag import retrieve_context
from llm_service import generate_answer


pdf_path = "uploads/CloudWise_AI_Zeroth_Review-_1_ (1).pdf"


# Step 1: Process PDF
print("Processing PDF...")

chunks = process_pdf(pdf_path)

print("Total chunks:", len(chunks))


# Step 2: Generate embeddings
print("\nGenerating embeddings...")

vector_store = create_vector_store(chunks)

print("Embeddings generated:", len(vector_store))


# Step 3: Ask question
question = "What are the objectives of CloudWise AI?"

print("\nQuestion:")
print(question)


# Step 4: Retrieve relevant context
print("\nRetrieving relevant context...")

context = retrieve_context(
    question,
    vector_store,
    top_k=2
)


# Step 5: Generate answer
print("\n========================================")
print("CONTEXT SENT TO LLM")
print("========================================")

for item in context:

    print(f"\n[Page {item['page_number']}]")
    print(item["text"])
print("\nGenerating answer...")

answer = generate_answer(
    context,
    question
)


# Step 6: Display answer
print("\n========================================")
print("AI ANSWER")
print("========================================")

print(answer)


# Step 7: Display sources
print("\n========================================")
print("SOURCES")
print("========================================")

for item in context:

    print(
        f"[Page {item['page_number']}] "
        f"(similarity: {item['similarity']:.3f})"
    )