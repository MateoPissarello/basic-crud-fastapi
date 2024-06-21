from fastapi import status as status_code
from fastapi import APIRouter
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas import auth as auth_schemas

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post(
    "/login",
    status_code=status_code.HTTP_200_OK
)
async def login(user_req: auth_schemas.UserLogin):
    if user_req.email == "admin@gmail.com" and user_req.password == "admin":
        token = create_token(user_req.model_dump())
    return JSONResponse(content={"token": token})
