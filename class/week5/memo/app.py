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

@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    memos = list(db.memos.find({}, {'_id': False}))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'memos':memos})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def posting():
        # 1. 클라이언트 데이터 받기
        url_receive = request.form['url_give']
        comment_receive = request.form['comment_give']

        # 2. meta tag 크롤링
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        og_title = soup.select_one('meta[property="og:title"]')
        og_image = soup.select_one('meta[property="og:image"]')
        og_description = soup.select_one('meta[property="og:description"]')

        title = og_title["content"]
        image = og_image["content"]
        desc = og_description["content"]

        # 3. DB에 정보 저장 : url, title, image, desc, comment
        doc = {
            'title': title,
            'image': image,
            'desc': desc,
            'comment': comment_receive,
            'url': url_receive
        }
        db.memos.insert_one(doc)

        return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)