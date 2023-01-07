import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb
from st_clickable_images import clickable_images

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '6be4e7cd599507ab6b764f0bfe5b22b7'
tmdb.language = 'ko-KR' # 우리나라 기준 데이터 가져오기

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True) # 내림차순 정렬
    sim_scores = sim_scores[1:11] # 자기빼고 10개
    movie_indices = [i[0] for i in sim_scores] # 인덱스 정보 추출
    images = []
    titles = []
    overviews = []
    
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)
        
        # 이미지 없는 경우 빈 이미지 보여주기
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'
            
        images.append(image_path)
        titles.append(details['title'])
        overviews.append(details['overview'])
    
    return images, titles, overviews

movies = pickle.load(open('movies.pickle', 'rb')) 
# wb는 write & 여기는 읽는 거니까 rb
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide') # 화면을 넓게
st.header('NaFlix')

movie_list = movies['title'].values
title = st.selectbox('Choose a Movie you like', movie_list)
if st.button('Recommend'):
    # 진행중 바 만들기
    with st.spinner('Loading ...'):
        images, titles, overviews = get_recommendations(title)
        
        clicked = clickable_images(
            images,
            titles=[f"overview: {overviews[i]}" for i in range(10)],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "300px"},
            key= None
            )
     