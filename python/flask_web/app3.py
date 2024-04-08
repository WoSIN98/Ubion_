from flask import Flask, render_template, request, redirect, url_for
## module 로드
import database


app = Flask(__name__)

## database에 있는 MyDB1 Claas를 생성
_db = database.MyDB(
    _host = '172.30.1.63',
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
    
    ## 유저가 보낸 데이터를 DB server의 정보와 비교     
    query = """
        SELECT * FROM `user` WHERE `id` = %s AND `password` = %s   
    """  # %s

    # _db 안에 있는 sql_query() 함수를 호출
    result = _db.sql_query(query, _id, _pass)
    print(result)                     # result는 [{}] 형태. 데이터가 존재하지 않다면 빈 리스트
    # 로그인이 성공? -> result 데이터가 존재할 때.
    if result:
        return '로그인 성공'
    else:   # 로그인 실패 시 로그인 화면으로 되돌아간다.
        return redirect('/second')


## 127.0.0.1:5000/login2 [post] 주소 생성
@app.route('/login2', methods=['post'])
def login2():
    # get 방식으로 데이터를 보내는 경우 -> request.args
    # post 방식으로 데이터를 보내는 경우 -> request.form
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
        # return '로그인 성공'
        ## 로그인 성공시 main.html을 되돌려준다.
        # 로그인 정보 중 유저의 이름을 변수에 저장
        user_name = result[0]['name']
        print('로그인을 한 유저의 이름 : ', user_name)
        return render_template('main.html', _name = user_name)
    else:
        return redirect('/second')

app.run(debug = True)


## <!-- javascript에서는 f'{}' 쓸려면 {{}}로 해야한다.-->
## <!--  {{%  %}} : python 코드를 의미  -->