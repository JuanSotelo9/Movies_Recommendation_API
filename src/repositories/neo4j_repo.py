"""
Capa de acceso a datos para Neo4j
"""

from db.neo4j import neo4j_session, neo4j_record_to_dict
from models import (
    GenreCreate, ActorCreate, MovieCreate, UserCreate,
    RatingCreate, FriendshipCreate
)

class GenreRepo:
    """Repositorio para manejar operaciones relacionadas con géneros en Neo4j."""
    @staticmethod
    def get_all() -> list[dict]:
        """Obtiene todos los géneros almacenados en Neo4j."""
        with neo4j_session() as session:
            result = session.run("MATCH (g:Genre) RETURN g ORDER BY g.name")
            return [dict(record["g"].items()) for record in result]

    @staticmethod
    def get_by_id(genre_id: int) -> dict | None:
        """Obtiene un género por su ID."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (g:Genre {id: $id}) RETURN g",
                id=genre_id
            )
            record = result.single()
            return dict(record["g"].items()) if record else None
        
    @staticmethod
    def create(genre_id: int, data: GenreCreate) -> dict:
        """Crea un nuevo género en Neo4j."""
        with neo4j_session() as session:
            result = session.run(
                "CREATE (g:Genre {id: $id}) ON CREATE SET g.name = $name RETURN g",
                id=genre_id, name=data.name
            )
            record = result.single()
            return dict(record["g"].items())
        
    @staticmethod
    def delete(genre_id: int) -> bool:
        """Elimina un género por su ID."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (g:Genre {id: $id}) DETACH DELETE g",
                id=genre_id
            )
            
            return result.consumed().counters.nodes_deleted > 0
        
    @staticmethod
    def update(genre_id: int, data: GenreCreate) -> dict | None:
        """Actualiza un género existente."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (g:Genre {id: $id}) SET g.name = $name RETURN g",
                id=genre_id, name=data.name
            )
            record = result.single()
            return dict(record["g"].items()) if record else None
        
class ActorRepo:
    """Repositorio para manejar operaciones relacionadas con actores en Neo4j."""
    
    @staticmethod
    def get_all() -> list[dict]:
        """Obtiene todos los actores almacenados en Neo4j."""
        with neo4j_session() as session:
            result = session.run("MATCH (a:Actor) RETURN a ORDER BY a.name")
            return [dict(record["a"].items()) for record in result]
        
    @staticmethod
    def get_by_id(actor_id: int) -> dict | None:
        """Obtiene un actor por su ID junto con las peliculas en las que actuo."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (a:Actor {id: $id})" \
                "OPTIONAL MATCH (a)-[:ACTED_IN]->(m:Movie) " \
                "RETURN a, collect(m.title) AS movies",
                id=actor_id
            )
            record = result.single()
            if not record:
                return None
            actor = dict(record["a"].items())
            actor["movies"] = record["movies"]
            return actor
        
    @staticmethod
    def create(actor_id: int, data: ActorCreate) -> dict:
        """Crea un nuevo actor en Neo4j."""
        with neo4j_session() as session:
            result = session.run(
                "CREATE (a:Actor {id: $id}) ON CREATE SET a.name = $name, a.birth_year = $birth_year RETURN a",
                id=actor_id, name=data.name, birth_year=data.birth_year
            )
            record = result.single()
            return dict(record["a"].items()) if record else None
        
    @staticmethod
    def delete(actor_id: int) -> bool:
        """Elimina un actor por su ID."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (a:Actor {id: $id}) DETACH DELETE a",
                id=actor_id
            )
            
            return result.consumed().counters.nodes_deleted > 0
    
    @staticmethod
    def update(actor_id: int, data: ActorCreate) -> dict | None:
        """Actualiza un actor existente."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (a:Actor {id: $id})" \
                " SET a.name = $name, a.birth_year = $birth_year" \
                " RETURN a",
                id=actor_id, name=data.name, birth_year=data.birth_year
            )
            record = result.single()
            return dict(record["a"].items()) if record else None
        
class MovieRepo:
    """Repositorio para manejar operaciones relacionadas con películas en Neo4j."""
    @staticmethod
    def get_all(type_filter: str | None = None) -> list[dict]:
        """Obtiene todas las películas almacenadas en Neo4j."""
        with neo4j_session() as session:
            if type_filter:
                result = session.run("MATCH (m:Movie {type: $type}) RETURN m ORDER BY m.year DESC", type=type_filter)
            else:
                result = session.run("MATCH (m:Movie) RETURN m ORDER BY m.year DESC")
            return [dict(record["m"].items()) for record in result]
        
    @staticmethod
    def get_by_id(movie_id: int) -> dict | None:
        """Obtiene una película por su ID junto con sus géneros y actores."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (m:Movie {id: $id})"
                "OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre) " \
                "OPTIONAL MATCH (a:Actor)-[:ACTED_IN]->(m) " \
                "RETURN " \
                "m, " \
                "collect(DISTINCT {id: g.id, name: g.name}) AS genres," \
                "collect(DISTINCT {id: a.id, name: a.name}) AS actors",
                id=movie_id
            )
            record = result.single()
            if not record:
                return None
            movie = dict(record["m"].items())

            movie["genres"] = [g for g in record["genres"] if g["id"] is not None]
            movie["actors"] = [a for a in record["actors"] if a["id"] is not None]
            return movie
        
    @staticmethod
    def create(movie_id: int, data: MovieCreate) -> dict:
        """Crea una nueva película en Neo4j y sus relaciones con generos y actores."""
        with neo4j_session() as session:
            tx = session.begin_transaction()
            try:
                result = tx.run(
                    """
                    MERGE (m:Movie {id: $id})
                    ON CREATE SET 
                        m.title = $title, 
                        m.year = $year, 
                        m.type = $type,
                        m.synopsis = $synopsis
                    RETURN m
                    """,
                    id=movie_id, title=data.title, year=data.year, type=data.type, synopsis=data.synopsis
                )
                movie = dict(result.single()["m"].items())

                # Crear relaciones con géneros
                for genre in data.genre_ids:
                    tx.run(
                        "MATCH (m:Movie {id: $movie_id}), (g:Genre {id: $genre_id}) "
                        "MERGE (m)-[:HAS_GENRE]->(g)",
                        movie_id=movie_id, genre_id=genre
                    )

                # Crear relaciones con actores
                for actor in data.actor_ids:
                    tx.run(
                        "MATCH (a:Actor {id: $actor_id}), (m:Movie {id: $movie_id}) "
                        "MERGE (a)-[:ACTED_IN]->(m)",
                        movie_id=movie_id, actor_id=actor
                    )

                tx.commit()
                return movie
            except Exception as e:
                tx.rollback()
                raise e

    @staticmethod
    def delete(movie_id: int) -> bool:
        """Elimina una película por su ID."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (m:Movie {id: $id}) DETACH DELETE m",
                id=movie_id
            )
            
            return result.consumed().counters.nodes_deleted > 0

    @staticmethod
    def update(movie_id: int, data: MovieCreate) -> dict | None:
        """Actualiza una película existente."""
        with neo4j_session() as session:
            tx = session.begin_transaction()
            try:
                result = tx.run(
                    """
                    MATCH (m:Movie {id: $id})
                    SET 
                        m.title = $title, 
                        m.year = $year, 
                        m.type = $type,
                        m.synopsis = $synopsis
                    RETURN m
                    """,
                    id=movie_id, title=data.title, year=data.year, type=data.type, synopsis=data.synopsis
                )
                record = result.single()
                if not record:
                    tx.rollback()
                    return None
                movie = dict(record["m"].items())

                tx.run("MATCH (m:Movie {id: $movie_id})-[r:HAS_GENRE]->() DELETE r", movie_id=movie_id)
                tx.run("MATCH ()-[r:ACTED_IN]->(m:Movie {id: $movie_id}) DELETE r", movie_id=movie_id)
                
                for genre in data.genre_ids:
                    tx.run(
                        "MATCH (m:Movie {id: $movie_id}), (g:Genre {id: $genre_id}) "
                        "MERGE (m)-[:HAS_GENRE]->(g)",
                        movie_id=movie_id, genre_id=genre
                    )
                for actor in data.actor_ids:
                    tx.run(
                        "MATCH (a:Actor {id: $actor_id}), (m:Movie {id: $movie_id}) "
                        "MERGE (a)-[:ACTED_IN]->(m)",
                        movie_id=movie_id, actor_id=actor
                    )

                tx.commit()
                return movie
            except Exception as e:
                tx.rollback()
                raise e
            
class UserRepo:
    """Repositorio para manejar operaciones relacionadas con usuarios en Neo4j."""
    @staticmethod
    def get_all() -> list[dict]:
        """Obtiene todos los usuarios almacenados en Neo4j."""
        with neo4j_session() as session:
            result = session.run("MATCH (u:User) RETURN u ORDER BY u.name")
            return [dict(r["u"].items()) for r in result]
        
    @staticmethod
    def get_by_id(user_id: int) -> dict | None:
        """Obtiene un usuario por su ID junto con sus géneros favoritos y películas calificadas."""
        with neo4j_session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $id})
                OPTIONAL MATCH (u)-[:LIKES]->(g:Genre)
                OPTIONAL MATCH (u)-[:FRIEND]->(f:User)
                RETURN
                    u,
                    collect(DISTINCT g.name)  AS favorite_genres,
                    collect(DISTINCT f.name)  AS friends
                """,
                id=user_id
            )
            record = result.single()
            if not record:
                return None
            user = dict(record["u"].items())
            user["favorite_genres"] = [g for g in record["favorite_genres"] if g]
            user["friends"] = [f for f in record["friends"] if f]
            return user
    
    @staticmethod
    def create(user_id: int, data: UserCreate) -> dict:
        """Crea un nuevo usuario en Neo4j."""
        with neo4j_session() as session:
            tx = session.begin_transaction()
            try:
                result = tx.run(
                    """
                    MERGE (u:User {id: $id})
                    ON CREATE SET u.name = $name, u.email = $email
                    RETURN u
                    """,
                    id=user_id, name=data.name, email=data.email
                )
                user = dict(result.single()["u"].items())
 
                for gid in data.favorite_genre_ids:
                    tx.run(
                        "MATCH (u:User {id:$uid}),(g:Genre {id:$gid}) MERGE (u)-[:LIKES]->(g)",
                        uid=user_id, gid=gid
                    )
                tx.commit()
                return user
            except Exception:
                tx.rollback()
                raise
        
    @staticmethod
    def delete(user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        with neo4j_session() as session:
            result = session.run(
                "MATCH (u:User {id: $id}) DETACH DELETE u",
                id=user_id
            )
            return result.consume().counters.nodes_deleted > 0
        
    @staticmethod
    def update(user_id: int, data: UserCreate) -> dict | None:
        """Actualiza un usuario existente."""
        with neo4j_session() as session:
            tx = session.begin_transaction()
            try:
                result = tx.run(
                    "MATCH (u:User {id:$id}) SET u.name=$name, u.email=$email RETURN u",
                    id=user_id, name=data.name, email=data.email
                )
                record = result.single()
                if not record:
                    tx.rollback()
                    return None
                user = dict(record["u"].items())
 
                tx.run("MATCH (u:User {id:$id})-[r:LIKES]->() DELETE r", id=user_id)
                for gid in data.favorite_genre_ids:
                    tx.run(
                        "MATCH (u:User {id:$uid}),(g:Genre {id:$gid}) MERGE (u)-[:LIKES]->(g)",
                        uid=user_id, gid=gid
                    )
                tx.commit()
                return user
            except Exception:
                tx.rollback()
                raise
        
        