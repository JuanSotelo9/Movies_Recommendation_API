"""
Modelos Pydantic para validación de datos.

Pydantic valida automáticamente los tipos al recibir datos del cliente
y al serializar respuestas. Si un campo no cumple el tipo esperado,
FastAPI devuelve un 422 Unprocessable Entity con detalles del error.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional

class GenreCreate(BaseModel):
    """Datos necesarios para crear un nuevo género."""
    name: str = Field(..., min_length=2, max_length=100, examples=["Horror"])

class Genre(GenreCreate):
    """Género completo con id (se devuelve al cliente)."""
    id: int

class ActorCreate(BaseModel):
    name:       str = Field(..., min_length=2, max_length=200)
    birth_year: Optional[int] = Field(None, ge=1880, le=2025)

class Actor(ActorCreate):
    id: int

class MovieCreate(BaseModel):
    title:    str = Field(..., min_length=1, max_length=300)
    year:     Optional[int] = Field(None, ge=1888, le=2030)
    type:     Literal["movie", "series"] = "movie"
    synopsis: Optional[str] = None
    # IDs de géneros y actores para crear las relaciones de inmediato
    genre_ids: list[int] = Field(default=[], description="IDs de géneros asociados")
    actor_ids: list[int] = Field(default=[], description="IDs de actores que participan")

class Movie(BaseModel):
    id:       int
    title:    str
    year:     Optional[int]
    type:     str
    synopsis: Optional[str]

class UserCreate(BaseModel):
    name:             str = Field(..., min_length=2, max_length=200)
    email:            EmailStr
    favorite_genre_ids: list[int] = Field(default=[], description="IDs de géneros favoritos")

class User(BaseModel):
    id:    int
    name:  str
    email: str

class RatingCreate(BaseModel):
    user_id:  int
    movie_id: int
    rating:   float = Field(..., ge=0.0, le=5.0)
    watched:  bool = True

class Rating(RatingCreate):
    pass


class FriendshipCreate(BaseModel):
    user1_id: int
    user2_id: int


class BenchmarkTimes(BaseModel):
    """Tiempos de ejecución comparativos entre los dos motores."""
    neo4j_ms:    float
    postgres_ms: float
    winner:      Literal["neo4j", "postgres", "tie"]


class FriendMovie(BaseModel):
    """Una película que un amigo calificó bien y yo no he visto."""
    movie_id:           int
    title:              str
    year:               Optional[int]
    type:               str
    avg_friend_rating:  float
    friends_who_watched: list[dict]  # [{name, rating}]

class Q1Response(BaseModel):
    query_id:  str = "q1"
    user_id:   int
    results:   list[FriendMovie]
    benchmark: BenchmarkTimes


class ActorConnection(BaseModel):
    """Un actor conectado a 2 grados de separación del actor base."""
    actor_id:        int
    name:            str
    degree:          int
    connection_path: list[dict]   # [{actor, movie}]

class Q2Response(BaseModel):
    query_id:    str = "q2"
    actor_x:     dict             # {id, name}
    results:     list[ActorConnection]
    total_found: int
    benchmark:   BenchmarkTimes


class GenreSuggestion(BaseModel):
    """Un género sugerido con películas de ejemplo."""
    genre:               str
    score:               float     # 0-1, relevancia relativa
    similar_users_count: int
    sample_movies:       list[dict]

class Q3Response(BaseModel):
    query_id:         str = "q3"
    reference_movie:  dict         # {id, title, my_rating}
    my_genres:        list[str]
    suggested_genres: list[GenreSuggestion]
    benchmark:        BenchmarkTimes