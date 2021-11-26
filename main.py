from flask import Flask, render_template, request, redirect
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


@main.route('/history')
def history():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('history.html', articles=articles)


@main.route('/history/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@main.route('/history/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    return render_template('post_delete.html', article=article)


@main.route('/history/<int:id>/delete/yep')
def post_delete_yep(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/history')
    except:
        return "Delete error"


@main.route('/history/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/history')
        except:
            return "Error"
    else:
        article = Article.query.get(id)
        return render_template('post_update.html', article=article)


@main.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        print(article.text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/history')
        except:
            return "Error"
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    main.run(debug=True)
