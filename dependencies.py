from fastapi import Header, HTTPException
from app.config import STATIC_TOKEN

def verify_token(authorization: str = Header(...)) -> None:
    if authorization != f"Bearer {STATIC_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
