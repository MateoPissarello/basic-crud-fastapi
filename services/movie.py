from models.movie import Movie as MovieModel
from schemas.movie import CreateMovie, ModifyMoviePut


class MovieService:
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        return self.db.query(MovieModel).all()

    def get_movie_by_id(self, movie_id: int):
        return (
            self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        )  # noqa

    def get_movies_by_category(self, category: str):
        return (
            self.db.query(MovieModel).filter(MovieModel.category == category).all()
        )  # noqa

    def create_movie(self, movie: CreateMovie):
        new_movie = MovieModel(**movie.dict(exclude_unset=True))
        self.db.add(new_movie)
        self.db.commit()
        self.db.refresh(new_movie)
        return new_movie

    def put_movie(self, movie_id: int, movie_new_data: ModifyMoviePut):
        movie = self.get_movie_by_id(movie_id)
        if movie:
            for key, value in movie_new_data.dict().items():
                setattr(movie, key, value)
            self.db.commit()
            self.db.refresh(movie)
            return movie

    def get_movie_by_title(self, title: str):
        return self.db.query(MovieModel).filter(MovieModel.title == title).first()

    def delete_movie(self, movie_id: int):
        movie = self.get_movie_by_id(movie_id)
        if movie:
            self.db.delete(movie)
            self.db.commit()
            return {"message": "Movie deleted"}
        return None
