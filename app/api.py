from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.decision_agent import decision_agent
from app.memory.memory_store import update_user_preferences
from app.utils.jwt import create_token


from app.db import engine, Base
from app.db import SessionLocal
from app.models.user import User
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.models.chat import Chat
from app.services.chat_db import get_all_chats, save_all_chats

from fastapi import Depends
from app.utils.auth import get_current_user


from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 🔥 حددها هيك
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

# 🧠 شكل البيانات اللي رح تجي من المستخدم
class DecisionRequest(BaseModel):
    query: str
    budget: int | None = None
    goal: str | None = None
    priority: str | None = None


@app.get("/")
def root():
    return {"message": "AI Decision API is running 🚀"}



@app.post("/register")
def register(data: dict = Body(...)):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == data["email"]).first()

    if existing:
        return {"error": "Email already exists"}

    hashed = hash_password(data["password"])

    user = User(
        email=data["email"],
        password=hashed
    )

    db.add(user)
    db.commit()

    db.close()

    return {"message": "User created"}



@app.post("/login")
def login(data: dict = Body(...)):
    db = SessionLocal()

    user = db.query(User).filter(User.email == data["email"]).first()

    if not user or not verify_password(data["password"], user.password):
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": user.id})

    return {"token": token}



@app.get("/chats")
def get_chats(user=Depends(get_current_user)):
    return get_all_chats(user)



@app.post("/chats")
def save_chats(data: dict = Body(...), user=Depends(get_current_user)):
    conversations = data["conversations"]
    save_all_chats(conversations, user)
    return {"status": "ok"}



@app.post("/decision")
def make_decision(request: DecisionRequest):
    # preferences
    prefs = {}

    if request.budget:
        prefs["budget"] = str(request.budget)
    if request.goal:
        prefs["goal"] = request.goal
    if request.priority:
        prefs["priority"] = request.priority

    if prefs:
        update_user_preferences(prefs)

 
    result = decision_agent(request.query)

    return {
        "query": request.query,
        "result": result
    }


@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, user=Depends(get_current_user)):
    db = SessionLocal()

    chat = db.query(Chat).filter(
         Chat.id == chat_id,
         Chat.user_id == user
    ).first()

    if chat:
        db.delete(chat)
        db.commit()

    db.close()
    return {"status":"deleted"}    