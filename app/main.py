from openai import OpenAI
import os
from dotenv import load_dotenv
from app.rag.retriever import retrieve
from app.agent.decision_agent import decision_agent
from app.memory.memory_store import update_user_preferences

# load env variables
load_dotenv()

# create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if __name__ == "__main__":
    print("Enter your preferences (press enter to skip):")

    budget = input("Budget: ")
    goal = input("Goal (e.g., programming, gaming): ")
    priority = input("Priority (e.g., battery, performance): ")

    prefs = {}

    if budget:
       prefs["budget"] = budget
    if goal:
       prefs["goal"] = goal
    if priority:
       prefs["priority"] = priority

    if prefs:
       update_user_preferences(prefs)
    user_input = input("Enter your decision problem: ")

    result = decision_agent(user_input)

    print("\n" + "="*50)
    print("AI Decision:\n")
    print(result)
    print("="*50)