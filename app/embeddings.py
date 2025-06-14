from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY
from pathlib import Path

embedding_fn = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY,
    disallowed_special=()
)

BASE_DIR = Path(__file__).resolve().parent.parent  # goes up to project root

def create_vectorstore(docs, index_path="vector_store/faiss_index"):
    abs_path = BASE_DIR / index_path
    vectordb = FAISS.from_documents(docs, embedding_fn)
    vectordb.save_local(str(abs_path))  # Save to correct folder

def load_vectorstore(index_path="vector_store/faiss_index"):
    abs_path = BASE_DIR / index_path
    print(f"📂 Loading vector store from: {abs_path}")
    return FAISS.load_local(str(abs_path), embedding_fn, allow_dangerous_deserialization=True)
