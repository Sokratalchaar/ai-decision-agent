import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_user_preferences(new_data):
    memory = load_memory()
    memory.update(new_data)
    save_memory(memory)


def get_user_preferences():
    return load_memory()