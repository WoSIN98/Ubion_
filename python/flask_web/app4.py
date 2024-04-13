from flask import Flask, render_template, request, redirect, url_for
import database
from datetime import datetime

app = Flask(__name__)

_db = database.MyDB(
    _host = '172.30.1.22',
    _user = 'ubion',
    _pw = '1234',
    _db = 'ubion'
)

@app.route('/')                   
def index():
    return render_template('index.html')          


@app.route('/second')
def second():
    return render_template('login.html')

@app.route('/login')
def login():

    req = request.args
    print(req)              
                                                    
   
    _id = req['input_id']
    _pass = req['input_pass']
    print(f'유저가 보낸 id : {_id}, 비밀번호 : {_pass}')
    
     
    query = """
        SELECT * FROM `user` WHERE `id` = %s AND `password` = %s   
    """  

  
    result = _db.sql_query(query, _id, _pass)
    print(result)                    
    
    if result:
        return '로그인 성공'
    else:  
        return redirect('/second')



@app.route('/login2', methods=['post'])
def login2():
   
   
    req = request.form
    print('post 방식 데이터 : ', req)
    _id = req['input_id']
    _pass = req['input_pass']
    print(f'유저가 보낸 id : {_id}, 비밀번호 : {_pass}')

    query = """
        SELECT * FROM `user` WHERE `id` = %s AND `password` = %s
"""
    result = _db.sql_query(query, _id, _pass)
    if result:
       
        user_name = result[0]['name']
        print('로그인을 한 유저의 이름 : ', user_name)
        return redirect('/board')
    else:
        return redirect('/second')                # redirect와 render_template 차이 확인
    

## 게시글을 보여주는 주소를 생성
@app.route('/board')
def board():
    # DB server에 있는 board table에 정보를 로드 
    query = """
        SELECT 
        `No`, `title`, `writer`, `create_dt`
        FROM
        `board`
        ORDER BY
        `No` DESC
    """
    result = _db.sql_query(query)
    print('board table의 data : ', result)
    return render_template('main.html', _data = result, _cnt = len(result))
    

## 회원가입 화면을 보여주는 주소를 생성
@app.route('/signup')
def signup():
    return render_template('signup.html')

## 회원의 정보를 받아오는 주소를 생성
# 127.0.0.1:5000/signup2 [post]
@app.route('/signup2', methods=['post'])             # []로 쓰는 이유 get post 둘 다 한꺼번에 쓸 수도 있다.
    # 유저가 보낸 정보를 확인 -> 변수에 저장 
    # 유저가 보낸 정보는 request 안에 dict형태로 들어있다.
    # {key(input태그에 있는 name 속성의 값) : value(input태그에 유저가 입력한 데이터)}
    # post 방식으로 데이터를 보내면 request 안에 form에 데이터가 존재 
def signup2():
    req = request.form
    print('회원가입 데이터 : ', dict(req))
    _id = req['input_id']
    _pass = req['input_pass']
    _name = req['input_name']
    print('회원의 ID', _id, '비밀번호', _pass, '이름', _name)
    
    # 받아온 회원 정보를 DB에 INSERT문을 실행
    query = """
        INSERT INTO
        `user`
        VALUES (%s, %s, %s)
    """
    # 에러났을 때 예외처리
    try:
        result = _db.sql_query(query, _id, _pass, _name)
        print(result)
        # 회원 가입이 완료되었으면
        return redirect('/second')
    
    except:
        return "ID 중복"

## 글쓰기 화면을 보여주는 주소를 생성
@app.route('/write')
def write():
    return render_template('write.html')

## 유저가 보내는 글의 정보를 DB서버에 저장하는 주소
@app.route('/save_content', methods = ['post'])
def save_content():
    # 유저가 보낸 글의 정보를 확인하고 변수에 저장
    req = request.form
    _title = req['input_title']
    _writer = req['input_writer']
    _content = req['input_content']
    print('글 제목 : ', _title)
    print('작성자 : ', _writer)
    print('본문 : ', _content)
    # 현재시간
    _time = datetime.now()
    print('현재 시간 : ',_time)
    # DB server에 데이터를 저장
    query = """
        INSERT INTO
        `board`(`title`,`writer`,`create_dt`,`content`)
        VALUES (%s, %s, %s, %s)        
    """
    result = _db.sql_query(query, _title, _writer, _time, _content)
    print('DB server의 결과 : ', result)
    return redirect('/board')


## 게시글 하나의 정보를 출력하는 주소를 생성
@app.route('/read')
def read():
    # get 방식으로 보낸 데이터를 변수에 저장
    _no = request.args['No']
    print(_no)
    query = """
        SELECT
        `title`,`writer`,`content`
        FROM
        `board`
        WHERE
        `No` = %s
    """
    result = _db.sql_query(query, _no)  # 데이터의 형태가 [{}]         
    data = result[0]  # 데이터 형태가 {}   # 데이터가 하나 밖에 없으니 이렇게 실행
    print(data)
    return render_template('view_content.html', _data = data) 

app.run(debug = True)
