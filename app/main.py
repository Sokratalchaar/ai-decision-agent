from openai import OpenAI
import os
from dotenv import load_dotenv
from app.rag.retriever import retrieve

# load env variables
load_dotenv()

# create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_llm(prompt):
    docs = retrieve(prompt)

    context = "\n".join([doc.page_content for doc in docs])

    system_prompt = f"""
    You are an AI Decision Assistant.

    Use the following retrieved information to help answer:

    {context}

    Always respond in this format:

    1. Problem Understanding
    2. Options Identified
    3. Comparison Table
    4. Pros and Cons
    5. Final Recommendation
    6. Reasoning
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    user_input = input("Enter your decision problem: ")
    result = ask_llm(user_input)

    print("\n" + "="*50)
    print("AI DECISION RESULT")
    print("="*50 + "\n")
    print(result)