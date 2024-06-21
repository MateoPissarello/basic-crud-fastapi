from fastapi.security import HTTPBearer
from fastapi import status as status_code
from fastapi import HTTPException, Request
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(
                status_code=status_code.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )
