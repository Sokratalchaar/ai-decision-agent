from app.rag.retriever import retrieve

def research_agent(query, allowed_names):
    docs = retrieve(query)

    filtered_context = ""

    for doc in docs:
        for name in allowed_names:
            if name.lower() in doc.page_content.lower():
                filtered_context += doc.page_content + "\n"

    return filtered_context