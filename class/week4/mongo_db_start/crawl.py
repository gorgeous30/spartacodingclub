from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## 코딩 할 준비 ##
db.movies.update_many({'star': '0'}, {'$set': {'star': '9.38'}})