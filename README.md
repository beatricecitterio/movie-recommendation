# **README**
This file explains how to use the contents of this repository. Beside the readme.md file, the repository contains the report of the project, a jpeg picture (cinema.jpeg) and three python scripts (suggestion_alg.py, movie_reco.py and tmdb_api.py).

## **How to use this repository**
In order to be able to use the algorithm we developed, the user needs to first download two datasets from the following url: https://grouplens.org/datasets/movielens/32m/. <br>
The ml-32m.zip file contains four .csv files. For the sake of this project the user only needs to consider movies.csv and ratings.csv. Once these files are saved, the user must change the path in the first lines of suggestion_alg.py to their directory.<br>

ratings.csv contains a line for every rating of one movie by one user. Ratings range from 0 to 5 with .5 increments. movies.csv contains the information about each movie (id, title and genre). <br>

Once the data has been downloaded and the path correctly set, the user should be able to use the suggestion software autonomously by running ```python movie_reco.py``` in their terminal.

## **Contents of each file**
### **suggestion_alg.py**
This file contains the algorithm we developed. We assume to be given a genre and a number of movies. The first step is to provide to the new_user a list of movies to rate, which is done through the ```movies_to_rate()``` function. <br>

Once the new_user provides their rating, the idea behind our suggestion system is the following: we store the new ratings in a dictionary (discarding the movies the user has not seen), and we filter the ratings dataframe by keeping only the movies that have been rated by the new_user. We create a pivot_df, where each line corresponds to a user and each column corresponds to one of the movies rated by new_user. We decided to fill n/a values with 2.5, in order not to penalize too much non-rated movies.<br>

Once we have the pivot_df, we compute the dissimilarity of each user with the new_user as the euclidean distance between their ratings. <br>

Then, we consider the 20 users who are most similar to new_user, in terms of taste, and we compute an average of their ratings. We discard movies that the new_user has already seen, and we output as suggestion the movies with highest average rating (when there is a tie, we output the most popular).<br>

Finally, we decided to also include some must-see suggestions to the user, i.e. the most popular movies of the genre they selected, excluding clearly the movies that they have already rated.

### **tmdb_api.py**
The purpose of this file is to fetch some data from the TMDb (The Movie Database) API. In particular, for each movie, the script retrieves information about the title, the runtime, the director, the main actors. It provides also an overview of the plot, the link to the trailer and to the poster image and, finally, the list of streaming platforms it is available on. <br>

This information is used in the suggestion page of our recommendation system. <br>

Besides the main function, ```fetch_movie_info()```, the script also includes two helper functions, ```fetch_trailer()``` and ```fetch_platforms()```, which fetch, respectively, the URL of the trailer on YouTube and the platforms on which the movie is available.

### **movie_reco.py**
This file implements the GUI of our application, using Python's Tkinter library. We decided to build a multipage GUI as follows:
- **welcome page**: contains a message and a picture (cinema.jpeg). There is a start button which takes the user to the next page
- **genre selection page**: this page is made of a dropdown menu where the user can choose one of the available genres. Then, the user has the possibility to choose the number of movies to rate (either 5 or 10, for a more accurate suggestion). The ```next``` button takes the user to the rating page
- **movie rating page**: this page displays a list of the most popular movies of the selected genre. The user is supposed to rate them from 0 to 5 (only .5 increments are allowed), or write 'Not seen'. Finally, the user can choose how many suggestions to receive, and the ```next``` takes them to the next page.
- **recommendation page**: the ```process_ratings()``` function collects the input of the user and validates it. If valid, user is taken to the recommendation page, where the output of ```suggestion()``` is showed. In particular, for each movie, the graphic also displays a series of additional information, such as movie poster, actors, director, length, plot...

## **Bibliography**
F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. https://doi.org/10.1145/2827872