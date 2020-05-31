from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('homestudy.html')

@app.route('/mypage')
def mypage():
   return '여기는 my page입니다'

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)
