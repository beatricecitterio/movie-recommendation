import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

ratings = pd.read_csv('/Users/beatricecitterio/ratings.csv')
movies = pd.read_csv('/Users/beatricecitterio/movies.csv')

ratings = ratings.drop(columns='timestamp')

movie_counts = ratings['movieId'].value_counts().reset_index()
movie_counts.columns = ['movieId', 'count']
movie_counts # create this df so that we know the popularity of each movie (i.e. how many times it has been rated)

genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'Any Genre']
top_movies = {}
for genre in genres:
    if genre == 'Any Genre':
        mov = movies.merge(movie_counts, on = 'movieId').sort_values(by= 'count', ascending = False)
        top_movies[genre] = mov.nlargest(20, 'count')
    else: 
        genre_movies = movies[movies['genres'].str.contains(genre, case=False)]
        genre_movies = genre_movies.merge(movie_counts, on = 'movieId').sort_values(by= 'count', ascending = False)
        top_movies[genre] = genre_movies.nlargest(20, 'count')

def movies_to_rate(genre: str, n = 10):
    return list(top_movies[genre][:n].title)

def suggestion(new_rating: list, genre: str, n = 10, number_of_suggestions = 3):
    new_rating_dict = {}
    for i in range(n):
        new_rating_dict[list(top_movies[genre][:n].movieId)[i]] = new_rating[i]

    new_rating_filtered =  {k: v for k, v in new_rating_dict.items() if v != 'Not seen'}
    filtered_ratings = ratings[ratings['movieId'].isin(new_rating_filtered.keys())]

    pivot_df = filtered_ratings.pivot(index='userId', columns='movieId', values='rating').fillna(2.5)

    new_user_ratings = pd.DataFrame([new_rating_filtered], index=['new_user'])
    dissimilarities = euclidean_distances(pivot_df, new_user_ratings)

    most_similar_user = pivot_df.index[np.argmin(dissimilarities)]

    print(f'Most similar user ID: {most_similar_user}')

    user_ratings = ratings[ratings['userId'] == most_similar_user]
    movies_by_genre = movies[movies['genres'].str.contains(genre, case=False)]
    user_ratings = user_ratings[user_ratings['movieId'].isin(movies_by_genre.movieId)]

    user_ratings_filtered = user_ratings.sort_values(by = 'rating', ascending=False)

    suggested_movies = user_ratings_filtered[~user_ratings_filtered['movieId'].isin(new_rating_filtered.keys())]
    suggested_movies = suggested_movies.merge(movie_counts).sort_values(by = ['rating', 'count'], ascending=False)
    final_suggestions = suggested_movies[:number_of_suggestions]
    final_suggestions = movies[movies['movieId'].isin(final_suggestions.movieId)].title
    return final_suggestions
