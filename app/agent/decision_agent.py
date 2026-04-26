from app.rag.retriever import retrieve
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.memory.memory_store import get_user_preferences, update_user_preferences
from app.agent.research_agent import research_agent
from app.agent.analysis_agent import analysis_agent

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
def extract_preferences_llm(text):
    prompt = f"""
Extract user preferences from the following text.

Return ONLY JSON like this:
{{
  "budget": number or null,
  "goal": string or null,
  "priority": string or null
}}

Text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    import json
    try:
        prefs = json.loads(content)
    except:
        prefs = {}

    return prefs

def classify_query(query):
    prompt = f"""
Classify the following user query into ONE of these categories:

- decision → user wants recommendation
- comparison → comparing products
- options → user asks for available choices/options
- info → asking about a product
- general → greeting or casual

Query:
{query}

Answer ONLY with one word.
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content.strip().lower()

def decision_agent(user_query):
    query_type = classify_query(user_query)
     # 🔥 1. extract from LLM
    extracted = extract_preferences_llm(user_query)

    # load user preferences
    prefs = get_user_preferences()
    # 🔥 3. override memory with new data
    cleaned = {k: v for k, v in extracted.items() if v}

    prefs.update(cleaned)

    # 🔥 4. SAVE memory (المهم 🔥)
    if cleaned:
        update_user_preferences(prefs)
        
    
    prefs_text = ""
    if query_type == "decision":
       prefs_text = "\n".join([f"- {k}: {v}" for k, v in prefs.items()])


    context = research_agent(user_query)

    # 💣 2. Analysis Agent
    analysis = ""
    if query_type == "decision":
       analysis = analysis_agent(user_query, context, prefs_text)

    

    # Decision Agent (final)
    final_prompt = f"""
You are an AI assistant.

Query type: {query_type}

IMPORTANT:
- If query is "general" → respond naturally, ignore memory
- If query is "info" → explain using context only
- If query is "decision" → use memory and analysis and give a recommendation
- If query is "options" → list available options clearly WITHOUT giving a final recommendation

STRICT RULES:
- ALWAYS answer based on the user's question intent
- DO NOT force a recommendation unless it's a decision query
- If listing options → be clear and structured (bullet points)

User question:
{user_query}

{"User preferences:\n" + prefs_text if (prefs_text and query_type == "decision") else ""}

{"Analysis:\n" + analysis if (analysis and query_type == "decision") else ""}

Context:
{context}

Now give the best possible answer.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": final_prompt}]
    )

    return response.choices[0].message.content