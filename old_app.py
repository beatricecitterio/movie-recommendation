from tmdb_api import fetch_movie_info
from suggestion_alg import format_title, movies_to_rate, suggestion
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

def create_scrollable_frame(root):
    canvas = tk.Canvas(root, bg="white", bd=0, highlightthickness=0)
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
    for widget in root.winfo_children():
        widget.destroy() 

    # GENRE SELECTION
    tk.Label(root, text="Which genre are you in the mood for?",font=("Helvetica", 20, 'bold'), fg="darkred", bg="white" ).pack(pady=20) 
    global genre_var
    genre_var = tk.StringVar() 
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 
              'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    genre_dropdown = ttk.Combobox(root, textvariable=genre_var, values=genres, state='readonly', foreground="darkred") 
    genre_dropdown.pack(pady=5)
    genre_dropdown.current(0) 

    # NUMBER OF RATINGS SELECTION
    tk.Label(root, text="Choose the number of movies to rate:",font=("Helvetica", 16, 'bold'), fg="darkred", bg="white").pack(pady=15) 
    global num_ratings_var
    num_ratings_var = tk.IntVar()
    num_ratings_var.set(5) 
    ttk.Radiobutton(root, text="5", variable=num_ratings_var, value=5, style="TRadiobutton").pack(pady=5)
    ttk.Radiobutton(root, text="10", variable=num_ratings_var, value=10, style="TRadiobutton").pack(pady=5)

    # NEXT BUTTON
    tk.Button(root, text="Next", command=open_rating_page, relief="flat").pack(pady=20) 
    return num_ratings_var, genre_var

def open_rating_page():
    genre = genre_var.get()
    num_ratings = num_ratings_var.get()

    for widget in root.winfo_children():
        widget.destroy()

    # Create scrollable frame
    scrollable_frame = create_scrollable_frame(root)

    # MOVIE RATINGS INPUT
    global rating_entries
    rating_entries = {}
    tk.Label(scrollable_frame, text="Rate the following movies:", font=("Helvetica", 20, 'bold'), fg="darkred", bg="white").pack(pady=(20, 5))
    tk.Label(scrollable_frame, text="Select a rating from 0 to 5 stars, or choose 'Not seen'", font=("Helvetica", 15), fg="darkred", bg="white").pack(pady=(5, 10))

    def create_star_selector(parent, movie):
        rating_var = tk.StringVar(value="Not seen")
        star_frame = tk.Frame(parent, bg="white")
        star_frame.pack(pady=(5, 5))

        def set_rating(value):
            rating_var.set(value)
            highlight_stars(star_frame, value)

        def highlight_stars(frame, value):
            for idx, widget in enumerate(frame.winfo_children()):
                if isinstance(widget, tk.Button):
                    if isinstance(value, int): 
                        if widget.cget('text') == 'Not seen':
                            widget.config(bg="white", fg="black")  
                        else:
                            widget.config(fg="gold" if idx < value else "gray")  
                    if widget.cget('text') == 'Not seen' and value == 'Not seen':
                        widget.config(bg="gold", fg="darkred")  
                    elif widget.cget('text') == 'Not seen':
                        widget.config(bg="white", fg="black")  


        for i in range(1, 6):
            star_button = tk.Button(star_frame, text="★", font=("Helvetica", 14), fg="gray", bg="white", relief="flat")
            star_button.config(command=lambda val=i: set_rating(val))
            star_button.pack(side="left", padx=2)

        not_seen_button = tk.Button(star_frame, text="Not seen", font=("Helvetica", 12), fg="black", bg="white", relief="flat")
        not_seen_button.config(command=lambda: set_rating("Not seen"))
        not_seen_button.pack(side="left", padx=(10, 2))

        rating_entries[movie] = rating_var

    movies = movies_to_rate(genre, num_ratings)
    for movie in movies:
        movie_frame = tk.Frame(scrollable_frame, bg="white")
        movie_frame.pack(pady=20, padx=10, anchor='center')

        movie_info = fetch_movie_info(format_title(movie))
        poster_url = movie_info.get('Poster URL', 'No Image Available')

        tk.Label(movie_frame, text=movie, font=("Helvetica", 14, 'bold'), bg="white", fg="black").pack(pady=(0, 5))

        try:
            response = requests.get(poster_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((80, 120), Image.Resampling.LANCZOS)
            poster_img = ImageTk.PhotoImage(img)
            poster_label = tk.Label(movie_frame, image=poster_img, bg='white')
            poster_label.image = poster_img
            poster_label.pack(pady=(0, 5))
        except:
            tk.Label(movie_frame, text="No Image", bg="white", fg="black").pack(pady=(0, 5))

        create_star_selector(movie_frame, movie)

        movie_search_query = "+".join(movie.split())
        tmdb_url = f"https://www.themoviedb.org/search?query={movie_search_query}"
        link = tk.Label(movie_frame, text="More info here", font=("Helvetica", 12, "underline"), fg="blue", bg="white", cursor="hand2")
        link.pack(pady=(5, 5))
        link.bind("<Button-1>", lambda e, url=tmdb_url: webbrowser.open(url))

    # SELECTION OF NUMBER OF SUGGESTIONS
    tk.Label(scrollable_frame, text="How many suggestions would you like to get?", font=("Helvetica", 16, 'bold'), fg="darkred", bg="white").pack(pady=(15,5))
    global num_suggestions_var
    num_suggestions_var = tk.IntVar()
    num_suggestions_var.set(3)
    ttk.Radiobutton(scrollable_frame, text="1", variable=num_suggestions_var, value=1, style="TRadiobutton").pack()
    ttk.Radiobutton(scrollable_frame, text="3", variable=num_suggestions_var, value=3, style="TRadiobutton").pack()
    ttk.Radiobutton(scrollable_frame, text="5", variable=num_suggestions_var, value=5, style="TRadiobutton").pack()

    # NEXT BUTTON
    tk.Button(scrollable_frame, text="Next", command=process_ratings, relief="flat").pack(pady=20)


def show_loading_gif():
    global gif_label, frames

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Wait for it...", font=("Helvetica", 24, 'bold'), fg="darkblue", bg="white").pack(pady=20)

    gif_label = tk.Label(root, bg="white")
    gif_label.pack(pady=20)

    gif_path = "static/loading.gif"  
    gif = Image.open(gif_path)

    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(gif)
            frames.append(frame)
            gif.seek(len(frames)) 
    except EOFError:
        pass 

    def update(index):
        if gif_label.winfo_exists(): 
            frame = frames[index]
            gif_label.config(image=frame)
            index = (index + 1) % len(frames)
            root.after(100, update, index)  

    update(0)  

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

    show_loading_gif()

    root.after(3000, open_recommendation_page)  

def open_recommendation_page():
    for widget in root.winfo_children():
        widget.destroy()

    scrollable_frame = create_scrollable_frame(root)

    genre = genre_var.get()
    num_suggestions = num_suggestions_var.get()
    recommended_movies, mustsee_movies = suggestion(user_ratings, genre, len(user_ratings), num_suggestions)

    # HEADER
    tk.Label(scrollable_frame, text="Recommended movies for you!", font=("Helvetica", 24, "bold"), fg="darkred", bg="white", anchor="w", justify="left").pack(pady=(20, 10), anchor='w')
    tk.Label(scrollable_frame, text="Based on your likings and mood:", font=("Helvetica", 20, "bold"), fg="darkred", bg="white", anchor="w", justify="left").pack(pady=(10, 5), anchor='w')

    def create_star_rating(parent, avg_rating):
        full_stars = round(avg_rating)
        empty_stars = 5 - full_stars

        for _ in range(full_stars):
            tk.Label(parent, text="★", font=("Helvetica", 14), fg="gold", bg="white").pack(side="left")
        for _ in range(empty_stars):
            tk.Label(parent, text="☆", font=("Helvetica", 14), fg="gold", bg="white").pack(side="left")

    # RECOMMENDATIONS
    for movie, avg_rating in recommended_movies:
        movie_info = fetch_movie_info(format_title(movie))

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

        movie_frame = tk.Frame(scrollable_frame, bg='white')
        movie_frame.pack(pady=10, padx=10, anchor='w', fill='x')

        details_frame = tk.Frame(movie_frame, bg='white', height=200)
        details_frame.grid(row=0, column=1, sticky='w')

        tk.Label(details_frame, text=movie_info['Title'], font=("Helvetica", 16, "bold"), fg="darkblue", bg="white").pack(pady=(10, 2), anchor='w')
        rating_frame = tk.Frame(details_frame, bg="white")
        rating_frame.pack(pady=2, anchor='w')
        create_star_rating(rating_frame, avg_rating)
        tk.Label(details_frame, text=f"Length: {movie_info['Length (min)']} mins", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2, anchor='w')
        tk.Label(details_frame, text=f"Director: {movie_info['Director']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2, anchor='w')
        tk.Label(details_frame, text=f"Actors: {movie_info['Actors']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2, anchor='w')
        tk.Label(details_frame, text=f"Plot: {movie_info['Plot']}", wraplength=500, font=("Helvetica", 14, "italic"), fg="black", bg="white").pack(pady=5, anchor='w')
        
        # TRAILER
        trailer_url = movie_info['Trailer URL']
        link = tk.Label(details_frame, text="Watch Trailer", font=("Helvetica", 14, "underline"), fg="blue", bg='white', cursor="hand2")
        link.pack(pady=5, anchor='w')
        link.bind("<Button-1>", lambda e, url=trailer_url: webbrowser.open(url))

        # POSTER
        poster_url = movie_info['Poster URL']
        try:
            response = requests.get(poster_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((150, 200), Image.Resampling.LANCZOS)
            poster_img = ImageTk.PhotoImage(img)
            poster_label = tk.Label(movie_frame, image=poster_img, bg='white')
            poster_label.image = poster_img
            poster_label.grid(row=0, column=0, padx=10, sticky='w')
        except:
            pass

    # MUST SEE RECOMMENDATIONS
    must_see_frame = tk.Frame(scrollable_frame, bg='white')
    must_see_frame.pack(pady=(20, 10), padx=10, anchor="w", fill='x')

    # HEADER
    tk.Label(must_see_frame, text="And some must-sees!", 
            font=("Helvetica", 20, "bold"), fg='darkred', bg='white', anchor='w', justify='left').pack(pady=(10, 5), anchor='w')

    for movie, avg_rating in mustsee_movies:
        movie_info = fetch_movie_info(format_title(movie))

        movie_frame = tk.Frame(must_see_frame, bg='white')
        movie_frame.pack(pady=10, padx=10, anchor='w', fill='x')

        details_frame = tk.Frame(movie_frame, bg='white', height=200)
        details_frame.grid(row=0, column=1, sticky='w')

        tk.Label(details_frame, text=movie_info['Title'], font=("Helvetica", 16, "bold"), fg="darkblue", bg="white").pack(pady=(10, 2), anchor='w')
        rating_frame = tk.Frame(details_frame, bg="white")
        rating_frame.pack(pady=2, anchor='w')
        create_star_rating(rating_frame, avg_rating)
        tk.Label(details_frame, text=f"Length: {movie_info['Length (min)']} mins", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2, anchor='w')
        tk.Label(details_frame, text=f"Director: {movie_info['Director']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2, anchor='w')
        tk.Label(details_frame, text=f"Actors: {movie_info['Actors']}", font=("Helvetica", 14), fg="black", bg="white").pack(pady=2, anchor='w')
        tk.Label(details_frame, text=f"Plot: {movie_info['Plot']}", wraplength=500, font=("Helvetica", 14, "italic"), fg="black", bg="white").pack(pady=5, anchor='w')
        
        # TRAILER
        trailer_url = movie_info['Trailer URL']
        link = tk.Label(details_frame, text="Watch Trailer", font=("Helvetica", 14, "underline"), fg="blue", bg='white', cursor="hand2")
        link.pack(pady=5, anchor='w')
        link.bind("<Button-1>", lambda e, url=trailer_url: webbrowser.open(url))

        # POSTER
        poster_url = movie_info['Poster URL']
        try:
            response = requests.get(poster_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((150, 200), Image.Resampling.LANCZOS)
            poster_img = ImageTk.PhotoImage(img)
            poster_label = tk.Label(movie_frame, image=poster_img, bg='white')
            poster_label.image = poster_img
            poster_label.grid(row=0, column=0, padx=10, sticky='w')
        except:
            pass


    scrollable_frame.update_idletasks()
    scrollable_frame.master.configure(scrollregion=scrollable_frame.master.bbox("all"))


# GUI SETUP
root = tk.Tk() 
root.title("Movie Recommendation System")
root.geometry("600x600") 
root.configure(bg="white") 

# WELCOME PAGE
heading = tk.Label(root, text="Welcome to our movie recommendation system!", font=("helvetica", 24, "bold"), fg="darkred", bg="white")
heading.pack(pady=30) 

gif_path = "static/cinema.gif"  
gif = Image.open(gif_path)

frames = []
try:
    while True:
        frame = ImageTk.PhotoImage(gif)
        frames.append(frame)
        gif.seek(len(frames))  
except EOFError:
    pass 

gif_label = tk.Label(root, bg="white")
gif_label.pack(pady=10)

def update(index):
    if gif_label.winfo_exists(): 
        frame = frames[index]
        gif_label.config(image=frame)
        index = (index + 1) % len(frames)
        root.after(100, update, index) 

update(0) 

# START BUTTON
start_button = tk.Button(root, text="Snacks ready, let's choose the movie", font=("Helvetica", 16, "bold"),fg="darkblue",bg="white",relief="flat",borderwidth=0, command=open_genre_page)
start_button.pack(pady=20)

# GLOBAL STYLES
style_radiobutt = ttk.Style()
style_radiobutt.configure('TRadiobutton', font=('Helvetica', 12))
style_radiobutt.map('TRadiobutton', foreground=[('selected', 'darkred'),('!selected', 'gray')], background=[('selected', 'white'), ('!selected', 'white')])

root.mainloop()