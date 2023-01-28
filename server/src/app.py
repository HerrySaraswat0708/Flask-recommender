from flask import Flask,render_template,redirect,Response,request
import requests
import joblib
from flask_fontawesome import FontAwesome
import random 
import math
with open('movies.joblib','rb') as f:
    movies=joblib.load(f) 
with open('similarity.joblib','rb') as f:
    similarity=joblib.load(f) 


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3136368ff79fd8b05a0b46aa15630807&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    


def fetch_tag(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3136368ff79fd8b05a0b46aa15630807&language=en-US'.format(movie_id))
    data = response.json()
    return data['tagline']
   
    
def fetch_rating(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3136368ff79fd8b05a0b46aa15630807&language=en-US'.format(movie_id))
    data = response.json()
    return data['vote_average']
    

poster_before=[]
tag_before=[]
rating_before=[]
index_before=[]

for i in range(0,9):
    index=math.ceil(random.random()*10)
    movie_index=movies.iloc[index].movie_id
    movies_list = sorted(enumerate(similarity[38]),reverse=True,key=lambda x:x[1])[1:10]
for i in movies_list:
    poster_before.append(fetch_poster(movies.iloc[i[0]].movie_id))
    tag_before.append(fetch_tag(movies.iloc[i[0]].movie_id))
    rating_before.append(fetch_rating(movies.iloc[i[0]].movie_id))
    index_before.append(i[0])

app = Flask(__name__)
fa=FontAwesome(app)
@app.route('/', methods=['GET','POST'])
def home():
    movie_lst=[]
    poster=[]
    indexes=[]
    tag=[]
    rating=[]
    if request.method=='POST':
        movie=request.form['movie']
        index=movies[movies['title']==movie].index[0]
        distances = similarity[index]
        movie_lst = sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:11]
        for i in movie_lst:
            poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
            tag.append(fetch_tag(movies.iloc[i[0]].movie_id))
            rating.append(fetch_rating(movies.iloc[i[0]].movie_id))
            indexes.append(i[0])
            print(rating)
        
    return render_template('home.html',movies=movies['title'],indexes=indexes,path=poster,tag=tag,rating=rating,index_before=index_before,tag_before=tag_before,rating_before=rating_before,poster_before=poster_before)

@app.route('/about')
def about():
    return render_template('about.html')



if __name__=="__main__":
    app.run(debug=True)