#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
  
app = Flask(__name__)
app.secret_key = "cairocoders-ednalan-06300131"
  
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/testingdb'
                                        #mysql+pymysql://username:passwd@host/databasename 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
db = SQLAlchemy(app)
  
#Creating model table for our CRUD database
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
  
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
  
#query on all our employee data
@app.route('/')
def Index():
    all_data = Employee.query.all()
    return render_template("index.html", employees = all_data)
  
#insert data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
  
        my_data = Employee(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
  
        flash("Employee Inserted Successfully")
        return redirect(url_for('Index'))
  
#update employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
  
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('Index'))
  
#delete employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('Index'))
  
if __name__ == "__main__":
    app.run(debug=True)
</id>


//index.html
{% extends 'base.html' %}
{% include 'header.html' %}
 
{% block title %} Home {% endblock %}
  
{% block body %}
<div class="container">
    <div class="row">
        <div class="col md-12">
            <div class="jumbotron p-3">
                <h2>Manage <b>Employees </b>  <button type="button"  class="btn btn-success float-right"
                data-toggle="modal" data-target="#mymodal">Add New Employees</button> </h2>
                {% with messages = get_flashed_messages() %}
                {% if messages %}
                 
    {% for message in messages %}
                <div class="alert alert-success alert-dismissable" role="alert">
                    <button type="button" class="close" data-dismiss="alert" aria-label="close">
                        <span aria-hidden="true">x</span>
                    </button>
                {{message}}
                </div>
                {% endfor %}
     
                {% endif %}
                {% endwith %}
  
                <table class="table table-hover table-striped">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Action</th>
                    </tr>
                   {% for row in employees %}
                    <tr>
                        <td>{{row.id}}</td>
                        <td>{{row.name}}</td>
                        <td>{{row.email}}</td>
                        <td>{{row.phone}}</td>
                        <td>
                            <a href="/update/{{row.id}}" class="btn btn-warning btn-xs" data-toggle="modal" data-target="#modaledit{{row.id}}">Edit</a>
                            <a href="/delete/{{row.id}}" class="btn btn-danger btn-xs" onclick="return confirm('Are You Sure To Delete ?')">Delete</a>
                        </td>
                    </tr>
     <!-- Modal Edit Employee-->
     <div id="modaledit{{row.id}}" class="modal fade" role="dialog">
        <div class="modal-dialog">
        <div class="modal-content">
       <div class="modal-header"><h4 class="modal-title">Update Information</h4></div>
        <div class="modal-body">
        <form action="{{url_for('update')}}" method="POST">
         <div class="form-group">
          <label>Name:</label>
          <input type="hidden"  name="id" value="{{row.id}}">
          <input type="text" class="form-control" name="name" value="{{row.name}}">
         </div>
         <div class="form-group">
          <label>Email:</label>
          <input type="text" class="form-control" name="email" value="{{row.email}}">
         </div>
         <div class="form-group">
          <label>Phone:</label>
          <input type="text" class="form-control" name="phone" value="{{row.phone}}">
         </div>
         <div class="form-group">
          <button class="btn btn-primary" type="submit">Update</button>
         </div>
        </form>
        </div>
        <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
      </div>
     </div> 
     {% endfor %}
    </table>
   </div>
  
  <!-- Modal Add Employee-->
  <div id="mymodal" class="modal fade" role="dialog">
      <div class="modal-dialog">
     <div class="modal-content">
    <div class="modal-header"><h4 class="modal-title">Add Employee</h4></div>
    <div class="modal-body">
     <form action="{{url_for('insert')}}" method="POST">
      <div class="form-group">
       <label>Name:</label>
       <input type="text" class="form-control" name="name" required="1">
      </div>
      <div class="form-group">
       <label>Email:</label>
       <input type="email" class="form-control" name="email" required="1">
      </div>
      <div class="form-group">
       <label>Phone:</label>
       <input type="number" class="form-control" name="phone" required="1">
      </div>
      <div class="form-group">
      <button class="btn btn-primary" type="submit">Add Employee</button>
      </div>
     </form>
    </div>
    <div class="modal-footer">
    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
    </div>
   </div>
   </div>
  </div>
   
 </div>
 </div>
</div>
{% endblock %}


//base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <meta charset="UTF-8">
    <title>{% block title %} {% endblock %} </title>
</head>
<body>
{% block body %} {% endblock %}
  
  
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
  
</body>
</html>

