import os 
import secrets
from PIL import Image
from magic import  db
from flask import render_template, url_for, flash, redirect, request, session, json, g, Blueprint, current_app
from magic.main.forms import * 
from sqlalchemy import desc
from sqlalchemy.sql import func
from magic.models import *
import uuid
from datetime import datetime, timedelta
import requests 

main = Blueprint('main', __name__)


# class back(object):
   
        
#     cfg = current_app.config.get
#     cookie = cfg('REDIRECT_BACK_COOKIE', 'back')
#     default_view = cfg('REDIRECT_BACK_DEFAULT', '/')

#     @staticmethod
#     def anchor(func, cookie=cookie):
#         @functools.wraps(func)
#         def result(*args, **kwargs):
#             session[cookie] = request.url
#             return func(*args, **kwargs)
#         return result

#     @staticmethod
#     def url(default=default_view, cookie=cookie):
#         return session.get(cookie, url_for(default))

#     @staticmethod
#     def redirect(default=default_view, cookie=cookie):
#         return redirect(back.url(default, cookie))
# back = back()


@main.route('/')
def home(): 
    featured = Post.query.filter_by(featured=True).order_by(desc(Post.id)).all()
    funny = Post.query.filter_by(cat_id=1).all()
    lifestyle = Post.query.filter_by(cat_id=2).all()
    inspire = Post.query.filter_by(cat_id=3).all()
    animation = Post.query.filter_by(cat_id=4).all()
    trending = Post.query.order_by(desc(Post.id)).all()
    if g.phone:
        return render_template('main/index.html', title='Homepage',phone=g.phone,featured=featured,funny=funny,lifestyle=lifestyle,animation=animation, trending=trending, inspire=inspire)
    return render_template('main/index.html', title='Homepage',featured=featured,funny=funny,lifestyle=lifestyle,animation=animation, trending=trending,inspire=inspire)
 

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        phone = form.phone.data
        net = form.network.data
        if net == 'airtel':
            req = requests.get(f"http://138.197.179.16/airtel/api/v1/subscribers/status/tutor/{phone}")
            response = req.json()
            if 'MSISDN not found' in response['message']:
                session['phone'] = phone
                session.permanent = True
                next = request.args.get('next')
                return redirect(next or url_for('main.home'))
    return render_template('main/login.html',form=form,title='Login Page')



@main.before_request
def before_request():
    g.phone = None
    if 'phone' in session:
        g.phone = session['phone']
          

@main.route('/single<title>')
def single(title):
    single = Post.query.filter_by(title=title).first()
    if g.phone:
        return render_template('main/vidsingle.html',title='Single',phone=g.phone,single=single)
    return redirect(url_for('main.login'))

@main.route('/category/<string:name>')
def category(name):
    page = request.args.get('page', 1, type=int)
    cat = Category.query.filter_by(name=name).first()
    posts = Post.query.filter_by(cat_id=cat.id).order_by(desc(Post.id)).paginate(page=page, per_page=8)
    catname = cat.name
    if g.phone:
        return render_template('main/category.html', title= catname,catname=catname,phone=g.phone,posts=posts)
    return redirect(url_for('main.login'))


# @main.route('/vote/<int:post_id>')
# def like(post_id):
#     post = Post.query.filter_by(id=post_id).first()
#     if g.phone:
#         post.like += 1
#         db.session.commit()
#         return redirect(url_for('main.home'))
#     return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    session.pop('phone',None)
    flash('You have been logged out!')
    return redirect(url_for('main.home'))
