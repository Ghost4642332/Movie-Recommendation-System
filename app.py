import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def generate_google_search_url(query):
    """
    Generates a Google search URL for the given query.
    """
    encoded_query = requests.utils.quote(query+ " movie")   # Encode the query for URL
    google_url = f"https://www.google.com/search?q={encoded_query}"
    return google_url

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit app header
st.header('Movie Recommender System')

# Load movie data and similarity matrix
with open('movies_dict.pkl', 'rb') as file:
    movies = pickle.load(file)
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Display each recommended movie with a clickable poster
    for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        with eval(f"col{i+1}"):  # Dynamically select the column
            st.text(name)
            # Create a clickable image that redirects to Google search
            google_url = generate_google_search_url(name)
            st.markdown(
                f'<a href="{google_url}" target="_blank">'
                f'<img src="{poster}" width="100%">'
                '</a>',
                unsafe_allow_html=True
            )