import os
import random
import requests
from dotenv import load_dotenv
import movie_storage_sql as storage

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
if not OMDB_API_KEY:
    raise ValueError("OMDb API Key not set yet!")


class Colors:
    BLUE = '\033[94m'
    LIGHT_BLUE = "\033[94m"
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'


def press_enter_to_continue():
    input(f"{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")


def print_title():
    print(Colors.BLUE + Colors.LIGHT_BLUE + "Jessy's Movies Database" + Colors.RESET)


def get_movies():
    return storage.get_movies()


def add_movie():
    title_input = input("Enter movie title: ").strip()
    if not title_input:
        print(f"{Colors.RED}Title cannot be empty!{Colors.RESET}")
        return

    for movie in get_movies():
        if movie['title'].lower() == title_input.lower():
            print(f"{Colors.RED}Movie already exists!{Colors.RESET}")
            return

    url = f"http://www.omdbapi.com/?t={title_input}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{Colors.RED}Could not reach OMDb API.{Colors.RESET}")
        return

    data = response.json()
    if data.get("Response") == "False":
        print(f"{Colors.RED}Movie not found in OMDb.{Colors.RESET}")
        return

    title = data.get("Title", title_input)

    year_str = data.get("Year", "")
    year = int(year_str) if year_str.isdigit() else None

    imdb_rating = data.get("imdbRating", "")
    rating = float(imdb_rating) if imdb_rating not in ("N/A", "") else None

    director = data.get("Director", "Unknown")
    actors = data.get("Actors", "Unknown").split(", ")
    poster_url = data.get("Poster", "")

    try:
        storage.add_movie(title, year, rating, director, actors, poster_url)
        print(f"{Colors.YELLOW}Movie added successfully!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")

    press_enter_to_continue()


def delete_movie():
    title_input = input("Enter title to delete: ").strip()
    if not title_input:
        print(f"{Colors.RED}Title cannot be empty!{Colors.RESET}")
        return

    deleted = storage.delete_movie(title_input)

    if deleted == 0:
        print(f"{Colors.RED}Movie not found!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Movie deleted successfully.{Colors.RESET}")

    press_enter_to_continue()


def calculate_median(numbers):
    numbers_sorted = sorted(numbers)
    n = len(numbers_sorted)
    mid = n // 2
    if n % 2 == 1:
        return numbers_sorted[mid]
    else:
        return (numbers_sorted[mid - 1] + numbers_sorted[mid]) / 2


def stats():
    movies = get_movies()
    ratings = [float(m['rating']) for m in movies if m['rating'] not in [None, "Unknown"]]

    if not ratings:
        print("No ratings available.")
        press_enter_to_continue()
        return

    avg = sum(ratings)/len(ratings)
    med = calculate_median(ratings)
    high = max(ratings)
    low = min(ratings)

    best_movies = [m['title'] for m in movies if m['rating'] == high]
    worst_movies = [m['title'] for m in movies if m['rating'] == low]

    print(f"Average rating: {avg:.2f}")
    print(f"Median rating: {med:.2f}")
    print(f"Highest rating: {high} → {', '.join(best_movies)}")
    print(f"Lowest rating: {low} → {', '.join(worst_movies)}")
    press_enter_to_continue()


def random_movie():
    movies = get_movies()
    if not movies:
        print("No movies available.")
        press_enter_to_continue()
        return
    movie = random.choice(movies)
    print(f"Random movie: {movie['title']} → Rating: {movie['rating']}")
    press_enter_to_continue()


def search_movie():
    query = input("Enter keyword to search: ").lower()
    movies = get_movies()
    found = False
    for movie in movies:
        if query in movie['title'].lower():
            print(f"{Colors.YELLOW}{movie['title']} → {movie['rating']}{Colors.RESET}")
            found = True
    if not found:
        print(f"{Colors.RED}No movies found.{Colors.RESET}")
    press_enter_to_continue()


def sort_by_rating():
    movies = get_movies()

    movies_sorted = sorted(
        movies,
        key=lambda m: m['rating'] or -1,
        reverse=True
    )

    for m in movies_sorted:
        print(f"{m['title']}: {m['rating']}")

    press_enter_to_continue()


def filter_movies():
    min_rating = input("Minimum rating (leave blank for no filter): ").strip()
    start_year = input("Start year (leave blank for no filter): ").strip()
    end_year = input("End year (leave blank for no filter): ").strip()

    try:
        min_rating = float(min_rating) if min_rating else None
    except ValueError:
        min_rating = None
    try:
        start_year = int(start_year) if start_year else None
    except ValueError:
        start_year = None
    try:
        end_year = int(end_year) if end_year else None
    except ValueError:
        end_year = None

    filtered = []
    for m in get_movies():
        r = m['rating'] if m['rating'] not in [None, "Unknown"] else -1
        y = m['year'] if isinstance(m['year'], int) else -1
        if min_rating is not None and r < min_rating:
            continue
        if start_year is not None and y < start_year:
            continue
        if end_year is not None and y > end_year:
            continue
        filtered.append(m)

    for m in filtered:
        print(f"{m['title']} ({m['year']}) → {m['rating']}")
    press_enter_to_continue()


def generate_website():
    movies = get_movies()

    template_path = os.path.join(
        os.path.dirname(__file__),
        "_static",
        "index_template.html"
    )

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"{Colors.RED}Template file not found in _static/index_template.html{Colors.RESET}")
        press_enter_to_continue()
        return

    movie_grid_html = ""
    for m in movies:
        movie_html = "<li class='movie'>\n"
        if m['poster_url']:
            movie_html += f"  <img class='movie-poster' src='{m['poster_url']}' alt='{m['title']} poster'>\n"
        movie_html += f"  <div class='movie-title'>{m['title']}</div>\n"
        movie_html += f"  <div class='movie-year'>{m['year']}</div>\n"
        movie_html += "</li>\n"
        movie_grid_html += movie_html

    template = template.replace("__TEMPLATE_TITLE__", "Jess' Movie Collection")
    template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    output_path = os.path.join(os.path.dirname(__file__), "index.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"{Colors.YELLOW}Website was generated successfully.{Colors.RESET}")
    press_enter_to_continue()


def main():
    print_title()
    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Stats")
        print("5. Random movie")
        print("6. Search movie")
        print("7. Sort by rating")
        print("8. Filter movies")
        print("9. Generate website")

        print()
        choice = input(f"{Colors.YELLOW}Enter choice: {Colors.RESET}")

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            movies = get_movies()
            for m in movies:
                print(f"{m['title']} ({m['year']}) → {m['rating']}")
            press_enter_to_continue()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            stats()
        elif choice == "5":
            random_movie()
        elif choice == "6":
            search_movie()
        elif choice == "7":
            sort_by_rating()
        elif choice == "8":
            filter_movies()
        elif choice == "9":
            generate_website()
        else:
            print(f"{Colors.RED}Invalid choice!{Colors.RESET}")


if __name__ == "__main__":
    main()