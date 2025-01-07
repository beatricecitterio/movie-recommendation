# Movie Recommendation System 
### Project Report

Our project is a **movie recommendation system**, that has the form of a **webb application** written in the **Python** language. We intend our app to be used by anyone looking for some inspiration for a movie to watch, comfortably from their sofa on their pc. 

The main components are the **recommendation algorithm** and the **GUI**.
The GUI is opened through a back-end server, which automatically opens a web page. It is composed by a sequence of multiple windows: after a first welcome page, in the first windows the user inserts which genre of movie they would like to watch and how much they enjoyed a chosen number of movies; then these inputs are processed by the algorithm, and finally a window with suggestions and info on the movies is displayed.  
A secondary component of our project is a program to retrieve info from a public API that allowed us to display more information on the movies to be rated and suggested.
In the README file, available in the GitHub repo, more information on the main algorithm and the logic of the program is provided. 


A big issue we encountered with our project was the running time: to open the old GUI (a desktop app) and to process the final window, the program took some seconds. We believe that this problem was related to the Tkinter Python module, used to build the desktop app GUI. Moreover, we were aware that the old logic was not so intuitive and practical, and the user needed to install datasets by themselves.  
We overcome these hurdles by improving the final form of our project developing a web app, instead of a desktop app, using different modules.
Currently, the user still needs to wait some seconds while the necessary datasets get installed. However, the program does that by itself and waiting times are definitely reduced, thus we are satisfied with the solution. Now our reco system is easier to use comfortably from one's sofa!  
As for longer running times of the suggestion pipeline, we tackled this problem displaying a funny gif during the longest process, in order for the user to be entratained during the waiting time. 

'''
problema dei not seen
'''

As we were working on this project, some additional ideas came to our mind. Some of them are implemented, like to provide the user with the trailer and average rating of the movie suggested, to help them choose.
Mainly, we would like to be able to provide users with a link from where to use the recommendation system web app, instead of downloading it from the command line. 
Moreover, we think that the reco system could be further implemented as an extension for common research engines like Google, so that it would be more accessible and hopefully popular.  
Another development we would be interested in is to ask the user to rate the suggested film they choose to watch, and to save the ratings inserted by the user. Then, we would create an account for each user, save their data and update the recommendation algorithm as they use this program and watch and rate movies. This way, our project would be similar to modern recommendation systems, but with the additional feature of asking the user to rate a movie each time they watch it, which in our opinion is funny and useful to improve suggestions. 
In this case, our reco system could also be implemented as a smartphone app.  
Finally, another feature we tried to add is that the user could indicate whether they are satisfied or not with the suggestions, and if not that new movies are recommended, because it could happen that the user has already seen the suggested ones. 

