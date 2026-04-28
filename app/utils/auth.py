from fastapi import Header
from app.utils.jwt import decode_token

def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    return payload["user_id"]