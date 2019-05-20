import os 
import secrets
from PIL import Image
from magic import  db, bcrypt
from sqlalchemy import desc
from sqlalchemy.sql import func
from magic.models import *
from datetime import datetime, timedelta
import requests 
from flask import render_template, url_for, flash, redirect, request, Blueprint
from datetime import datetime
from magic.admin.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from magic.admin.utils import *  


admin = Blueprint('admin', __name__)

@admin.route('/videomagic/admin-login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password,form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('You are not an admin, Please go and get Shola!!!', 'danger')
    return render_template('admin/login.html', title= 'Verified Admin Login', form=form)

@admin.route('/admin-dashboard')
@login_required
def dashboard():
    posts = Post.query.order_by(desc(Post.id)).all()
    return render_template('admin/dashboard.html', title='Admin Dashboard', posts=posts)


@admin.route('/admin-dashboard/upload-post', methods=['GET','POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.video.data:
            video_file = save_post_video(form.video.data)
        if form.thumbnail.data:
            thumbnail = save_post_thumbnail(form.thumbnail.data)
        if form.category.data == 'funny':
            new_post = Post(title=form.title.data,short_desc=form.short_description.data,vid=video_file,thumbnail=thumbnail,cat_id=1,featured=False)
            db.session.add(new_post)
            db.session.commit()
        elif form.category.data == 'lifestyle':
            new_post = Post(title=form.title.data,short_desc=form.short_description.data,vid=video_file,thumbnail=thumbnail,cat_id=2,featured=False)
            db.session.add(new_post)
            db.session.commit()
        elif form.category.data == 'inspire':
            new_post = Post(title=form.title.data,short_desc=form.short_description.data,vid=video_file,thumbnail=thumbnail,cat_id=3,featured=False)
            db.session.add(new_post)
            db.session.commit()
        elif form.category.data == 'animation':
            new_post = Post(title=form.title.data,short_desc=form.short_description.data,vid=video_file,thumbnail=thumbnail,cat_id=4,featured=False)
            db.session.add(new_post)
            db.session.commit()

        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/upload.html', form=form, title="Upload New Post")

@admin.route('/admin-dashboard/create-admin', methods=['GET','POST'])
@login_required
def create_admin():
    form = CreateAdminForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.thumbnail.data:
            thumbnail=save_profile_thumbnail(form.thumbnail.data)
        new_admin = Admin(name=form.name.data, email=form.email.data, role=form.role.data, password=hashed_password,thumbnail=thumbnail)
        db.session.add(new_admin)
        db.session.commit()
        flash('You are now an admin')
        msg = Message('TOP SECRET', sender="shola.albert@gmail.com", recipients=[form.email.data])
        msg.body = f'''
                Hello {form.name.data}, You are now a {form.role.data} for Videomagic. 
                Your login password is {form.password.data}. Please keep this information very confidential. 
                You can refer to Shola for any further enquiries! 
         '''
        mail.send(msg)
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/createadmin.html', form=form, title= "Create New Admin")


@admin.route('/admin_reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
       return redirect(url_for('admin.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        admin=Admin.query.filter_by(email=form.email.data).first()
        send_reset_email(admin)
        flash('An email has been sent with instruction to reset your password!')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/forgot-password.html',title='Reset Password',form=form) 


@admin.route('/admin_reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
       return redirect(url_for('admin.dashboard'))
    admin = Admin.verify_reset_token(token)
    if admin is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('admin.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin.password = hashed_password 
        db.session.commit()
        flash('Your password has been updated! You are now able to login','success')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset-password.html', title='Reset Password', form=form)

@admin.route('/admin-dashboard/admin')
@login_required
def admins():
    admins = Admin.query.all()
    return render_template('admin/admins.html', title="Video Magic Admin Page", admins=admins)


@admin.route('/admin-dashboard/delete-admin/<admin_id>')
@login_required
def delete_admin(admin_id):
    admin = Admin.query.filter_by(id=admin_id).first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return redirect(url_for('admin.admins'))
    return redirect('admin.admins')

@admin.route('/admin-dashboard/edit-post/<post_id>',methods=['GET','POST'])    
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.short_desc = form.short_description.data
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit.html', form=form, title= "Edit Post")


@admin.route('/admin-dashboard/make-feature/<post_id>')
@login_required
def make_feature(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        post.featured = True
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin_logout')
def logout():
    logout_user()
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin-dashboard/remove-feature/<post_id>')
@login_required
def remove_feature(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        post.featured = False
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.dashboard'))