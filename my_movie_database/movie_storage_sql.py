from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db"
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
        "poster_url TEXT)"))
    connection.commit()


def get_movies():
    """
    Retrieve all movies from the database.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, director, actors FROM movies"))
        rows = result.fetchall()

    movies = []
    for row in rows:
        actors_list = row[4].split(",") if row[4] else []
        movies.append({
            "title": row[0],
            "year": row[1],
            "rating": row[2],
            "director": row[3],
            "actors": actors_list})
    return movies


def add_movies(title, year, rating, director, actors):
    """
    Add a new movie to the database.
    """
    actors_str = ",".join(actors)
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating, director, actors) "
                    "VALUES (:title, :year, :rating, :director, :actors)"),
                {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "director": director,
                    "actors": actors_str})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movies(title):
    """
    Delete a movie from the database by its title.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title})
        connection.commit()
        return result.rowcount