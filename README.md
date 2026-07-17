
# 🎬 My Movies Database

A command-line movie collection manager with SQLite storage and automatic website generation.  
Data is fetched from the [OMDb API](https://www.omdbapi.com/) and displayed in a colourful terminal interface.

---

## 📋 Features

- Add movies by fetching real data (title, year, rating, poster) from OMDb
- List all movies
- Delete and update movie ratings
- Display statistics: average, median, best and worst rated movies
- Get a random movie suggestion
- Search movies by partial title (case-insensitive)
- Sort and display movies by rating (highest first)
- Generate a static HTML website (`index.html`) to show your collection
- Persistent storage in a local SQLite database (`movies.db`)

---

## 🔧 Prerequisites

- Python 3.8 or higher
- An OMDb API key (free tier available at [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx))

---

## ⚙️ Installation & Setup

1. **Clone the repository** or download the source code:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```
2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your API key**:

   Create a new .env file in the project root:

   ```text
   OMDB_API_KEY=your_api_key_here
   ```
   The .gitignore file already excludes .env to keep your key private.

---

## 🚀 Usage
- Run the main program from the terminal:

   ```bash
   python movies.py
   ```
- You'll see a menu with the following options:

   ```text
    0. Exit
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating
    9. Generate website
    ```
- Choose an option by entering the corresponding number.

- Detailed Menu Options:
   ```text
    1. List movies – Shows all movies with year and rating.
   
    2. Add movie – Prompts for a movie title, then fetches data from OMDb. The movie is saved to the database.
   
    3. Delete movie – Removes a movie by its exact title.
   
    4. Update movie – Change the rating of an existing movie (year remains untouched).
   
    5. Stats – Displays average rating, median rating, best and worst rated movies.
   
    6. Random movie – Picks a random movie from your collection.
   
    7. Search movie – Finds all movies whose title contains the given substring.
   
    8. Movies sorted by rating – Lists all movies ordered from highest to lowest rating.
   
    9. Generate website – Creates a fresh index.html (and copies style.css) to display your collection in a browser.
   ```

---

## 🌐 Website Generation
- When you select “Generate website”, the program:

   - Reads the HTML template index_template.html
   
   - Replaces __TEMPLATE_TITLE__ and __TEMPLATE_MOVIE_GRID__ placeholders
   
   - Writes the result to index.html

- Open index.html in any browser to see your movie collection with posters, titles, years and ratings.

---

## 📦 Dependencies
- All dependencies are listed in requirements.txt:

  - requests – HTTP requests for the OMDb API

  - sqlalchemy – ORM and database abstraction for SQLite

  - python-dotenv – Loads environment variables from .env

---

## ⚠️ Notes
- The database file movies.db is created automatically on first run.

- The terminal output is colour-coded; it looks best in modern terminal emulators that support ANSI escape codes.

- If a movie is not found via the API, an appropriate error message is shown.

- The .env file is not included in version control; each user must provide their own OMDb API key.

---

## 📝 License
- This project is provided for educational purposes. You may modify and use it for non-commercial purposes only. Commercial use is not permitted without explicit permission.

---

## Enjoy building your movie collection! 🍿