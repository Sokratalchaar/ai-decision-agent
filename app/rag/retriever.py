from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def load_db():
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db

def retrieve(query):
    db = load_db()
    docs = db.similarity_search(query, k=3)
    return docs