from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Root"], prefix="/root")


@router.get("/")
def message():
    return HTMLResponse(content="<h1>Hola mundo desde FastAPI<h1/>")
