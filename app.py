from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbsparta_plus_week1

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    all_users = list(db.users.find({}, {'_id': False}))

    id_receive = request.form['id_give']
    password_receive = request.form['password_give']

    # for (): (let i=0;i<all_users.length;i++)랑 비슷하게 가야함.
    #     if (id_receive==all_users['id']) & (password_receive==all_users['password']):
    #         return jsonify({'all_diary': all_users})

@app.route('/signup', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    nickname_receive = request.form['nickname_give']
    password_receive = request.form['password_give']

    doc = {
        'id':id_receive,
        'nickname':nickname_receive,
        'password':password_receive,
    }
    db.users.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)