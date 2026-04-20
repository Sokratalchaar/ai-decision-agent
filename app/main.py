from openai import OpenAI
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    user_input = input("Enter your decision problem: ")
    result = ask_llm(user_input)

    print("\nAI Response:\n")
    print(result)