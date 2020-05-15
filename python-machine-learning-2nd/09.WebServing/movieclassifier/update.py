
# sqlite에 수집된 피드백 데이터를 사용해서 예측 모델을 업데이트
## 실시간으로 하는 경우: 계산 비용이 비싸고 충돌이 발생할 수 있음

import pickle
import sqlite3
import numpy as np
import os

# 로컬 디렉토리에서 import
from vectorizer import vect

def update_model(db_path, model, batch_size=10000):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * from review_db')

    results = c.fetchmany(batch_size)
    while results:
        data = np.array(results)
        X = data[:, 0]
        y = data[:, 1].astype(int)

        classes = np.array([0, 1])
        X_train = vect.transform(X)
        model.partial_fit(X_train, y, classes=classes)
        results = c.fetchmany(batch_size)

    conn.close()
    return model

cur_dir = os.path.dirname(__file__)

clf = pickle.load(open(os.path.join(cur_dir,
                  'pkl_objects',
                  'classifier.pkl'), 'rb'))
db = os.path.join(cur_dir, 'reviews.sqlite')

# 개별 파일 실행할때는 해당 코드가 필요한데, app.py __main__에서 해당 부분 수행함
# clf = update_model(db_path=db, model=clf, batch_size=10000)

# 영구적으로 classifier.pkl 파일에 반영
pickle.dump(clf, open(os.path.join(cur_dir,
            'pkl_objects', 'classifier.pkl'), 'wb')
            , protocol=4)
