
from datetime import datetime
import uuid

from database import get_connection


# =====================================================
# CREATE CHAT SESSION
# =====================================================

def create_chat_session(
    title="New Chat",
    document_id=None
):

    session_id = str(
        uuid.uuid4()
    )

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now()

    cursor.execute(
        """
        INSERT INTO chat_sessions
        (
            session_id,
            title,
            document_id,
            created_at
        )
        VALUES (%s, %s, %s, %s)
        RETURNING
            session_id,
            title,
            document_id,
            created_at;
        """,
        (
            session_id,
            title,
            document_id,
            created_at
        )
    )

    row = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "session_id": row[0],
        "title": row[1],
        "document_id": row[2],
        "created_at": row[3].isoformat()
    }


# =====================================================
# SAVE MESSAGE
# =====================================================

def save_message(
    session_id,
    role,
    content
):

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now()

    cursor.execute(
        """
        INSERT INTO chat_messages
        (
            session_id,
            role,
            content,
            created_at
        )
        VALUES (%s, %s, %s, %s)
        RETURNING
            id,
            session_id,
            role,
            content,
            created_at;
        """,
        (
            session_id,
            role,
            content,
            created_at
        )
    )

    row = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "id": row[0],
        "session_id": row[1],
        "role": row[2],
        "content": row[3],
        "created_at": row[4].isoformat()
    }


# =====================================================
# GET CHAT MESSAGES
# =====================================================

def get_chat_messages(
    session_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            session_id,
            role,
            content,
            created_at
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY created_at ASC;
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    messages = []

    for row in rows:

        messages.append({
            "id": row[0],
            "session_id": row[1],
            "role": row[2],
            "content": row[3],
            "created_at": row[4].isoformat()
        })

    return messages


# =====================================================
# GET ALL CHAT SESSIONS
# =====================================================

def get_chat_sessions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            session_id,
            title,
            document_id,
            created_at
        FROM chat_sessions
        ORDER BY created_at DESC;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    sessions = []

    for row in rows:

        sessions.append({
            "session_id": row[0],
            "title": row[1],
            "document_id": row[2],
            "created_at": row[3].isoformat()
        })

    return sessions


# =====================================================
# GET CHAT DETAILS
# =====================================================

def get_chat_details(
    session_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            session_id,
            title,
            document_id,
            created_at
        FROM chat_sessions
        WHERE session_id = %s;
        """,
        (session_id,)
    )

    row = cursor.fetchone()

    if row is None:

        cursor.close()
        connection.close()

        return None


    chat = {
        "session_id": row[0],
        "title": row[1],
        "document_id": row[2],
        "created_at": row[3].isoformat()
    }


    cursor.execute(
        """
        SELECT
            id,
            role,
            content,
            created_at
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY created_at ASC;
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()


    messages = []

    for row in rows:

        messages.append({
            "id": row[0],
            "role": row[1],
            "content": row[2],
            "created_at": row[3].isoformat()
        })


    chat["messages"] = messages

    return chat


# =====================================================
# DELETE CHAT SESSION
# =====================================================

def delete_chat_session(
    session_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM chat_sessions
        WHERE session_id = %s;
        """,
        (session_id,)
    )

    deleted = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    return deleted


# =====================================================
# UPDATE CHAT TITLE
# =====================================================

def update_chat_title(
    session_id,
    title
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE chat_sessions
        SET title = %s
        WHERE session_id = %s;
        """,
        (
            title,
            session_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "session_id": session_id,
        "title": title
    }

