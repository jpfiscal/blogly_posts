"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route("/")
def home():
    """Redirect to the users list page"""
    return redirect("/users")

@app.route("/users")
def list_users():
    """List users in db"""
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new")
def new_user_form():
    """List users in db"""
    return render_template("create_user.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user to the db"""

    first_name = request.form['ip_first_name']
    last_name = request.form['ip_last_name']
    img = request.form['ip_img']

    user = User(first_name=first_name, last_name=last_name, image_url=img)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def view_user(user_id):
    """Show info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """bring user to the edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """edit the existing user record in the table"""
    user = User.query.filter_by(id=user_id).first()
    user.first_name = request.form['ip_first_name']
    user.last_name = request.form['ip_last_name']
    user.image_url = request.form['ip_img']\
    
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete a selected user from db"""
    User.query.filter_by(id=user_id).delete()

    db.session.commit()
    return redirect("/users")