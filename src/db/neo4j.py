"""
Módulo para manejar la conexión a Neo4j y proporcionar utilidades relacionadas.
"""
import os
from neo4j import GraphDatabase, Driver, Session
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

_driver = Driver | None = None

def init_driver():
    """
    Inicializa el driver de Neo4j usando las variables de entorno.
    Debe llamarse antes de usar cualquier función que requiera una sesión.
    """
    global _driver
    if _driver is None:
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")
        _driver = GraphDatabase.driver(uri, auth=(user, password))

        _driver.verify_connectivity()
        print("Conexión a Neo4j establecida correctamente.")

def close_driver():
    """
    Cierra la conexión al servidor de Neo4j.
    """
    global _driver
    if _driver is not None:
        _driver.close()
        print("Conexión a Neo4j cerrada.")

def get_session() -> Session:
    """
    Obtiene una sesión de Neo4j para ejecutar consultas.
    """
    if _driver is None:
        raise Exception("El driver de Neo4j no ha sido inicializado. Llama a init_driver() primero.")
    return _driver.session()

@contextmanager
def neo4j_session():
    """
    Context manager para manejar sesiones de Neo4j.
    Asegura que la sesión se cierre correctamente después de su uso.
    Uso:
        with neo4j_session() as session:
            # ejecutar consultas con session.run(...)
    """
    session = get_session()
    try:
        yield session
    finally:
        session.close()

def neo4j_record_to_dict(record) -> dict:
    """
    Convierte un registro de Neo4j a un diccionario plano.
    Esto es útil para transformar los resultados de las consultas en un formato más manejable.
    """
    result = {}
    for key in record.keys():
        value = record[key]
        if hasattr(value, "items"):
            result[key] = dict(value.items())
        elif isinstance(value, list):
            result[key] = [
                dict(item.items()) if hasattr(item, "items") 
                else item for item in value]
        else:
            result[key] = value
    return result