import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_pinecone import Pinecone as PineconeVectorStore
from pinecone import Pinecone

# -----------------------------
# Load PDF
# -----------------------------

loader = PyPDFLoader("./story.pdf")
docs = loader.load()

# -----------------------------
# Embeddings
# -----------------------------
import os
import streamlit as st

# Check environment variables first, then safely check Streamlit secrets
import os
import streamlit as st
from pinecone import Pinecone

# Helper function to grab secrets safely from env OR Streamlit secrets
def get_secret(key_name):
    return os.getenv(key_name) or st.secrets.get(key_name)

# 1. Fetch Keys safely
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
PINECONE_API_KEY = get_secret("PINECONE_API_KEY")

# 2. Check missing keys before initializing Pinecone
if not PINECONE_API_KEY:
    st.error("⚠️ PINECONE_API_KEY is missing! Please set it in Streamlit Secrets or environment variables.")
    

if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY is missing! Please set it in Streamlit Secrets or environment variables.")
    

# 3. Initialize Pinecone safely
pc = Pinecone(api_key=PINECONE_API_KEY)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    output_dimensionality=1024
)

# -----------------------------
# Pinecone
# -----------------------------

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("genai")

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# --------------------------------------------------
# Upload ONCE
# Uncomment only the first time
# --------------------------------------------------

# vector_store.add_documents(docs)
# print("PDF uploaded successfully!")

# -----------------------------
# Gemini LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# -----------------------------
# Ask Questions
# -----------------------------

while True:

    query = input("\nAsk your question (type exit to quit): ")

    if query.lower() == "exit":
        break

    # Retrieve relevant chunks
    retrieved_docs = vector_store.similarity_search(
        query,
        k=3
    )

    print("Retrieved docs:", len(retrieved_docs))

    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{query}
"""

    try:

        response = llm.invoke(prompt)

        # Extract only text
        if isinstance(response.content, list):

            answer = ""

            for item in response.content:
                if item.get("type") == "text":
                    answer += item["text"]

        else:
            answer = response.content

        print("\nAnswer:\n")
        print(answer)

    except Exception as e:
        print("Error:", e)
from dotenv import load_dotenv
load_dotenv()

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# -----------------------------
# Load PDF
# -----------------------------

loader = PyPDFLoader("./story.pdf")
docs = loader.load()

# -----------------------------
# Embeddings
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or st.secrets["PINECONE_API_KEY"]
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    output_dimensionality=1024
)

# -----------------------------
# Pinecone
# -----------------------------

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("genai")

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# --------------------------------------------------
# Upload ONCE
# Uncomment only the first time
# --------------------------------------------------

# vector_store.add_documents(docs)
# print("PDF uploaded successfully!")

# -----------------------------
# Gemini LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# -----------------------------
# Ask Questions
# -----------------------------

while True:

    query = input("\nAsk your question (type exit to quit): ")

    if query.lower() == "exit":
        break

    # Retrieve relevant chunks
    retrieved_docs = vector_store.similarity_search(
        query,
        k=3
    )

    print("Retrieved docs:", len(retrieved_docs))

    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{query}
"""

    try:

        response = llm.invoke(prompt)

        # Extract only text
        if isinstance(response.content, list):

            answer = ""

            for item in response.content:
                if item.get("type") == "text":
                    answer += item["text"]

        else:
            answer = response.content

        print("\nAnswer:\n")
        print(answer)

    except Exception as e:
        print("Error:", e)
