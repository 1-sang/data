
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)

class HelloForm(Form):
    sayhello = TextAreaField('',[validators.DataRequired()])

# 시작페이지에 텍스트필드 추가
@app.route('/')
def index():
    form = HelloForm(request.form)
    return render_template('first_app.html', form=form)

# html 폼으로 전달된 내용을 검증한 후 hello.html 페이지를 출력
@app.route('/hello', methods=['POST'])
def hello():
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['sayhello']
        return render_template('hello.html', name=name)
    return render_template('first_app.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
