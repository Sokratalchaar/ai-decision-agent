from app.rag.retriever import retrieve
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def decision_agent(user_query):
    # STEP 1: Retrieve context (RAG)
    docs = retrieve(user_query)
    context = "\n".join([doc.page_content for doc in docs])

    # STEP 2: Build structured reasoning prompt
    prompt = f"""
You are an AI Decision Agent.

Follow these steps:

1. Understand the user's goal
2. Use the retrieved information
3. Identify options
4. Compare them clearly
5. Give a final recommendation

User query:
{user_query}

Retrieved context:
{context}

Respond in this format:

1. Problem Understanding
2. Options
3. Comparison Table
4. Pros and Cons
5. Final Recommendation
6. Reasoning
"""

    # STEP 3: Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content