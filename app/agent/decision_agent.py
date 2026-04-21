from app.rag.retriever import retrieve
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.memory.memory_store import get_user_preferences, update_user_preferences

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def decision_agent(user_query):
    # STEP 1: Retrieve context (RAG)
    docs = retrieve(user_query)
    context = "\n".join([doc.page_content for doc in docs])

    # load user preferences
    prefs = get_user_preferences()

    prefs_text = "\n".join([f"{k}: {v}" for k, v in prefs.items()])

    # STEP 2: Build structured reasoning prompt
    prompt = f"""
You are an AI Decision Agent.

User preferences:
{prefs_text}

User query:
{user_query}

Retrieved context:
{context}

Instructions:
- Personalize the decision based on user preferences
- If preferences are missing, assume reasonable defaults

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