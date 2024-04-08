from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')                   
def index():
    # 문자열을 return 하는 것이 아니라 html 문서를 리턴
    # render_template() : templates 폴더 안에 있는 html 문서를 호출
    return render_template('index.html')         # render_template의 함수 기본경로가 templates로 되어있다.   


@app.route('/second')
def second():
    # return 'Second Page'
    return render_template('login.html')

## 주소를 생성(/login)
# 로그인 정보(request 메세지)를 받아오는 주소
@app.route('/login')
def login():
    # 해당 주소로 요청이 들어왔을 때 (유저가 보낸 데이터가 포함)
    # request.args는 유저가 서버에게 get 방식으로 보낸 데이터가 저장되어 있는 공간
    req = request.args
    print(req)              # 프롬프트에 output찍힌다. ImmutableMultiDict([('input_id', 'asdf'), ('input_pass', '1234')])  딕셔너리 형태 
                                                    # 'asdf'를 뽑으려면 > req['input_id']
    ## 유저가 보낸 아이디 값을 변수에 저장
    _id = req['input_id']
    _pass = req['input_pass']
    print(f'유저가 보낸 id : {_id}, 비밀번호 : {_pass}')
    
    ## _id가 test이고 _pass가 1111인 경우에만 로그인 성공 메시지 리턴. 
    # 아니라면 로그인 페이지(/second)로 되돌아간다. 
    if (_id == 'test') and (_pass == '1111'):     
            # 실제는 DB에서 SELECT * FROM table WHERE ID = 'test' AND pass = '1234' 식으로 조회해서 로그인 할 것.
        return '로그인 성공'
    else: 
        return redirect('/second')         

# 디버그 모드 on으로 바꾸기  (파일이 바뀔 때마다 알아서 리스타트)
app.run(debug = True)



