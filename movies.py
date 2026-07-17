import statistics
import random
import web_generator
from movie_storage import movie_storage_sql as storage
from movie_storage.movie_api import get_data_from_api
from dotenv import load_dotenv

load_dotenv()

def user_input(menu):
    """
    Display the menu and return the user's chosen option as an integer.
    Args:
        menu (list): List of menu option strings.
    Returns:
        int: The index of the chosen menu option (0 to len(menu)-1).
    """
    print("\033[32m\033[1m\n \033[4mMenu:\033[0m")

    for index, option in enumerate(menu):
        print(f"\033[34m {index}.\033[32m {option}\033[0m")
    while True:
        try:
            user_choice = int(input(f"\033[33m\n Enter choice"
                                    f" (0-{len(menu) - 1}): \033[0m"))
            if 0<= user_choice < len(menu):
                return user_choice
            print(f"\033[31m Please enter a number between 0 and"
                  f" {len(menu) - 1}\033[0m")
        except ValueError:
            print("\033[31m Invalid input. Pleas enter a number.\033[0m")


def list_movies():
    """Print all movies with their year and rating."""
    movies = storage.list_movies()
    print(f"\033[34m\n {len(movies)}\033[32m movies in total\033[0m")

    for movie, data in movies.items():
        print(f"\033[35m\033[1m {movie} ({data['year']}):\033[34m {data['rating'] :.1f}\033[0m")


def add_movie():
    """Add a new movie by fetching its data from OMDb."""
    movies = storage.list_movies()
    movie = input("\033[33m\n Enter new movie name: \033[0m").strip()
    if not movie:
        print("\033[31m Movie name cannot be empty.\033[0m")
        return

    if movie in movies:
        print(f"\033[31m Movie\033[35m\033[1m  {movie}"
              f"\033[31m already exist.\033[0m")
        return

    print("\033[36m Fetching movie data...\033[0m")
    movie_data = get_data_from_api(movie)
    if movie_data is None:
        return

    title = movie_data.get('Title', '').strip()
    year_str = movie_data.get('Year', '')
    rating_str = movie_data.get('imdbRating', '')
    poster = movie_data.get('Poster', '')

    try:
        year = int(year_str.split('-')[0])
    except (ValueError, AttributeError):
        print(f"\033[31m Invalid year '{year_str}' received from API.\033[0m")
        return

    if rating_str == 'N/A' or not rating_str:
        print(f"\033[31m No rating available for '{title}'.\033[0m")
        return

    try:
        rating = float(rating_str)
        if not (0 <= rating <= 10):
            print(f"\033[31m Rating {rating} out of range (1-10).\033[0m")
            return
    except ValueError:
        print(f"\033[31m Invalid rating format '{rating_str}'.\033[0m")
        return

    try:
        storage.add_movie(title, year, rating, poster)
        print(f"\033[32m Movie \033[35m\033[1m{title}\033[32m"
              f"({year}) added successfully!\033[0m")
    except Exception as e:
        print(f"\033[31m Database error: {e}\033[0m")


def delete_movie():
    """Delete a movie from the collection."""
    movies = storage.list_movies()
    movie = input("\033[33m\n Enter movie name to delete: \033[0m").strip()
    if movie not in movies:
        print(f"\033[31m Movie \033[35m\033[1m{movie}\033[31m\033[1m"
              f" doesn't exist!\033[0m")
    else:
        storage.delete_movie(movie)
        print(f"\033[32m Movie \033[35m\033[1m{movie}\033[32m"
              f" successfully deleted\033[0m")
    return


def update_movie():
    """Update the rating of an existing movie (preserves the year)."""
    movies = storage.list_movies()
    movie = input("\033[33m\n Enter movie name: \033[0m").strip()
    if movie not in movies:
        print(f"\033[31m Movie \033[35m\033[1m{movie}\033[31m"
              f" doesn't exist!\033[0m")
        return
    try:
        rating = float(input("\033[33m Enter new movie rating (0-10):"
                             " \033[0m"))
        if 0 <= rating <= 10:
            storage.update_movie(movie, rating)
            print(f"\033[32m Movie \033[35m\033[1m{movie}\033[32m"
                  f" successfully  updated\033[0m")
        else:
            print(f"\033[31m Rating \033[34m{rating :.1f}\033[31m"
                  f" is invalid\033[0m")
    except ValueError:
        print("\033[31m Invalid rating. Please enter a number.\033[0m")
    return


def stats():
    """Display statistics: average, median, best and worst movie."""
    movies = storage.list_movies()
    if not movies:
        print("\033[31m Library not found!\033[0m")
        return

    ratings = [movie['rating'] for movie in movies.values()]
    best_movie = max(movies, key=lambda movie: movies[movie]['rating'])
    worst_movie = min(movies, key=lambda movie: movies[movie]['rating'])
    average_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)

    print(f"\033[32m\n Average rating:\033[34m {average_rating :.1f}\033[0m")
    print(f"\033[32m Median rating:\033[34m {median_rating :.1f}\033[0m")
    print(f"\033[32m Best movie:\033[35m\033[1m {best_movie}"
          f" ({movies[best_movie]['year']}),\033[34m"
          f" {movies[best_movie]['rating']:.1f}\033[0m")
    print(f"\033[32m Worst movie:\033[35m\033[1m {worst_movie}"
          f" ({movies[worst_movie]['year']}),\033[34m"
          f" {movies[worst_movie]['rating']:.1f}\033[0m")


def random_movie():
    """Pick and display a random movie from the collection."""
    movies = storage.list_movies()
    if not movies:
        print("\033[31m No movies available to choose from.\033[0m")
        return
    movie = random.choice(list(movies))
    print(f"\033[32m\n Your movie for tonight:\033[35m\033[1m {movie}"
          f" ({movies[movie]['year']}),\033[32m it's rated"
          f" \033[34m{movies[movie]['rating'] :.1f}\033[0m")


def search_movie():
    """Search for movies whose name contains a substring (case‑insensitive)."""
    movies = storage.list_movies()
    part_of_movie_name = input("\033[33m\n Enter part of movie name:"
                               " \033[0m").strip()
    found = False
    for movie, data in movies.items():
        if part_of_movie_name.lower() in movie.lower():
            print(f"\033[35m\033[1m {movie} ({data['year']}"
                  f"),\033[34m {data['rating'] :.1f}\033[0m")
            found = True
    if not found:
        print(f"\033[31m No movies containing\033[35m\033[1m"
              f" {part_of_movie_name}\033[31m found.\033[0m")


def movies_sorted_by_rating():
    """Print all movies sorted by rating (highest first)."""
    movies = storage.list_movies()
    if not movies:
        print("\033[31m No movies to display.\033[0m")
        return
    print("\n")
    sorted_movies = sorted(movies.items(),
                           key=lambda item: item[1]['rating'],
                           reverse = True)
    for movie, data in sorted_movies:
        print(f"\033[35m\033[1m {movie} ({data['year']}):"
              f" \033[34m{data['rating'] :.1f}\033[0m")


def generate_website():
    """Generates a website from an SQL database."""
    web_generator.generate_web()


def main():
    """Main program loop."""
    menu = [
        "Exit",
        "List movies",
        "Add movie",
        "Delete movie",
        "Update movie",
        "Stats",
        "Random movie",
        "Search movie",
        "Movies sorted by rating",
        "Generate website"
    ]
    print("\033[32m\033[1m\n ********** My Movies Database **********\033[0m")

    while True:
        menu_point = user_input(menu)
        if menu_point == 0:
            print("\033[32m\033[1m\n Bye!\033[0m")
            break
        elif menu_point == 1:
            list_movies()
        elif menu_point == 2:
            add_movie()
        elif menu_point == 3:
            delete_movie()
        elif menu_point == 4:
            update_movie()
        elif menu_point == 5:
            stats()
        elif menu_point == 6:
            random_movie()
        elif menu_point == 7:
            search_movie()
        elif menu_point == 8:
            movies_sorted_by_rating()
        elif menu_point == 9:
            generate_website()
        input("\033[33m\n Press enter to continue \033[0m")


if __name__ == "__main__":
    main()