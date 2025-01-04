import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import re

# WRITE THE PATH WHERE THE CSV ARE STORED HERE
path = 'Users/beatricecitterio'

ratings = pd.read_csv(f'{path}/ratings.csv')
movies = pd.read_csv(f'{path}/movies.csv')

def format_title(title: str):
    ''' 
    This function takes as input a string, which is the title of the movie, and formats it correctly.
    In particular, it removes the year, it removes some specific patterns and orders the words correctly.
    '''
    # remove (a.k.a. ...) patterns
    title = re.sub(r'\(a\.k\.a\..*?\)', '', title).strip()
    
    # remove year (e.g., "(1994)")
    title = re.sub(r'\(\d{4}\)', '', title).strip()
    
    match = re.match(r'(.+), The$', title)
    if match:
        return f"The {match.group(1)}"
    
    match = re.match(r'(.+), A$', title)
    if match:
        return f"A {match.group(1)}"
    
    match = re.match(r'(.+), An$', title)
    if match:
        return f"An {match.group(1)}"
    
    return title.strip()


movies['Formatted Title'] = movies['title'].apply(format_title)

ratings = ratings.drop(columns='timestamp') # we are not interested in this column at the moment

movie_counts = ratings['movieId'].value_counts().reset_index() # this stores the popularity of each movie
movie_counts.columns = ['movieId', 'count'] 

# now we create a subsection of the movie df for each genre
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

def movies_to_rate(genre: str, n = 5):
    ''' 
    This function takes as input the genre selected by the user and the number of movies they want to rate.
    It returns the titles of the movies the user should rate.
    '''
    return list(top_movies[genre][:n]['Formatted Title'])

def suggestion(new_rating: list, genre: str, n = 5, number_of_suggestions = 3):
    '''
    This function takes as input the ratings the user has given to the movies, the genre the movies belong to, the number of movies rated
    and the number of suggestion the user wants to receive.
    Based on the user's ratings, the fuction finds the most similar users in the dataframe, computes their average rating over the selected
    genre and returns the most appreciated movies. 
    On top of that, it also suggests some popular movies of the selected genre.
    '''

    new_rating_dict = {}
    for i in range(n):
        new_rating_dict[list(top_movies[genre][:n].movieId)[i]] = new_rating[i] 

    new_rating_filtered =  {k: v for k, v in new_rating_dict.items() if v != 'Not seen'} # remove unseen movies
    filtered_ratings = ratings[ratings['movieId'].isin(new_rating_filtered.keys())] # filter original df keeping only movies rated by new user 

    pivot_df = filtered_ratings.pivot(index='userId', columns='movieId', values='rating').fillna(2.5) 

    new_user_ratings = pd.DataFrame([new_rating_filtered], index=['new_user']) 
    dissimilarities = euclidean_distances(pivot_df, new_user_ratings) # compute dissimilarities between new user and old users
   
    most_similar_users = pivot_df.index[np.argsort(dissimilarities.flatten())[:20]] # return 20 most similar users

    user_ratings = ratings[ratings['userId'].isin(most_similar_users)]
    movies_by_genre = movies[movies['genres'].str.contains(genre, case=False)] 
    user_ratings = user_ratings[user_ratings['movieId'].isin(movies_by_genre.movieId)]

    user_ratings_filtered = user_ratings.sort_values(by = 'rating', ascending=False) 

    suggested_movies = user_ratings_filtered[~user_ratings_filtered['movieId'].isin(new_rating_filtered.keys())] # select only unseenn movies
    suggested_movies = suggested_movies.sort_values(by = 'movieId')
    suggested_movies['rating']=suggested_movies.groupby('movieId')['rating'].transform('mean') # compute average rating
    suggested_movies = suggested_movies.merge(movie_counts).sort_values(by = ['rating', 'count'], ascending=False) 
    
    final_suggestions_df = suggested_movies.drop_duplicates(subset='movieId').head(number_of_suggestions) 

    final_suggestions = movies[movies['movieId'].isin(final_suggestions_df.movieId)]['Formatted Title'] 

    mustsee_suggestions_bygenre=movies_by_genre[~movies_by_genre['movieId'].isin(new_rating_filtered.keys()) 
                                           & ~movies_by_genre['movieId'].isin(final_suggestions_df['movieId'])]
    mustsee_suggestions_df=mustsee_suggestions_bygenre.merge(movie_counts).sort_values(by = ['count'], ascending=False).head(number_of_suggestions)
    mustsee_suggestions=movies[movies['movieId'].isin(mustsee_suggestions_df.movieId)]['Formatted Title']

    return final_suggestions, mustsee_suggestions