from flask import Flask, request, render_template, flash, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed 
import re
from flask_sqlalchemy import SQLAlchemy
from models import Member, db, Image
from wtforms import validators
from forms import MemberForm, ImageForm, ImageSearch
import flask
import os
from tables import Image_Results
import secrets
from flask_login import current_user

basedirectory = os.path.abspath(os.path.dirname(__file__))#basedir to use in imageloading

app = Flask(__name__)

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

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedirectory, 'static/img') # you'll need to create a folder named uploads

PHOTO_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER
#db = SQLAlchemy(app)#initialise the database configuration

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

    # class UploadForm(FlaskForm):
    #     image = FileField(u'Image File', [validators.regexp(r'^[^/\\]\.jpg$')])
    #     description = TextAreaField(u'Image Description')

    #     def validate_image(form, field):
    #         if field.data:
    #             field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

db = SQLAlchemy(app)


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(['png', 'jpg']), FileRequired('File was empty!')])
    

@app.route('/image_final', methods=['GET', 'POST'])#Use this method to test the us of this field with other form fields
def upload_file():
    image = Image()
    form = ImageForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        f_name, f_ext = os.path.splitext(filename)
        picture_fn = f_name + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
        image.image_file = picture_fn#Dont forget to change the image path if it workd later on
        image.name = form.name.data
        db.session.add(image)
        db.session.commit()
    else:
        file_url = None

    return render_template('image_final.html', form=form, file_url=file_url)

@app.route('/edit-image', methods=['GET', 'POST'])
def edit():
    image = Image()#
    form = ImageForm()
    qry = db.session.query(Image).filter(Image.name.contains("oben"))
    image_fn = qry.first()#result from the query 
    image_file = url_for('static', filename='img/' + image_fn.image_file)#

    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        f_name, f_ext = os.path.splitext(filename)
        picture_fn = f_name + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
        image_fn.image_file = picture_fn#Dont forget to change the image path if it workd later on
        #image_fn.name = form.name.data
        #db.session.add(image)
        db.session.commit()
    else:
        file_url = None
    return render_template('edit-image.html', form=form, file_url=file_url, image_file=image_file)
    
@app.route('/image-result', methods=['GET', 'POST'])
def view_image():
    image = Image()#
    qry = db.session.query(Image).filter(Image.name.contains("oben"))
    image_fn = qry.first()#result from the query 

    image_file = url_for('static', filename='img/' + image_fn.image_file)#This concatenates the image iflename and extension to the static/img folder where the images are uploaded and saved 
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_fn.image_file) #this is the filepath to the image displayed in the html template 
    return render_template('image-result.html', image_file=image_file)

def save(member, form, picture_fn, new=False):#member args to pass data to our, form is the argument to pass the data to the member model
    member.image_file = picture_fn#The filename is the picture filename from the caller function new_member
    member.full_name = form.full_name.data
    member.gender = form.gender.data  
    member.date_added = form.date_added.data 
    member.telephone_no = form.telephone_no.data  
    member.address = form.address.data 
    member.a_o_residence = form.a_o_residence.data 
    member.d_o_birth = form.d_o_birth.data
    member.age = form.age.data 
    member.m_status = form.m_status.data   
    member.no_children = form.no_children.data 
    member.occupation = form.occupation.data 
    member.l_o_educ = form.l_o_educ.data 
    member.p_o_work = form.p_o_work.data
    member.employer = form.employer.data  
    member.nationality = form.nationality.data
    member.tribe = form.tribe.data
    member.clan = form.clan.data
    member.ch_born = form.ch_born.data 
    member.f_faith = form.f_faith.data
    member.d_o_baptism = form.d_o_baptism.data
    member.ch_of_baptism = form.ch_of_baptism.data
    member.ch_family = form.ch_family.data
    member.l_o_AY = form.l_o_AY.data 
    member.lang_spoken = form.lang_spoken.data
    member.skills = form.skills.data 
    member.inc_projects = form.inc_projects.data 
    member.hobbies = form.hobbies.data
    member.ch_programs = form.ch_programs.data
    
    if new:
        db.session.add(member)
    db.session.commit()#s


@app.route('/image_load', methods=['GET', 'POST'])#Use this method to test the us of this field with other form fields
def reister():
    form = MemberForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    #form = UploadForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    if request.method == 'POST' and form.validate_on_submit():
        member = Member()#Instantiate the member model 
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        f_name, f_ext = os.path.splitext(filename)
        picture_fn = f_name + f_ext
        #member.image_file = picture_fn
        save(member, form, picture_fn, new=True)#The picture filename is passed as an arguement to the save function
        flash("Successfully created new member")
        
    else:
        file_url = None

    return render_template('image_load.html', form=form, file_url=file_url)
    

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    form_picture.save(picture_path)   

    return picture_fn


@app.route('/image', methods=['GET', 'POST'])
def test():
    form = ImageForm()
    image = Image()
    if form.validate_on_submit():
        if form.photo.data:
            picture_file = save_picture(form.photo.data)
            image.image_file = picture_file
            image.name = form.name.data
            db.session.add(image)
            db.session.commit()
          
    #image_file = url_for('static', filename='img' + image_f)    
    return render_template('image.html', form=form)

if __name__ == '__main__':
    app.run()