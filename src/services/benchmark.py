"""
Las 3 consultas del ejercicio ejecutadas en paralelo contra
PostgreSQL y Neo4J, con medición de tiempos.
 
Estrategia:
  1. Ejecutar la misma consulta en ambas DBs
  2. Medir el tiempo de cada una con time.perf_counter()
  3. Empaquetar resultados + tiempos en el formato de respuesta acordado
"""
import time
from db.postgres import pg_cursor
from db.neo4j import neo4j_session, neo4j_record_to_dict
from models import BenchmarkTimes, Q1Response, Q2Response, Q3Response
 
 
def _make_benchmark(neo4j_ms: float, postgres_ms: float) -> BenchmarkTimes:
    """Construye el objeto de tiempos determinando el ganador."""
    if neo4j_ms < postgres_ms * 0.95:   # Neo4J gana por más de 5%
        winner = "neo4j"
    elif postgres_ms < neo4j_ms * 0.95: # PostgreSQL gana por más de 5%
        winner = "postgres"
    else:
        winner = "tie"
 
    return BenchmarkTimes(
        neo4j_ms=round(neo4j_ms, 2),
        postgres_ms=round(postgres_ms, 2),
        winner=winner,
    )
 
def query_friends_movies(user_id: int, min_rating: float = 4.0, limit: int = 20) -> Q1Response:
    """
    Consulta 1: Películas que mis amigos calificaron >4★ que yo no he visto
    """
 
    # ── PostgreSQL ───────────────────────────────────────────
    t0 = time.perf_counter()
    with pg_cursor() as cur:
        cur.execute("""
            SELECT
                m.id            AS movie_id,
                m.title,
                m.year,
                m.type,
                AVG(r.rating)   AS avg_friend_rating,
                JSON_AGG(
                    JSON_BUILD_OBJECT('name', u.name, 'rating', r.rating)
                    ORDER BY r.rating DESC
                )               AS friends_who_watched
            FROM friendships f
            -- Obtener el id del amigo sin importar en qué columna está
            JOIN ratings r ON r.user_id = CASE
                                WHEN f.user1_id = %(uid)s THEN f.user2_id
                                ELSE f.user1_id
                             END
            JOIN movies m  ON m.id  = r.movie_id
            JOIN users u   ON u.id  = r.user_id
            WHERE
                (f.user1_id = %(uid)s OR f.user2_id = %(uid)s)
                AND r.rating > %(min_r)s
                -- Subquery: excluir películas que yo ya califiqué
                AND m.id NOT IN (
                    SELECT movie_id FROM ratings WHERE user_id = %(uid)s
                )
            GROUP BY m.id, m.title, m.year, m.type
            ORDER BY avg_friend_rating DESC
            LIMIT %(lim)s
        """, {"uid": user_id, "min_r": min_rating, "lim": limit})
        pg_rows = cur.fetchall()
    postgres_ms = (time.perf_counter() - t0) * 1000
 
    # ── Neo4J ────────────────────────────────────────────────
    t0 = time.perf_counter()
    with neo4j_session() as session:
        result = session.run("""
            MATCH (me:User {id: $uid})-[:FRIEND]->(friend)-[r:RATED]->(m:Movie)
            WHERE r.stars > $min_r
              AND NOT (me)-[:RATED]->(m)
            RETURN
                m.id          AS movie_id,
                m.title       AS title,
                m.year        AS year,
                m.type        AS type,
                avg(r.stars)  AS avg_friend_rating,
                collect({name: friend.name, rating: r.stars}) AS friends_who_watched
            ORDER BY avg_friend_rating DESC
            LIMIT $lim
        """, uid=user_id, min_r=min_rating, lim=limit)
        neo4j_rows = [neo4j_record_to_dict(r) for r in result]
    neo4j_ms = (time.perf_counter() - t0) * 1000
 
    # Usamos resultados de Neo4J como fuente de verdad para la respuesta
    results = [
        {
            "movie_id":           row["movie_id"],
            "title":              row["title"],
            "year":               row["year"],
            "type":               row["type"],
            "avg_friend_rating":  round(float(row["avg_friend_rating"]), 2),
            "friends_who_watched": row["friends_who_watched"],
        }
        for row in neo4j_rows
    ]
 
    return Q1Response(
        user_id=user_id,
        results=results,
        benchmark=_make_benchmark(neo4j_ms, postgres_ms),
    )
 
def query_actor_network(actor_id: int) -> Q2Response:
    """
    Consulta 2: Actores a 2 grados de separación de un Actor X
    """
 
    # ── PostgreSQL ───────────────────────────────────────────
    t0 = time.perf_counter()
    with pg_cursor() as cur:
        # Obtener nombre del actor X
        cur.execute("SELECT id, name FROM actors WHERE id = %s", (actor_id,))
        actor_x_pg = cur.fetchone()
 
        if actor_x_pg:
            cur.execute("""
                WITH coactors AS (
                    -- Paso 1: actores que compartieron película con actor X
                    SELECT DISTINCT ma2.actor_id AS coactor_id
                    FROM movie_actors ma1
                    JOIN movie_actors ma2 ON ma1.movie_id = ma2.movie_id
                    WHERE ma1.actor_id = %(aid)s
                      AND ma2.actor_id <> %(aid)s
                ),
                second_degree AS (
                    -- Paso 2: actores que compartieron con los co-actores
                    SELECT DISTINCT
                        ma_result.actor_id,
                        -- El "puente": co-actor y película compartida
                        c.coactor_id,
                        ma_bridge.movie_id AS bridge_movie_id
                    FROM coactors c
                    JOIN movie_actors ma_bridge ON ma_bridge.actor_id = c.coactor_id
                    JOIN movie_actors ma_result ON ma_result.movie_id  = ma_bridge.movie_id
                    WHERE ma_result.actor_id <> %(aid)s
                      AND ma_result.actor_id NOT IN (SELECT coactor_id FROM coactors)
                )
                SELECT DISTINCT
                    a.id   AS actor_id,
                    a.name AS name,
                    2      AS degree,
                    -- Construir el camino de conexión como JSONB para que DISTINCT funcione
                    JSON_BUILD_ARRAY(
                        JSON_BUILD_OBJECT(
                            'actor', bridge_actor.name,
                            'movie', bridge_movie.title
                        )
                    )::jsonb AS connection_path
                FROM second_degree sd
                JOIN actors a            ON a.id  = sd.actor_id
                JOIN actors bridge_actor ON bridge_actor.id = sd.coactor_id
                JOIN movies bridge_movie ON bridge_movie.id = sd.bridge_movie_id
                ORDER BY a.name
            """, {"aid": actor_id})
            pg_rows = cur.fetchall()
        else:
            pg_rows = []
    postgres_ms = (time.perf_counter() - t0) * 1000
 
    # ── Neo4J ────────────────────────────────────────────────
    t0 = time.perf_counter()
    with neo4j_session() as session:
        actor_result = session.run(
            "MATCH (a:Actor {id: $id}) RETURN a", id=actor_id
        ).single()
        actor_x_neo = dict(actor_result["a"].items()) if actor_result else None
 
        if actor_x_neo:
            result = session.run("""
                MATCH (ax:Actor {id: $aid})-[:ACTED_IN]->(m1:Movie)<-[:ACTED_IN]-(co)
                      -[:ACTED_IN]->(m2:Movie)<-[:ACTED_IN]-(result)
                WHERE result.id <> ax.id
                  AND co.id     <> ax.id
                  AND result.id <> co.id
                RETURN DISTINCT
                    result.id   AS actor_id,
                    result.name AS name,
                    2           AS degree,
                    collect(DISTINCT {actor: co.name, movie: m2.title})[0..1]
                                AS connection_path
                ORDER BY result.name
            """, aid=actor_id)
            neo4j_rows = [neo4j_record_to_dict(r) for r in result]
        else:
            neo4j_rows = []
    neo4j_ms = (time.perf_counter() - t0) * 1000
 
    actor_x_info = actor_x_neo or (dict(actor_x_pg) if actor_x_pg else {"id": actor_id, "name": "?"})
 
    results = [
        {
            "actor_id":        row["actor_id"],
            "name":            row["name"],
            "degree":          row["degree"],
            "connection_path": row.get("connection_path", []),
        }
        for row in neo4j_rows
    ]
 
    return Q2Response(
        actor_x=actor_x_info,
        results=results,
        total_found=len(results),
        benchmark=_make_benchmark(neo4j_ms, postgres_ms),
    )
 
 
# ══════════════════════════════════════════════════════════════
#  CONSULTA 3
#  Géneros nuevos: usuarios con rating similar en Inception
#  que ven géneros que yo no tengo en mis favoritos
# ══════════════════════════════════════════════════════════════
 
def query_genre_suggestions(user_id: int, movie_id: int = 1, rating_tolerance: float = 0.5) -> Q3Response:
    """
    Consulta 3: Géneros nuevos: usuarios con rating similar en Inception
    que ven géneros que yo no tengo en mis favoritos
    """
 
    # ── PostgreSQL ───────────────────────────────────────────
    t0 = time.perf_counter()
    with pg_cursor() as cur:
        # Info de la película de referencia
        cur.execute(
            "SELECT id, title FROM movies WHERE id = %s", (movie_id,)
        )
        ref_movie = cur.fetchone()
 
        cur.execute("""
            WITH my_rating AS (
                -- Mi calificación de la película de referencia
                SELECT rating FROM ratings
                WHERE user_id = %(uid)s AND movie_id = %(mid)s
            ),
            similar_users AS (
                -- Usuarios que calificaron similar (dentro de la tolerancia)
                SELECT r.user_id
                FROM ratings r, my_rating mr
                WHERE r.movie_id   = %(mid)s
                  AND r.user_id   <> %(uid)s
                  AND ABS(r.rating - mr.rating) <= %(tol)s
            ),
            my_genres AS (
                -- Mis géneros favoritos actuales
                SELECT genre_id FROM user_favorite_genres WHERE user_id = %(uid)s
            ),
            genre_counts AS (
                -- Géneros que los usuarios similares tienen como favoritos
                -- y que yo NO tengo
                SELECT
                    g.id,
                    g.name,
                    COUNT(DISTINCT su.user_id) AS cnt
                FROM similar_users su
                JOIN user_favorite_genres ufg ON ufg.user_id = su.user_id
                JOIN genres g                 ON g.id = ufg.genre_id
                WHERE ufg.genre_id NOT IN (SELECT genre_id FROM my_genres)
                GROUP BY g.id, g.name
            )
            SELECT
                gc.name,
                gc.cnt AS similar_users_count,
                -- Películas de ejemplo de ese género bien calificadas
                (
                    SELECT JSON_AGG(sub.info)
                    FROM (
                        SELECT JSON_BUILD_OBJECT(
                            'title',      m.title,
                            'avg_rating', ROUND(AVG(r2.rating)::numeric, 1)
                        ) AS info
                        FROM movies m
                        JOIN movie_genres mg ON mg.movie_id = m.id AND mg.genre_id = gc.id
                        JOIN ratings r2      ON r2.movie_id = m.id
                        GROUP BY m.id, m.title
                        ORDER BY AVG(r2.rating) DESC
                        LIMIT 3
                    ) sub
                ) AS sample_movies
            FROM genre_counts gc
            ORDER BY gc.cnt DESC
        """, {"uid": user_id, "mid": movie_id, "tol": rating_tolerance})
        pg_rows = cur.fetchall()
 
        # Mi calificación de la película
        cur.execute(
            "SELECT rating FROM ratings WHERE user_id=%s AND movie_id=%s",
            (user_id, movie_id)
        )
        my_rating_row = cur.fetchone()
        my_rating_val = float(my_rating_row["rating"]) if my_rating_row else None
 
        # Mis géneros favoritos
        cur.execute("""
            SELECT g.name FROM user_favorite_genres ufg
            JOIN genres g ON g.id = ufg.genre_id
            WHERE ufg.user_id = %s
        """, (user_id,))
        my_genres = [r["name"] for r in cur.fetchall()]
 
    postgres_ms = (time.perf_counter() - t0) * 1000
 
    # ── Neo4J ────────────────────────────────────────────────
    t0 = time.perf_counter()
    with neo4j_session() as session:
        result = session.run("""
            MATCH (me:User {id: $uid})-[myR:RATED]->(ref:Movie {id: $mid})
            MATCH (other:User)-[otherR:RATED]->(ref)
            WHERE other.id <> me.id
              AND abs(myR.stars - otherR.stars) <= $tol
 
            MATCH (other)-[:LIKES]->(g:Genre)
            WHERE NOT (me)-[:LIKES]->(g)
 
            WITH g, count(DISTINCT other) AS cnt
            ORDER BY cnt DESC
 
            // Películas de ejemplo del género
            OPTIONAL MATCH (sample:Movie)-[:HAS_GENRE]->(g)
            OPTIONAL MATCH (:User)-[sr:RATED]->(sample)
            WITH g, cnt, sample, avg(sr.stars) AS avg_stars
            ORDER BY avg_stars DESC
 
            RETURN
                g.name AS genre,
                cnt    AS similar_users_count,
                collect({title: sample.title, avg_rating: round(avg_stars * 10) / 10})[0..3]
                       AS sample_movies
        """, uid=user_id, mid=movie_id, tol=rating_tolerance)
        neo4j_rows = [neo4j_record_to_dict(r) for r in result]
    neo4j_ms = (time.perf_counter() - t0) * 1000
 
    # Calcular score normalizado (el género más popular = 1.0)
    max_cnt = max((r["similar_users_count"] for r in neo4j_rows), default=1)
    suggested = [
        {
            "genre":               row["genre"],
            "score":               round(row["similar_users_count"] / max_cnt, 2),
            "similar_users_count": row["similar_users_count"],
            "sample_movies":       [m for m in row.get("sample_movies", []) if m.get("title")],
        }
        for row in neo4j_rows
    ]
 
    return Q3Response(
        reference_movie={
            "id":        movie_id,
            "title":     ref_movie["title"] if ref_movie else "?",
            "my_rating": my_rating_val,
        },
        my_genres=my_genres,
        suggested_genres=suggested,
        benchmark=_make_benchmark(neo4j_ms, postgres_ms),
    )