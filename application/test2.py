import pymysql
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR, TEXT 
import mysql.connector
from datetime import datetime
from models import Member, db
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm

basedirectory = os.path.abspath(os.path.dirname(__file__))#basedir to use in imageloading


app = Flask(__name__)   

# this userpass assumes you did not create a password for your database
# and the database username is the default, 'root'
userpass = 'mysql+pymysql://joshlufafa:fhdu23AJ8j3hmvbluf@'
basedir  = '127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/kyambogosda'
# this socket is going to be very different on a Windows computer
#socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'


# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Agdgajj938n2!gjjskg@;[pbqbktofd'

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedirectory, 'uploads') # you'll need to create a folder named uploads


db = SQLAlchemy(app)#initialise the database 
# this variable, db, will be used for all SQLAlchemy commands






if __name__ == '__main__':
    app.run(debug=True) 
         