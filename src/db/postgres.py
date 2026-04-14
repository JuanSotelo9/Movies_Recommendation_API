"""
Conexión y pool de conexiones para PostgreSQL usando psycopg2.
"""

import os
import psycopg2
from psycopg2 import pool, extras
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()

_pool: pool.ThreadedConnectionPool | None = None

def init_pool(min_conn: int = 2, max_conn: int = 10) -> None:
    """
    Crea el pool de conexiones PostgreSQL.
    Debe llamarse UNA SOLA VEZ al arrancar la aplicación.

    ThreadedConnectionPool es thread-safe: varios hilos pueden
    pedir y devolver conexiones simultáneamente sin condiciones de carrera.
    """
    global _pool

    _pool = pool.ThreadedConnectionPool(
        minconn=min_conn,
        maxconn=max_conn,
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "movies_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "password"),
    )
    print(f"PostgreSQL pool creado ({min_conn}-{max_conn} conexiones)")

def get_connection() -> psycopg2.extensions.connection:
    """
    Obtiene una conexión del pool.
    Si todas las conexiones están ocupadas y ya se alcanzó max_conn,
    este método BLOQUEA hasta que se libere una.
    """
    if _pool is None:
        raise RuntimeError("Pool no inicializado. Llama a init_pool() primero.")
    return _pool.getconn()

def release_connection(conn: psycopg2.extensions.connection) -> None:
    """
    Devuelve una conexión al pool para que otros la reutilicen.
    SIEMPRE debe llamarse en un bloque finally para garantizar la devolución.
    """
    if _pool:
        _pool.putconn(conn)


def close_pool() -> None:
    """
    Cierra todas las conexiones del pool.
    Debe llamarse al apagar la aplicación (evento shutdown).
    """
    if _pool:
        _pool.closeall()
        print("PostgreSQL pool cerrado")

@contextmanager
def pg_cursor():
    """
    Context manager que gestiona automáticamente:
      - obtener/devolver conexión del pool
      - commit si todo fue bien
      - rollback si hubo excepción
      - cierre del cursor
    """
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        release_connection(conn)