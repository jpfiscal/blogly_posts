"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                           nullable = False,
                           unique = True)
    last_name = db.Column(db.String(50),
                           nullable = False,
                           unique = False)
    image_url = db.Column(db.String(200),
                          nullable = True,
                          default = 'img/default_profile.jpeg')
    posts = db.relationship('Post')

    def __repr__(self):
        return f"<User {self.id, self.first_name, self.last_name, self.image_url}>"
    
class Post(db.Model):
    __tablename__ = "post"
    
    id=db.Column(db.Integer, 
                 primary_key = True, 
                 autoincrement = True)
    title = db.Column(db.String(100), 
                      nullable = False, 
                      unique = True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                     db.ForeignKey('user.id'))
    
    user = db.relationship('User')

    def __repr__(self):
        return f"<Post {self.id, self.title, self.created_at, self.user}>"
