from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CreateMovie(BaseModel):
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=5, max_length=50)
    year: int = Field(
        le=2024,
    )
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=3, max_length=20)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "title": "El título de la película",
                "overview": "Descripción de la película",
                "year": 2021,
                "rating": 9.0,
                "category": "Categoria de la película",
            }
        },
    }


class ModifyMoviePatch(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None


class ModifyMoviePut(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


class RetrieveMovie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str
    model_config = ConfigDict(from_attributes=True)
