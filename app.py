from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)
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

@app.route('/login', methods=['POST'])
def login():
    all_users = list(db.users.find({}, {'_id': False}))

    id_receive = request.form['id_give']
    password_receive = request.form['password_give']

    # for (): (let i=0;i<all_users.length;i++)랑 비슷하게 가야함.
    #     if (id_receive==all_users['id']) & (password_receive==all_users['password']):
    #         return jsonify({'all_diary': all_users})


@app.route('/post/register')
def post_page():
    id_receive = request.form['id_give']

    return render_template('index.html')

@app.route('/post/register', methods=['POST'])
def post():
    title_receive = request.form['title_give']
    img_receive = request.form['image_give']
    content_receive = request.form['content_give']
    participants_receive = request.form['participants_give']
    post_receive = request.form['postnum_give']

    doc = {
        'title':title_receive,
        'image':img_receive,
        'content':content_receive,
        'participants': participants_receive,
        'postnum': post_receive,
    }
    db.posts.insert_one(doc)

    return jsonify({'msg': '등록완료!'})

@app.route('/post/edit')
def post_for_edit():
    id_receive = request.form['id_give']

    return render_template('index.html')

@app.route('/post/edit', methods=['POST'])
def post_edit():
    title_receive = request.form['title_give']
    img_receive = request.form['image_give']
    content_receive = request.form['content_give']
    participants_receive = request.form['participants_give']
    post_receive = request.form['postnum_give']

    doc = {
        'title': title_receive,
        'image': img_receive,
        'content': content_receive,
        'participants': participants_receive,
    }
    db.posts.update_one({'postnum':post_receive}, {'$set':doc})

    return jsonify({'msg': '수정 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)