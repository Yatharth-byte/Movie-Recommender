from PIL import Image
import requests,io
import json
import streamlit as st
import PIL.Image
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import pickle

data = pd.read_csv('/content/drive/MyDrive/Major Project/2019.csv')
sim = pickle.load(open('/content/drive/MyDrive/Major Project/similarity_score.pkl','rb'))
with open('/content/drive/MyDrive/Major Project/movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
tmp = []
sim_movie_list=[]
movie_link_dic = {}
for i in range(len(movie_titles)):
  movie_link_dic[movie_titles[i][0]] = movie_titles[i][2]
index = pd.Series(data.index,index = (data['movie_title']+' '+data['genres']))
index_ac1 = pd.Series(data.index,index = (data['actor_1_name']))
index_ac2 = pd.Series(data.index,index = (data['actor_2_name']))
index_ac3 = pd.Series(data.index,index = (data['actor_3_name']))

genres_happy = ['Animation','Comedy','History','TV','Game-Show','Music',
                'Film-Noir','Western','Fantasy','Horror','Documentary',
                'Science','Action','Movie','Crime','Sport','War','Mystery',
                'Biography','Reality-TV','Drama','Musical','Fiction','Sci-Fi',
                'Adventure','News','Romance','Short','Family','Thriller']
genres_sad = ['Comedy','Game-Show','Music','Fantasy','Action','Sport','Musical',
              'Adventure','Thriller']
genres_anger = ['Comedy','Game-Show','Music','Fantasy','Musical','Adventure',
                'Thriller','Fiction','Romance','Family']
genres_disgust = ['Family','Animation','Biography','Drama','Sport','Fiction',
                  'Sci-Fi','Documentary','Science','Action','Movie']

def fetch_movie_poster(imdb_link):
    url_data = requests.get(imdb_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_dp = s_data.find("meta", property="og:image")
    imdb_title = s_data.find('meta', property='og:title')
    movie_poster_link = imdb_dp.attrs['content']
    movie_name = imdb_title.attrs['content']
    movie_name = movie_name.replace(' - IMDb','')
    u = urlopen(movie_poster_link)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    image = image.resize((250, 400), )
    return image,movie_name

def index_model_for_movies(actor_movie_index,genre_selected):
  global tmp
  global sim_movie_list
  for i in actor_movie_index:
    if genre_selected in data['genres'][i]:
      tmp=list(enumerate(sim[index[i]]))
    sim_movie_list.extend(sorted(tmp,key=lambda x: x[1],reverse = True))
  return list(set(sim_movie_list))

def recommend(iact1,iput2,iput3):
  try:
    list_ac1 = list(index_ac1[iact1])
  except:
    list_ac1 = []
  try:
    list_ac2 = list(index_ac2[iact1])
  except:
    list_ac2 = []
  try:
    list_ac3 = list(index_ac3[iact1])
  except:
    list_ac3 = []

  if list_ac1:
    list_ac = list_ac1
  elif list_ac2:
    list_ac = list_ac2
  else:
    list_ac = list_ac3
  
  if user_iput2 == "happy":
    list_of_tuples = index_model_for_movies(list_ac,user_iput3)
  elif user_iput2 == "sad":
    list_of_tuples = index_model_for_movies(list_ac,user_iput3)
  elif user_iput2 == "anger":
    list_of_tuples = index_model_for_movies(list_ac,user_iput3)
  else:
    list_of_tuples = index_model_for_movies(list_ac,user_iput3)
  
  results_len = len(list_of_tuples)
  iter_movie = iter(data['movie_title'].iloc[[j[0] for j in list_of_tuples[:10]]])

  img_list = []
  img_name_list = []
  if results_len >= 10:
    for _ in range(10):
      try:
        tmp = fetch_movie_poster(movie_link_dic[next(iter_movie)])
        img_list.append(tmp[0])
        img_name_list.append(tmp[1])
      except:
        pass
  elif results_len >=5:
    for _ in range(5):
      try:
        tmp = fetch_movie_poster(movie_link_dic[next(iter_movie)])
        img_list.append(tmp[0])
        img_name_list.append(tmp[1])
      except:
        pass
  else:
    for _ in range(3):
      try:
        tmp = fetch_movie_poster(movie_link_dic[next(iter_movie)])
        img_list.append(tmp[0])
        img_name_list.append(tmp[1])
      except:
        pass
  st.image(img_list,width = 250,caption=img_name_list)

st.title('Movie Recommender based on actors, genre and mood...')
content = st.expander("Read Me First!!!")
content.write("This is a Movie Recommender System based on your choice of ACTOR, GENRE and MOOD.")
content.write("---------------------------------------------------------------------------------")
content.write("Movies are upto 2019 year only and even among them not all movies may be present")
content.write("================================================================================")
content.write("Select ACTOR from the drop down menu -OR- click on it and start typing.")
content.write("Select MOOD which further narrows Genre list accordingly...")
content.write("For GENRE happy, since the person is happy, he/she can see movies from all genre.")
content.write("For GENRE sad/anger/disgust, appropriate genres are automatically filtered from menu to select.")
content.write("Press View to see your choices")
content.write("")

st.header('Actor?')
user_act1 = st.selectbox('',set(data['actor_1_name'].append(data['actor_2_name'].append(data['actor_3_name']))))


st.header('What is your mood?')
user_iput2 = st.selectbox('',["happy","sad","anger","disgust"])

if user_iput2 == "happy":
  st.header('Genre?')
  user_iput3 = st.selectbox('',genres_happy)
elif user_iput2 == "sad":
  st.header('Genre?')
  user_iput3 = st.selectbox('',genres_sad)
elif user_iput2 == "anger":
  st.header('Genre?')
  user_iput3 = st.selectbox('',genres_anger)
else:
  st.header('Genre?')
  user_iput3 = st.selectbox('',genres_disgust)

if st.button('View'):
    st.write("You Chose:",user_act1)
    st.write("Mood:",user_iput2)
    st.write("Genre:",user_iput3)

recommend(user_act1,user_iput2,user_iput3)
