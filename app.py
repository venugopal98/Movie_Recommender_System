# import necessary libraries
import pickle
import streamlit as st
import pandas as pd
from PIL import Image


import requests

# load movies and similarity

temp_movies = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(temp_movies)

similarity  = pickle.load(open('similarity.pkl','rb'))

# set page title and favicon
st.set_page_config(page_title='Recommender System', page_icon = ':clapper:', layout = 'wide', initial_sidebar_state = 'auto')

# set title of webpage
st.title("Movie Recommender System")
st.text("A web app which suggests five other similar movies for a particular movie selected.")

# user input for target movie
movie = st.selectbox(
    "Please select a movie",movies['title']
)
suggest = st.button('Suggest movies')

def recommend_movies(movie):
    movie_inx = movies[movies['title'] == movie].index[0]
    similar_movies = similarity[movie_inx]
    list_of_movies = sorted(list(enumerate(similar_movies)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_info = []

    for i in list_of_movies:
        recommended_movies.append(movies.iloc[i[0]])
        print(movies.iloc[i[0]])
        data = requests.get(
            f'https://api.themoviedb.org/3/movie/{movies.iloc[i[0]].id}?api_key=').json()
        print(data["tagline"])
        print('............................................')
        recommended_movies_info.append(data['tagline'])
        print(recommended_movies_info)
        poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        recommended_movies_posters.append(poster_path)


    return recommended_movies,recommended_movies_posters,recommended_movies_info

try :
    if suggest:
        movie_names,movie_posters,movie_info = recommend_movies(movie)
        print(".......................................00")
        print(movie_info)
        movie1,movie2,movie3,movie4,movie5 = st.beta_columns(5)


        movie1.image(movie_posters[0])
        movie1.subheader(movie_names[0].title)
        movie1.markdown(movie_info[0])



        movie2.image(movie_posters[1])
        movie2.subheader(movie_names[1].title)
        movie2.markdown(movie_info[1])


        movie3.image(movie_posters[2])
        movie3.subheader(movie_names[2].title)
        movie3.markdown(movie_info[2])


        movie4.image(movie_posters[3])
        movie4.subheader(movie_names[3].title)
        movie4.markdown(movie_info[3])


        movie5.image(movie_posters[4])
        movie5.subheader(movie_names[4].title)
        movie5.markdown(movie_info[4])
except:
    print('Exception occured while suggesting a movie')
