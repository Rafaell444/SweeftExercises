import string
from datetime import datetime
from random import choices

from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(3), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=3))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()

        return short_url


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', )


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/add_link', methods=['POST'])
@login_required
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html',
                           new_link=link.short_url, original_url=link.original_url)


if __name__ == '__main__':
    app.run(debug=True)
