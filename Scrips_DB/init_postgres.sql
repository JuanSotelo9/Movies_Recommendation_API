-- =============================================================
--  INIT_POSTGRES.SQL
--  Script de inicialización para el ejercicio Neo4J vs PostgreSQL
--  Ejecutar con: psql -U postgres -f init_postgres.sql
-- =============================================================

-- Crear base de datos (ejecutar como superusuario si es necesario)
-- CREATE DATABASE movies_db;
-- \c movies_db;

-- Limpiar tablas si ya existen (orden inverso por FK)
DROP TABLE IF EXISTS user_favorite_genres CASCADE;
DROP TABLE IF EXISTS movie_genres CASCADE;
DROP TABLE IF EXISTS movie_actors CASCADE;
DROP TABLE IF EXISTS ratings CASCADE;
DROP TABLE IF EXISTS friendships CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS actors CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =============================================================
--  TABLAS
-- =============================================================

CREATE TABLE genres (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE actors (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    birth_year INTEGER
);

CREATE TABLE movies (
    id       SERIAL PRIMARY KEY,
    title    VARCHAR(300) NOT NULL,
    year     INTEGER,
    type     VARCHAR(20) CHECK (type IN ('movie', 'series')),
    synopsis TEXT
);

CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE friendships (
    user1_id INTEGER NOT NULL REFERENCES users(id),
    user2_id INTEGER NOT NULL REFERENCES users(id),
    PRIMARY KEY (user1_id, user2_id),
    CHECK (user1_id < user2_id)
);

CREATE TABLE ratings (
    user_id  INTEGER NOT NULL REFERENCES users(id),
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    rating   NUMERIC(3,1) CHECK (rating >= 0 AND rating <= 5),
    watched  BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE movie_genres (
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    genre_id INTEGER NOT NULL REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE movie_actors (
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    actor_id INTEGER NOT NULL REFERENCES actors(id),
    PRIMARY KEY (movie_id, actor_id)
);

CREATE TABLE user_favorite_genres (
    user_id  INTEGER NOT NULL REFERENCES users(id),
    genre_id INTEGER NOT NULL REFERENCES genres(id),
    PRIMARY KEY (user_id, genre_id)
);

-- =============================================================
--  GÉNEROS
-- =============================================================

INSERT INTO genres (id, name) VALUES
(1,  'Sci-Fi'),
(2,  'Drama'),
(3,  'Thriller'),
(4,  'Action'),
(5,  'Comedy'),
(6,  'Horror'),
(7,  'Romance'),
(8,  'Animation'),
(9,  'Documentary'),
(10, 'Fantasy'),
(11, 'Crime'),
(12, 'Adventure');

SELECT setval('genres_id_seq', (SELECT MAX(id) FROM genres));

-- =============================================================
--  ACTORES
-- =============================================================

INSERT INTO actors (id, name, birth_year) VALUES
(1,  'Leonardo DiCaprio',    1974),
(2,  'Tom Hanks',            1956),
(3,  'Scarlett Johansson',   1984),
(4,  'Cillian Murphy',       1976),
(5,  'Anne Hathaway',        1982),
(6,  'Matt Damon',           1970),
(7,  'Natalie Portman',      1981),
(8,  'Christian Bale',       1974),
(9,  'Meryl Streep',         1949),
(10, 'Brad Pitt',            1963),
(11, 'Marion Cotillard',     1975),
(12, 'Tom Hardy',            1977),
(13, 'Emily Blunt',          1983),
(14, 'Joseph Gordon-Levitt', 1981),
(15, 'Ellen Page',           1987),
(16, 'Ken Watanabe',         1959),
(17, 'Robin Wright',         1966),
(18, 'Gary Sinise',          1955),
(19, 'Jessica Lange',        1949),
(20, 'Edward Norton',        1969),
(21, 'Helena Bonham Carter', 1966),
(22, 'Michael Caine',        1933),
(23, 'Jessica Chastain',     1977),
(24, 'Timothée Chalamet',    1995),
(25, 'Zendaya',              2003),
(26, 'Oscar Isaac',          1979),
(27, 'Florence Pugh',        1996),
(28, 'Robert Downey Jr.',    1965),
(29, 'Gwyneth Paltrow',      1972),
(30, 'Chris Evans',          1981);

SELECT setval('actors_id_seq', (SELECT MAX(id) FROM actors));

-- =============================================================
--  PELÍCULAS Y SERIES
-- =============================================================

INSERT INTO movies (id, title, year, type, synopsis) VALUES
(1,  'Inception',               2010, 'movie',  'Un ladrón que roba secretos corporativos a través del uso de tecnología de sueños compartidos.'),
(2,  'Interstellar',            2014, 'movie',  'Un equipo de exploradores viaja a través de un agujero de gusano en el espacio.'),
(3,  'The Dark Knight',         2008, 'movie',  'Batman enfrenta al Joker, un criminal que siembra el caos en Gotham.'),
(4,  'Forrest Gump',            1994, 'movie',  'La historia de un hombre con bajas capacidades intelectuales pero gran corazón.'),
(5,  'Fight Club',              1999, 'movie',  'Un oficinista insomne y un vendedor de jabón forman un club de lucha.'),
(6,  'The Revenant',            2015, 'movie',  'Un explorador busca sobrevivir en la naturaleza salvaje tras ser atacado por un oso.'),
(7,  'Oppenheimer',             2023, 'movie',  'La historia del físico que lideró el Proyecto Manhattan.'),
(8,  'Dune',                    2021, 'movie',  'Un joven noble debe liderar a su pueblo en el planeta más peligroso del universo.'),
(9,  'Black Widow',             2021, 'movie',  'Natasha Romanoff confronta su pasado como espía.'),
(10, 'Iron Man',                2008, 'movie',  'Un genio millonario construye una armadura de metal para escapar de terroristas.'),
(11, 'Avengers: Endgame',       2019, 'movie',  'Los Vengadores buscan revertir los efectos del chasquido de Thanos.'),
(12, 'Dune: Part Two',          2024, 'movie',  'Paul Atreides une fuerzas con los Fremen mientras busca venganza.'),
(13, 'The Wolf of Wall Street', 2013, 'movie',  'La historia del corredor de bolsa Jordan Belfort y su vida de excesos.'),
(14, 'A Beautiful Mind',        2001, 'movie',  'La vida del matemático John Nash y su lucha contra la esquizofrenia.'),
(15, 'Whiplash',                2014, 'movie',  'Un joven baterista busca la perfección bajo un instructor despiadado.'),
(16, 'Breaking Bad',            2008, 'series', 'Un profesor de química con cáncer se convierte en productor de metanfetamina.'),
(17, 'Game of Thrones',         2011, 'series', 'Casas nobles compiten por el control del Trono de Hierro en Westeros.'),
(18, 'Stranger Things',         2016, 'series', 'Un grupo de niños enfrenta fuerzas sobrenaturales en su pequeño pueblo.'),
(19, 'The Crown',               2016, 'series', 'La vida de la familia real británica desde los años 40 hasta los 2000.'),
(20, 'Dark',                    2017, 'series', 'Cuatro familias alemanas interconectadas a través del tiempo y del espacio.'),
(21, 'The Witcher',             2019, 'series', 'Las historias del brujo Geralt de Rivia en el Continente.'),
(22, 'Chernobyl',               2019, 'series', 'El relato del desastre nuclear de Chernobyl en 1986.'),
(23, 'The Last of Us',          2023, 'series', 'Un sobreviviente de un apocalipsis fúngico debe cruzar Estados Unidos con una niña.'),
(24, 'House of the Dragon',     2022, 'series', 'La historia de la Casa Targaryen 200 años antes de Game of Thrones.'),
(25, 'Wednesday',               2022, 'series', 'Las aventuras de la hija de la Familia Addams en la academia Nevermore.');

SELECT setval('movies_id_seq', (SELECT MAX(id) FROM movies));

-- =============================================================
--  USUARIOS
-- =============================================================

INSERT INTO users (id, name, email) VALUES
(1,  'Carlos Mendoza',   'carlos@example.com'),
(2,  'Ana García',       'ana@example.com'),
(3,  'Luis Torres',      'luis@example.com'),
(4,  'María López',      'maria@example.com'),
(5,  'Pedro Ramírez',    'pedro@example.com'),
(6,  'Sofía Herrera',    'sofia@example.com'),
(7,  'Diego Castillo',   'diego@example.com'),
(8,  'Valentina Cruz',   'valentina@example.com'),
(9,  'Andrés Morales',   'andres@example.com'),
(10, 'Isabela Vargas',   'isabela@example.com'),
(11, 'Camila Rios',      'camila@example.com'),
(12, 'Mateo Salazar',    'mateo@example.com'),
(13, 'Daniela Fuentes',  'daniela@example.com'),
(14, 'Sebastián Rojas',  'sebastian@example.com'),
(15, 'Gabriela Pinto',   'gabriela@example.com');

SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- =============================================================
--  RELACIONES PELÍCULA - GÉNERO
-- =============================================================

INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1,  1), (1,  3), (1,  4),
(2,  1), (2,  2), (2,  12),
(3,  4), (3,  3), (3,  11),
(4,  2), (4,  7),
(5,  2), (5,  3), (5,  11),
(6,  4), (6,  2), (6,  12),
(7,  2), (7,  3), (7,  9),
(8,  1), (8,  10),(8,  12),
(9,  4), (9,  3), (9,  12),
(10, 4), (10, 1), (10, 12),
(11, 4), (11, 1), (11, 10),
(12, 1), (12, 10),(12, 12),
(13, 2), (13, 5), (13, 11),
(14, 2), (14, 9),
(15, 2), (15, 3),
(16, 3), (16, 11),(16, 2),
(17, 10),(17, 4), (17, 2),
(18, 6), (18, 1), (18, 2),
(19, 2), (19, 9),
(20, 1), (20, 3), (20, 6),
(21, 10),(21, 4), (21, 12),
(22, 9), (22, 2), (22, 3),
(23, 6), (23, 2), (23, 12),
(24, 10),(24, 4), (24, 2),
(25, 5), (25, 6), (25, 3);

-- =============================================================
--  RELACIONES PELÍCULA - ACTOR
-- =============================================================

INSERT INTO movie_actors (movie_id, actor_id) VALUES
(1,  1),  (1,  11), (1,  12), (1,  14), (1,  15), (1,  16), (1,  22),
(2,  6),  (2,  5),  (2,  22), (2,  23),
(3,  8),  (3,  22), (3,  12),
(4,  2),  (4,  17), (4,  18),
(5,  10), (5,  20), (5,  21),
(6,  1),  (6,  12),
(7,  4),  (7,  13), (7,  27), (7,  28),
(8,  24), (8,  25), (8,  26),
(9,  3),  (9,  27),
(10, 28), (10, 29),
(11, 28), (11, 3),  (11, 30),
(12, 24), (12, 25), (12, 26),
(13, 1),
(14, 7),
(22, 13);

-- =============================================================
--  AMISTADES (bidireccionales, user1_id < user2_id)
-- =============================================================

INSERT INTO friendships (user1_id, user2_id) VALUES
(1,  2),  (1,  3),  (1,  7),  (1,  9),
(2,  4),  (2,  6),  (2,  11),
(3,  5),  (3,  8),  (3,  10),
(4,  9),  (4,  12),
(5,  7),  (5,  13),
(6,  11), (6,  15),
(7,  10), (7,  14),
(8,  12), (8,  15),
(9,  13),
(10, 14),
(11, 13),
(12, 14),
(13, 15);

-- =============================================================
--  CALIFICACIONES
-- =============================================================

INSERT INTO ratings (user_id, movie_id, rating, watched) VALUES
(1,  1,  5.0, TRUE), (1,  3,  4.5, TRUE), (1,  6,  4.0, TRUE),
(1,  7,  4.5, TRUE), (1,  16, 5.0, TRUE), (1,  18, 3.5, TRUE),
(2,  1,  4.5, TRUE), (2,  4,  5.0, TRUE), (2,  15, 4.5, TRUE),
(2,  19, 4.0, TRUE), (2,  2,  4.5, TRUE), (2,  11, 4.0, TRUE),
(3,  1,  5.0, TRUE), (3,  2,  5.0, TRUE), (3,  8,  4.5, TRUE),
(3,  12, 4.5, TRUE), (3,  17, 4.0, TRUE), (3,  21, 3.5, TRUE),
(4,  5,  4.5, TRUE), (4,  16, 5.0, TRUE), (4,  20, 4.5, TRUE),
(4,  22, 4.0, TRUE), (4,  9,  3.5, TRUE),
(5,  1,  4.0, TRUE), (5,  7,  5.0, TRUE), (5,  11, 4.5, TRUE),
(5,  16, 4.5, TRUE), (5,  22, 4.0, TRUE),
(6,  4,  4.5, TRUE), (6,  15, 5.0, TRUE), (6,  25, 4.5, TRUE),
(6,  19, 4.0, TRUE),
(7,  1,  5.0, TRUE), (7,  2,  4.5, TRUE), (7,  3,  4.0, TRUE),
(7,  7,  4.5, TRUE), (7,  8,  4.5, TRUE), (7,  20, 5.0, TRUE),
(8,  8,  5.0, TRUE), (8,  12, 5.0, TRUE), (8,  17, 4.5, TRUE),
(8,  21, 4.0, TRUE), (8,  24, 4.5, TRUE),
(9,  5,  5.0, TRUE), (9,  13, 4.5, TRUE), (9,  16, 4.5, TRUE),
(9,  22, 4.0, TRUE), (9,  3,  4.0, TRUE),
(10, 1,  4.5, TRUE), (10, 2,  5.0, TRUE), (10, 7,  4.5, TRUE),
(10, 22, 4.0, TRUE), (10, 20, 4.5, TRUE),
(11, 4,  4.5, TRUE), (11, 6,  4.0, TRUE), (11, 25, 4.5, TRUE),
(11, 19, 3.5, TRUE),
(12, 5,  4.5, TRUE), (12, 16, 5.0, TRUE), (12, 18, 4.5, TRUE),
(12, 23, 4.5, TRUE), (12, 20, 4.0, TRUE),
(13, 4,  5.0, TRUE), (13, 15, 4.5, TRUE), (13, 19, 4.5, TRUE),
(13, 22, 4.0, TRUE),
(14, 3,  4.5, TRUE), (14, 5,  4.0, TRUE), (14, 7,  5.0, TRUE),
(14, 11, 4.5, TRUE), (14, 16, 4.5, TRUE),
(15, 8,  4.5, TRUE), (15, 17, 5.0, TRUE), (15, 19, 4.5, TRUE),
(15, 21, 4.0, TRUE), (15, 24, 4.5, TRUE);

-- =============================================================
--  GÉNEROS FAVORITOS POR USUARIO
-- =============================================================

INSERT INTO user_favorite_genres (user_id, genre_id) VALUES
(1,  1),  (1,  3),  (1,  4),
(2,  2),  (2,  7),  (2,  5),
(3,  1),  (3,  10), (3,  12),
(4,  6),  (4,  3),  (4,  11),
(5,  4),  (5,  2),  (5,  9),
(6,  8),  (6,  5),  (6,  7),
(7,  1),  (7,  2),  (7,  3),
(8,  10), (8,  4),  (8,  12),
(9,  11), (9,  3),  (9,  2),
(10, 1),  (10, 9),  (10, 2),
(11, 5),  (11, 7),  (11, 8),
(12, 6),  (12, 1),  (12, 3),
(13, 2),  (13, 9),  (13, 5),
(14, 4),  (14, 11), (14, 3),
(15, 10), (15, 2),  (15, 7);

-- =============================================================
--  ÍNDICES para mejorar rendimiento en las 3 consultas
-- =============================================================

-- Q1: películas de amigos no vistas
CREATE INDEX idx_friendships_user1 ON friendships(user1_id);
CREATE INDEX idx_friendships_user2 ON friendships(user2_id);
CREATE INDEX idx_ratings_user       ON ratings(user_id);
CREATE INDEX idx_ratings_movie      ON ratings(movie_id);
CREATE INDEX idx_ratings_rating     ON ratings(rating);

-- Q2: red de actores
CREATE INDEX idx_movie_actors_actor ON movie_actors(actor_id);
CREATE INDEX idx_movie_actors_movie ON movie_actors(movie_id);

-- Q3: géneros favoritos y calificaciones
CREATE INDEX idx_user_fav_genres_user  ON user_favorite_genres(user_id);
CREATE INDEX idx_user_fav_genres_genre ON user_favorite_genres(genre_id);
CREATE INDEX idx_movie_genres_genre    ON movie_genres(genre_id);
CREATE INDEX idx_movie_genres_movie    ON movie_genres(movie_id);

-- =============================================================
--  VERIFICACIÓN
-- =============================================================

SELECT '=== RESUMEN DE DATOS ===' AS info;
SELECT 'Géneros'           AS tabla, COUNT(*) AS registros FROM genres
UNION ALL
SELECT 'Actores',                    COUNT(*) FROM actors
UNION ALL
SELECT 'Películas/Series',           COUNT(*) FROM movies
UNION ALL
SELECT 'Usuarios',                   COUNT(*) FROM users
UNION ALL
SELECT 'Amistades',                  COUNT(*) FROM friendships
UNION ALL
SELECT 'Calificaciones',             COUNT(*) FROM ratings
UNION ALL
SELECT 'Película-Género',            COUNT(*) FROM movie_genres
UNION ALL
SELECT 'Película-Actor',             COUNT(*) FROM movie_actors
UNION ALL
SELECT 'Géneros favoritos usuario',  COUNT(*) FROM user_favorite_genres;
