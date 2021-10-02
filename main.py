from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(main)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        #print(title)
        intro = request.form['intro']
        #print(intro)
        text = request.form['text']
        #print(text)

        article = Article(title=title, intro=intro, text=text)
        print(article.text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    main.run( debug = True )

