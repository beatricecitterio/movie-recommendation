# **README**
This file explains how to use the contents of this repository. Besides the ```readme.md```, the repository contains the report of the project, two gifs (```loading.gif``` and ```cinema.gif```, contained in the ```static``` folder), four python scripts (```app.py```, ```old_app.py```, ```suggestion_alg.py``` and ```tmdb_api.py```) and an html file contained in the templates folder. Finally, ```requirements.txt``` contains the dependencies which need to be installed.

## **How to use this repository**
To use our recommendation system, the user should first clone the repository by running: <br>
```git clone https://github.com/beatricecitterio/movie-recommendation.git```<br>
```cd movie-recommendation``` <br>

Then, we suggest to create a new environment:<br> 
```conda create --name env_name python``` <br>
```conda acitvate env_name``` <br>

Then, the user should install the dependencies:
```pip install -r requirements.txt```<br>
and finally run ```python app.py```. This will open a web page with an interactive interface. <br>

This command will automatically also install the datasets we used, which come from The MovieLens Datasets -25M. In particular, we only used ```movies.csv``` and ```ratings.csv```.

## **Contents of each file**
### **app.py**
This file consists of the backend server of our recommendation system, which we built using the Flask module. It uses the TMDb API to fetch information on the movies (posters, descriptions, trailers...). <br>

There are three main routes: the Home Route ('/'), which renders the HTML page, the Get Movies ('/get_movies') interface, which provides the movies to rate (along with the additional information) and finally the Get Recommendations ('/get_recommendations'), which receives user ratings, genre and number of requested suggestions and calls the suggestion function.

### **suggestion_alg.py**
This file contains the algorithm we developed. We assume to be given a genre and a number of movies. The first step is to provide to the new_user a list of movies to rate, which is done through the ```movies_to_rate()``` function. <br>

Once the new_user provides their rating, the idea behind our suggestion system is the following: we store the new ratings in a dictionary (discarding the movies the user has not seen), and we filter the ratings dataframe by keeping only the movies that have been rated by the new_user. We create a ```pivot_df```, where each line corresponds to a user and each column corresponds to one of the movies rated by new_user. We decided to fill n/a values with 2.5, in order not to penalize too much non-rated movies.<br>

Once we have the ```pivot_df```, we compute the dissimilarity of each user with the new_user as the euclidean distance between their ratings. <br>

Then, we consider the 20 users who are most similar to new_user, in terms of taste, and we compute an average of their ratings. We discard movies that the new_user has already seen, and we output as suggestion the movies with highest average rating (when there is a tie, we output the most popular).<br>

Finally, we decided to also include some must-see suggestions to the user, i.e. the most popular movies of the genre they selected, clearly excluding the movies that they have already rated.

### **tmdb_api.py**
The purpose of this file is to fetch some data from the TMDb (The Movie Database) API. In particular, for each movie, the script retrieves information about the title, the runtime, the director, the main actors. It provides also an overview of the plot, the link to the trailer and to the poster image and, finally, the list of streaming platforms it is available on. <br>

This information is used in the suggestion page of our recommendation system. <br>

Besides the main function, ```fetch_movie_info()```, the script also includes two helper functions, ```fetch_trailer()``` and ```fetch_platforms()```, which fetch, respectively, the URL of the trailer on YouTube and the platforms on which the movie is available.

### **old_app.py**
We decided to keep this file in the repository as it shows our first approach in building the GUI. We then decided to try a different approach as the interface was slow and graphically imperfect. However, since we built the second approach starting from this, it might still be interesting to see this file. <br>

This file implements the GUI of our application, using Python's Tkinter library. We decided to build a multipage GUI as follows:
- **welcome page**: contains a message and a gif (cinema.gif). There is a start button which takes the user to the next page
- **genre selection page**: this page is made of a dropdown menu where the user can choose one of the available genres. Then, the user has the possibility to choose the number of movies to rate (either 5 or 10, for a more accurate suggestion). The ```next``` button takes the user to the rating page
- **movie rating page**: this page displays a list of the most popular movies of the selected genre. The user is supposed to rate them from 0 to 5 (only .5 increments are allowed), or write 'Not seen'. Finally, the user can choose how many suggestions to receive, and the ```next``` takes them to the next page.
- **recommendation page**: the ```process_ratings()``` function collects the input of the user and validates it. If valid, user is taken to the recommendation page, where the output of ```suggestion()``` is showed. In particular, for each movie, the graphic also displays a series of additional information, such as movie poster, actors, director, length, plot...

### **index.html**
This HTML file implements the frontend interface for our system. It is structured into multiple pages, which resemble the exact same structure and graphic we created in ```old_app.py```.

## **Bibliography**
F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. https://doi.org/10.1145/2827872
