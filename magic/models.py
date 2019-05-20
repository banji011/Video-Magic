from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask import current_app
from magic import db, login_manager
from flask_login import UserMixin 


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


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
    featured = db.Column(db.Boolean, unique=False, default=True)
    category = db.relationship('Category', backref='cat_posts', foreign_keys=[cat_id])
    

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False, default="defaultimg.jpg")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None 
        return Admin.query.get(user_id)

    def __repr__(self):
        return f"Admin('{self.name}','{self.email}', '{self.thumbnail}')"