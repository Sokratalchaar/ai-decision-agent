from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analysis_agent(user_query, context, prefs_text):
    prompt = f"""
You are an AI Analysis Agent.

User preferences:
{prefs_text}

User question:
{user_query}

Context:
{context}

IMPORTANT:
- Focus ONLY on products mentioned in the user query
- If the user mentioned specific products (e.g. MacBook, Dell), do NOT introduce others
- You may use the context only to enrich information about those products

Your job:
- Identify the products mentioned in the question
- Compare them clearly
- Highlight key differences
- Do NOT give final recommendation

Output:
- Key differences
- Pros and cons
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content