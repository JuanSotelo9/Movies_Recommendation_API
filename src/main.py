"""

"""

from db.postgres import init_pool, close_pool
from db.neo4j import init_driver, close_driver

from repositories.postgres_repo import GenreRepo  as PgGenreRepo
from repositories.postgres_repo import MovieRepo  as PgMovieRepo
from repositories.postgres_repo import ActorRepo  as PgActorRepo
from repositories.postgres_repo import UserRepo   as PgUserRepo

def separador(titulo: str):
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print(f"{'─' * 50}")

separador("Iniciando conexiones")
init_pool()
init_driver()

separador("PostgreSQL — Géneros")
 
generos = PgGenreRepo.get_all()
print(f"Total géneros encontrados: {len(generos)}")
for g in generos[:4]:           # mostrar solo los primeros 4
    print(f"  id={g['id']}  nombre={g['name']}")
 
 
separador("PostgreSQL — Una película por ID")
 
pelicula = PgMovieRepo.get_by_id(1)   # Inception
print(f"Título   : {pelicula['title']} ({pelicula['year']})")
print(f"Tipo     : {pelicula['type']}")
print(f"Géneros  : {pelicula['genres']}")
print(f"Actores  : {pelicula['actors']}")
 
 
separador("PostgreSQL — Actor con sus películas")
 
actor = PgActorRepo.get_by_id(1)      # Leonardo DiCaprio
print(f"Actor    : {actor['name']} (nacido {actor['birth_year']})")
print(f"Películas: {actor['movies']}")
 
 
separador("PostgreSQL — Usuario con géneros favoritos")
 
usuario = PgUserRepo.get_by_id(1)     # Carlos Mendoza
print(f"Usuario  : {usuario['name']} — {usuario['email']}")
print(f"Favoritos: {usuario['favorite_genres']}")
print(f"Calificaciones hechas: {usuario['movies_rated']}")