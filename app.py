from crypt import methods
import hashlib, jwt, datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta99@cluster0.0ngea.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
# client = MongoClient('mongodb+srv://test:sparta@cluster0.wze36.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta_plus_week1

import certifi
ca = certifi.where()

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt
import hashlib

SECRET_KEY = 'SPARTA'

#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.miniproject.find_one({"id": payload['id']})
    #     return render_template('login.html', nickname = user_info['nick'])
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg = "로그인 시간이 만료됐습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg= " 로그인 정보가 존재하지 않습니다."))
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
def post_main():
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.miniproject.find_one({"id": payload['id']})
    #     return render_template('login.html', nickname = user_info['nick'])
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg = "로그인 시간이 만료됐습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg= " 로그인 정보가 존재하지 않습니다."))
    return render_template('main.html')

# GET posts list
@app.route('/posts/list', methods=['GET'])
def main_post():
    post_list = list(db.posts.find({}, {'_id': False})).reverse()
    return jsonify({'msg': post_list})

# GET posts detail
@app.route('/posts/detail')
def detail():
    return render_template('postDetail.html')

# GET /posts/detail
@app.route('/posts/detail', methods=['GET'])
def post_detail():
    post_list = list(db.posts.find({}, {'_id': False})).reverse()
    return jsonify({'data': post_list})


@app.route("/login", methods = ["POST"])
def login_page():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    #id, 암호화된 pw를 가지고 해당 유저를 찾습니다.
    result = db.users.find_one({'id': id_receive, 'pw':pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
        # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/post/register')
def post_page():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('register.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login.html", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/post/register', methods=['POST'])
def post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('register.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login.html", msg="로그인 정보가 존재하지 않습니다."))

    title_receive = request.form['title_give']
    img_receive = request.form['image_give']
    content_receive = request.form['content_give']
    participants_receive = request.form['participants_give']
    # post_receive = request.form['postnum_give']
    date_receive = request.form["date_give"]

    doc = {
        'id': user_info['id'],
        'nick': user_info['nick'],
        'title':title_receive,
        'image':img_receive,
        'content':content_receive,
        'participants': participants_receive,
       # 'postnum': post_receive,
        'date': date_receive
    }
    db.posts.insert_one(doc)

    return jsonify({'msg': '등록완료!'})

@app.route('/post/edit')
def post_for_edit():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('edit.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login.html", msg="로그인 정보가 존재하지 않습니다."))

    return render_template('index.html')

@app.route('/post/edit', methods=['POST'])
def post_edit():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('edit.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login.html", msg="로그인 정보가 존재하지 않습니다."))

    title_receive = request.form['title_give']
    img_receive = request.form['image_give']
    content_receive = request.form['content_give']
    participants_receive = request.form['participants_give']

    doc = {
        'title': title_receive,
        'image': img_receive,
        'content': content_receive,
        'participants': participants_receive,
    }
    db.posts.update_one({'title_receive':title_give}, {'$set':doc})

    return jsonify({'msg': '수정 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
