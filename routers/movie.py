from fastapi import APIRouter, Depends, Query, Path
from typing import List
from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status as status_code
from fastapi import HTTPException
from schemas import movie as movie_schemas
from services.movie import MovieService

router = APIRouter(tags=["Movies"], prefix="/movies")


@router.get(
    "/",
    response_model=List[movie_schemas.RetrieveMovie],
    dependencies=[Depends(JWTBearer())],
)
async def get_movies() -> List[movie_schemas.RetrieveMovie]:
    db = Session()
    movies = MovieService(db).get_movies()
    # data = [sqlalchemy_model_to_dict(movie) for movie in movies]
    return JSONResponse(content=jsonable_encoder(movies))


@router.get("/by_category", response_model=List[movie_schemas.RetrieveMovie])
async def get_movies_filter(
    category: str = Query(min_length=5, max_length=20)
) -> List[movie_schemas.RetrieveMovie]:
    db = Session()
    data = MovieService(db).get_movies_by_category(category)
    if data:
        return JSONResponse(content=jsonable_encoder(data))
    raise HTTPException(
        status_code=status_code.HTTP_404_NOT_FOUND, detail="Movies not found"
    )


# Post
@router.post("/", response_model=movie_schemas.RetrieveMovie)
async def create_movie(
    movie: movie_schemas.CreateMovie,
) -> movie_schemas.RetrieveMovie:
    db = Session()
    check_movie = MovieService(db).get_movie_by_title(movie.title)
    if check_movie:
        raise HTTPException(
            status_code=status_code.HTTP_409_CONFLICT,
            detail="Movie already exists in the database",
        )
    post_movie_data = MovieService(db).create_movie(movie)
    return JSONResponse(
        content=jsonable_encoder(post_movie_data),
        status_code=status_code.HTTP_201_CREATED,
    )


@router.get("/{movie_id}", response_model=movie_schemas.RetrieveMovie)
async def get_movie(
    movie_id: int = Path(ge=1, le=2000)
) -> movie_schemas.RetrieveMovie:  # Validación de parámetros de ruta
    db = Session()
    movie = MovieService(db).get_movie_by_id(movie_id)
    if movie:
        return JSONResponse(
            content=jsonable_encoder(movie), status_code=status_code.HTTP_200_OK  # noqa
        )
    raise HTTPException(
        status_code=status_code.HTTP_404_NOT_FOUND,
        detail=f"Movie not found under id {movie_id}",
    )


# delete
@router.delete("/{movie_id}", response_model=dict)
async def delete_movie(movie_id: int) -> dict:
    db = Session()
    delete_message = MovieService(db).delete_movie(movie_id)
    if delete_message:
        return JSONResponse(content=delete_message)
    raise HTTPException(
        status_code=status_code.HTTP_404_NOT_FOUND,
        detail=f"Movie not found under the id {movie_id}",
    )


# Put
@router.put("/{movie_id}", response_model=movie_schemas.RetrieveMovie)
async def update_movie_put(
    movie_id: int, movie_new_data: movie_schemas.ModifyMoviePut
) -> movie_schemas.RetrieveMovie:
    db = Session()
    movie_update = MovieService(db).put_movie(movie_id, movie_new_data)
    if movie_update:
        return JSONResponse(
            content=jsonable_encoder(movie_update),
            status_code=status_code.HTTP_200_OK,  # noqa
        )
    raise HTTPException(
        status_code=status_code.HTTP_404_NOT_FOUND, detail="Movie not found"
    )


@router.patch("/{movie_id}", response_model=movie_schemas.RetrieveMovie)
async def update_movie_patch(
    movie_id: int, movie_new_data: movie_schemas.ModifyMoviePatch
) -> movie_schemas.RetrieveMovie:
    db = Session()
    movie = MovieService(db).get_movie_by_id(movie_id)
    if movie:
        modify_data = movie_new_data.dict(exclude_unset=True)
        for key, value in modify_data.items():
            setattr(movie, key, value)
        db.commit()
        db.refresh(movie)
        db.close()
        return JSONResponse(
            content=jsonable_encoder(movie), status_code=status_code.HTTP_200_OK  # noqa
        )
    raise HTTPException(
        status_code=status_code.HTTP_404_NOT_FOUND, detail="Movie not found"
    )
