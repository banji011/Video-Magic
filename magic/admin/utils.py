import os
import secrets
from PIL import Image
from moviepy.editor import *
from flask import url_for, current_app
from flask_mail import Message
from magic import mail 

def save_post_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/bg-img', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return ('img/bg-img/' + picture_fn)

def save_post_video(form_video):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(current_app.root_path, 'static/vid', video_fn)
    file = form_video
    file.save(video_path)
    return ('vid/' + video_fn)

def save_profile_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/core-img', picture_fn)

    output_size=(125,125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return ('img/core-img/' + picture_fn)

def send_reset_email(admin):
    token = admin.get_reset_token()
    msg = Message('Password Reset Request', sender='shola.albert@gmail.com', recipients=[admin.email] )
    msg.body = f''' To reset your password, visit the following link: 
    {url_for('admin.reset_token',token=token,_external=True)}
    If you did not make this request, simply ignore this message and no changes will be made
    ''' 
    
    mail.send(msg)