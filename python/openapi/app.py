## 프레임워크 로드
from flask import Flask, request
import pandas as pd 
import database

## Flask Class 생성
# __name__ : 현재 파일의 이름 
app = Flask(__name__)

## database에 있는 MyDB Class 생성
_db = database.MyDB(
    _host = '172.30.1.22',
    _user = 'ubion',
    _pw = '1234',
    _db = 'ubion'
)

## api 생성
# 127.0.0.1:5000/ 요청 시 아래의 함수를 호출
# id와 password를 데이터로 입력받는다.
@app.route('/')
def index():
    # 유저가 보낸 데이터를 확인하고 변수에 저장
    try:
        _id = request.args['input_id']
        _pass = request.args['input_pass']
    except:
        return "parameter error 매개변수 키값 오류"
    print(_id, _pass)

    query = """
        SELECT * FROM user WHERE id = %s AND password = %s
    """
    result = _db.sql_query(query, _id, _pass)

    if result:
        # 외부의 csv 파일을 로드
        # 상위 폴더로 이동 -> csv 하위폴더로 이동 -> 파일이름
        df = pd.read_csv('../../csv/corona.csv', index_col = 0)    # corona.csv에 첫 col이 0,1...이므로 이걸 인덱스로 쓰겠다.
        data = df.to_dict()
        return data
    else: 
        return "입력 데이터 오류"
## 웹서버를 실행
app.run(debug = True)