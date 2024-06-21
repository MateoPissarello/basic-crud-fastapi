from fastapi import FastAPI

from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import router as movie_router
from routers.auth import router as auth_router
from routers.root import router as root_router

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

app.include_router(movie_router)
app.include_router(auth_router)
app.include_router(root_router)
app.add_middleware(ErrorHandler)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)
