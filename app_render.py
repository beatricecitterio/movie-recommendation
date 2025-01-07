from flask import Flask, render_template, request, jsonify
from tmdb_api import fetch_movie_info
from suggestion_alg_render import format_title, movies_to_rate, suggestion
import requests
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movies', methods=['POST'])
def get_movies():
    data = request.json
    genre = data['genre']
    num_ratings = int(data['numRatings'])
    movies = movies_to_rate(genre, num_ratings)
    
    movies_with_info = []
    for movie in movies:
        movie_info = fetch_movie_info(format_title(movie))
        movies_with_info.append({
            'title': movie,
            'poster_url': movie_info.get('Poster URL', 'No Image Available'),
            'tmdb_url': f"https://www.themoviedb.org/search?query={'+'.join(movie.split())}"
        })
    
    return jsonify(movies_with_info)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    user_ratings = data['ratings']
    genre = data['genre']
    num_suggestions = int(data['numSuggestions'])
    
    recommended_movies, mustsee_movies = suggestion(user_ratings, genre, len(user_ratings), num_suggestions)
    
    recommendations = {
        'recommended': [],
        'mustsee': []
    }
    
    for movie, rating in recommended_movies:
        movie_info = fetch_movie_info(format_title(movie))
        if movie_info:
            recommendations['recommended'].append({
                'title': movie_info['Title'],
                'rating': rating,
                'length': movie_info['Length (min)'],
                'director': movie_info['Director'],
                'actors': movie_info['Actors'],
                'plot': movie_info['Plot'],
                'poster_url': movie_info['Poster URL'],
                'trailer_url': movie_info['Trailer URL']
            })
    
    for movie, rating in mustsee_movies:
        movie_info = fetch_movie_info(format_title(movie))
        if movie_info:
            recommendations['mustsee'].append({
                'title': movie_info['Title'],
                'rating': rating,
                'length': movie_info['Length (min)'],
                'director': movie_info['Director'],
                'actors': movie_info['Actors'],
                'plot': movie_info['Plot'],
                'poster_url': movie_info['Poster URL'],
                'trailer_url': movie_info['Trailer URL']
            })
    
    return jsonify(recommendations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
