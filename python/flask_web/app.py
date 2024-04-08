## 기본적인 웹서버 설정
# flask 웹프레임워크를 로드
from flask import Flask 

## Flask라는 Class 생성 
# 생성자 함수의 필수 인자 : 파일의 이름(app.py) 
## __name__ : 현재 파일의 이름 
app = Flask(__name__)


## 프롬프트에서 cd C:\Users\Jws\Documents\ubion\python\flask_web (flask_web 우클릭 copy path)
# > dir
# > python app.py
# Ctrl + C로 서버 닫기

## 주소를 생성(api생성) -> 식당에서 메뉴를 만든다.  # router 설명  
# localhost : 5000/ 요청시 index 함수를 호출 
@app.route('/')                   # 아래로 연결 
def index():
    return 'Hello World'          # response

## 주소를 생성 
# localhost : 5000/second
@app.route('/second')
def second():                # 위와 함수명 달라야 한다.
    return 'Second Page'


## Flask Class 안에 있는 함수(웹서버의 구동)를 호출 
app.run()



# > python app.py
# 웹페이지에 127.0.0.1:5000/