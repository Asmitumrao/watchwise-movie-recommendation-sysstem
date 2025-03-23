import pickle
import streamlit as st
import requests


def fetch_poster_by_name_omdb(movie_name):
    api_key='21a3b8c6'
    search_url = "http://www.omdbapi.com/"
    params = {"apikey": api_key, "t": movie_name}
    
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        poster_url = data.get("Poster")
        return poster_url or "Poster not available."
    else:
        return f"Error: {response.status_code} - {response.text}"

def fetch_tmdb_poster(movie_id):
    # TMDB movie details endpoint
    api_key='8265bd1679663a7ea12ac168da84d2e8'
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": api_key}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            # Construct full poster URL
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return poster_url

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        # recommended_movie_posters.append(fetch_poster(movie_id))
        name=movies.iloc[i[0]].title
        # recommended_movie_posters.append(fetch_tmdb_poster(movie_id))
        recommended_movie_posters.append(fetch_poster_by_name_omdb(name))
        recommended_movie_names.append(name)
    # st.write(recommended_movie_names)
    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    # st.write(selected_movie)
    # recommend(selected_movie)

    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    # col1, col2, col3, col4, col5 = st.beta_columns(5)
    # with col1:
    #     st.text(recommended_movie_names[0])
    #     st.image(recommended_movie_posters[0])
    # with col2:
    #     st.text(recommended_movie_names[1])
    #     st.image(recommended_movie_posters[1])

    # with col3:
    #     st.text(recommended_movie_names[2])
    #     st.image(recommended_movie_posters[2])
    # with col4:
    #     st.text(recommended_movie_names[3])
    #     st.image(recommended_movie_posters[3])  
    # with col5:
    #     st.text(recommended_movie_names[4])
    #     st.image(recommended_movie_posters[4])

    col1, col2, col3, col4, col5 = st.columns(5)

    # Populate each column with a movie name and poster
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])





