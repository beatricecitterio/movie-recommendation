import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from suggestion_alg import movies_to_rate, suggestion

def open_genre_page():
    # Clear previous entries
    for widget in root.winfo_children():
        widget.destroy() #we clear previous widgets to create the new page

    # First Page - Genre and Number of Ratings Selection
    tk.Label(root, text="Which genre are you in the mood for?",font=("Helvetica", 20), fg="darkred", bg="ivory" ).pack(pady=20) # we add to the root the label select genre, with some space (padding, pady) around it
    global genre_var
    genre_var = tk.StringVar() #create genre var where some input will be stored
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'Any Genre']
    genre_dropdown = ttk.Combobox(root, textvariable=genre_var, values=genres, state='readonly', foreground="darkred") #create pop down list, you say that this is a variable and link it to genre_var (automatically stores the selection of the user)
    genre_dropdown.pack(pady=5)
    genre_dropdown.current(0) #i think here 'Action' will show up, whereas we could add something like empty space or 'select genre' or something else

    # Number of Ratings Selection
    tk.Label(root, text="Choose the number of movies to rate:",font=("Helvetica", 20), fg="darkred", bg="ivory").pack(pady=15) #same logic to create 
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
    tk.Label(root, text="Rate the following movies:", font=("Helvetica", 20), fg="darkred", bg="ivory").pack(pady=(20, 5))
    tk.Label(root, text="(0-5, 0.5 increments, or 'Not seen')", font=("Helvetica", 15), fg="darkred", bg="ivory").pack(pady=(5, 10))

    movies = movies_to_rate(genre, num_ratings) #where do we get the num ratings var?
    for movie in movies:
        tk.Label(root, text=movie, font=("Helvetica", 14), bg="ivory").pack(pady=2)
        entry = tk.Entry(root)
        entry.pack(pady=2)
        rating_entries[movie] = entry

    # Number of Recommendations Selection
    tk.Label(root, text="How many suggestions would you like to get?", font=("Helvetica", 20), fg="darkred", bg="ivory").pack(pady=(15,5))
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

# Move to recommendation page
def open_recommendation_page():
    # Clear previous entries
    for widget in root.winfo_children():
        widget.destroy()

    # Get recommendations using the provided suggestion function
    genre = genre_var.get()
    num_suggestions = num_suggestions_var.get()
    recommended_movies, mustsee_movies = suggestion(user_ratings, genre, len(user_ratings), num_suggestions)

    # Display recommendations
    tk.Label(root, text="Recommended movies for you!", font=("Helvetica", 24, "bold"), fg="darkred", bg="ivory").pack(pady=(20, 10))
    tk.Label(root, text="Based on your likings and mood:", font=("Helvetica", 20, "bold"), fg="darkred", bg="ivory").pack(pady=(10, 5))
    for movie in recommended_movies:
        tk.Label(root, text=movie, font=("Helvetica", 14, "italic"), fg="black", bg="ivory").pack(pady=10)
    tk.Label(root, text="And some must-sees!", font=("Helvetica", 20, "bold"), fg="darkred", bg="ivory").pack(pady=(10, 5))
    for movie in mustsee_movies:
        tk.Label(root, text=movie, font=("Helvetica", 14, "italic"), fg="black", bg="ivory").pack(pady=10)



# GUI Window Setup
root = tk.Tk() # we define here the current window, root
root.title("Movie Recommendation System")
root.geometry("600x600") #penso sia una sorta di titolo 
root.configure(bg="ivory") #configure background

# Starting Page 

# botton_frame = tk.Frame(root, bg="ivory")
# botton_frame.pack(expand=True, fill='both', padx=20, pady=20) #configure background frame 
heading = tk.Label(root, text="Welcome to our new movie reco system!", font=("Impact", 24, "bold"), fg="darkred", bg="Ivory")
heading.pack(pady=30) #place heading on the frame, with style

start_button = tk.Button(root, text="Snacks ready, let's choose the movie", font=("Helvetica", 12),fg="darkred",bg="white",relief="flat",borderwidth=0, command=open_genre_page)
start_button.pack(pady=20)

#global styles 
style_radiobutt = ttk.Style()
style_radiobutt.configure('TRadiobutton', font=('Helvetica', 12))
style_radiobutt.map('TRadiobutton', foreground=[('selected', 'darkred'),('!selected', 'gray')], background=[('selected', 'ivory'), ('!selected', 'ivory')])


# Start GUI Main Loop
root.mainloop()


