from jwt import encode, decode
import os
from dotenv import load_dotenv

load_dotenv()


def create_token(data: dict) -> str:
    token = encode(payload=data, key=os.getenv("SECRET_KEY_JWT"), algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    try:
        return decode(jwt=token, key=os.getenv("SECRET_KEY_JWT"), algorithms=["HS256"])
    except Exception as e:
        raise e
