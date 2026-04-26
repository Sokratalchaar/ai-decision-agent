import json
from app.db import SessionLocal
from app.models.chat import Chat

def get_all_chats():
    db = SessionLocal()
    chats = db.query(Chat).all()

    result = []
    for chat in chats:
        result.append({
            "id": chat.id,
            "title": chat.title,
            "messages": json.loads(chat.messages)
        })

    db.close()
    return result


def save_all_chats(conversations):
    db = SessionLocal()

    db.query(Chat).delete()  # 🔥 overwrite

    for conv in conversations:
        chat = Chat(
            id=conv["id"],
            title=conv.get("title", ""),
            messages=json.dumps(conv["messages"])
        )
        db.add(chat)

    db.commit()
    db.close()