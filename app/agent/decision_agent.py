from app.rag.retriever import retrieve
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.memory.memory_store import get_user_preferences, update_user_preferences

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def filter_options_by_budget(options, budget):
    filtered = []

    for option in options:
        name = option["name"]
        price = option["price"]

        if price <= budget:
            filtered.append(option)

    return filtered


def decision_agent(user_query):
    # load user preferences
    prefs = get_user_preferences()

    budget = int(prefs.get("budget", 999999))
    prefs_text = "\n".join([f"- {k}: {v}" for k, v in prefs.items()])

    options = [
        {"name": "MacBook Air M2", "price": 1200},
        {"name": "Dell XPS 15", "price": 1800}
    ]

    filtered_options = filter_options_by_budget(options, budget)


   
    options_text = "\n".join(
        [f"- {opt['name']} (${opt['price']})" for opt in filtered_options]
    )

    # Retrieve context (RAG)
    docs = retrieve(user_query)
    context = "\n".join([doc.page_content for doc in docs])

    

    # Build structured reasoning prompt
    prompt = f"""
You are an AI Decision Agent.

User preferences:
{prefs_text}

Available options (filtered by system):
{options_text}

Retrieved context:
{context}

Instructions:
- ONLY choose from the available options
- Do not suggest options outside the list
- Strongly follow user preferences

Respond in this format:
1. Problem Understanding
2. Options
3. Comparison Table
4. Pros and Cons
5. Final Recommendation
6. Reasoning
"""


    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content