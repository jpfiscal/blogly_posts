"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag
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

############################### USERS ###############################

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

############################### POSTS ###############################

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """load new post form"""
    user = User.query.filter_by(id=user_id).first()
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """save new post for selected user"""
    title = request.form['ip_title']
    content = request.form['ip_content']
    tag_ids = request.form.getlist('tags[]')

    post = Post(title=title, content=content, user_id=user_id)
    
    db.session.add(post)
    db.session.commit()

    # Associate selected tags with new post
    for tag_id in tag_ids:
        tag= Tag.query.get(tag_id)
        if tag:
            post.tags.append(tag)
    
    db.session.commit()

    return redirect(f"/users/{user_id}")
    
@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """Load a selected post onto a page"""
    post = Post.query.filter_by(id=post_id).first()
    tags = Post.query.get(post_id).tags
    return render_template("post_details.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """load form to edit selected post"""
    post = Post.query.filter_by(id=post_id).first()
    tags = Tag.query.all()
    post_tags_ids = [tag.id for tag in post.tags]
    return render_template("edit_post.html", post=post, tags=tags, post_tags_ids=post_tags_ids)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """edit the existing post record in the table"""
    post = Post.query.filter_by(id=post_id).first()
    post.title = request.form['ip_title']
    post.content = request.form['ip_content']
    
    selected_tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags[]')]

    post.tags=[Tag.query.get(tag_id) for tag_id in selected_tag_ids]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete selected post from db"""
    post = Post.query.filter_by(id=post_id).first()
    user_id = post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user_id}")

############################### TAGS ###############################

@app.route("/tags")
def view_tags():
    """Show a list of all tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/new")
def new_tag_form():
    """Show form to create new tag."""
    return render_template("new_tag.html")

@app.route("/tags/new", methods=["POST"])
def create_tag():
    """Create and save a new tag into db."""
    tag_name = request.form['ip_tag_name']

    tag = Tag(name=tag_name)
    
    db.session.add(tag)
    db.session.commit()

    return redirect("/users")

@app.route("/tags/<int:tag_id>")
def view_tag(tag_id):
    """See details of a selected tag."""
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template("tag_detail.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Show form to edit existing tag."""
    tag = Tag.query.filter_by(id=tag_id).first()
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Show form to edit existing tag."""
    tag = Tag.query.filter_by(id=tag_id).first()
    tag.name = request.form['ip_tag_name']

    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag_id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Show form to edit existing tag."""
    Tag.query.filter_by(id=tag_id).delete()

    db.session.commit()
    return redirect(f"/tags")