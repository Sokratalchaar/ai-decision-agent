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

    if not filtered_options:
        return "No available options within your budget."
   
    options_text = "\n".join(
        [f"- {opt['name']} (${opt['price']})" for opt in filtered_options]
    )

    # 💣 1. Research Agent
    allowed_names = [opt["name"] for opt in filtered_options]

    context = research_agent(user_query, allowed_names)

    # 💣 2. Analysis Agent
    analysis = analysis_agent(user_query, context, options_text, prefs_text)

    

    # Decision Agent (final)
    final_prompt = f"""
You are a Decision Agent.

User preferences:
{prefs_text}

Available options:
{options_text}

Analysis:
{analysis}

Important rules:
- You are STRICTLY limited to the provided options
- Do NOT introduce any new options under any condition
- If an option is not listed, ignore it completely
- If you mention any option outside the list, your answer is invalid

Now give FINAL decision.

Format:
1. Problem Understanding
2. Options
3. Comparison Summary
4. Final Recommendation
5. Reasoning
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": final_prompt}]
    )

    return response.choices[0].message.content