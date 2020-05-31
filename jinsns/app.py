from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/feed', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    feeds = list(db.feeds.find({}, {'_id': False}))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'feeds':feeds})

## API 역할을 하는 부분
@app.route('/feed', methods=['POST'])
def posting():
        # 1. 클라이언트 데이터 받기
        content_receive = request.form['content_give']
        date_receive = request.form['date_give']
        like_receive = request.form['like_give']

        # 2. DB에 정보 저장 : content, date
        doc = {
            'content': content_receive,
            'date': date_receive,
            'like': like_receive,
        }
        db.feeds.insert_one(doc)

        return jsonify({'result': 'success'})

@app.route('/api/like', methods=['POST'])
def feed_like():
    # 1. 클라이언트가 전달한 date_give를 date_receive 변수에 넣습니다.
    date_receive = request.form['date_give']
    # 2. feeds 목록에서 find_one으로 date가 date_receive와 일치하는 feed를 찾습니다.
    feed = db.feeds.find_one({'date': date_receive})
    # 3. feed의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = int(feed['like']) + 1
    # 4. feeds 목록에서 date가 date_receive인 문서의 like 를 new_like로 변경합니다.
    db.feeds.update_one({'date': date_receive}, {'$set': {'like': new_like}})
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': 'Thank you😍'})

@app.route('/api/delete', methods=['POST'])
def feed_delete():
    # 1. 클라이언트가 전달한 date_give를 date_receive 변수에 넣습니다.
    date_receive = request.form['date_give']
    # 2. feeds 목록에서 delete_one으로 date가 date_receive와 일치하는 feed를 제거합니다.
    db.feeds.delete_one({'date': date_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success','msg':'Deleted'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)