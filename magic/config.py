import os 
from datetime import timedelta

class Config:
    SECRET_KEY =  '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI =  'mysql://olabanji:olabanji011@localhost/videomagic'
    PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True 
    MAIL_USERNAME = 'shola.albert@gmail.com'
    MAIL_PASSWORD = 'Olabanji011'