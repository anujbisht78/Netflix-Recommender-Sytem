import streamlit as st 
import pickle
import pandas as pd
import requests

#fetch poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

similarity=pickle.load(open('similarity.pkl','rb'))


import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
    ]
imageCarouselComponent(imageUrls=imageUrls, height=200)

#for giving the names of the movie
def recommend(movie):
    movie_index= movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_poster=[]
    
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        
        #fetching the movies poster from API
        recommended_poster.append(fetch_poster(movie_id))
        
    # giving 5 movies     
    return recommended_movies,recommended_poster

# """Dataframe cant pickled"""
# movie_list = pickle.load(open('movies.pkl','rb'))
# movie_list=movie_list['title'].values

# """Movies Dictonary"""
movie_dict = pickle.load(open('movies_dict.pkl','rb'))
#converting into DataFrame
movies=pd.DataFrame(movie_dict)

st.title('Movie Recommender System')

#Adding a select Box
selected_movie = st.selectbox(
    'Select or Type a Movie Name',
    movies['title'].values,index=None,placeholder="Select a Movie Name")


if st.button('Show Recommendation'):
    (names,posters)=recommend(selected_movie)
    st.write('You selected:', selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    