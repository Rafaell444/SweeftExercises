from app import app
from flask import render_template, redirect, request, abort, jsonify, url_for, g
from app.models import Link, User
from app import db


@app.route("/")
def home():
    return render_template('index.html', )


@app.route('/<short_url>', methods=['GET'])
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


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1>", 404


@app.route("/stats")
def stats():
    links = Link.query.all()

    return render_template("stats.html", links=links)


@app.route('/premium')
def prem_page():
    return render_template("premium_page.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/add_link_prem', methods=['POST'])
def add_link_prem():
    original_url = request.form['original_url']
    word = request.form['custom_word']

    link = Link(original_url=original_url)
    link.generate_premium_link(word)

    if link.generate_premium_link(word):
        return '<h1>already exists</h1>'

    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html', new_link=link.short_url, original_url=link.original_url)