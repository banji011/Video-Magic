from flask import Flask 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 


from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://olabanji011@localhost/videomagic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    posts = db.relationship('Post', backref='categories', lazy=True)

class Post(db.Model):
    __tablename__= 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.String(500), nullable=True)
    vid = db.Column(db.String(500), nullable=False, default='defaultvid.mp4')
    post_date = db.Column(db.String(300), nullable=False, default=datetime.utcnow)
    thumbnail = db.Column(db.String(500), nullable=False, default='defaultimg.jpg')
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    featured = db.Column(db.Boolean, unique=False, default=False)
    category = db.relationship('Category', backref='cat_posts', foreign_keys=[cat_id])
    
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False, default="defaultimg.jpg")



if __name__=='__main__':
    manager.run()