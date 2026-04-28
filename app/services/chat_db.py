import json
from app.db import SessionLocal
from app.models.chat import Chat

def get_all_chats(user_id):
    db = SessionLocal()
    chats = db.query(Chat).filter(Chat.user_id == user_id).all()

    result = []
    for chat in chats:
        result.append({
            "id": chat.id,
            "title": chat.title,
            "messages": json.loads(chat.messages)
        })

    db.close()
    return result


def save_all_chats(conversations, user_id):
    db = SessionLocal()

    for conv in conversations:
        existing = db.query(Chat).filter(
            Chat.id == conv["id"],
            Chat.user_id == user_id
        ).first()

        messages = conv.get("messages", [])

        if existing:
            existing.title = conv.get("title", "")
            existing.messages = json.dumps(messages)
        else:
            chat = Chat(
                id=conv["id"],
                title=conv.get("title", ""),
                messages=json.dumps(messages),
                user_id=user_id
            )
            db.add(chat)

    db.commit()
    db.close()