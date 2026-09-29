import os

import chromadb
from ollama import embed


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "embeddinggemma"

KNOWLEDGE_FOLDER = "knowledge"

CHROMA_PATH = "chroma_db"

COLLECTION_NAME = "local_ai_agent"


# ============================================================
# CHROMA DATABASE
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():
    """
    Load .txt and .md files from the knowledge folder.
    """

    documents = []

    # Make sure knowledge folder exists
    if not os.path.exists(KNOWLEDGE_FOLDER):

        print(
            f"Knowledge folder not found: "
            f"{KNOWLEDGE_FOLDER}"
        )

        return documents


    # --------------------------------------------
    # Read every file
    # --------------------------------------------

    for filename in os.listdir(KNOWLEDGE_FOLDER):

        filepath = os.path.join(
            KNOWLEDGE_FOLDER,
            filename
        )


        # Skip directories
        if not os.path.isfile(filepath):
            continue


        # Only process text/markdown files
        if not filename.endswith(
            (".txt", ".md")
        ):
            continue


        # Read file
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()


        documents.append(
            {
                "filename": filename,
                "content": content
            }
        )


    return documents


# ============================================================
# CHUNK TEXT
# ============================================================

def chunk_text(
    text,
    chunk_size=500
):
    """
    Split text into chunks of approximately
    chunk_size words.
    """

    words = text.split()

    chunks = []


    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[
                i:i + chunk_size
            ]
        )


        if chunk.strip():

            chunks.append(
                chunk
            )


    return chunks


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):
    """
    Convert text into an embedding vector
    using Ollama.
    """

    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )


    return response.embeddings[0]


# ============================================================
# INDEX DOCUMENTS
# ============================================================

def index_documents():
    """
    Load documents, split them into chunks,
    create embeddings and store them in ChromaDB.
    """

    documents = load_documents()


    # --------------------------------------------
    # No documents
    # --------------------------------------------

    if not documents:

        print(
            "No documents found inside "
            f"'{KNOWLEDGE_FOLDER}/'"
        )

        return


    total_chunks = 0


    # ========================================================
    # PROCESS EACH DOCUMENT
    # ========================================================

    for document in documents:

        filename = document["filename"]

        content = document["content"]


        print(
            f"\nProcessing: {filename}"
        )


        # --------------------------------------------
        # Split document
        # --------------------------------------------

        chunks = chunk_text(
            content
        )


        print(
            f"Found {len(chunks)} chunk(s)"
        )


        # ====================================================
        # PROCESS EACH CHUNK
        # ====================================================

        for index, chunk in enumerate(chunks):


            # ----------------------------------------
            # Create unique ID
            # ----------------------------------------

            document_id = (
                f"{filename}_{index}"
            )


            # ----------------------------------------
            # Check if already indexed
            # ----------------------------------------

            existing = collection.get(
                ids=[document_id]
            )


            if existing["ids"]:

                print(
                    f"Skipping existing chunk: "
                    f"{document_id}"
                )

                continue


            # ----------------------------------------
            # Create embedding
            # ----------------------------------------

            print(
                f"Embedding chunk "
                f"{index + 1}/{len(chunks)}..."
            )


            vector = create_embedding(
                chunk
            )


            # ----------------------------------------
            # Store in ChromaDB
            # ----------------------------------------

            collection.add(
                ids=[document_id],

                embeddings=[vector],

                documents=[chunk],

                metadatas=[
                    {
                        "source": filename
                    }
                ]
            )


            total_chunks += 1


    # ========================================================
    # COMPLETE
    # ========================================================

    print(
        f"\nIndexed {total_chunks} new chunk(s)."
    )


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve(
    query,
    top_k=3
):
    """
    Search the vector database for the most
    relevant document chunks.
    """

    # --------------------------------------------
    # Convert query to embedding
    # --------------------------------------------

    query_embedding = create_embedding(
        query
    )


    # --------------------------------------------
    # Search ChromaDB
    # --------------------------------------------

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k
    )


    # --------------------------------------------
    # Extract documents
    # --------------------------------------------

    documents = results.get(
        "documents",
        [[]]
    )[0]


    # --------------------------------------------
    # Extract metadata
    # --------------------------------------------

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    retrieved = []


    # --------------------------------------------
    # Build result list
    # --------------------------------------------

    for document, metadata in zip(
        documents,
        metadatas
    ):

        retrieved.append(
            {
                "content": document,
                "source": metadata["source"]
            }
        )


    return retrieved


# ============================================================
# TEST RAG SYSTEM
# ============================================================

if __name__ == "__main__":

    print(
        "=========================================="
    )

    print(
        "        LOCAL AI AGENT - RAG TEST"
    )

    print(
        "=========================================="
    )


    # --------------------------------------------
    # Index documents
    # --------------------------------------------

    print(
        "\n[Indexing knowledge base...]"
    )


    index_documents()


    # --------------------------------------------
    # Test retrieval
    # --------------------------------------------

    print(
        "\n[Testing retrieval...]"
    )


    query = (
        "What is an AI agent?"
    )


    results = retrieve(
        query,
        top_k=3
    )


    # --------------------------------------------
    # Display results
    # --------------------------------------------

    print(
        "\nRetrieved Documents:"
    )


    if not results:

        print(
            "No relevant documents found."
        )


    else:

        for result in results:

            print(
                "\n----------------------------------------"
            )

            print(
                "Source:",
                result["source"]
            )

            print(
                "Content:"
            )

            print(
                result["content"]
            )

            print(
                "----------------------------------------"
            )