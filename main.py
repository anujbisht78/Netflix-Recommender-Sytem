from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

# Load model variables
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Fetch movie poster function
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7543524441a260664a97044b8e2dc621&language=en-US".format(movie_id)  # Replace YOUR_API_KEY with your actual API key
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Recommend movies function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_poster = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_poster

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_movie = request.form['selected_movie']
        recommendations, posters = recommend(selected_movie)
        # Zip recommendations and posters
        movie_data = zip(recommendations, posters)
        return render_template('index.html', movies=movies, movie_data=movie_data, selected_movie=selected_movie)
    return render_template('index.html', movies=movies, movie_data=None, selected_movie=None)

if __name__ == '__main__':
    app.run(debug=True)
