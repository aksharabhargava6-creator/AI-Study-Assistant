from datetime import datetime

from database import get_connection


def load_documents():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            document_id,
            filename,
            uploaded_at,
            total_pages,
            total_chunks
        FROM documents
        ORDER BY uploaded_at DESC;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    documents = []

    for row in rows:

        document = {

            "document_id": row[0],

            "filename": row[1],

            "uploaded_at":
                row[2].isoformat(),

            "total_pages": row[3],

            "total_chunks": row[4]

        }

        documents.append(document)

    return documents


def add_document(
    document_id,
    filename,
    total_pages,
    total_chunks
):

    connection = get_connection()

    cursor = connection.cursor()

    uploaded_at = datetime.now()

    cursor.execute(
        """
        INSERT INTO documents
        (
            document_id,
            filename,
            uploaded_at,
            total_pages,
            total_chunks
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING
            document_id,
            filename,
            uploaded_at,
            total_pages,
            total_chunks;
        """,
        (
            document_id,
            filename,
            uploaded_at,
            total_pages,
            total_chunks
        )
    )

    row = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return {

        "document_id": row[0],

        "filename": row[1],

        "uploaded_at":
            row[2].isoformat(),

        "total_pages": row[3],

        "total_chunks": row[4]

    }


def delete_document(document_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM documents
        WHERE document_id = %s;
        """,
        (document_id,)
    )

    deleted = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    return deleted