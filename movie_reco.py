from imdb_api import fetch_movie_info
from suggestion_alg import format_title
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from suggestion_alg import movies_to_rate, suggestion
import webbrowser
from PIL import Image

def create_scrollable_frame(root):
    canvas = tk.Canvas(root, bg="white")
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame


def open_genre_page():
    # Clear previous entries
    for widget in root.winfo_children():
        widget.destroy() #we clear previous widgets to create the new page

    # First Page - Genre and Number of Ratings Selection
    tk.Label(root, text="Which genre are you in the mood for?",font=("Helvetica", 20), fg="darkred", bg="white" ).pack(pady=20) # we add to the root the label select genre, with some space (padding, pady) around it
    global genre_var
    genre_var = tk.StringVar() #create genre var where some input will be stored
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'Any Genre']
    genre_dropdown = ttk.Combobox(root, textvariable=genre_var, values=genres, state='readonly', foreground="darkred") #create pop down list, you say that this is a variable and link it to genre_var (automatically stores the selection of the user)
    genre_dropdown.pack(pady=5)
    genre_dropdown.current(0) #i think here 'Action' will show up, whereas we could add something like empty space or 'select genre' or something else

    # Number of Ratings Selection
    tk.Label(root, text="Choose the number of movies to rate:",font=("Helvetica", 20), fg="darkred", bg="white").pack(pady=15) #same logic to create 
    global num_ratings_var
    num_ratings_var = tk.IntVar()
    num_ratings_var.set(5) #sure needed? but doesn't hurt
    ttk.Radiobutton(root, text="5", variable=num_ratings_var, value=5, style="TRadiobutton").pack(pady=5)
    ttk.Radiobutton(root, text="10", variable=num_ratings_var, value=10, style="TRadiobutton").pack(pady=5)
    # Next Button
    tk.Button(root, text="Next", command=open_rating_page).pack(pady=20) 
    return num_ratings_var, genre_var



# Move to rating page
def open_rating_page():
    genre = genre_var.get()
    num_ratings = num_ratings_var.get()

    # Clear previous entries
    for widget in root.winfo_children():
        widget.destroy() #we clear previous widgets to create the new page

    # Movie Ratings Input
    global rating_entries
    rating_entries = {}
    tk.Label(root, text="Rate the following movies:", font=("Helvetica", 20), fg="darkred", bg="white").pack(pady=(20, 5))
    tk.Label(root, text="(0-5, 0.5 increments, or 'Not seen')", font=("Helvetica", 15), fg="darkred", bg="white").pack(pady=(5, 10))

    movies = movies_to_rate(genre, num_ratings) #where do we get the num ratings var?
    for movie in movies:
        tk.Label(root, text=movie, font=("Helvetica", 14), bg="white", fg="black").pack(pady=2)
        entry = tk.Entry(root)
        entry.pack(pady=2)
        rating_entries[movie] = entry

    # Number of Recommendations Selection
    tk.Label(root, text="How many suggestions would you like to get?", font=("Helvetica", 20), fg="darkred", bg="white").pack(pady=(15,5))
    global num_suggestions_var
    num_suggestions_var = tk.IntVar()
    num_suggestions_var.set(3)
    ttk.Radiobutton(root, text="1", variable=num_suggestions_var, value=1, style="TRadiobutton").pack()
    ttk.Radiobutton(root, text="3", variable=num_suggestions_var, value=3, style="TRadiobutton").pack()
    ttk.Radiobutton(root, text="5", variable=num_suggestions_var, value=5, style="TRadiobutton").pack()

    # Recommend Button
    tk.Button(root, text="Next", command=process_ratings).pack(pady=20)

# Process ratings before moving to recommendation page
def process_ratings():
    # Clear previous entries
    # for widget in root.winfo_children():
    #     widget.destroy() #we clear previous widgets to create the new page

    #Insert GIF 
    # download GIF here: https://images.app.goo.gl/wfK7KAYZPbeEAnF79
    # file = "/Users/matildedolfato/Desktop/popcorns.gif"
    # info = Image.open(file)
    # frames = info.n_frames  # number of frames
    # photoimage_objects = []
    # for i in range(frames):
    #     obj = tk.PhotoImage(file=file, format=f"gif -index {i}")
    #     photoimage_objects.append(obj)

    # def animation(current_frame=0):
    #     global loop
    #     image = photoimage_objects[current_frame]
    #     gif_label.configure(image=image)
    #     current_frame = current_frame + 1
    #     if current_frame == frames:
    #         current_frame = 0
    #     loop = root.after(info.info['duration'] , lambda: animation(current_frame))

    # gif_label = tk.Label(root, image="")
    # gif_label.pack()
    # animation()

    global user_ratings
    user_ratings = []
    try:
        for entry in rating_entries.values():
            rating = entry.get()
            if rating == 'Not seen':
                user_ratings.append('Not seen')
            else:
                float_rating = float(rating)
                if 0 <= float_rating <= 5 and float_rating % 0.5 == 0:
                    user_ratings.append(float_rating)
                else:
                    raise ValueError
    except ValueError:
        messagebox.showerror("Input Error!", "Ratings must be between 0 and 5, in 0.5 increments, or 'Not seen'.")
        return
    open_recommendation_page()

def open_recommendation_page():
    # Clear previous entries
    for widget in root.winfo_children():
        widget.destroy()

    # Create scrollable frame
    scrollable_frame = create_scrollable_frame(root)

    # Get recommendations
    genre = genre_var.get()
    num_suggestions = num_suggestions_var.get()
    recommended_movies, mustsee_movies = suggestion(user_ratings, genre, len(user_ratings), num_suggestions)

    # Header
    tk.Label(scrollable_frame, text="Recommended movies for you!", font=("Helvetica", 24, "bold"), fg="darkred", bg="white").pack(pady=(20, 10))
    tk.Label(scrollable_frame, text="Based on your likings and mood:", font=("Helvetica", 20, "bold"), fg="darkred", bg="white").pack(pady=(10, 5))

    # Display Recommendations with Details
    for movie in recommended_movies:
        # Fetch additional details
        movie_info = fetch_movie_info(format_title(movie))  # Format and fetch movie info

        if not movie_info:
            movie_info = {
                'Title': movie,
                'Genres': 'N/A',
                'Length (min)': 'N/A',
                'Director': 'N/A',
                'Actors': 'N/A',
                'Plot': 'No description available.',
                'Poster URL': 'No Image Available',
                'Trailer URL': 'No trailer available'
            }

        # Title
        tk.Label(scrollable_frame, text=movie_info['Title'], font=("Helvetica", 16, "bold"), fg="darkblue", bg="white").pack(pady=(10, 2))

        # Details
        # tk.Label(scrollable_frame, text=f"Genre: {movie_info['Genres']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(scrollable_frame, text=f"Length: {movie_info['Length (min)']} mins", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(scrollable_frame, text=f"Director: {movie_info['Director']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(scrollable_frame, text=f"Actors: {movie_info['Actors']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(scrollable_frame, text=f"Plot: {movie_info['Plot']}", wraplength=500, font=("Helvetica", 14, "italic"), fg="black", bg="white").pack(pady=10)
        
    # Trailer Link
        trailer_url = movie_info['Trailer URL']
        link = tk.Label(scrollable_frame, text="Watch Trailer", font=("Helvetica", 14, "underline"), fg="blue", bg='white', cursor="hand2")
        link.pack(pady=5)
        link.bind("<Button-1>", lambda e, url=trailer_url: webbrowser.open(url))


    # Must-see Movies Section
    must_see_frame = tk.Frame(scrollable_frame, bg='white')
    must_see_frame.pack(pady=(20, 10), padx=10, anchor="center")  # Center-align it

    # Title for must-see section
    tk.Label(must_see_frame, text="And some must-sees!", 
            font=("Helvetica", 20, "bold"), fg='darkred', bg='white').pack(pady=(10, 5))

    for movie in mustsee_movies:
        # Fetch additional details
        movie_info = fetch_movie_info(format_title(movie))  # Format and fetch movie info

        # Title
        tk.Label(must_see_frame, text=movie_info['Title'], font=("Helvetica", 16, "bold"), fg="darkblue", bg="white").pack(pady=(10, 2))

        # Details
        # tk.Label(must_see_frame, text=f"Genre: {movie_info['Genres']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(must_see_frame, text=f"Length: {movie_info['Length (min)']} mins", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(must_see_frame, text=f"Director: {movie_info['Director']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(must_see_frame, text=f"Actors: {movie_info['Actors']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2)
        tk.Label(must_see_frame, text=f"Plot: {movie_info['Plot']}", wraplength=500, font=("Helvetica", 14, "italic"), fg="black", bg="white").pack(pady=5)

        # Trailer Link
        trailer_url = movie_info['Trailer URL']
        link = tk.Label(must_see_frame, text="Watch Trailer", font=("Helvetica", 14, "underline"), fg="blue", bg='white', cursor="hand2")
        link.pack(pady=5)
        link.bind("<Button-1>", lambda e, url=trailer_url: webbrowser.open(url))

    scrollable_frame.update_idletasks()  # Force redraw of all widgets
    scrollable_frame.master.configure(scrollregion=scrollable_frame.master.bbox("all"))


# GUI Window Setup
root = tk.Tk() # we define here the current window, root
root.title("Movie Recommendation System")
root.geometry("600x600") #penso sia una sorta di titolo 
root.configure(bg="white") #configure background

# Starting Page 

# botton_frame = tk.Frame(root, bg="ivory")
# botton_frame.pack(expand=True, fill='both', padx=20, pady=20) #configure background frame 
heading = tk.Label(root, text="Welcome to our new movie reco system!", font=("helvetica", 24, "bold"), fg="darkred", bg="white")
heading.pack(pady=30) #place heading on the frame, with style

start_button = tk.Button(root, text="Snacks ready, let's choose the movie", font=("Helvetica", 17, "bold"),fg="darkred",bg="white",relief="flat",borderwidth=0, command=open_genre_page)
start_button.pack(pady=20)

#global styles 
style_radiobutt = ttk.Style()
style_radiobutt.configure('TRadiobutton', font=('Helvetica', 12))
style_radiobutt.map('TRadiobutton', foreground=[('selected', 'darkred'),('!selected', 'gray')], background=[('selected', 'white'), ('!selected', 'white')])


# Start GUI Main Loop
root.mainloop()