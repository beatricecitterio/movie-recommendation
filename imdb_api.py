import requests

API_KEY = 'ab012f78ec043a753602ee6d9b8383f4'
BASE_URL = 'https://api.themoviedb.org/3'


def fetch_movie_info(query):
    # Search for the movie
    search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
    search_response = requests.get(search_url).json()

    if not search_response['results']:
        return {
            'Title': query,
            'Genres': 'N/A',
            'Length (min)': 'N/A',
            'Director': 'N/A',
            'Actors': 'N/A',
            'Plot': 'No description available.',
            'Trailer URL': 'No trailer available',
            'Poster URL': 'No poster available',
            'Platforms': 'No platform information available'
        }

    movie_id = search_response['results'][0]['id']
    title = search_response['results'][0]['title']
    plot = search_response['results'][0]['overview']

    # Get movie details
    details_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
    details_response = requests.get(details_url).json()

    length = details_response['runtime']

    # Extract genres
    genres = [genre['name'] for genre in details_response['genres']]

    # Extract poster URL
    poster_path = details_response.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else 'No poster available'

    # Get credits (actors)
    credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
    credits_response = requests.get(credits_url).json()

    # Extract top 5 actors
    actors = [cast['name'] for cast in credits_response['cast'][:5]]

    director = next((crew['name'] for crew in credits_response['crew'] if crew['job'] == 'Director'), 'Not Available')

    trailer_url = fetch_trailer(movie_id)
    platforms = fetch_platforms(movie_id)

    return {
        'Title': title,
        'Genres': ', '.join(genres),
        'Actors': ', '.join(actors),
        'Plot': plot,
        'Length (min)': length,
        'Director': director,
        'Trailer URL': trailer_url,
        'Poster URL': poster_url,
        'Platforms': platforms
    }


def fetch_trailer(movie_id):
    # Fetch video details for the movie
    url = f"{BASE_URL}/movie/{movie_id}/videos?api_key={API_KEY}"
    response = requests.get(url).json()

    # Find the trailer in the video list
    for video in response['results']:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"  # Trailer URL

    return "No trailer available"


def fetch_platforms(movie_id):
    # Fetch watch providers
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    response = requests.get(url).json()

    results = response.get('results', {}).get('US', {}).get('flatrate', [])

    if not results:
        return 'No platform information available'

    platforms = [provider['provider_name'] for provider in results]
    return ', '.join(platforms)
