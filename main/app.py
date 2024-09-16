# main Flask application that run the server

# imports of required libraries and modules

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bd65c61c4395956e10063e64d9cd4e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    """
    a database model for users
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='joined')

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}')"


class Post(db.Model):
    """
    a database model for the posts
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post '{self.title}' created at {self.date_posted}"


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    """
        The defualt home page route
    """
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
        registeration form
    """
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
        login form route
    """
    form = LoginForm()
    return render_template('login.html', title='login', form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
