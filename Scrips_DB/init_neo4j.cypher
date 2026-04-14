// =============================================================
//  INIT_NEO4J.CYPHER
//  Script de inicialización para el ejercicio Neo4J vs PostgreSQL
//
//  OPCIÓN A - Neo4J Browser / Cypher Shell:
//    Pegar y ejecutar bloque por bloque en el browser de Neo4J
//    O ejecutar: cypher-shell -u neo4j -p <password> -f init_neo4j.cypher
//
//  OPCIÓN B - Node.js (recomendada para correr todo de una vez):
//    Usar init_neo4j.js que carga el dataset.json directamente
// =============================================================


// --- Limpiar base de datos (CUIDADO: elimina todo) ---
MATCH (n) DETACH DELETE n;


// =============================================================
//  CONSTRAINTS e ÍNDICES
// =============================================================

CREATE CONSTRAINT genre_id   IF NOT EXISTS FOR (g:Genre)  REQUIRE g.id   IS UNIQUE;
CREATE CONSTRAINT actor_id   IF NOT EXISTS FOR (a:Actor)  REQUIRE a.id   IS UNIQUE;
CREATE CONSTRAINT movie_id   IF NOT EXISTS FOR (m:Movie)  REQUIRE m.id   IS UNIQUE;
CREATE CONSTRAINT user_id    IF NOT EXISTS FOR (u:User)   REQUIRE u.id   IS UNIQUE;
CREATE CONSTRAINT user_email IF NOT EXISTS FOR (u:User)   REQUIRE u.email IS UNIQUE;


// =============================================================
//  GÉNEROS
// =============================================================

CREATE (:Genre {id: 1,  name: 'Sci-Fi'});
CREATE (:Genre {id: 2,  name: 'Drama'});
CREATE (:Genre {id: 3,  name: 'Thriller'});
CREATE (:Genre {id: 4,  name: 'Action'});
CREATE (:Genre {id: 5,  name: 'Comedy'});
CREATE (:Genre {id: 6,  name: 'Horror'});
CREATE (:Genre {id: 7,  name: 'Romance'});
CREATE (:Genre {id: 8,  name: 'Animation'});
CREATE (:Genre {id: 9,  name: 'Documentary'});
CREATE (:Genre {id: 10, name: 'Fantasy'});
CREATE (:Genre {id: 11, name: 'Crime'});
CREATE (:Genre {id: 12, name: 'Adventure'});


// =============================================================
//  ACTORES
// =============================================================

CREATE (:Actor {id: 1,  name: 'Leonardo DiCaprio',    birth_year: 1974});
CREATE (:Actor {id: 2,  name: 'Tom Hanks',            birth_year: 1956});
CREATE (:Actor {id: 3,  name: 'Scarlett Johansson',   birth_year: 1984});
CREATE (:Actor {id: 4,  name: 'Cillian Murphy',       birth_year: 1976});
CREATE (:Actor {id: 5,  name: 'Anne Hathaway',        birth_year: 1982});
CREATE (:Actor {id: 6,  name: 'Matt Damon',           birth_year: 1970});
CREATE (:Actor {id: 7,  name: 'Natalie Portman',      birth_year: 1981});
CREATE (:Actor {id: 8,  name: 'Christian Bale',       birth_year: 1974});
CREATE (:Actor {id: 9,  name: 'Meryl Streep',         birth_year: 1949});
CREATE (:Actor {id: 10, name: 'Brad Pitt',            birth_year: 1963});
CREATE (:Actor {id: 11, name: 'Marion Cotillard',     birth_year: 1975});
CREATE (:Actor {id: 12, name: 'Tom Hardy',            birth_year: 1977});
CREATE (:Actor {id: 13, name: 'Emily Blunt',          birth_year: 1983});
CREATE (:Actor {id: 14, name: 'Joseph Gordon-Levitt', birth_year: 1981});
CREATE (:Actor {id: 15, name: 'Ellen Page',           birth_year: 1987});
CREATE (:Actor {id: 16, name: 'Ken Watanabe',         birth_year: 1959});
CREATE (:Actor {id: 17, name: 'Robin Wright',         birth_year: 1966});
CREATE (:Actor {id: 18, name: 'Gary Sinise',          birth_year: 1955});
CREATE (:Actor {id: 19, name: 'Jessica Lange',        birth_year: 1949});
CREATE (:Actor {id: 20, name: 'Edward Norton',        birth_year: 1969});
CREATE (:Actor {id: 21, name: 'Helena Bonham Carter', birth_year: 1966});
CREATE (:Actor {id: 22, name: 'Michael Caine',        birth_year: 1933});
CREATE (:Actor {id: 23, name: 'Jessica Chastain',     birth_year: 1977});
CREATE (:Actor {id: 24, name: 'Timothée Chalamet',    birth_year: 1995});
CREATE (:Actor {id: 25, name: 'Zendaya',              birth_year: 2003});
CREATE (:Actor {id: 26, name: 'Oscar Isaac',          birth_year: 1979});
CREATE (:Actor {id: 27, name: 'Florence Pugh',        birth_year: 1996});
CREATE (:Actor {id: 28, name: 'Robert Downey Jr.',    birth_year: 1965});
CREATE (:Actor {id: 29, name: 'Gwyneth Paltrow',      birth_year: 1972});
CREATE (:Actor {id: 30, name: 'Chris Evans',          birth_year: 1981});


// =============================================================
//  PELÍCULAS Y SERIES
// =============================================================

CREATE (:Movie {id: 1,  title: 'Inception',               year: 2010, type: 'movie',  synopsis: 'Un ladrón que roba secretos corporativos a través del uso de tecnología de sueños compartidos.'});
CREATE (:Movie {id: 2,  title: 'Interstellar',            year: 2014, type: 'movie',  synopsis: 'Un equipo de exploradores viaja a través de un agujero de gusano en el espacio.'});
CREATE (:Movie {id: 3,  title: 'The Dark Knight',         year: 2008, type: 'movie',  synopsis: 'Batman enfrenta al Joker, un criminal que siembra el caos en Gotham.'});
CREATE (:Movie {id: 4,  title: 'Forrest Gump',            year: 1994, type: 'movie',  synopsis: 'La historia de un hombre con bajas capacidades intelectuales pero gran corazón.'});
CREATE (:Movie {id: 5,  title: 'Fight Club',              year: 1999, type: 'movie',  synopsis: 'Un oficinista insomne y un vendedor de jabón forman un club de lucha.'});
CREATE (:Movie {id: 6,  title: 'The Revenant',            year: 2015, type: 'movie',  synopsis: 'Un explorador busca sobrevivir en la naturaleza salvaje tras ser atacado por un oso.'});
CREATE (:Movie {id: 7,  title: 'Oppenheimer',             year: 2023, type: 'movie',  synopsis: 'La historia del físico que lideró el Proyecto Manhattan.'});
CREATE (:Movie {id: 8,  title: 'Dune',                    year: 2021, type: 'movie',  synopsis: 'Un joven noble debe liderar a su pueblo en el planeta más peligroso del universo.'});
CREATE (:Movie {id: 9,  title: 'Black Widow',             year: 2021, type: 'movie',  synopsis: 'Natasha Romanoff confronta su pasado como espía.'});
CREATE (:Movie {id: 10, title: 'Iron Man',                year: 2008, type: 'movie',  synopsis: 'Un genio millonario construye una armadura de metal para escapar de terroristas.'});
CREATE (:Movie {id: 11, title: 'Avengers: Endgame',       year: 2019, type: 'movie',  synopsis: 'Los Vengadores buscan revertir los efectos del chasquido de Thanos.'});
CREATE (:Movie {id: 12, title: 'Dune: Part Two',          year: 2024, type: 'movie',  synopsis: 'Paul Atreides une fuerzas con los Fremen mientras busca venganza.'});
CREATE (:Movie {id: 13, title: 'The Wolf of Wall Street', year: 2013, type: 'movie',  synopsis: 'La historia del corredor de bolsa Jordan Belfort y su vida de excesos.'});
CREATE (:Movie {id: 14, title: 'A Beautiful Mind',        year: 2001, type: 'movie',  synopsis: 'La vida del matemático John Nash y su lucha contra la esquizofrenia.'});
CREATE (:Movie {id: 15, title: 'Whiplash',                year: 2014, type: 'movie',  synopsis: 'Un joven baterista busca la perfección bajo un instructor despiadado.'});
CREATE (:Movie {id: 16, title: 'Breaking Bad',            year: 2008, type: 'series', synopsis: 'Un profesor de química con cáncer se convierte en productor de metanfetamina.'});
CREATE (:Movie {id: 17, title: 'Game of Thrones',         year: 2011, type: 'series', synopsis: 'Casas nobles compiten por el control del Trono de Hierro en Westeros.'});
CREATE (:Movie {id: 18, title: 'Stranger Things',         year: 2016, type: 'series', synopsis: 'Un grupo de niños enfrenta fuerzas sobrenaturales en su pequeño pueblo.'});
CREATE (:Movie {id: 19, title: 'The Crown',               year: 2016, type: 'series', synopsis: 'La vida de la familia real británica desde los años 40 hasta los 2000.'});
CREATE (:Movie {id: 20, title: 'Dark',                    year: 2017, type: 'series', synopsis: 'Cuatro familias alemanas interconectadas a través del tiempo y del espacio.'});
CREATE (:Movie {id: 21, title: 'The Witcher',             year: 2019, type: 'series', synopsis: 'Las historias del brujo Geralt de Rivia en el Continente.'});
CREATE (:Movie {id: 22, title: 'Chernobyl',               year: 2019, type: 'series', synopsis: 'El relato del desastre nuclear de Chernobyl en 1986.'});
CREATE (:Movie {id: 23, title: 'The Last of Us',          year: 2023, type: 'series', synopsis: 'Un sobreviviente de un apocalipsis fúngico debe cruzar Estados Unidos con una niña.'});
CREATE (:Movie {id: 24, title: 'House of the Dragon',     year: 2022, type: 'series', synopsis: 'La historia de la Casa Targaryen 200 años antes de Game of Thrones.'});
CREATE (:Movie {id: 25, title: 'Wednesday',               year: 2022, type: 'series', synopsis: 'Las aventuras de la hija de la Familia Addams en la academia Nevermore.'});


// =============================================================
//  USUARIOS
// =============================================================

CREATE (:User {id: 1,  name: 'Carlos Mendoza',  email: 'carlos@example.com'});
CREATE (:User {id: 2,  name: 'Ana García',      email: 'ana@example.com'});
CREATE (:User {id: 3,  name: 'Luis Torres',     email: 'luis@example.com'});
CREATE (:User {id: 4,  name: 'María López',     email: 'maria@example.com'});
CREATE (:User {id: 5,  name: 'Pedro Ramírez',   email: 'pedro@example.com'});
CREATE (:User {id: 6,  name: 'Sofía Herrera',   email: 'sofia@example.com'});
CREATE (:User {id: 7,  name: 'Diego Castillo',  email: 'diego@example.com'});
CREATE (:User {id: 8,  name: 'Valentina Cruz',  email: 'valentina@example.com'});
CREATE (:User {id: 9,  name: 'Andrés Morales',  email: 'andres@example.com'});
CREATE (:User {id: 10, name: 'Isabela Vargas',  email: 'isabela@example.com'});
CREATE (:User {id: 11, name: 'Camila Rios',     email: 'camila@example.com'});
CREATE (:User {id: 12, name: 'Mateo Salazar',   email: 'mateo@example.com'});
CREATE (:User {id: 13, name: 'Daniela Fuentes', email: 'daniela@example.com'});
CREATE (:User {id: 14, name: 'Sebastián Rojas', email: 'sebastian@example.com'});
CREATE (:User {id: 15, name: 'Gabriela Pinto',  email: 'gabriela@example.com'});


// =============================================================
//  RELACIONES: PELÍCULA -> GÉNERO  [:HAS_GENRE]
// =============================================================

MATCH (m:Movie {id:1}),  (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:1}),  (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:1}),  (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:2}),  (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:2}),  (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:2}),  (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:3}),  (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:3}),  (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:3}),  (g:Genre {id:11}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:4}),  (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:4}),  (g:Genre {id:7})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:5}),  (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:5}),  (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:5}),  (g:Genre {id:11}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:6}),  (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:6}),  (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:6}),  (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:7}),  (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:7}),  (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:7}),  (g:Genre {id:9})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:8}),  (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:8}),  (g:Genre {id:10}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:8}),  (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:9}),  (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:9}),  (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:9}),  (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:10}), (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:10}), (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:10}), (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:11}), (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:11}), (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:11}), (g:Genre {id:10}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:12}), (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:12}), (g:Genre {id:10}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:12}), (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:13}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:13}), (g:Genre {id:5})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:13}), (g:Genre {id:11}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:14}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:14}), (g:Genre {id:9})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:15}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:15}), (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:16}), (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:16}), (g:Genre {id:11}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:16}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:17}), (g:Genre {id:10}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:17}), (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:17}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:18}), (g:Genre {id:6})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:18}), (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:18}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:19}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:19}), (g:Genre {id:9})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:20}), (g:Genre {id:1})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:20}), (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:20}), (g:Genre {id:6})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:21}), (g:Genre {id:10}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:21}), (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:21}), (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:22}), (g:Genre {id:9})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:22}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:22}), (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:23}), (g:Genre {id:6})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:23}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:23}), (g:Genre {id:12}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:24}), (g:Genre {id:10}) CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:24}), (g:Genre {id:4})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:24}), (g:Genre {id:2})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:25}), (g:Genre {id:5})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:25}), (g:Genre {id:6})  CREATE (m)-[:HAS_GENRE]->(g);
MATCH (m:Movie {id:25}), (g:Genre {id:3})  CREATE (m)-[:HAS_GENRE]->(g);


// =============================================================
//  RELACIONES: ACTOR -> PELÍCULA  [:ACTED_IN]
// =============================================================

MATCH (a:Actor {id:1}),  (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:11}), (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:12}), (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:14}), (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:15}), (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:16}), (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:22}), (m:Movie {id:1})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:6}),  (m:Movie {id:2})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:5}),  (m:Movie {id:2})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:22}), (m:Movie {id:2})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:23}), (m:Movie {id:2})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:8}),  (m:Movie {id:3})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:22}), (m:Movie {id:3})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:12}), (m:Movie {id:3})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:2}),  (m:Movie {id:4})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:17}), (m:Movie {id:4})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:18}), (m:Movie {id:4})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:10}), (m:Movie {id:5})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:20}), (m:Movie {id:5})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:21}), (m:Movie {id:5})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:1}),  (m:Movie {id:6})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:12}), (m:Movie {id:6})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:4}),  (m:Movie {id:7})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:13}), (m:Movie {id:7})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:27}), (m:Movie {id:7})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:28}), (m:Movie {id:7})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:24}), (m:Movie {id:8})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:25}), (m:Movie {id:8})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:26}), (m:Movie {id:8})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:3}),  (m:Movie {id:9})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:27}), (m:Movie {id:9})  CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:28}), (m:Movie {id:10}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:29}), (m:Movie {id:10}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:28}), (m:Movie {id:11}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:3}),  (m:Movie {id:11}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:30}), (m:Movie {id:11}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:24}), (m:Movie {id:12}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:25}), (m:Movie {id:12}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:26}), (m:Movie {id:12}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:1}),  (m:Movie {id:13}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:7}),  (m:Movie {id:14}) CREATE (a)-[:ACTED_IN]->(m);
MATCH (a:Actor {id:13}), (m:Movie {id:22}) CREATE (a)-[:ACTED_IN]->(m);


// =============================================================
//  RELACIONES: USUARIO <-> USUARIO  [:FRIEND]  (bidireccional)
// =============================================================

MATCH (a:User {id:1}),  (b:User {id:2})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:1}),  (b:User {id:3})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:1}),  (b:User {id:7})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:1}),  (b:User {id:9})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:2}),  (b:User {id:4})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:2}),  (b:User {id:6})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:2}),  (b:User {id:11}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:3}),  (b:User {id:5})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:3}),  (b:User {id:8})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:3}),  (b:User {id:10}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:4}),  (b:User {id:9})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:4}),  (b:User {id:12}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:5}),  (b:User {id:7})  CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:5}),  (b:User {id:13}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:6}),  (b:User {id:11}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:6}),  (b:User {id:15}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:7}),  (b:User {id:10}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:7}),  (b:User {id:14}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:8}),  (b:User {id:12}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:8}),  (b:User {id:15}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:9}),  (b:User {id:13}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:10}), (b:User {id:14}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:11}), (b:User {id:13}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:12}), (b:User {id:14}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);
MATCH (a:User {id:13}), (b:User {id:15}) CREATE (a)-[:FRIEND]->(b), (b)-[:FRIEND]->(a);


// =============================================================
//  RELACIONES: USUARIO -> PELÍCULA  [:RATED]  (con propiedad stars)
// =============================================================

MATCH (u:User {id:1}),  (m:Movie {id:1})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:1}),  (m:Movie {id:3})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:1}),  (m:Movie {id:6})  CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:1}),  (m:Movie {id:7})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:1}),  (m:Movie {id:16}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:1}),  (m:Movie {id:18}) CREATE (u)-[:RATED {stars:3.5}]->(m);
MATCH (u:User {id:2}),  (m:Movie {id:1})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:2}),  (m:Movie {id:4})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:2}),  (m:Movie {id:15}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:2}),  (m:Movie {id:19}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:2}),  (m:Movie {id:2})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:2}),  (m:Movie {id:11}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:3}),  (m:Movie {id:1})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:3}),  (m:Movie {id:2})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:3}),  (m:Movie {id:8})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:3}),  (m:Movie {id:12}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:3}),  (m:Movie {id:17}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:3}),  (m:Movie {id:21}) CREATE (u)-[:RATED {stars:3.5}]->(m);
MATCH (u:User {id:4}),  (m:Movie {id:5})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:4}),  (m:Movie {id:16}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:4}),  (m:Movie {id:20}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:4}),  (m:Movie {id:22}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:4}),  (m:Movie {id:9})  CREATE (u)-[:RATED {stars:3.5}]->(m);
MATCH (u:User {id:5}),  (m:Movie {id:1})  CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:5}),  (m:Movie {id:7})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:5}),  (m:Movie {id:11}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:5}),  (m:Movie {id:16}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:5}),  (m:Movie {id:22}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:6}),  (m:Movie {id:4})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:6}),  (m:Movie {id:15}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:6}),  (m:Movie {id:25}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:6}),  (m:Movie {id:19}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:7}),  (m:Movie {id:1})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:7}),  (m:Movie {id:2})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:7}),  (m:Movie {id:3})  CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:7}),  (m:Movie {id:7})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:7}),  (m:Movie {id:8})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:7}),  (m:Movie {id:20}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:8}),  (m:Movie {id:8})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:8}),  (m:Movie {id:12}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:8}),  (m:Movie {id:17}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:8}),  (m:Movie {id:21}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:8}),  (m:Movie {id:24}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:9}),  (m:Movie {id:5})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:9}),  (m:Movie {id:13}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:9}),  (m:Movie {id:16}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:9}),  (m:Movie {id:22}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:9}),  (m:Movie {id:3})  CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:10}), (m:Movie {id:1})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:10}), (m:Movie {id:2})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:10}), (m:Movie {id:7})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:10}), (m:Movie {id:22}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:10}), (m:Movie {id:20}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:11}), (m:Movie {id:4})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:11}), (m:Movie {id:6})  CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:11}), (m:Movie {id:25}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:11}), (m:Movie {id:19}) CREATE (u)-[:RATED {stars:3.5}]->(m);
MATCH (u:User {id:12}), (m:Movie {id:5})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:12}), (m:Movie {id:16}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:12}), (m:Movie {id:18}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:12}), (m:Movie {id:23}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:12}), (m:Movie {id:20}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:13}), (m:Movie {id:4})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:13}), (m:Movie {id:15}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:13}), (m:Movie {id:19}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:13}), (m:Movie {id:22}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:14}), (m:Movie {id:3})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:14}), (m:Movie {id:5})  CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:14}), (m:Movie {id:7})  CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:14}), (m:Movie {id:11}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:14}), (m:Movie {id:16}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:15}), (m:Movie {id:8})  CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:15}), (m:Movie {id:17}) CREATE (u)-[:RATED {stars:5.0}]->(m);
MATCH (u:User {id:15}), (m:Movie {id:19}) CREATE (u)-[:RATED {stars:4.5}]->(m);
MATCH (u:User {id:15}), (m:Movie {id:21}) CREATE (u)-[:RATED {stars:4.0}]->(m);
MATCH (u:User {id:15}), (m:Movie {id:24}) CREATE (u)-[:RATED {stars:4.5}]->(m);


// =============================================================
//  RELACIONES: USUARIO -> GÉNERO  [:LIKES]  (géneros favoritos)
// =============================================================

MATCH (u:User {id:1}),  (g:Genre {id:1})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:1}),  (g:Genre {id:3})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:1}),  (g:Genre {id:4})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:2}),  (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:2}),  (g:Genre {id:7})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:2}),  (g:Genre {id:5})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:3}),  (g:Genre {id:1})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:3}),  (g:Genre {id:10}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:3}),  (g:Genre {id:12}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:4}),  (g:Genre {id:6})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:4}),  (g:Genre {id:3})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:4}),  (g:Genre {id:11}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:5}),  (g:Genre {id:4})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:5}),  (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:5}),  (g:Genre {id:9})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:6}),  (g:Genre {id:8})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:6}),  (g:Genre {id:5})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:6}),  (g:Genre {id:7})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:7}),  (g:Genre {id:1})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:7}),  (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:7}),  (g:Genre {id:3})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:8}),  (g:Genre {id:10}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:8}),  (g:Genre {id:4})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:8}),  (g:Genre {id:12}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:9}),  (g:Genre {id:11}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:9}),  (g:Genre {id:3})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:9}),  (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:10}), (g:Genre {id:1})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:10}), (g:Genre {id:9})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:10}), (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:11}), (g:Genre {id:5})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:11}), (g:Genre {id:7})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:11}), (g:Genre {id:8})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:12}), (g:Genre {id:6})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:12}), (g:Genre {id:1})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:12}), (g:Genre {id:3})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:13}), (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:13}), (g:Genre {id:9})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:13}), (g:Genre {id:5})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:14}), (g:Genre {id:4})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:14}), (g:Genre {id:11}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:14}), (g:Genre {id:3})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:15}), (g:Genre {id:10}) CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:15}), (g:Genre {id:2})  CREATE (u)-[:LIKES]->(g);
MATCH (u:User {id:15}), (g:Genre {id:7})  CREATE (u)-[:LIKES]->(g);


// =============================================================
//  VERIFICACIÓN
// =============================================================

MATCH (n) RETURN labels(n)[0] AS tipo, count(n) AS nodos
ORDER BY nodos DESC;

MATCH ()-[r]->() RETURN type(r) AS relacion, count(r) AS cantidad
ORDER BY cantidad DESC;
