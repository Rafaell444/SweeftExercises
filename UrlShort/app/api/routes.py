from app import app, db
from app.models import Link, User
from flask import request, jsonify, url_for, g
from app import auth


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()

    if not user:
        return False

    if not user.verify_password(password):
        return False

    g.user = user
    return True


@app.route('/api/links/get/<short_url>', methods=['GET'])
def api_get_short_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    return link


@app.route('/api/links/create', methods=['POST'])
def api_create_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)

    db.session.add(link)
    db.session.commit()

    return jsonify({'short url': link.short_url})


@app.route('/api/links/create/premium', methods=['POST'])
@auth.login_required
def api_create_premium_link():
    user = User.query.filter_by(username=g.user.username).first()
    original_url = request.form['original_url']
    word = request.form['custom_word']

    short_url_exists = Link.query.filter_by(short_url=word).first()

    if short_url_exists:
        return "custom name already used, please use another one"

    if user.is_premium == 1:

        link = Link(original_url=original_url)
        link.generate_premium_link(word)

        db.session.add(link)
        db.session.commit()

        return 'premium link created successfully'
    return "You Are not Premium Member"


@app.route('/api/users/create', methods=['POST'])
def api_register_user():
    username = request.form['username']
    password = request.form['password']

    if username is None or password is None:
        return 'please enter username and password'

    if User.query.filter_by(username=username).first() is not None:
        return jsonify('user already exists')

    user = User(username=username)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'user successfully created': user.username}), 201, {'Location': url_for('api_register_user',
                                                                           id=user.user_id,
                                                                           _external=True)}


@app.route('/api/users/premium/activate/', methods=['GET'])
@auth.login_required
def api_activate_premium_user():
    user = User.query.filter_by(username=g.user.username).first()

    if user.is_premium == 1:

        user.activate_premium()

        return 'premium activated'
    return "User is not premium"
