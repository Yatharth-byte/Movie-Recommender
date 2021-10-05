import streamlit as st
import pandas as pd
import pickle

data = pd.read_csv('assets/2019.csv')
sim = pickle.load(open('assets/similarity_score.pkl','rb'))

index = pd.Series(data.index,index = (data['movie_title']+' '+data['genres']))
index_ac1 = pd.Series(data.index,index = (data['actor_1_name']))
index_ac2 = pd.Series(data.index,index = (data['actor_2_name']))
index_ac3 = pd.Series(data.index,index = (data['actor_3_name']))

#+ ' ' + data['actor_2_name']+' '+ data['actor_3_name']

# genres_list = ['Animation','Comedy','History','TV','Game-Show','Music',
#                'Film-Noir','Western','Fantasy','Horror','Documentary',
#                'Science','Action','Movie','Crime','Sport','War','Mystery',
#                'Biography','Reality-TV','Drama','Musical','Fiction','Sci-Fi',
#                'Adventure','News','Romance','Short','Family','Thriller']

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
    for i in list_ac:
      if user_iput3 in data['genres'][i]:
        tmp=list(enumerate(sim[index[i]]))
      a=sorted(tmp,key=lambda x: x[1],reverse = True)
      st.write(data['movie_title'].iloc[[j[0] for j in a[1:5]]])
  elif user_iput2 == "sad":
    for i in list_ac:
      if user_iput3 in data['genres'][i]:
        tmp=list(enumerate(sim[index[i]]))
      a=sorted(tmp,key=lambda x: x[1],reverse = True)
      st.write(data['movie_title'].iloc[[j[0] for j in a[1:5]]])
  elif user_iput2 == "anger":
    for i in list_ac:
      if user_iput3 in data['genres'][i]:
        tmp=list(enumerate(sim[index[i]]))
      a=sorted(tmp,key=lambda x: x[1],reverse = True)
      st.write(data['movie_title'].iloc[[j[0] for j in a[1:5]]])
  else:
    for i in list_ac:
      if user_iput3 in data['genres'][i]:
        tmp=list(enumerate(sim[index[i]]))
      a=sorted(tmp,key=lambda x: x[1],reverse = True)
      st.write(data['movie_title'].iloc[[j[0] for j in a[1:5]]])
    

st.title('Movie Recommender based on actors, genre and mood...')
#user_act1,user_act2,user_act3 = "NULL","NULL","NULL"
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
