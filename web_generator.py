import movie_storage_sql as storage


def serialize_movie_grid(title, data):
    """Creates an HTML list item string for a single animal, safely accessing nested data."""
    output = ""
    try:
        output += '  <li>\n'
        output += '    <div class="movie">\n'
        output += f'      <img class="movie-poster" src="{data["poster"]}" />\n'
        output += f'      <div class="movie-title">{title}</div>\n'
        output += f'      <div class="movie-year">{data["year"]}</div>\n'
        output += f'      <div class="movie-rating">{data["rating"]}</div>\n'
        output += '    </div>\n'
        output += '  </li>\n'

    except KeyError:
        output += "\n"

    return output


def read_template(template_path):
    """Reads an HTML template file with error handling."""
    try:
        with open(template_path, "r") as fileobj:
            return fileobj.read()

    except FileNotFoundError:
        print(f"Error: The template file '{template_path}' was not found.")


def add_movie_to_template(template, output):
    movies_grid = template.replace("__TEMPLATE_MOVIE_GRID__", output)
    return movies_grid


def add_template_title_to_movies_grid(movies_grid):
    template_title = "My Film Collection"
    movies_grid_whit_template_title = movies_grid.replace("__TEMPLATE_TITLE__", template_title)
    return movies_grid_whit_template_title


def write_movies_file(movies_grid):
    with open("index.html", "w") as fileobj:
        fileobj.write(movies_grid)
    print(f"\033[32m Website was generated successfully.\033[0m")


def generate_web():
    movies = storage.list_movies()
    output = ""
    for movie, data in movies.items():
        output += serialize_movie_grid(movie, data)
    template = read_template('index_template.html')
    movies_grid = add_movie_to_template(template, output)
    movies_grid_whit_template_title = add_template_title_to_movies_grid(movies_grid)
    write_movies_file(movies_grid_whit_template_title)
