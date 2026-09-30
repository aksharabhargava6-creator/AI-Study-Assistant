
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from pypdf import PdfReader

import os
import uuid


from chunker import chunk_text

from vector_store import (
    create_vector_store
)

from document_registry import (
    add_document,
    load_documents,
    delete_document
)

from chat_service import (
    create_chat_session,
    save_message,
    get_chat_messages,
    get_chat_sessions,
    get_chat_details,
    delete_chat_session,
    update_chat_title
)

from database import get_connection


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="AI Study Assistant"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================================
# UPLOAD FOLDER
# =====================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():

    return {
        "status":
            "AI Study Assistant is running"
    }


# =====================================================
# UPLOAD PDF
# =====================================================

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # -------------------------------------------------
    # Validate file type
    # -------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    # -------------------------------------------------
    # Generate document ID
    # -------------------------------------------------

    document_id = str(
        uuid.uuid4()
    )


    stored_filename = (
        f"{document_id}.pdf"
    )


    file_path = os.path.join(
        UPLOAD_FOLDER,
        stored_filename
    )


    # -------------------------------------------------
    # Save PDF
    # -------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)


    # -------------------------------------------------
    # Read PDF
    # -------------------------------------------------

    try:

        reader = PdfReader(
            file_path
        )

    except Exception:

        if os.path.exists(file_path):

            os.remove(file_path)

        raise HTTPException(
            status_code=400,
            detail="Unable to read PDF file"
        )


    # -------------------------------------------------
    # Extract and chunk text
    # -------------------------------------------------

    chunks = []

    chunk_number = 1


    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = (
            page.extract_text()
            or ""
        )


        page_chunks = chunk_text(
            text
        )


        for chunk in page_chunks:

            chunks.append({

                "chunk_number":
                    chunk_number,

                "page_number":
                    page_number,

                "text":
                    chunk

            })

            chunk_number += 1


    # -------------------------------------------------
    # Generate embeddings
    # -------------------------------------------------

    create_vector_store(
        chunks,
        document_id
    )


    # -------------------------------------------------
    # Save document metadata
    # -------------------------------------------------

    document = add_document(

        document_id,

        file.filename,

        len(reader.pages),

        len(chunks)

    )


    # -------------------------------------------------
    # Return response
    # -------------------------------------------------

    return {

        "message":
            "PDF uploaded successfully",

        "document":
            document

    }


# =====================================================
# ASK QUESTION
# =====================================================

@app.post("/ask")
def ask_question(
    question: str,
    document_id: str,
    session_id: str = None
):

    from rag import answer_question


    # -------------------------------------------------
    # Validate question
    # -------------------------------------------------

    if not question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )


    # -------------------------------------------------
    # Verify document
    # -------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT document_id
        FROM documents
        WHERE document_id = %s;
        """,
        (document_id,)
    )

    existing_document = (
        cursor.fetchone()
    )

    cursor.close()
    connection.close()


    if existing_document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    # -------------------------------------------------
    # Create or verify chat session
    # -------------------------------------------------

    if session_id is None:

        session = create_chat_session(

            "New Study Chat",

            document_id

        )

        session_id = (
            session["session_id"]
        )


    else:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                session_id,
                document_id
            FROM chat_sessions
            WHERE session_id = %s;
            """,
            (session_id,)
        )

        existing_session = (
            cursor.fetchone()
        )

        cursor.close()
        connection.close()


        if existing_session is None:

            raise HTTPException(
                status_code=404,
                detail="Chat session not found"
            )


        session_document_id = (
            existing_session[1]
        )


        if (
            session_document_id
            != document_id
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Chat session belongs "
                    "to a different document"
                )
            )


    # -------------------------------------------------
    # Save user question
    # -------------------------------------------------

    save_message(

        session_id,

        "user",

        question

    )


    # -------------------------------------------------
    # Update chat title
    # -------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT title
        FROM chat_sessions
        WHERE session_id = %s;
        """,
        (session_id,)
    )

    chat_row = cursor.fetchone()

    cursor.close()
    connection.close()


    if (
        chat_row is not None
        and chat_row[0] == "New Study Chat"
    ):

        title = question.strip()


        if len(title) > 40:

            title = (
                title[:40]
                + "..."
            )


        update_chat_title(

            session_id,

            title

        )


    # -------------------------------------------------
    # RAG
    # -------------------------------------------------

    result = answer_question(

        question,

        document_id

    )


    # -------------------------------------------------
    # Extract answer
    # -------------------------------------------------

    answer = result.get(

        "answer",

        ""

    )


    # -------------------------------------------------
    # Save assistant response
    # -------------------------------------------------

    save_message(

        session_id,

        "assistant",

        answer

    )


    # -------------------------------------------------
    # Return response
    # -------------------------------------------------

    return {

        "session_id":
            session_id,

        "question":
            question,

        "answer":
            answer,

        "sources":
            result.get(
                "sources",
                []
            )

    }


# =====================================================
# LIST DOCUMENTS
# =====================================================

@app.get("/documents")
def list_documents():

    documents = load_documents()

    return {
        "documents":
            documents
    }


# =====================================================
# GET SINGLE DOCUMENT
# =====================================================

@app.get("/documents/{document_id}")
def get_document(
    document_id: str
):

    documents = load_documents()


    for document in documents:

        if (
            document["document_id"]
            == document_id
        ):

            return document


    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


# =====================================================
# DELETE DOCUMENT
# =====================================================

@app.delete(
    "/documents/{document_id}"
)
def delete_document_endpoint(
    document_id: str
):

    deleted = delete_document(
        document_id
    )


    if deleted == 0:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    # -------------------------------------------------
    # Delete vector store
    # -------------------------------------------------

    vector_store_path = os.path.join(

        "vector_stores",

        f"{document_id}.json"

    )


    if os.path.exists(
        vector_store_path
    ):

        os.remove(
            vector_store_path
        )


    # -------------------------------------------------
    # Delete PDF
    # -------------------------------------------------

    pdf_path = os.path.join(

        UPLOAD_FOLDER,

        f"{document_id}.pdf"

    )


    if os.path.exists(
        pdf_path
    ):

        os.remove(
            pdf_path
        )


    return {

        "message":
            "Document deleted successfully",

        "document_id":
            document_id

    }


# =====================================================
# CREATE CHAT
# =====================================================

@app.post("/chats")
def create_chat(
    document_id: str = None
):

    # -------------------------------------------------
    # Validate document if supplied
    # -------------------------------------------------

    if document_id is not None:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT document_id
            FROM documents
            WHERE document_id = %s;
            """,
            (document_id,)
        )

        existing_document = (
            cursor.fetchone()
        )

        cursor.close()
        connection.close()


        if existing_document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )


    # -------------------------------------------------
    # Create session
    # -------------------------------------------------

    session = create_chat_session(

        "New Study Chat",

        document_id

    )


    return {

        "message":
            "Chat session created successfully",

        "chat":
            session

    }


# =====================================================
# LIST CHATS
# =====================================================

@app.get("/chats")
def list_chats():

    sessions = get_chat_sessions()

    return {

        "chats":
            sessions

    }


# =====================================================
# GET CHAT DETAILS
# =====================================================

@app.get(
    "/chats/{session_id}"
)
def get_chat_details_endpoint(
    session_id: str
):

    chat = get_chat_details(
        session_id
    )


    if chat is None:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )


    return chat


# =====================================================
# GET CHAT MESSAGES
# =====================================================

@app.get(
    "/chats/{session_id}/messages"
)
def get_messages(
    session_id: str
):

    messages = get_chat_messages(
        session_id
    )


    return {

        "session_id":
            session_id,

        "messages":
            messages

    }


# =====================================================
# DELETE CHAT
# =====================================================

@app.delete(
    "/chats/{session_id}"
)
def delete_chat(
    session_id: str
):

    deleted = delete_chat_session(
        session_id
    )


    if deleted == 0:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )


    return {

        "message":
            "Chat session deleted successfully",

        "session_id":
            session_id

    }

