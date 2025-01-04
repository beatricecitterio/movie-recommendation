# Movie Recommendation System 
### Project Report

Our project is a **movie recommendation system**, in the form of a **desktop application** written in the **Python** language. 

The main components are the **recommendation algorithm** and the **GUI**.  
The GUI is a sequence of multiple windows: in the first ones the user inserts which genre of movie they would like and how much they liked a chosen number of movies; then these inputs are processed by the algorithm, and finally a window with suggestions and info on the movies is displayed. 

The biggest issue with our project is the running time: to open the GUI and to process the final window, the program takes some seconds.  
We believe that this problem is related to the Tkinter Python module, used to build the GUI, which is arguably slow to run. Also, it could be due to data extraction from the internet, but our best guess remains the first. The algorithm itself outputs movie suggestions immediately if ran independently from the GUI, thus it is not the problem for sure.   
We thought of partly tackling this problem displaying a funny gif during the longest process, in order for the user to be entratained during the waiting time. 

As we were working on this project, some ideas came to our mind. Some of them are implemented, like to provide the user with the trailer and average rating of the movie suggested, to help them choose.
Moreover, we think the reco system could be further implemented as a website or an extension for common research engines like Google, so that it would be more accessible and practical to use.  
A development we would be interested in is to ask the user to rate the suggested film they choose to watch, and to save the ratings inserted by the user. Then, we would create an account for each user, save their data and update the recommendation algorithm as they use this program and watch and rate movies. This way, our project would be similar to modern recommendation systems, but with the additional feature of asking the user to rate a movie each time they watch it, which in our opinion is funny and useful to improve suggestions. 
In this case, our reco system could also be implemented as a smartphone app.  
Finally, another feature we tried to add is that the user could indicate whether they are satisfied or not with the suggestions, and if not that new movies are recommended, because it could happen that the user has already seen the suggested ones. 

