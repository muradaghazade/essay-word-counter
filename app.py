from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    words_count = db.Column(db.Integer, nullable=False)
    addedat = db.Column(db.String(500), nullable = False)

    def __init__(self, content, words_count):
        self.content = content
        self.words_count = words_count
        self.addedat = str(datetime.now().date())

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        texts = Text.query.all()
        return render_template('index.html', texts=texts)
    else:
        text = request.form['text']
        words_list = text.split()
        words_count = str(len(words_list))
        print(text)
        print(words_list)
        new_text = Text(text, words_count)
        db.session.add(new_text)
        db.session.commit()
        return render_template('result.html', text=text, words_count=words_count)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)