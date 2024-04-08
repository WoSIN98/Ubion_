from flask import Flask, render_template

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
@app.route('/login')
def login():
    return ''

# 디버그 모드 on으로 바꾸기  (파일이 바뀔 때마다 알아서 리스타트)
app.run(debug = True)



