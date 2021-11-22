
@app.route('/image_load', methods=['GET', 'POST'])
def upload():
    form = UploadForm(request.form)
    if request.method == 'POST':
        image_data = request.FILES[form.image.name].read()
        open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)
    return render_template('image_load.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)


<p><input type="submit" name="btn" value="upload"></p>#Html statement to confirm form submission    

#html for image upload
{% for field in form %}
    {% if field.type == "FileField" %}
    <form method="POST" enctype="multipart/form-data">
        {{ form.hidden_tag() }}
        {{ form.photo }}
        {% for error in form.photo.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}

        {% if file_url %}
        <br>
        <img src="{{ file_url }}">
        {% endif %}
        <p><input type="submit" name="btn" value="Upload"></p>
    </form>
    {% endif %}
{% endfor %}

<a href="{{ url_for('books', genre='biography') }}">Books</a>


#This uses the image-load
@app.route('/image_load', methods=['GET', 'POST'])#Use this method to test the us of this field with other form fields
def upload_file():
    form = UploadForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    return render_template('image_load.html', form=form, file_url=file_url)



#This is the working version of the image upload and save user data form
@app.route('/image_load', methods=['GET', 'POST'])#Use this method to test the us of this field with other form fields
def upload_file():
    form = MemberForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    #form = UploadForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    if request.method == 'POST' and form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        member = Member()#Instantiate the member model 
        save(member, form, new=True)
        flash("Successfully created new member")
        
    else:
        file_url = None

    return render_template('image_load.html', form=form, file_url=file_url)
    

#image files 


@app.route('/searchimage', methods=['GET', 'POST'])
def search_image():
    search_form = ImageForm(request.form) #if errors, you can pass the request.form argument here (request.form)   
    if request.method == 'POST':
        name = search_form.name.data
        qry = db.session.query(Image).filter(Image.name.contains(name))
        results = qry.all() 
        if not results:
            flash('No results found')
            return redirect('searchimage')

        else:
            table = Image_Results(results)#create a table to use in displaying the search results
            table.border = True
            #table.column = True
            return render_template('imageresult.html', table=table)
            
    return render_template('searchimage.html', form=search_form)    


@app.route('/image/<int:id>', methods=['GET', 'POST'])#This method loads the the profile object for view in the html page
def view_image(id):
    qry = db.session.query(Image).filter(id==id)
    image = qry.first()
    if image:
        form = MemberForm(formdata=request.form, obj=image)#
    return render_template('image.html', form=form, image=image) 

@app.route('/image_final', methods=['GET', 'POST'])#Use this method to test the us of this field with other form fields
def upload_file():
    image = Image()
    form = UploadForm()#The request method brings about the frontend error in the template file ie "No file was chosen"
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        image.file_path = file_url
        image.name = form.name.data
        db.session.add(image)
        db.session.commit()
    else:
        file_url = None

    return render_template('image_final.html', form=form, file_url=file_url)
      


#index.html page for image-test.py
<div class="media">
    <img class="rounded-circle account-img" src="{{ image_file  }}">
    <p>Name: {{ form.name }}</p>   
</div>


#image display.py code
image = Image()#
    qry = db.session.query(Image).filter(Image.name.contains("logo"))
    image_fn = qry.first()#result from the query 
    if image:
        form = ImageForm(formdata=request.form, obj=image)

    image_file = url_for('static', filename='img/' + image_fn.image_file)
    print(image_file)


#This is code for the login template 
# <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
 
<form action="" method="POST">
    <p>
        <label for="username">Username</label>
        <input type="text" name="username">
    </p>
    <p>
        <label for="password">Password</label>
        <input type="password" name="password">
    </p>
 
    <div class="msg">{{ msg }}</div> 
    <input type="submit" value="Login">   
</form>
 
</body>
</html>    


#backup for register.html file

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
 
<form action="" method="POST">
 
    {{ form.csrf_token() }}
 
    {% for field in form if field.name != "csrf_token" %}
        <p>{{ field.label() }}</p>
        <p>{{ field }}
            {% for error in field.errors %}
                {{ error }}
            {% endfor %}
        </p>
    {% endfor %}
    <div class="msg">{{ msg }}</div> 
    <input type="submit" value="Register">   
</form>
 
</body>
</html>

#backup from test.py file

class TimeForm(FlaskForm):
    opening = StringField('Opening Hour')
    closing = StringField('Closing Hour')
    day = HiddenField('Day')

class BusinessForm(FlaskForm):
    name = StringField('Business Name')
    hours = FieldList(FormField(TimeForm), min_entries=7, max_entries=7)

@app.route('/calendar', methods=['post','get'])
def calendar():
    form = BusinessForm()
    if form.validate_on_submit():
        results = []
        for idx, data in enumerate(form.hours.data):
            results.append('{day}: [{open}]:[{close}]'.format(
                day=calendar.day_name[idx],
                open=data["opening"],
                close=data["closing"],
                )
            )
        return render_template('calendar.html', results=results)
    print(form.errors)
    return render_template('calendar.html', form=form)


@app.route('/services.html', methods=['GET', 'POST'])#Dont forget to delete this, it belongs to another website
def test():
    return render_template('services.html')

@app.route('/home.html', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/about.html', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')   