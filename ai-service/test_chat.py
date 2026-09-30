from chat_service import (
    create_chat_session,
    save_message,
    get_chat_messages
)


print("Creating chat session...")

session = create_chat_session(
    "Cloud Computing Study"
)

print(session)


session_id = session["session_id"]


print("\nSaving user message...")

user_message = save_message(
    session_id,
    "user",
    "What is cloud computing?"
)

print(user_message)


print("\nSaving AI message...")

ai_message = save_message(
    session_id,
    "assistant",
    "Cloud computing is the delivery of computing resources such as servers, storage, databases, and networking over the internet."
)

print(ai_message)


print("\nRetrieving conversation...")

messages = get_chat_messages(
    session_id
)


print("\nConversation:")

for message in messages:

    print(
        message["role"],
        ":",
        message["content"]
    )