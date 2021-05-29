from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np

# import HashingVectorizer from local dir
from vectorizer import vect

app = Flask(__name__)

######## Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'pkl_objects',
                 'classifier.pkl'), 'rb'))
db = os.path.join(cur_dir, 'tweets.sqlite')

def classify(document):
    label = {-1:'Sin sentimiento', 0:'Neutro', 1:'Positivo',2: 'Negativo'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba

def train(document, y):
    X = vect.transform([document])
    clf.partial_fit(X, [y])

def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO tweets_db (tweet, sentiment, date)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

def sqlite_select(path):
	conn = sqlite3.connect(path)
	c = conn.cursor()
	c.execute("SELECT tweet, sentiment, date FROM tweets_db")
	results = c.fetchall()
	return results


######## Flask
class TweetForm(Form):
    tweet = TextAreaField('',
                         [validators.DataRequired(),
                         validators.length(min=15)])

@app.route('/')
def index():
    form = TweetForm(request.form)
    return render_template('tweetform.html', form=form)

@app.route('/sqliteReport', methods=['POST'])
def sqliteReport():
	dataset =sqlite_select(db)
	return render_template('sqliteReport.html', dataset=dataset)

@app.route('/results', methods=['POST'])
def results():
    form = TweetForm(request.form)
    if request.method == 'POST' and form.validate():
        tweet = request.form['tweet']
        y, proba = classify(tweet)
        return render_template('results.html',
                                content=tweet,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('tweetform.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    tweet = request.form['tweet']
    prediction = request.form['prediction']
    inv_label = {'Sin sentimiento':-1, 'Neutro':0,'Positivo':1,'Negativo':2}
    y = inv_label[prediction]
    train(tweet, y)
    sqlite_entry(db, tweet, y)
    
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
