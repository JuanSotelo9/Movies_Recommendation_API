"""
Capa de acceso a datos para PostgreSQL.
"""

from db.postgres import pg_cursor
from models import (
    GenreCreate, ActorCreate, MovieCreate,
    UserCreate, RatingCreate, FriendshipCreate,
)

class GenreRepo:

    @staticmethod
    def get_all() -> list[dict]:
        """
        Obtiene todos los géneros ordenados por nombre.
        """
        with pg_cursor() as cur:
            cur.execute("SELECT id, name FROM genres ORDER BY name")
            return cur.fetchall()  # → [{"id": 1, "name": "Action"}, ...]

    @staticmethod
    def get_by_id(genre_id: int) -> dict | None:
        """
        Busca un género por su ID.
        """
        with pg_cursor() as cur:
            cur.execute(
                "SELECT id, name FROM genres WHERE id = %s",
                (genre_id,)   # ← siempre una tupla, incluso con un solo parámetro
            )
            return cur.fetchone()

    @staticmethod
    def create(data: GenreCreate) -> dict:
        """
        Inserta un nuevo género y retorna el registro creado.
        """
        with pg_cursor() as cur:
            cur.execute(
                "INSERT INTO genres (name) VALUES (%s) RETURNING id, name",
                (data.name,)
            )
            return cur.fetchone()  # → {"id": 13, "name": "Musical"}

    @staticmethod
    def update(genre_id: int, data: GenreCreate) -> dict | None:
        """
        Actualiza el nombre de un género.
        """
        with pg_cursor() as cur:
            cur.execute(
                "UPDATE genres SET name = %s WHERE id = %s RETURNING id, name",
                (data.name, genre_id)
            )
            return cur.fetchone()

    @staticmethod
    def delete(genre_id: int) -> bool:
        """
        Elimina un género. Retorna True si existía, False si no.
        """
        with pg_cursor() as cur:
            cur.execute("DELETE FROM genres WHERE id = %s", (genre_id,))
            return cur.rowcount > 0


class ActorRepo:

    @staticmethod
    def get_all() -> list[dict]:
        with pg_cursor() as cur:
            cur.execute("SELECT id, name, birth_year FROM actors ORDER BY name")
            return cur.fetchall()

    @staticmethod
    def get_by_id(actor_id: int) -> dict | None:
        """
        Obtiene un actor con las películas en las que participó.
        """
        with pg_cursor() as cur:
            cur.execute("""
                SELECT
                    a.id,
                    a.name,
                    a.birth_year,
                    array_agg(m.title ORDER BY m.year)
                        FILTER (WHERE m.id IS NOT NULL) AS movies
                FROM actors a
                LEFT JOIN movie_actors ma ON ma.actor_id = a.id
                LEFT JOIN movies m        ON m.id = ma.movie_id
                WHERE a.id = %s
                GROUP BY a.id
            """, (actor_id,))
            return cur.fetchone()

    @staticmethod
    def create(data: ActorCreate) -> dict:
        with pg_cursor() as cur:
            cur.execute(
                """
                INSERT INTO actors (name, birth_year)
                VALUES (%s, %s)
                RETURNING id, name, birth_year
                """,
                (data.name, data.birth_year)
            )
            return cur.fetchone()

    @staticmethod
    def update(actor_id: int, data: ActorCreate) -> dict | None:
        with pg_cursor() as cur:
            cur.execute(
                """
                UPDATE actors
                SET name = %s, birth_year = %s
                WHERE id = %s
                RETURNING id, name, birth_year
                """,
                (data.name, data.birth_year, actor_id)
            )
            return cur.fetchone()

    @staticmethod
    def delete(actor_id: int) -> bool:
        with pg_cursor() as cur:
            cur.execute("DELETE FROM actors WHERE id = %s", (actor_id,))
            return cur.rowcount > 0


class MovieRepo:

    @staticmethod
    def get_all(type_filter: str | None = None) -> list[dict]:
        """
        Lista películas con filtro opcional por tipo (movie/series).
        """
        with pg_cursor() as cur:
            if type_filter:
                cur.execute(
                    "SELECT id, title, year, type, synopsis FROM movies WHERE type = %s ORDER BY year DESC",
                    (type_filter,)
                )
            else:
                cur.execute(
                    "SELECT id, title, year, type, synopsis FROM movies ORDER BY year DESC"
                )
            return cur.fetchall()

    @staticmethod
    def get_by_id(movie_id: int) -> dict | None:
        """
        Obtiene una película con sus géneros y actores.
        """
        with pg_cursor() as cur:
            cur.execute("""
                SELECT
                    m.id,
                    m.title,
                    m.year,
                    m.type,
                    m.synopsis,
                    -- Array de géneros: [{"id": 1, "name": "Sci-Fi"}, ...]
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object('id', g.id, 'name', g.name))
                        FILTER (WHERE g.id IS NOT NULL),
                        '[]'
                    ) AS genres,
                    -- Array de actores: [{"id": 1, "name": "DiCaprio"}, ...]
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object('id', a.id, 'name', a.name))
                        FILTER (WHERE a.id IS NOT NULL),
                        '[]'
                    ) AS actors
                FROM movies m
                LEFT JOIN movie_genres mg ON mg.movie_id = m.id
                LEFT JOIN genres g        ON g.id = mg.genre_id
                LEFT JOIN movie_actors ma ON ma.movie_id = m.id
                LEFT JOIN actors a        ON a.id = ma.actor_id
                WHERE m.id = %s
                GROUP BY m.id
            """, (movie_id,))
            return cur.fetchone()

    @staticmethod
    def create(data: MovieCreate) -> dict:
        """
        Crea una película con sus géneros y actores en una transacción.
        """
        with pg_cursor() as cur:
            # 1. Insertar la película principal
            cur.execute(
                """
                INSERT INTO movies (title, year, type, synopsis)
                VALUES (%s, %s, %s, %s)
                RETURNING id, title, year, type, synopsis
                """,
                (data.title, data.year, data.type, data.synopsis)
            )
            movie = cur.fetchone()
            movie_id = movie["id"]

            # 2. Insertar relaciones con géneros (si se especificaron)
            if data.genre_ids:
                # executemany envía todos los inserts en una sola operación
                cur.executemany(
                    "INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)",
                    [(movie_id, gid) for gid in data.genre_ids]
                )

            # 3. Insertar relaciones con actores (si se especificaron)
            if data.actor_ids:
                cur.executemany(
                    "INSERT INTO movie_actors (movie_id, actor_id) VALUES (%s, %s)",
                    [(movie_id, aid) for aid in data.actor_ids]
                )

            return movie

    @staticmethod
    def update(movie_id: int, data: MovieCreate) -> dict | None:
        """
        Actualiza película y reemplaza sus géneros/actores.
        """
        with pg_cursor() as cur:
            # 1. Actualizar datos básicos
            cur.execute(
                """
                UPDATE movies
                SET title = %s, year = %s, type = %s, synopsis = %s
                WHERE id = %s
                RETURNING id, title, year, type, synopsis
                """,
                (data.title, data.year, data.type, data.synopsis, movie_id)
            )
            movie = cur.fetchone()
            if not movie:
                return None

            # 2. Borrar relaciones anteriores y reinsertar
            cur.execute("DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
            cur.execute("DELETE FROM movie_actors WHERE movie_id = %s", (movie_id,))

            if data.genre_ids:
                cur.executemany(
                    "INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)",
                    [(movie_id, gid) for gid in data.genre_ids]
                )
            if data.actor_ids:
                cur.executemany(
                    "INSERT INTO movie_actors (movie_id, actor_id) VALUES (%s, %s)",
                    [(movie_id, aid) for aid in data.actor_ids]
                )

            return movie

    @staticmethod
    def delete(movie_id: int) -> bool:
        """
        Elimina una película.
        """
        with pg_cursor() as cur:
            cur.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
            return cur.rowcount > 0

class UserRepo:

    @staticmethod
    def get_all() -> list[dict]:
        with pg_cursor() as cur:
            cur.execute("SELECT id, name, email FROM users ORDER BY name")
            return cur.fetchall()

    @staticmethod
    def get_by_id(user_id: int) -> dict | None:
        """Obtiene un usuario con sus géneros favoritos y calificaciones."""
        with pg_cursor() as cur:
            cur.execute("""
                SELECT
                    u.id,
                    u.name,
                    u.email,
                    COALESCE(
                        json_agg(DISTINCT g.name) FILTER (WHERE g.id IS NOT NULL),
                        '[]'
                    ) AS favorite_genres,
                    COUNT(DISTINCT r.movie_id) AS movies_rated
                FROM users u
                LEFT JOIN user_favorite_genres ufg ON ufg.user_id = u.id
                LEFT JOIN genres g                 ON g.id = ufg.genre_id
                LEFT JOIN ratings r                ON r.user_id = u.id
                WHERE u.id = %s
                GROUP BY u.id
            """, (user_id,))
            return cur.fetchone()

    @staticmethod
    def create(data: UserCreate) -> dict:
        with pg_cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email",
                (data.name, data.email)
            )
            user = cur.fetchone()

            if data.favorite_genre_ids:
                cur.executemany(
                    "INSERT INTO user_favorite_genres (user_id, genre_id) VALUES (%s, %s)",
                    [(user["id"], gid) for gid in data.favorite_genre_ids]
                )
            return user

    @staticmethod
    def update(user_id: int, data: UserCreate) -> dict | None:
        with pg_cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id, name, email",
                (data.name, data.email, user_id)
            )
            user = cur.fetchone()
            if not user:
                return None

            cur.execute("DELETE FROM user_favorite_genres WHERE user_id = %s", (user_id,))
            if data.favorite_genre_ids:
                cur.executemany(
                    "INSERT INTO user_favorite_genres (user_id, genre_id) VALUES (%s, %s)",
                    [(user_id, gid) for gid in data.favorite_genre_ids]
                )
            return user

    @staticmethod
    def delete(user_id: int) -> bool:
        with pg_cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            return cur.rowcount > 0

class RatingRepo:

    @staticmethod
    def get_by_user(user_id: int) -> list[dict]:
        """Lista todas las calificaciones de un usuario con info de la película."""
        with pg_cursor() as cur:
            cur.execute("""
                SELECT
                    r.user_id,
                    r.movie_id,
                    r.rating,
                    r.watched,
                    m.title,
                    m.year,
                    m.type
                FROM ratings r
                JOIN movies m ON m.id = r.movie_id
                WHERE r.user_id = %s
                ORDER BY r.rating DESC
            """, (user_id,))
            return cur.fetchall()

    @staticmethod
    def upsert(data: RatingCreate) -> dict:
        """
        Inserta o actualiza una calificación (UPSERT).
        """
        with pg_cursor() as cur:
            cur.execute(
                """
                INSERT INTO ratings (user_id, movie_id, rating, watched)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, movie_id) DO UPDATE
                    SET rating  = EXCLUDED.rating,
                        watched = EXCLUDED.watched
                RETURNING user_id, movie_id, rating, watched
                """,
                (data.user_id, data.movie_id, data.rating, data.watched)
            )
            return cur.fetchone()

    @staticmethod
    def delete(user_id: int, movie_id: int) -> bool:
        with pg_cursor() as cur:
            cur.execute(
                "DELETE FROM ratings WHERE user_id = %s AND movie_id = %s",
                (user_id, movie_id)
            )
            return cur.rowcount > 0

class FriendshipRepo:

    @staticmethod
    def get_friends(user_id: int) -> list[dict]:
        """
        Obtiene los amigos de un usuario.
        """
        with pg_cursor() as cur:
            cur.execute("""
                SELECT
                    CASE
                        WHEN f.user1_id = %s THEN f.user2_id
                        ELSE f.user1_id
                    END AS friend_id,
                    u.name AS friend_name,
                    u.email AS friend_email
                FROM friendships f
                JOIN users u ON u.id = CASE
                    WHEN f.user1_id = %s THEN f.user2_id
                    ELSE f.user1_id
                END
                WHERE f.user1_id = %s OR f.user2_id = %s
                ORDER BY u.name
            """, (user_id, user_id, user_id, user_id))
            return cur.fetchall()

    @staticmethod
    def create(data: FriendshipCreate) -> dict:
        """
        Crea una amistad asegurando user1_id < user2_id (invariante del schema).
        """
        u1 = min(data.user1_id, data.user2_id)
        u2 = max(data.user1_id, data.user2_id)

        with pg_cursor() as cur:
            cur.execute(
                """
                INSERT INTO friendships (user1_id, user2_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING user1_id, user2_id
                """,
                (u1, u2)
            )
            return cur.fetchone() or {"user1_id": u1, "user2_id": u2, "note": "ya existía"}

    @staticmethod
    def delete(user1_id: int, user2_id: int) -> bool:
        u1 = min(user1_id, user2_id)
        u2 = max(user1_id, user2_id)
        with pg_cursor() as cur:
            cur.execute(
                "DELETE FROM friendships WHERE user1_id = %s AND user2_id = %s",
                (u1, u2)
            )
            return cur.rowcount > 0
