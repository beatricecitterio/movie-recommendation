import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

ratings = pd.read_csv('/Users/matildedolfato/Desktop/magistrai/soft_eng/project/ratings.csv')
movies = pd.read_csv('/Users/matildedolfato/Desktop/magistrai/soft_eng/project/movies.csv')

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

#here we assume to have n, x (num suggestions), genre (str), ratings (new_rating list)

def suggestion(new_rating: list, genre: str, n = 5, number_of_suggestions = 3):
    new_rating_dict = {}
    for i in range(n):
        new_rating_dict[list(top_movies[genre][:n].movieId)[i]] = new_rating[i] #create ratings list given input by the user

    new_rating_filtered =  {k: v for k, v in new_rating_dict.items() if v != 'Not seen'} #keep only seen ones
    filtered_ratings = ratings[ratings['movieId'].isin(new_rating_filtered.keys())] #filter original df keeping only movies rated by new user 

    pivot_df = filtered_ratings.pivot(index='userId', columns='movieId', values='rating').fillna(2.5) #organise it as original df

    new_user_ratings = pd.DataFrame([new_rating_filtered], index=['new_user']) #create df with ratings by new user
    dissimilarities = euclidean_distances(pivot_df, new_user_ratings) 
    # print('length dissimilrities:',len(dissimilarities)) 
    # num users is 118301
    print(dissimilarities)

    most_similar_user = pivot_df.index[np.argmin(dissimilarities)]
    most_similar_users = pivot_df.index[np.argsort(dissimilarities.flatten())[:20]]


    print(f'Most similar user ID: {most_similar_user}') 

    user_ratings = ratings[ratings['userId'].isin(most_similar_users)]
    #user_ratings = ratings[ratings['userId'] == most_similar_user] #prendo i movies visti dai most similar users
    movies_by_genre = movies[movies['genres'].str.contains(genre, case=False)] #seleziono dal mio dataset originale i movies in base al genere scelto
    user_ratings = user_ratings[user_ratings['movieId'].isin(movies_by_genre.movieId)] #tengo dei movies visti dai miei most similar quelli di quel genere

    user_ratings_filtered = user_ratings.sort_values(by = 'rating', ascending=False) #ordino mio df in base al rating 


    suggested_movies = user_ratings_filtered[~user_ratings_filtered['movieId'].isin(new_rating_filtered.keys())] #prendo quelli che non ha visto
    suggested_movies = suggested_movies.merge(movie_counts).sort_values(by = ['rating', 'count'], ascending=False) #ci aggiungo il count e ranko per rating del mio most similar, e poi per popularità
    # Select the first `n` rows, dropping duplicates based on the 'movieId' column
    final_suggestions_df = suggested_movies.drop_duplicates(subset='movieId').head(number_of_suggestions) #keeps the highest rating, but i don't think it matters now
    final_suggestions_df
    final_suggestions = movies[movies['movieId'].isin(final_suggestions_df.movieId)].title #ritorno il titolo degli x film rated meglio- piu popolari

    # voglio fare un dataset con i piu visti di quel genere togliendo quelli che ha rated e quelli già consigliati FREGANDOCENE DI RATING!! I PIU SEEN!
    # ha senso fare questa dopo la prima, perche nella prima li ordino prima per similarity poi per rating e solo alla fine per count 
    mustsee_suggestions_bygenre=movies_by_genre[~movies_by_genre['movieId'].isin(new_rating_filtered.keys()) 
                                           & ~movies_by_genre['movieId'].isin(final_suggestions_df['movieId'])]
    mustsee_suggestions_df=mustsee_suggestions_bygenre.merge(movie_counts).sort_values(by = ['count'], ascending=False).head(number_of_suggestions)
    mustsee_suggestions=movies[movies['movieId'].isin(mustsee_suggestions_df.movieId)].title

    return final_suggestions, mustsee_suggestions
