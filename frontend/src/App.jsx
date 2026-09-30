
import { useEffect, useState } from "react";

import {
  uploadDocument,
  getDocuments,
  askQuestion,
  getChats,
  getChatDetails,
  createChat,
  deleteChat
} from "./services/api";


function App() {

  // =====================================================
  // STATE
  // =====================================================

  const [documents, setDocuments] = useState([]);

  const [selectedDocument, setSelectedDocument] =
    useState(null);

  const [chats, setChats] = useState([]);

  const [sessionId, setSessionId] =
    useState(null);

  const [messages, setMessages] =
    useState([]);

  const [question, setQuestion] =
    useState("");

  const [asking, setAsking] =
    useState(false);

  const [uploading, setUploading] =
    useState(false);

  const [error, setError] =
    useState("");


  // =====================================================
  // LOAD DOCUMENTS
  // =====================================================

  useEffect(() => {

    async function loadDocuments() {

      try {

        const result =
          await getDocuments();

        setDocuments(
          result.documents
        );

      } catch (error) {

        setError(
          error.message ||
          "Failed to load documents."
        );

      }

    }

    loadDocuments();

  }, []);


  // =====================================================
  // LOAD CHAT HISTORY
  // =====================================================

  useEffect(() => {

    async function loadChats() {

      try {

        const result =
          await getChats();

        setChats(
          result.chats
        );

      } catch (error) {

        setError(
          error.message ||
          "Failed to load chat history."
        );

      }

    }

    loadChats();

  }, []);


  // =====================================================
  // UPLOAD DOCUMENT
  // =====================================================

  async function handleUpload(event) {

    const file =
      event.target.files[0];

    if (!file) {

      return;

    }


    if (
      file.type !==
      "application/pdf"
    ) {

      setError(
        "Please select a PDF file."
      );

      return;

    }


    try {

      setUploading(true);

      setError("");


      const result =
        await uploadDocument(file);


      setDocuments(
        (previousDocuments) => [

          ...previousDocuments,

          result.document

        ]
      );


      setSelectedDocument(
        result.document
      );


      setSessionId(null);

      setMessages([]);


    } catch (error) {

      setError(
        error.message ||
        "Failed to upload document."
      );

    } finally {

      setUploading(false);

      event.target.value = "";

    }

  }


  // =====================================================
  // CREATE NEW CHAT
  // =====================================================

  async function handleNewChat() {

    try {

      setError("");


      const result =
        await createChat(
          selectedDocument
            ? selectedDocument.document_id
            : null
        );


      const newChat =
        result.chat;


      setChats(
        (previousChats) => [

          newChat,

          ...previousChats

        ]
      );


      setSessionId(
        newChat.session_id
      );


      setMessages([]);

      setQuestion("");


    } catch (error) {

      setError(
        error.message ||
        "Failed to create new chat."
      );

    }

  }


  // =====================================================
  // ASK QUESTION
  // =====================================================

  async function handleAsk() {

    if (!question.trim()) {

      return;

    }


    if (!selectedDocument) {

      setError(
        "Please select a document first."
      );

      return;

    }


    try {

      setAsking(true);

      setError("");


      const currentQuestion =
        question.trim();


      // Add user message immediately

      setMessages(
        (previousMessages) => [

          ...previousMessages,

          {
            role: "user",
            content: currentQuestion
          }

        ]
      );


      setQuestion("");


      const result =
        await askQuestion(

          currentQuestion,

          selectedDocument.document_id,

          sessionId

        );


      // Save session ID if this
      // was the first question

      if (!sessionId) {

        setSessionId(
          result.session_id
        );


        // Reload chat history

        const chatsResult =
          await getChats();

        setChats(
          chatsResult.chats
        );

      }


      // Add AI response

      setMessages(
        (previousMessages) => [

          ...previousMessages,

          {
            role: "assistant",

            content:
              result.answer,

            sources:
              result.sources || []

          }

        ]
      );


    } catch (error) {

      setError(
        error.message ||
        "Failed to get answer."
      );

    } finally {

      setAsking(false);

    }

  }


  // =====================================================
  // SELECT DOCUMENT
  // =====================================================

  function handleSelectDocument(
    document
  ) {

    setSelectedDocument(
      document
    );

    setSessionId(null);

    setMessages([]);

    setQuestion("");

    setError("");

  }


  // =====================================================
  // LOAD EXISTING CHAT
  // =====================================================

  async function handleSelectChat(
    chat
  ) {

    try {

      setError("");


      const result =
        await getChatDetails(
          chat.session_id
        );


      setSessionId(
        result.session_id
      );


      setMessages(
        result.messages
      );


      setQuestion("");


      // Find the document
      // associated with this chat

      if (result.document_id) {

        const document =
          documents.find(
            (item) =>
              item.document_id ===
              result.document_id
          );


        if (document) {

          setSelectedDocument(
            document
          );

        }

      }

    } catch (error) {

      setError(
        error.message ||
        "Failed to load chat."
      );

    }

  }


  // =====================================================
  // DELETE CHAT
  // =====================================================

  async function handleDeleteChat(
    event,
    chat
  ) {

    event.stopPropagation();


    try {

      setError("");


      await deleteChat(
        chat.session_id
      );


      setChats(
        (previousChats) =>
          previousChats.filter(
            (item) =>
              item.session_id !==
              chat.session_id
          )
      );


      if (
        sessionId ===
        chat.session_id
      ) {

        setSessionId(null);

        setMessages([]);

      }

    } catch (error) {

      setError(
        error.message ||
        "Failed to delete chat."
      );

    }

  }


  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="app">


      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">


        <div className="logo">

          <h2>
            AI Study Assistant
          </h2>

        </div>


        <button
          className="new-chat-button"
          onClick={handleNewChat}
        >

          + New Chat

        </button>


        {/* ================= DOCUMENTS ================= */}

        <div className="sidebar-section">

          <h3>
            Documents
          </h3>


          {documents.length === 0 ? (

            <div className="document-item">

              No documents yet

            </div>

          ) : (

            documents.map(
              (document) => (

                <div
                  className={
                    selectedDocument?.document_id ===
                    document.document_id

                      ? "document-item selected"

                      : "document-item"
                  }

                  key={
                    document.document_id
                  }

                  onClick={() =>
                    handleSelectDocument(
                      document
                    )
                  }
                >

                  📄{" "}

                  {document.filename}

                </div>

              )
            )

          )}

        </div>


        {/* ================= CHAT HISTORY ================= */}

        <div className="sidebar-section">

          <h3>
            Chat History
          </h3>


          {chats.length === 0 ? (

            <div className="chat-item">

              No chats yet

            </div>

          ) : (

            chats.map(
              (chat) => (

                <div
                  className="chat-item"
                  key={
                    chat.session_id
                  }

                  onClick={() =>
                    handleSelectChat(
                      chat
                    )
                  }
                >

                  <span>

                    💬{" "}

                    {chat.title ||
                      "New Study Chat"}

                  </span>


                  <button
                    className="delete-chat-button"
                    onClick={(event) =>
                      handleDeleteChat(
                        event,
                        chat
                      )
                    }
                  >

                    ×

                  </button>

                </div>

              )
            )

          )}

        </div>


      </aside>


      {/* ================= MAIN CONTENT ================= */}

      <main className="main-content">


        {/* ================= TOP BAR ================= */}

        <header className="top-bar">


          <div>

            <h1>
              Study Assistant
            </h1>


            <p>

              {selectedDocument

                ? `Studying: ${selectedDocument.filename}`

                : "Select a document to start studying"

              }

            </p>

          </div>


          {/* ================= UPLOAD ================= */}

          <label
            className="upload-button"
          >

            {uploading

              ? "Uploading..."

              : "Upload PDF"

            }


            <input
              type="file"
              accept="application/pdf"
              onChange={
                handleUpload
              }
              hidden
            />

          </label>


        </header>


        {/* ================= ERROR ================= */}

        {error && (

          <div className="error-message">

            {error}

          </div>

        )}


        {/* ================= CHAT AREA ================= */}

        <section className="chat-area">


          {!selectedDocument ? (

            <div className="welcome-message">

              <div className="ai-icon">

                🤖

              </div>


              <h2>

                How can I help you study?

              </h2>


              <p>

                Select a document and ask
                questions about your study
                material.

              </p>

            </div>


          ) : messages.length === 0 ? (

            <div className="welcome-message">

              <div className="ai-icon">

                🤖

              </div>


              <h2>

                Ready to study!

              </h2>


              <p>

                Ask a question about your
                selected document.

              </p>

            </div>


          ) : (

            <div className="messages-container">


              {messages.map(
                (message, index) => (

                  <div
                    className={
                      message.role === "user"

                        ? "message user-message"

                        : "message assistant-message"
                    }

                    key={index}
                  >


                    <div className="message-role">

                      {message.role === "user"

                        ? "You"

                        : "AI Study Assistant"

                      }

                    </div>


                    <div className="message-content">

                      {message.content}

                    </div>


                    {/* ================= SOURCES ================= */}

                    {message.role ===
                      "assistant" &&

                      message.sources &&

                      message.sources.length >
                        0 && (

                        <div className="sources">

                          <strong>
                            Sources
                          </strong>


                          {message.sources.map(
                            (
                              source,
                              sourceIndex
                            ) => (

                              <div
                                className="source-item"
                                key={
                                  sourceIndex
                                }
                              >

                                Page{" "}

                                {
                                  source.page_number
                                }


                                {" · "}


                                Similarity:{" "}


                                {typeof source.similarity ===
                                "number"

                                  ? source.similarity.toFixed(
                                      3
                                    )

                                  : "N/A"

                                }

                              </div>

                            )
                          )}

                        </div>

                      )
                    }


                  </div>

                )
              )}


              {/* ================= THINKING ================= */}

              {asking && (

                <div className="message assistant-message">

                  <div className="message-role">

                    AI Study Assistant

                  </div>


                  <div className="message-content">

                    Thinking...

                  </div>

                </div>

              )}


            </div>

          )}


        </section>


        {/* ================= INPUT ================= */}

        <div className="input-area">


          <input

            type="text"

            value={question}

            placeholder={

              selectedDocument

                ? "Ask a question about your document..."

                : "Select a document first..."

            }

            disabled={
              !selectedDocument ||
              asking
            }

            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }

            onKeyDown={(event) => {

              if (

                event.key === "Enter" &&

                !event.shiftKey

              ) {

                event.preventDefault();

                handleAsk();

              }

            }}

          />


          <button

            onClick={handleAsk}

            disabled={

              !selectedDocument ||

              !question.trim() ||

              asking

            }

          >

            {asking

              ? "..."

              : "➤"

            }

          </button>


        </div>


      </main>


    </div>

  );

}


export default App;

