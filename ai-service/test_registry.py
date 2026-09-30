from document_registry import delete_document


deleted = delete_document(
    "test-document-001"
)


if deleted == 1:

    print("Test document deleted successfully!")

else:

    print("Test document was not found!")