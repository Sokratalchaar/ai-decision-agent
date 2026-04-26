from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.decision_agent import decision_agent
from app.memory.memory_store import update_user_preferences
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body

from app.db import engine, Base
from app.models.chat import Chat
from app.services.chat_db import get_all_chats, save_all_chats

Base.metadata.create_all(bind=engine)



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 شكل البيانات اللي رح تجي من المستخدم
class DecisionRequest(BaseModel):
    query: str
    budget: int | None = None
    goal: str | None = None
    priority: str | None = None


@app.get("/")
def root():
    return {"message": "AI Decision API is running 🚀"}

@app.get("/chats")
def get_chats():
    return get_all_chats()


@app.post("/chats")
def save_chats(chats: list = Body(...)):
    save_all_chats(chats)
    return {"status": "ok"}


@app.post("/decision")
def make_decision(request: DecisionRequest):
    # 🟢 نخزّن preferences
    prefs = {}

    if request.budget:
        prefs["budget"] = str(request.budget)
    if request.goal:
        prefs["goal"] = request.goal
    if request.priority:
        prefs["priority"] = request.priority

    if prefs:
        update_user_preferences(prefs)

    # 🟢 نشغّل الagent
    result = decision_agent(request.query)

    return {
        "query": request.query,
        "result": result
    }