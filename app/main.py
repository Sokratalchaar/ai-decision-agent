from openai import OpenAI
import os
from dotenv import load_dotenv
from app.rag.retriever import retrieve
from app.agent.decision_agent import decision_agent

# load env variables
load_dotenv()

# create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if __name__ == "__main__":
    user_input = input("Enter your decision problem: ")

    result = decision_agent(user_input)

    print("\n" + "="*50)
    print("AI Decision:\n")
    print(result)
    print("="*50)