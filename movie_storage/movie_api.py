import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OMDB_API_KEY')


def get_data_from_api(title):
    """Fetches movie data from OMDb. Returns a dict on success, None on failure."""
    if not API_KEY:
        print("OMDB_API_KEY not found in .env or empty.")
        return None

    url = f'http://www.omdbapi.com/'
    params = {'apikey': API_KEY, 't': title}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Throws an HTTP error for 4xx/5xx
        data = response.json()

        # If movie not found, OMDb returns a 200 status code + {"Response":"False","Error":"..."}
        if data.get('Response') == 'False':
            print(f"Movie not found: {data.get('Error', 'Unknown error')}")
            return None

        return data

    except requests.exceptions.RequestException as e:
        # Network error, timeout, invalid URL, etc.
        print(f'Network/Request Error: {e}')
    except ValueError as e:
        # JSON decoding error
        print(f'Invalid JSON response: {e}')

    return None
