from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analysis_agent(user_query, context, options_text, prefs_text):
    prompt = f"""
You are an AI Analysis Agent.

User preferences:
{prefs_text}

Available options:
{options_text}

Context:
{context}

Important rules:
- You are STRICTLY limited to the provided options
- Do NOT introduce any new options
- Ignore any product not listed in the options
- Even if other products appear in the context, do NOT use them

Your job:
- Analyze ONLY the given options
- Compare them clearly
- Do NOT give final recommendation

Output:
- Key differences
- Strengths and weaknesses of each option
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content