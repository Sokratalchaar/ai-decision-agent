from app.rag.retriever import retrieve

def research_agent(query):
    docs = retrieve(query)

    return "\n".join([doc.page_content for doc in docs])