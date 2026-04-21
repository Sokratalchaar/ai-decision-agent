from dotenv import load_dotenv
import os

load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def create_vector_db():
    loader = TextLoader("data/laptops.txt")
    documents = loader.load()

    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(documents, embeddings)
    db.save_local("faiss_index")

    print("Vector DB created!")

if __name__ == "__main__":
    create_vector_db()