from crypt import methods
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.wze36.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_plus_week1

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('register.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id':id_receive,
        'pw':pw_hash,
        'nick':nickname_receive
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# GET post(main) page
@app.route('/posts', methods=['GET'])
def post():
    return render_template('main.html')

# GET posts list
@app.route('/posts/list', methods=['GET'])
def main_post():
    post_list = list(db.posts.find({}, {'_id': False})).reverse()
    return jsonify({'msg': post_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)