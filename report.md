# **Movie Recommendation System**
## **Project Report**
This file contains the report of the final project for Software Engineering (20875) by Beatrice Citterio and Matilde Dolfato.
### **Overview of the Project**
Our project is a **movie recommendation system**, that has the form of a **web application** written in the **Python** language. We intend our app to be used by anyone looking for some inspiration for a movie to watch, comfortably from their sofa on their pc. 

The main components are the **recommendation algorithm** and the **GUI**.  
The GUI is opened through a back-end server, which automatically opens a web page. It is composed by a sequence of multiple windows: after a first welcome page, in the first windows the user inserts which genre of movie they would like to watch and how much they enjoyed a chosen number of movies; then these inputs are processed by the algorithm, and finally a window with suggestions and info on the movies is displayed.  
A secondary component of our project is a program to retrieve info from a public API that allowed us to display more information on the movies to be rated and suggested.  
In the README file, available in the GitHub repo, more information on the main algorithm and the logic of the program is provided. 

### **Potential Issues**
A big issue we encountered with our project was the running time: to open the old GUI (a desktop app) and to process the final window, the program took some seconds. We believe that this problem was related to the Tkinter Python module, used to build the desktop app GUI. Moreover, we were aware that the old logic was not so intuitive and practical, and the user needed to install datasets by themselves.  
We overcome these hurdles by improving the final form of our project developing a web app, instead of a desktop app, using different modules.
Currently, the user still needs to wait some seconds while the necessary datasets get installed. However, the program does that by itself and waiting times are definitely reduced, thus we are satisfied with the solution. Now our reco system is easier to use comfortably from one's sofa!  
As for longer running times of the suggestion pipeline, we tackled this problem displaying a funny gif during the longest process, in order for the user to be entratained during the waiting time. 

### **Further Improvements**
As we were working on this project, some additional ideas came to our mind. Some of them are implemented, like to provide the user with the trailer and average rating of the movie suggested, to help them choose.
The main point we could further develop our project on is that we would like to be able to provide users with a link from where to use the recommendation system web app, instead of having to clone the repository and open it through python. This would help us to reach more people and make it usable even to those who have no idea of what python even is.
Moreover, we think that the recommendation system could be further implemented as an extension for common research engines like Google, so that it would be more accessible and hopefully popular.  

Another development we would be interested in is to keep track of the user preferences to make the experience even more personal. For example, we would create an account for each user, save their data (i.e. their ratings) and update the recommendation algorithm as they use this program and watch and rate movies. This way, our project would be similar to modern recommendation systems, but with the additional feature of asking the user to rate a movie every time they watch it, which in our opinion is fun and useful to improve suggestions. In this case, our recommendation system could also be implemented as a smartphone app.  

In addition, another interesting development could be to further investigate the MovieLens rating dataset to see whether there are some underlying trends. For example, we discarded at the beginning of the analysis the column 'timestamp' from ratings.csv, which determines the precise time and day when the rating was done. However, it could be useful to understand whether there are certain movies which are particularly appreciated in certain periods of the year or in certain hours of the day or they might be trending in certain years. Exploiting this could make our recommendations even more accurate.

Finally, another feature we tried to add is that the user could indicate whether they are satisfied or not with the suggestions. If not, new movies would be recommended. We thought of this in order to give the user more chances to receive as suggestions movies that they have not already seen, and improve their overall satisfaction.

