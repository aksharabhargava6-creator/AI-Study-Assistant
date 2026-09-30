
const API_BASE_URL = "http://127.0.0.1:8001";


// ==============================
// DOCUMENT APIs
// ==============================

export async function uploadDocument(file) {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    `${API_BASE_URL}/documents/upload`,
    {
      method: "POST",
      body: formData
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to upload document"
    );

  }

  return response.json();
}


export async function getDocuments() {

  const response = await fetch(
    `${API_BASE_URL}/documents`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to load documents"
    );

  }

  return response.json();
}


export async function deleteDocument(
  documentId
) {

  const response = await fetch(
    `${API_BASE_URL}/documents/${documentId}`,
    {
      method: "DELETE"
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to delete document"
    );

  }

  return response.json();
}


// ==============================
// QUESTION / RAG API
// ==============================

export async function askQuestion(
  question,
  documentId,
  sessionId = null
) {

  const params = new URLSearchParams();

  params.append(
    "question",
    question
  );

  params.append(
    "document_id",
    documentId
  );

  if (sessionId) {

    params.append(
      "session_id",
      sessionId
    );

  }

  const response = await fetch(
    `${API_BASE_URL}/ask?${params.toString()}`,
    {
      method: "POST"
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to get answer"
    );

  }

  return response.json();
}


// ==============================
// CHAT APIs
// ==============================

export async function getChats() {

  const response = await fetch(
    `${API_BASE_URL}/chats`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to load chats"
    );

  }

  return response.json();
}


export async function getChatDetails(
  sessionId
) {

  const response = await fetch(
    `${API_BASE_URL}/chats/${sessionId}`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to load chat"
    );

  }

  return response.json();
}


export async function createChat(
  documentId = null
) {

  const params = new URLSearchParams();

  if (documentId) {

    params.append(
      "document_id",
      documentId
    );

  }

  const url =
    params.toString().length > 0

      ? `${API_BASE_URL}/chats?${params.toString()}`

      : `${API_BASE_URL}/chats`;


  const response = await fetch(
    url,
    {
      method: "POST"
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to create chat"
    );

  }

  return response.json();
}


export async function deleteChat(
  sessionId
) {

  const response = await fetch(
    `${API_BASE_URL}/chats/${sessionId}`,
    {
      method: "DELETE"
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail ||
      "Failed to delete chat"
    );

  }

  return response.json();
}

