# flask 웹 프레임워크 로드
from flask import Flask, render_template, url_for

# database 안에 있는 MyDB class  로드
from static.python.database import MyDB
# Flask class 생성
app = Flask(__name__)

from dotenv import load_dotenv
import os
# env 로드
load_dotenv()

# MyDB class 생성
mydb = MyDB(
    os.getenv('host'),
    os.getenv('port'),
    os.getenv('user'),
    os.getenv('password'),
    os.getenv('db_name')
)


# localhost:5000/ api를 생성하여 img_slide.html을 되돌려주는 함수 생성
@app.route('/')
def slide():
    return render_template('img_slide.html')




# 웹서버를 실행
app.run(debug=True)