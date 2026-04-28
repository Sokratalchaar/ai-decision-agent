from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    messages = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))  