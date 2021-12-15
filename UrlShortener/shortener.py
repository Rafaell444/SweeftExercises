import string
from datetime import datetime
from random import choices

from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from auth import requires_auth

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(5), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
        short_url = ''.join(choices(characters, k=5))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()

        return short_url


class Link2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spec_url = db.Column(db.String(512))
    uniq_url = db.Column(db.String(), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uniq_url = self.generate_unique_link()

    def generate_unique_link(self):
        word = request.form['custom_word']
        uniq_url = ''.join(word)

        link2 = self.query.filter_by(uniq_url=uniq_url).first()

        if link2:
            return self.generate_unique_link()

        return uniq_url


@app.route("/")
def home():
    return render_template('index.html', )


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url)


@app.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html', new_link=link.short_url, original_url=link.original_url)


@app.route("/stats")
def stats():
    links = Link.query.all()

    return render_template("stats.html", links=links)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1>", 404


@app.route('/premium')
def prem_page():
    return render_template("premium_page.html")


@app.route('/<uniq_url>')
def redirect_to_uniq_url(uniq_url):
    link2 = Link2.query.filter_by(uniq_url=uniq_url).first_or_404()

    link2.visits = link2.visits + 1

    db.session.commit()

    return redirect(link2.spec_url)


@app.route("/add_spec_link", methods=['POST'])
@requires_auth
def add_special_link():
    spec_url = request.form['spec_url']
    link2 = Link2(spec_url=spec_url)

    db.session.add(link2)
    db.session.commit()

    return render_template("premium_link_added.html", new_link=link2.uniq_url, spec_url=link2.spec_url)


@app.route("/premium_stats")
def premium():
    links2 = Link2.query.all()

    return render_template("premium_stats.html", links2=links2)


if __name__ == '__main__':
    app.run(debug=True)
