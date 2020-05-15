
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np

# 로컬 디렉토리에서 HashingVectorizer를 import
from vectorizer import vect

# 로컬 디렉토리에서 업데이트함수 import > 피드백을 모델에 반영
from update import update_model

app = Flask(__name__)

# pickle 모듈로 저장된 분류기 복원
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'pkl_objects',
                 'classifier.pkl'), 'rb'))
db = os.path.join(cur_dir, 'reviews.sqlite')

# 텍스트 문서에 대한 예측 레이블과 확률 반환
def classify(document):
    label = {0: 'negative', 1: 'positive'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba

# 문서와 클래스 레이블이 주어지면 분류기 업데이트
def train(document, y):
    X = vect.transform([document])
    clf.partial_fit(X, [y])

# 사용자가 웹에서 입력한 리뷰, 클래스, 타임스탬프를 저장
# 어플리케이션을 재시작할때마다 clf 객체를 원본 상태로 재설정함
def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO review_db (review, sentiment, date)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

######## 플라스크를 위한 정의
# textarea 만들기 위한 클래스
class ReviewForm(Form):
    moviereview = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

# 입력한 내용을 분류기로 전달하고 결과가 result.html로 나옴
@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html',
                                content=review,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('reviewform.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']

    inv_label = {'negative': 0, 'positive': 1}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    train(review, y)
    sqlite_entry(db, review, y)
    return render_template('thanks.html')

if __name__ == '__main__':
    clf = update_model(db_path=db, model=clf, batch_size=10000)
    app.run(debug=True)
