from sqlalchemy import create_engine, text
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "movies.db")
DB_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DB_URL, echo=False)

with engine.connect() as connection:
    connection.execute(text(
        "CREATE TABLE IF NOT EXISTS movies ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT UNIQUE NOT NULL, "
        "year INTEGER, "
        "rating REAL, "
        "director TEXT, "
        "actors TEXT, "
        "poster_url TEXT)"
    ))
    connection.commit()


def get_movies():
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT title, year, rating, director, actors, poster_url FROM movies"
        ))
        rows = result.fetchall()

    movies = []
    for row in rows:
        actors_list = row[4].split(",") if row[4] else []
        movies.append({
            "title": row[0],
            "year": row[1],
            "rating": row[2],
            "director": row[3],
            "actors": actors_list,
            "poster_url": row[5]
        })
    return movies


def add_movie(title, year, rating, director, actors, poster_url):
    actors_str = ",".join(actors) if actors else ""

    with engine.connect() as connection:
        connection.execute(text(
            "INSERT INTO movies (title, year, rating, director, actors, poster_url) "
            "VALUES (:title, :year, :rating, :director, :actors, :poster_url)"
        ), {
            "title": title,
            "year": year,
            "rating": rating,
            "director": director,
            "actors": actors_str,
            "poster_url": poster_url
        })
        connection.commit()


def delete_movie(title):
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()

    return result.rowcount