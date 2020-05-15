
# flask web application 구동을 위한 파이썬 인터프리터
## templates 디렉토리에서 웹에 표시할 html 탐색

from flask import Flask, render_template

# 플라스크 인스턴스 초기화. 현재 디렉토리로부터 template 폴더를 찾음
app = Flask(__name__)

# 특정 url이 index 함수를 실행하도록 함
@app.route('/')

def index():
    return render_template('first_app.html')

if __name__ == '__main__':
    app.run(debug=True)
