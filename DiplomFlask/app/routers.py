from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, User
from slugify import slugify

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    return render_template('main_page.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        slug = slugify(username)

        new_user = User(username=username, password=password, first_name=first_name, last_name=last_name, age=age, slug=slug)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.profile', username=username))

    return render_template('register.html')


@main.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return 'Incorrect login or password', 401

    return redirect(url_for('main.profile', username=username))


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'User not found', 404
    return render_template('profile.html', user=user)
