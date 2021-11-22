import pymysql
from flask import Flask, url_for, render_template, Response, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR, TEXT 
from sqlalchemy.orm import relationship, backref
import mysql.connector
from wtforms import FormField, DateField, DateTimeField,RadioField, StringField, SelectField, FieldList, HiddenField, SelectMultipleField, widgets, IntegerField, FloatField
import calendar
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flaskwebgui import FlaskUI
from wtforms.validators import DataRequired, Length
from tables import All_Departments, All_Accounts, All_Projects, All_Givings
from datetime import datetime
import datetime
import dateutil.relativedelta
import io
import xlwt
from fpdf import FPDF
#from models import Member
#Import and use pandas for the project and table contribution
import pandas as pd

app = Flask(__name__)

# this userpass assumes you did not create a password for your database
# and the database username is the default, 'root'
userpass = 'mysql+pymysql://joshlufafa:fhdu23AJ8j3hmvbluf@'
basedir  = '127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/treasury'
# this socket is going to be very different on a Windows computer
#socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'


# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Agdgajj938n2!gjjskg@;[pbqbktofd'
#app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)
    
ui = FlaskUI(app)

def dow_name(dow):
    return calendar.day_name(dow)

class Dbconnect(object):
    def __init__(self):
        self.dbconnection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user = 'joshlufafa',
            passwd = 'fhdu23AJ8j3hmvbluf',
            database = 'treasury'

        )
        self.dbcursor = self.dbconnection.cursor()
       
     #save changes to the database   
    def commit_db(self):
        self.dbconnection.commit()

    def rollback(self):
        self.dbconnection.rollback()    

    def close_db(self):
        self.dbcursor.close()
        self.dbconnection.close()

db2 = Dbconnect()

"""One department has many members and many members belong to many departments, many to many relationship"""

project_accounts = db.Table('account_projects',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('account_id', db.Integer, db.ForeignKey('member_account.id', ondelete="cascade")),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id', ondelete="cascade"))
)

class Account(db.Model):
    __tablename__ = 'member_account'
    id = db.Column(db.Integer, primary_key=True)
    entries = db.relationship('Entry', backref='user_entries')#One user contributes to more than project 
    contribution = db.relationship('Contribution', backref='user_contributions', uselist=False)
    name = db.Column(db.String(120), index=False)
    gender = db.Column(db.String(128), unique=False, nullable=False)
    #now = datetime.now()
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today)
    acct_balance = db.Column(db.Float, nullable=False, default=0)#How to declare price fields in flask sqlalchemy, allocate money toward any field from the entry 
    acct_type = db.Column(db.String(128), unique=False, nullable=False)# either a member account or a visitors account
    acct_status = db.Column(db.String(128), index=True, nullable=False, default="Active")#Either active or closed, default is active 
    transactions = db.relationship('Transaction', backref='account_transactions') #One project has many invoices and one invoice belongs to a single project
    #allocations = db.relationship('AllocateTransaction', backref='allocated_transactions') #One project has many invoices and one invoice belongs to a single project

    def __repr__(self):
        return '<Account {}>'.format(self.name)


#Create an invoice for the project
class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, default=0) 
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today)
    authorizer = db.Column(db.String(120), index=False)# This defines the person who recieved the money or the one who authorised the payment, use the db-session tp get the person authorising the invoice
    reciever = db.Column(db.String(120), index=False)#Name of the person requesting the money
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120), index=False)
    contributions = db.relationship('Contribution', backref='project_contbns')#One project has one to many contributions, One to many relationship, compute the total 
    accounts = db.relationship('Account', secondary=project_accounts, lazy='subquery', backref=db.backref('accountprojects', lazy=True))
    #now = datetime.now()
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today)
    project_type = db.Column(db.String(128), unique=False, nullable=False)#Evangelism, donation, outreach, social department
    Owner = db.Column(db.String(128), unique=False, nullable=False)
    acct_balance = db.Column(db.Float, nullable=False, default=0)#How much has been collected so far on a particular project
    acct_status = db.Column(db.String(128), index=True, nullable=False)#Open or closed
    invoices = db.relationship('Invoice', backref='project_invoices') #One project has many invoices and one invoice belongs to a single project
    transaction = db.relationship('Transaction', backref='project_transactions')#One to One project has many transactions and one transaction belongs to one project
    total_collected = db.Column(db.Float, nullable=False, default=0)#Store the total amount collected without any withdraws

    def __repr__(self):
        return self.project_name
        #return '<Project {}>'.format(self.project_name)  

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    #projects = db.relationship('Project', backref='entry_projects')#One user contributes to more than project, one entry has many projects 
    #project = db.relationship('Project', secondary=project_entries, lazy='subquery', backref=db.backref('projectentries', lazy=True))
    reciept_no = db.Column(db.Integer, index=True, nullable=False, default=0) 
    #now = datetime.now()
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today)
    reciept_total = db.Column(db.Float, default=0)#Check for the best datatype to represent the amount total
    tithe = db.Column(db.Float, default=0)
    camp_off = db.Column(db.Float, default=0)#Camp meeting offering
    sabbath_sch = db.Column(db.Float, default=0)
    birthday = db.Column(db.Float, default=0)
    divine = db.Column(db.Float, default=0)
    third_sabb = db.Column(db.Float, default=0)#13th sabbath
    general_conf = db.Column(db.Float, default=0)
    operation_unity = db.Column(db.Float, default=0)
    prime_radio = db.Column(db.Float, default=0)
    lunch = db.Column(db.Float, default=0)
    evangelism = db.Column(db.Float, default=0)
    building = db.Column(db.Float, default=0)
    other_funds = db.Column(db.Float, default=0)
    account_id = db.Column(db.Integer, db.ForeignKey('member_account.id'))
    giving_id = db.Column(db.Integer, db.ForeignKey('giving.id'))
    #allocations = db.relationship('AllocateTransaction', backref='entry_allocations') #One project has many invoices and one invoice belongs to a single project

    #Compute the total amount of funds on a project by summing all the contributions on a given project
    

class Contribution(db.Model):
    __tablename__ = 'contributions'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('member_account.id'))
    amount = db.Column(db.Float, default=0)#The amount being contributed 
    giving_id = db.Column(db.Integer, db.ForeignKey('giving.id'))#The giving when the contribution was made
 
 #A many to many relationship where on giving has many projects and many projects belong to many givings
giving_project = db.Table('giving_project',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id', ondelete="cascade")),
    db.Column('giving_id', db.Integer, db.ForeignKey('giving.id', ondelete="cascade"))
)

class Giving(db.Model):
    __tablename__ = 'giving'
    id = db.Column(db.Integer, primary_key=True)
    #now = datetime.now()
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today) 
    entries = db.relationship('Entry', backref='added_entries')#add all created entries to a particular giving created in a given period of time
    contributions = db.relationship('Contribution', backref='added_contributions')
    #allocations = db.relationship('AllocateTransaction', backref='giving_allocations') #One project has many invoices and one invoice belongs to a single project

    """Totals from the collected entries from the frontend/ summaries of the giving"""
    total = db.Column(db.Float, default=0)#Check for the best datatype to represent the amount total
    tithe = db.Column(db.Float, default=0)
    camp_off = db.Column(db.Float, default=0)#Camp meeting offering
    sabbath_sch = db.Column(db.Float, default=0)
    birthday = db.Column(db.Float, default=0)
    divine = db.Column(db.Float, default=0)
    third_sabb = db.Column(db.Float, default=0)#13th sabbath
    general_conf = db.Column(db.Float, default=0)
    operation_unity = db.Column(db.Float, default=0)
    prime_radio = db.Column(db.Float, default=0)
    lunch = db.Column(db.Float, default=0)
    evangelism = db.Column(db.Float, default=0)
    building = db.Column(db.Float, default=0)
    other_funds = db.Column(db.Float, default=0)
    """Used in computing the total contributions for each project"""
    projects = db.relationship('Project', secondary=giving_project, lazy='subquery', backref=db.backref('giving_projects', lazy=True))
    def __repr__(self):
        return '<Giving {}>'.format(self.date_created)  

class Transaction(db.Model):
    __tablename__ = 'Transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, default=0) 
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today)
    authorizer = db.Column(db.String(120), index=False)# Person authorising the transaction
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('member_account.id'))
    #transactions = db.relationship('Project', backref='transaction_project')


""" Admin accounts creation is handles by this model"""
class UserAccount(db.Model):#This is the admins model.py file
    __tablename__ = 'admin_account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=False, nullable=False)
    password = db.Column(db.String(128), index=False, nullable=False)  

    def __repr__(self):
        return '<UserAccount {}>'.format(self.username)    




#This form is used to create a new project
class ProjectCreationForm(FlaskForm):
    project_name = StringField('Name', [DataRequired()])
    project_type = StringField('Project Type', [DataRequired()])
    Owner = StringField('Owner', [DataRequired()])
    acct_status = RadioField('Project Status', [DataRequired()], choices=[('Active', 'Active'), ('Closed', 'Closed')])

class InvoiceForm(FlaskForm):
    amount = FloatField('Amount')
    reciever = StringField('Name', [DataRequired()])

class ContributionForm(FlaskForm):
    amount = FloatField('Amount')#Field suitable to capture monetary figures in Flask

#This form is used to edit and display a project and add contributions to it
class ProjectForm(FlaskForm):
    name = StringField('Name')#The name of the project being contributed to
    contribution = FieldList(FormField(ContributionForm))#Optionlally get the contribution for the project sing the project object ie project.contribution.all()

class AccountForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    gender = RadioField('Gender', [DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')])
    acct_type = RadioField('Account Type', [DataRequired()], choices=[('Member', 'Member'), ('Visitor', 'Visitor')])
    acct_status = RadioField('Account Status', [DataRequired()], choices=[('Active', 'Active'), ('Closed', 'Closed')])

class EntryForm(FlaskForm):
    reciept_total = FloatField('Receipt Total')
    tithe = FloatField('Tithe')
    camp_off = FloatField('Campmeeting Offering')
    sabbath_sch = FloatField('Sabbath School')
    birthday = FloatField('Birthday')
    divine = FloatField('Divine')
    third_sabb = FloatField('13th Sabbath')
    general_conf = FloatField('General Conference')
    operation_unity = FloatField('Operation Unity')
    prime_radio = FloatField('Prime Radio')
    lunch = FloatField('Lunch')
    evangelism = FloatField('Evangelism')
    building = FloatField('Local Church Building')
    other_funds = FloatField('Other Funds')
    projects = FieldList(FormField(ProjectForm))

class InputGridTableForm(FlaskForm):
    """A form for one or more InputGridRecords"""
    gridtblrecords = FieldList(FormField(EntryForm), min_entries=1)


class DepositMoneyForm(FlaskForm):#Form for the member to be added to the department
    amount = FloatField('Amount', [DataRequired()])
    

class DepositForm(FlaskForm):#Form for the member to be added to the department
    amount = FloatField('Amount', [DataRequired()])
    
    project = SelectField(' Select Project', coerce=int, option_widget=widgets.CheckboxInput())

    def set_choices(self):
        self.project.choices = [(d.id, d.name) for d in Project.query.all()]


class SelectForm(FlaskForm):#Form for the member to be added to the department
    
    giving = SelectField('Givings', coerce=int, option_widget=widgets.CheckboxInput())
    #get the latest givings for the choices field
    def set_choices(self):
        self.giving.choices = [(d.id, d.date_created) for d in Giving.query.all()]

class GivingForm(FlaskForm):
    #select = SelectField('select:', choices=[('Member','Member'), ('church family','Church family'), ('gender','gender')])#provide a criteria for searching data
    search_string = DateField('search:', [DataRequired()])


class AllocateForm(FlaskForm):
    select = SelectField('select:', choices=[('Tithe','Tithe'), ('Campmeeting Offering','Campmeeting Offering'), ('Sabbath School','Sabbath School'), ('Birthday Thanks','Birthday Thanks'), ('Divine','Divine'), ('Thirteenth Sabbath','Thirteenth Sabbath'), ('General Conference','General Conference'), ('Operation Unity','Operation Unity'), ('Prime Radio','Prime Radio'), ('Lunch','Lunch'), ('Evangelism','Evangelism'), ('Building','Building'), ('Other Funds','Other Funds')])#provide a criteria for searching data
    amount = FloatField('Amount:', [DataRequired()])


class InvoiceForm(FlaskForm):
    reciever = StringField('Recieved By', [DataRequired()]) 
    amount = FloatField('amount', [DataRequired()])

class SearchForm(FlaskForm):
    #select = SelectField('select:', choices=[('Tithe','Tithe'), ('Campmeeting Offering','Campmeeting Offering'), ('Sabbath School','Sabbath School'), ('Birthday Thanks','Birthday Thanks'), ('Divine','Divine'), ('Thirteenth Sabbath','Thirteenth Sabbath'), ('General Conference','General Conference'), ('Operation Unity','Operation Unity'), ('Prime Radio','Prime Radio'), ('Lunch','Lunch'), ('Evangelism','Evangelism'), ('Building','Building'), ('Other Funds','Other Funds')])#provide a criteria for searching data
    search_string = DateTimeField('search Date:', [DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    #This methid uses the form-data directly from the login.html file not from the defined wtf forms in forms.py file 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #account = Account()#Query the account object directly without assigning it to a variable
        #qry = db.session.query(Account).filter(id==id).filter(Account.username.contains(username)).filter(Account.password.contains(password))
        qry = db.session.query(UserAccount).filter(id==id).filter(UserAccount.username==username).filter(UserAccount.password==password)
        #Query the database to see if the account exists
        existing_account = qry.first()
        if existing_account:
            session['loggedin'] = True
            session['id'] = existing_account.id
            session['username'] = existing_account.username
            msg = 'successfully logged in' 
            return redirect(url_for('index'))
        else:
            msg = 'Invalid username or password!'
            #return redirect('login') redirect back to the login page
    return render_template('login2.html', msg=msg)#Dont forgeet to change back to the original form ie login template instead of login2         

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def save_user(account, new=False):# This view is to save the new administrative user for the system
    account.username = request.form.get('username')#Alternatively use the form data
    account.password = request.form.get('password')#Alternatively use the form data
    if new:
        db.session.add(account)
        db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AdminForm(request.form)#we are using data from the htnl template directlt and not the form
    username = request.form.get('username')#form.username.data, alternatively use the form data
    password = request.form.get('password')#form.password.data
    password1 = request.form.get('password1')#form.password1.data
    msg = ''
    if request.method == 'POST':
        account = UserAccount()
        #Query the database and retrieve an account with similar data and if it exists, display errors
        qry = db.session.query(UserAccount).filter(id==id).filter(UserAccount.username==username).filter(UserAccount.password==password)
        existing_account = qry.first()
        #print(existing_account.username)
        if existing_account:
            msg = 'Account already exists'
            # elif not re.match(r'[A-Za-z0-9]+', username):#Validate username to use only numbers and letters
            #     msg = 'User name must contain only letters and numbers'#Dont forget to check how to validate frontend fields with re.match 
        elif password != password1:#authenticate password validation
            msg = 'Passwords didnt match'    
        else:  
            save_user(account, new=True)  
            msg = 'Successfully registered' 
    
    elif request.method == 'POST':
        msg = 'Please Fill in the form'
    return render_template('register2.html', msg=msg)#Incase of form errors use the form again to register   




@app.route('/create_project', methods=['GET', 'POST'])
def add_project():
    #project formand save the newly created project
    form = ProjectCreationForm()
    if request.method == 'POST':
        project = Project()
        project.project_name = form.project_name.data
        project.project_type = form.project_type.data
        project.Owner = form.Owner.data
        project.acct_status = form.acct_status.data
        db.session.add(project)
        db.session.commit()
    return render_template('accounts/add_project.html', form=form)    

@app.route('/create_account', methods=['GET', 'POST'])
def add_account():
    #project formand save the newly created project
    form = AccountForm()
    if request.method == 'POST':
        account = Account()
        account.name = form.name.data
        account.gender = form.gender.data
        account.acct_type = form.acct_type.data
        account.status = form.acct_status.data
        db.session.add(account)
        db.session.commit()
    return render_template('accounts/add_account.html', form=form)    

#@app.route('/add_contribution', methods=['GET', 'POST'])
def add_contribution(accounts, projects):
    #Gt all accounts
    #Get all projects
    #if request.method =='GET':
    for project in projects:
        #print(project.id)
        for account in accounts:
            contribution = Contribution()
            contribution.project_id = project.id
            contribution.account_id = account.id
            #print(account.id)
            db.session.add(contribution)
            db.session.commit()
            project.accounts.append(account)
            db.session.commit()

@app.route('/create_entry', methods=['GET', 'POST'])
def add_entry():
    #GEt all the projects that are currently active
    #add them to the entry being created
    #Get the user account from the database and assign them to the entry being created
    qry1 = db.session.query(Account)
    accounts = qry1.all()
    qry2 = db.session.query(Project).filter(Project.acct_status=='Active')#Get all the active projects
    projects = qry2.all()
    #Create all the projects, set the project contributions from the created entries
    #if request.method == 'POST':
    #Create the entries with the default values and set the various foreignkeys ie account and project
    #if request.method == 'GET':
    for account in accounts:
        entry = Entry()
        #print(account.id)
        entry.account_id = account.id
        db.session.add(entry)
        db.session.commit()
        print(entry.id) 
    #Call the Add contribution method at the time of creating the entries     
    add_contribution(accounts, projects)
            #Redirect to the edit or update function to set the values being entered for the various entries
            # for project in projects:
            #     entry.project.append(project)#Either way the association table will add the related fields to the database
            #     db.session.commit()
    return render_template('accounts/add_entry.html')

@app.route('/add_giving', methods=['GET', 'POST'])
def add_giving():
    qry1 = db.session.query(Account)
    accounts = qry1.all()
    qry2 = db.session.query(Project).filter(Project.acct_status=='Active')#Get all the active projects
    projects = qry2.all()

    if request.method == 'GET':
        giving = Giving()
        """This will be used in computing the totals in the report"""
        giving.projects = projects#These will be used in computing the totals for a report
        db.session.add(giving)
        db.session.commit()
        """Create the entries with the giving id specified"""
        for account in accounts:
            entry = Entry()
            #print(account.id)
            entry.account_id = account.id
            entry.giving_id = giving.id
            db.session.add(entry)
            db.session.commit()
        for project in projects:
            #print(project.id)
            for account in accounts:
                contribution = Contribution()
                contribution.project_id = project.id
                contribution.account_id = account.id
                contribution.giving_id = giving.id
                #print(account.id)
                db.session.add(contribution)
                db.session.commit()
                project.accounts.append(account)
                db.session.commit()
        return redirect(url_for('view_giving', giving_id=giving.id))  
    return render_template('accounts/add_giving.html')          

@app.route('/allgivings', methods=['GET','POST'])
def allgivings():
    qry = db.session.query(Giving)
    results = qry.all()
    table = All_Givings(results)
    #filter givings by month, year ie this month, last month, this year, last year
    today = datetime.date.today()#Use this for current month and year
    d2 = today - dateutil.relativedelta.relativedelta(months=1)  

    """Get the last or previous year from the current date"""
        
    d4 = today - dateutil.relativedelta.relativedelta(years=1)#Use thos as last month
    #print(d4.year)

    this_month = []
    last_month = []
    this_year = []
    last_year = []
    for giving in results:
        if giving.date_created.month == today.month:
            this_month.append(giving)
        elif giving.date_created.month == d2.month:
            last_month.append(giving)
        #Get givings for the current and previous year
        if giving.date_created.year == today.year:
            this_year.append(giving)
        elif giving.date_created.year == d4.year:
            last_year.append(giving)

    #print(this_year)
    return render_template('accounts/all_givings.html', table=table)

@app.route('/search_giving', methods=['GET', 'POST'])
def search_giving():
    giving_form = GivingForm(request.form) 
    if request.method == 'POST':#Perform a validation on the forms ysing the validate method
        return giving_search(giving_form)
    return render_template('accounts/search_giving.html', form=giving_form)


#@app.route('/giving_search', methods=['GET', 'POST'])
def giving_search(giving_form):
    msg = ''
    search_string = giving_form.search_string.data#['select']#Use a carlendar selector to select the date to be searched for
    results = []#This will handle the results from the query
    if search_string: 
        qry = db.session.query(Giving).filter(Giving.date_created==search_string)
        results = qry.all()
        print(results)
    else:
        msg = 'Cant Search For Input'#
    if not results:
        msg = 'Not Found'
        return msg
    else:
        table = Giving_Results(results)
        table.border = False
        return render_template('accounts/search_results.html', table=table, msg=msg)

@app.route('/set_total', methods=['GET','POST'])
def set_total():
    """pass the totals of each column in the entries to the giving totals"""
    try:
        if request.method == 'POST':
            
            giving_id = request.form['giving_id']
            qry = db.session.query(Giving).filter(Giving.id==giving_id)#Id from the invoking object
            giving = qry.first()
            print(giving.id)


            giving.total = request.form['reciept_total']
            giving.tithe = request.form['tithe']
            giving.camp_off = request.form['camp_off']
            giving.sabbath_sch = request.form['sabbath_sch']
            giving.birthday = request.form['birthday']
            giving.divine = request.form['divine']
            giving.third_sabb = request.form['third_sabb']
            giving.general_conf = request.form['general_conf']
            giving.operation_unity = request.form['operation_unity']
            giving.prime_radio = request.form['prime_radio']
            giving.lunch = request.form['lunch']
            giving.evangelism = request.form['evangelism']
            giving.building = request.form['building']
            giving.other_funds = request.form['other_funds']
            db.session.commit()
            success =1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        #db2.close_db()
        return jsonify('Record updated successfully')

@app.route('/view_giving/<int:giving_id>', methods=['GET', 'POST'])
def view_giving(giving_id):
    qry = db.session.query(Giving).filter(Giving.id==giving_id)#Id from the invoking object
    giving = qry.first()
    qry2 = db.session.query(Project).filter(Project.acct_status=='Active')#Get all the active projects
    projects = qry2.all()
    contributions = giving.contributions
    entries = giving.entries
    headers = ['ID', 'Name', 'Reciept Total', 'Tithe', 'Campmeeting Offering', 'sabbath School', 'Birthday Thanks', 'Divine', '13th Sabbath', 'General Conference', 'Operation Unity', 'Prime Radio', 'Lunch', 'Evangelism', 'Building', 'Other Funds']
    
    values = []
    ids = []
    project_lst = []
    #accounts_lst = []
    #project_collections = []    
    for project in projects:
        
        values1 = []#Captures the individual contributions
        values2 = []#Captures the id's of the contributions for editing in the frontend
        accounts_lst = []
        """New code"""
        project_collections = []
        project_contributions = project.contributions
        project_invoices = project.invoices
        project_transactions = project.transaction
        
            # for account in project.accounts:
            #     accounts_lst.append(account)
        for cont in contributions:
                 
            #Create a list of user accounts from the project accounts where each name appears only once 
            if cont.project_id == project.id:   
                values1.append(cont)
                values2.append(cont.id)
                print(cont.id)
                if project in project_lst:
                    pass
                else:    
                    project_lst.append(project)
            for account in project.accounts:
                if account.id == cont.account_id:    
                    if account in accounts_lst:
                        pass
                    else:
                        accounts_lst.append(account)#Get the accounts that will b displayed along with the contributions        
        #print(values1)    
        values.append(values1)
        ids.append(values2)

    
        """Compute the total contributions of each project and set the """
        total_contribution = sum([cont.amount for cont in project_contributions])
        #total_invoices = sum([inv.amount for inv in project_invoices])
        #SEt the total amount collected for each project in the giving
        if project.transaction != None:
            total_transactions = sum([trans.amount for trans in project_transactions])#Get all money added to a project via transactions
            """Add the total contribution to the total amount collected for a project"""
            total_collected = total_contribution + total_transactions
            project.total_collected = total_collected 
            db.session.commit()
        else:
            project.total_collected = total_contribution 
            

    for s in ids:
        print(s)
    print(accounts_lst) 
    print(project_lst) 

    """pass the totals of each column in the entries to the giving totals"""
    if request.method == 'POST':
        
        giving.total = request.form['reciept_total']
        giving.tithe = request.form['tithe']
        giving.camp_off = request.form['camp_off']
        giving.sabbath_sch = request.form['sabbath_sch']
        giving.birthday = request.form['birthday']
        giving.divine = request.form['divine']
        giving.third_sabb = request.form['third_sabb']
        giving.general_conf = request.form['general_conf']
        giving.operation_unity = request.form['operation_unity']
        giving.prime_radio = request.form['prime_radio']
        giving.lunch = request.form['lunch']
        giving.evangelism = request.form['evangelism']
        giving.building = request.form['building']
        giving.other_funds = request.form['other_funds']
        db.session.commit()
        print(giving.tithe)
        for project in giving.projects:
            print(project.acct_balance)
    
    return render_template('accounts/giving.html', headers=headers, entries=entries, projects=project_lst, values=values, ids=ids, contributions=contributions, accounts=accounts_lst, giving=giving)

#Edit the giving by adding an account 
@app.route('/add_giving_account/<int:giving_id>', methods=['GET', 'POST'])
def add_giving_account(giving_id):

    qry = db.session.query(Giving).filter(Giving.id==giving_id)
    giving = qry.first()
    """Get all the projects that are active"""
    qry2 = db.session.query(Project).filter(Project.acct_status=='Active')#Get all the active projects
    projects = qry2.all()

    form = AccountForm()
    if request.method == 'POST':
        account = Account()
        account.name = form.name.data
        account.gender = form.gender.data
        account.acct_type = form.acct_type.data
        account.status = form.acct_status.data
        db.session.add(account)
        db.session.commit()
        #Create an entry for the account that is being created
        entry = Entry()
        #print(account.id)
        entry.account_id = account.id
        entry.giving_id = giving.id
        db.session.add(entry)
        db.session.commit()
        
        #Add contribution objects to the various projects that belong to the account being created
        for project in projects:
            contribution = Contribution()
            contribution.project_id = project.id
            contribution.account_id = account.id
            contribution.giving_id = giving.id
            #print(account.id)
            db.session.add(contribution)
            db.session.commit()
            project.accounts.append(account)
            db.session.commit()
    return render_template('accounts/add_giving_account.html', form=form)  #This should redirect to the giving specified by the id      

@app.route('/add_giving_project/<int:giving_id>', methods=['GET', 'POST'])
def add_giving_project(giving_id):

    qry = db.session.query(Giving).filter(Giving.id==giving_id)
    giving = qry.first()
    qry1 = db.session.query(Account)
    accounts = qry1.all()

    form = ProjectCreationForm()
    if request.method == 'POST':
        project = Project()
        project.project_name = form.project_name.data
        project.project_type = form.project_type.data
        project.Owner = form.Owner.data
        project.acct_status = form.acct_status.data
        db.session.add(project)
        db.session.commit()

        for account in accounts:
            contribution = Contribution()
            contribution.project_id = project.id
            contribution.account_id = account.id
            contribution.giving_id = giving.id
            #print(account.id)
            db.session.add(contribution)
            db.session.commit()
            project.accounts.append(account)
            db.session.commit()
    return render_template('accounts/add_giving_project.html', form=form)
    #return  a redirect to the giving that is being added a project unto        

#@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    input_form = InputGridTableForm()
        # qry = db.session.query(Entry).filter(Entry.id==id)
        # entry = qry.first()
    qry = db.session.query(Entry)#Get all the entries in a given time and display them for edit
    results = qry.all()
    for entry in results:
        if entry:
            entry_form = EntryForm(formdata=request.form, obj=entry)
            if request.method == 'POST' and form.validate():
                reciept_total = form.reciept_total.data
                tithe = form.tithe.data
                camp_off = form.camp_off.data
                sabbath_sch = form.sabbath_sch.data
                birthday = form.birthday.data
                divine = form.divine.data
                third_sabb = form.third_sabb.data
                general_conf = form.general_conf.data
                operation_unity = form.operation_unity.data
                prime_radio = form.prime_radio.data
                lunch = form.lunch.data
                evangelism = form.evangelism.data
                building = form.building.data
                other_funds = form.other_funds.data
            #List all the entry details to be displayed and updated
                for project in entry.projects:
                    project_form = ProjectForm(formdata=request.form, obj=project)
                    project_form.name.data = project.name#Set the project form name 
                    #List all the fields attached to the project that you want to edit
                    for contribution in project.contributions:
                        contribution_form = ContributionForm(formdata=request.form, obj=contribution)
                        contribution.amount = contribution_form.amount.data#Set the amount from the frontend
                        #List the fields of the form to be displayed
                        project_form.contribution.append_entry(contribution_form)
                        db.session.add(contribution)
                        db.session.commit()#commit changes to the contribution object
                    entry_form.projects.append_entry(project_form)
                    db.session.add(project)
                    db.session.commit()#commit changes to the project objects
    input_form.gridtblrecords.append_entry(entry_form)
    db.session.add(entry)
    db.session.commit()#commit changes to the entries being edited
    headers = []#Create a list of headers to use in the frontend
    headers1 = []#Get all the project names in the specific entries and display theri respective

    return render_template('accounts/edit_entry.html', form=input_form)

@app.route('/entries', methods=['GET', 'POST'])
def all_entries():
    qry = db.session.query(Entry)#Get all the entries in a given time and display them for edit
    results = qry.all()
    headers = ['ID', 'Reciept Total', 'Tithe', 'Campmeeting Offering', 'sabbath School', 'Birthday Thanks', 'Divine', '13th Sabbath', 'General Conference', 'Operation Unity', 'Prime Radio', 'Lunch', 'Evangelism', 'Building', 'Other Funds']
    qry2 = db.session.query(Project).filter(Project.acct_status=='Active')#Get all the active projects
    projects = qry2.all()
    qry1 = db.session.query(Account)
    accounts = qry1.all()
    qry3 = db.session.query(Contribution)
    all_contributions = qry3.all()
    keys = []
    values = []     
    p = []
    q = []
    for project in projects:
        keys.append(project)
        values1 = []
        accounts_lst = []
        for account in project.accounts:
            accounts_lst.append(account)

        for cont in all_contributions:
            #Create a list of user accounts from the project accounts where each name appears only once 
            if cont.project_id == project.id:   
                #values1.append(cont)
                values1.append(cont)#Use the contribution object instead of the amount, then invoke the amount from the frontend
        #print(values1)    
        values.append(values1)  
    #print(values)
    p = []
    for i in values:
        for x in i:
            print(x)
    print(values)  
         
    dictionary = dict(zip(keys, values))
    #print(dictionary)
    for key, value in dictionary.items():
        #print(key, value)
        df = pd.DataFrame(value)
        #print(df)
    nested = list(zip(keys, values)) 
    
    #new = [[row[i] for row in values] for i in range(len(values))]
    #print(values)
    col_values = values
    #print(list(col_values))
    #print(list(table_rows))
    #new = [[row[i] for row in values] for i in range(len(values[1]))]
    #print(new)
    final =  zip(accounts_lst)

    """USe Pandas to render the columns of the project contributions"""
    
    return render_template('accounts/all entries.html', headers=headers, entries=results, projects=projects, dictionary=dictionary, accounts=accounts_lst, keys=keys, values=values, contributions=all_contributions)

@app.route('/ajax', methods=['POST'])
def ajax():
    if request.method == 'POST':
        qry = db.session.query(Entry).filter(Entry.id==request.json['id'])
        entry = qry.first()
        print(entry.id)
        #Query the database and get the entry with the given entry_id
        #qry = db.session.query(Entry).filter(Entry.id==entry_id)
        
        if entry:
            #entry_id = request.form['id']
            if request.method == 'POST':
                entry_id = request.json['id']
                reciept_total = request.json['reciepttotal']#.get('reciept_total')#request.form['reciept_total']
                print(reciept_total)
                tithe = request.json['tithe']#.get('tithe')
                camp_off = request.json['campoff']#.get('camp_off')
                sabbath_sch = request.json['sabbathsch']#.get('sabbath_sch')
                birthday = request.json['birthday']#.get('birthday')
                divine = request.json['divine']#.get('divine')
                third_sabb = request.json['thirdsabb']#.get('third_sabb')
                general_conf = request.json['generalconf']#.get('general_conf')
                operation_unity = request.json['operationunity']#.get('operation_unity')
                prime_radio = request.json['primeradio']#.get('prime_radio')
                lunch = request.json['lunch']#.get('lunch')
                evangelism = request.json['evangelism']#.get('evangelism')
                building = request.json['building']#.get('building')
                Other_funds = request.json['otherfunds']#.get('other_funds')
                for project in entry.projects:
                    for contribution in project.contributions:
                        contribution.amount = request.json['amount']#.get('amount')
                        db.session.add(contribution)
                        db.session.commit()
                db.session.add(entry)
                db.session.commit()
    return jsonify('Record updated successfully')    

@app.route('/update', methods=['GET', 'POST'])
def update():
    try:
        if request.method == 'POST':
            field = request.form['field'] 
            value = request.form['value']
            editid = request.form['id']

            if field == 'reciepttotal':
               sql = "UPDATE entries SET reciept_total=%s WHERE id=%s"
            if field == 'tithe':        
                sql = "UPDATE entries SET tithe=%s WHERE id=%s"
            if field == 'campoff':        
                sql = "UPDATE entries SET camp_off=%s WHERE id=%s"
            if field == 'sabbathsch':        
                sql = "UPDATE entries SET sabbath_sch=%s WHERE id=%s"
            if field == 'birthday':        
                sql = "UPDATE entries SET birthday=%s WHERE id=%s"
            if field == 'divine':        
                sql = "UPDATE entries SET divine=%s WHERE id=%s"
            if field == 'thirdsabb':        
                sql = "UPDATE entries SET third_sabb=%s WHERE id=%s"
            if field == 'generalconf':        
                sql = "UPDATE entries SET general_conf=%s WHERE id=%s"
            if field == 'operationunity':        
                sql = "UPDATE entries SET operation_unity=%s WHERE id=%s"
            if field == 'primeradio':        
                sql = "UPDATE entries SET prime_radio=%s WHERE id=%s"
            if field == 'lunch':        
                sql = "UPDATE entries SET lunch=%s WHERE id=%s"
            if field == 'evangelism':        
                sql = "UPDATE entries SET evangelism=%s WHERE id=%s"
            if field == 'building':        
                sql = "UPDATE entries SET building=%s WHERE id=%s"
            if field == 'otherfunds':        
                sql = "UPDATE entries SET other_funds=%s WHERE id=%s"
            if field == 'amount':        
                sql = "UPDATE contributions SET amount=%s WHERE id=%s"
            
            data = (value, editid)
            db2.dbcursor.execute(sql, data)
            db2.commit_db()
            success =1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        #db2.close_db()
        return jsonify('Record updated successfully')

@app.route('/test')
def test():
    return render_template('accounts/test9.html')

@app.route('/all_accounts', methods=['GET', 'POST'])
def all_accounts():
    qry = db.session.query(Account)
    results = qry.all()
    table = All_Accounts(results)
    return render_template('accounts/all-accounts.html', table=table)


@app.route('/view_account/<int:account_id>', methods=['GET', 'POST'])
def view_account(account_id):
    qry = db.session.query(Account).filter(Account.id==account_id)#
    account = qry.first() 
    
    return render_template('account/view-account.html', account=account)


@app.route('/deposit/<int:id>', methods=['GET','POST'])
def deposit(id):
    qry = db.session.query(Account).filter(Account.id==id)
    account = qry.first()

    if account:
        form = DepositMoneyForm()
        if request.method == 'POST' and form.validate():
            amount = form.amount.data
            new_balance = account.acct_balance + amount
            account.acct_balance = new_balance
            db.session.add(account)
            db.session.commit()
            print(account.acct_balance)
    return render_template('accounts/deposit_money.html',account=account, form=form)


@app.route('/all_projects', methods=['GET', 'POST'])
def all_projects():
    qry = db.session.query(Project)
    results = qry.all()
    table = All_Projects(results)
    return render_template('accounts/all_projects.html', table=table)


@app.route('/delete_account/<int:id>', methods=['GET','POST'])
def delete_account(id):
    qry = db.session.query(Account).filter(Account.id==id)
    account = qry.first()
    qry3 = db.session.query(Contribution)
    contributions = qry3.all()
    
    if account:
        sql_query2 = "DELETE FROM account_projects WHERE account_id='%s'" %account.id
        db2.dbcursor.execute(sql_query2)
        db2.commit_db()
        """Delete all contributions with the given account"""        
        for cont in contributions:
            if cont.account_id == account.id:
                db.session.delete(cont)
                db.session.commit() 
        
        """Delete all entries with the account_id being deleted""" 
        for entry in account.entries:
            #if entry.account_id == account.id:
            db.session.delete(entry)
            db.session.commit()       
    db.session.delete(account)
    db.session.commit()               


@app.route('/delete_project/<int:id>', methods=['GET','POST'])
def delete_project(id):
    qry = db.session.query(Project).filter(Project.id==id)
    project = qry.first()
    qry3 = db.session.query(Contribution)
    contributions = qry3.all()

    sql_query2 = "DELETE FROM account_projects WHERE project_id='%s'" %project.id
    db2.dbcursor.execute(sql_query2)
    db2.commit_db()  
    
    for cont in contributions:
        if cont.project_id == project.id:
            qry = db.session.query(Contribution).filter(Contribution.id==cont.id)
            cont = qry.first()
            db.session.delete(cont)
            db.session.commit()    
        #db.session.delete(account.contribution)        
    db.session.delete(project)
    db.session.commit()               


@app.route('/edit_account/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    #Get the account that you want to edit
    qry = db.session.query(Account).filter(Account.id==id)
    account = qry.first()
    
    if account:
        form = AccountForm(formdata=request.form, obj=account)
        if request.method == 'POST' and form.validate():
            account.name = form.name.data
            account.gender = form.gender.data
            account.acct_type = form.acct_type.data
            account.status = form.acct_status.data
            db.session.add(account)
            db.session.commit()
    return render_template('accounts/edit-account.html', form=form, account=account)        

@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    #Get the account that you want to edit
    qry = db.session.query(Project).filter(Project.id==id)
    project = qry.first()
    print(project.acct_status)
    print(project.Owner)
    
    if project:
        form = ProjectCreationForm(formdata=request.form, obj=project)
        if request.method == 'POST' and form.validate():
            project.project_name = form.project_name.data
            project.project_type = form.project_type.data
            project.Owner = form.Owner.data
            project.acct_status = form.acct_status.data
            db.session.add(project)
            db.session.commit()     
    return render_template('accounts/edit_project.html', form=form, project=project)        



@app.route('/view_project/<int:id>', methods=['GET', 'POST'])
def view_project(id):
    qry = db.session.query(Project).filter(Project.id==id)
    project = qry.first()

    """Compute the total contributions and the remaining balance of a project"""
    total_contribution = sum([cont.amount for cont in project.contributions])
    total_invoices = sum([inv.amount for inv in project.invoices])
    #SEt the total amount collected for each project in the giving
    if project.transaction != None:
        total_transactions = sum([trans.amount for trans in project.transaction])#Get all money added to a project via transactions
        """Add the total contribution to the total amount collected for a project"""
        total_collected = total_contribution + total_transactions
        project.total_collected = total_collected 
        if total_collected != 0 and total_collected >= total_invoices:#Check for another requirement for this calculation
            new_acct_balance = total_collected - total_invoices
            project.acct_balance = new_acct_balance
            db.session.commit()
            print(project.acct_balance)
            print(project.total_collected)
        else:
            print('No contributions Yet')    

    else:
        if total_contribution != 0 and total_contribution >= total_invoices:#Check for another requirement for this calculation
            new_acct_balance = total_contribution - total_invoices
            project.acct_balance = new_acct_balance
            project.total_collected = total_contribution
            db.session.commit()
            print(project.acct_balance)
            print(project.total_collected)
        else:
            print('No contribution yet')        
    return render_template('account/project.html', project=project)


@app.route('/create_invoice/<int:project_id>', methods=['GET', 'POST'])
def create_invoice(project_id):
    #Get the project you are creating the invoice for
    qry = db.session.query(Project).filter(Project.id==project_id)
    project = qry.first()

    form = InvoiceForm()
    amount = form.amount.data
    if request.method == 'POST':
        if project.acct_balance != 0 and amount <= project.acct_balance:
            invoice = Invoice()
            invoice.amount = form.amount.data
            #invoice.authorizer = session['username']
            invoice.reciever = form.reciever.data
            invoice.project_id = project.id
            db.session.add(invoice)
            db.session.commit()
                # new_balance = project.acct_balance - invoice.amount
                # project.acct_balance = new_balance
            db.session.commit()
            return redirect(url_for('view_project', id=project.id)) 
    return render_template('accounts/invoice.html', form=form, project=project)    

@app.route('/deposit_project/<int:id>', methods=['GET', 'POST'])
def deposit_project(id):
    #Get the account depositing the money 
    qry = db.session.query(Account).filter(Account.id==id)
    account = qry.first()
    print(account.acct_balance)
    form = DepositForm(request.form)
    form.project.choices = [(d.id, d.project_name) for d in Project.query.all()]
    msg = ''
    amount = form.amount.data
    if request.method == 'POST':
        if account.acct_balance != 0 and amount <= account.acct_balance:
            if request.method=='POST':
                transaction = Transaction()
                transaction.amount = form.amount.data
                transaction.account_id = account.id
                #transaction.authorizer = session['username']
                db.session.add(transaction)
                db.session.commit()
                selected_project = Project.query.get(form.project.data)
                transaction.project_id = selected_project.id#Either way the association table will add the related fields to the database
                
                #selected_department.department_member.append(member)
                db.session.commit()
                #Deduct the money from the account to set a new account balance
                new_balance = account.acct_balance - transaction.amount
                account.acct_balance = new_balance
                project_balance = selected_project.acct_balance + transaction.amount
                selected_project.acct_balance = project_balance
                selected_project.total_collected += transaction.amount
                print(selected_project.acct_balance)
                db.session.commit()
            else:
                form = DepositForm()    
        else:
            msg = 'Your account balance is low to complete operation'     

    return render_template('accounts/deposit.html', form=form)

#Edit the transaction object given its id
#@app.route('/edit_transaction/<int:account_id>')
@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction):
    #Get the account depositing the money 
    qry = db.session.query(Transaction).filter(Transaction.id==id)
    transaction = qry.first()
    #qry2 = db.session.query(Account).filter(Account.id==id)
    #account = qry2.first()
    form = DepositForm(formdata=request.form, obj=transaction)
    form.project.choices = [(d.id, d.project_name) for d in Project.query.all()]
    msg = ''

    #Reset the account balance before editing the transaction
    new_balance = account.acct_balance + transaction.amount
    if new_balance != 0 and amount <= new_balance:
        if request.method=='POST':
            transaction.amount = form.amount.data
            #transaction.account_id = account.id
            #transaction.authorizer = session['username']
            db.session.add(transaction)
            db.session.commit()
            selected_project = Project.query.get(form.project.data)
            transaction.project_id = selected_project.id#Either way the association table will add the related fields to the database
            
            #selected_department.department_member.append(member)
            db.session.commit()
            #Deduct the money from the new account to set a new account balance
            new_acctbalance = new_balance - transaction.amount
            account.acct_balance = new_acctbalance
            project_balance = selected_project.acct_balance + transaction.amount
            selected_project.acct_balance = project_balance
            db.session.commit()
        else:
            form = DepositForm()    
    else:
        msg = 'Your account balance is low to complete operation'     

    return render_template('accounts/edit_deposit.html', form=form)


"""Report for a given range of givings ie quarter"""
@app.route('/report', methods=['GET', 'POST'])
def report():
    #Define the start date and end date for the range ie using a form
    
    qry = db.session.query(Giving).filter(Giving.date_created <= '2021-10-01').filter(Giving.date_created >= '2021-10-01')
    results = qry.all()
    #create a list of projects from the giving projects
    project_lst = []

    #Default values for the iterators
    total_reciept_total = 0
    total_tithe  = 0
    total_camp_off = 0
    total_sabbath_sch = 0
    total_birthday = 0
    total_divine = 0
    total_third_sabb = 0 
    total_general_conf = 0
    total_operation_unity = 0
    total_prime_radio = 0
    total_lunch = 0
    total_evangelism = 0
    total_building = 0
    total_other_funds =0

    for giving in results:

        total_reciept_total += giving.total
        total_tithe  += giving.tithe
        total_camp_off += giving.camp_off
        total_sabbath_sch += giving.sabbath_sch
        total_birthday += giving.birthday
        total_divine += giving.divine
        total_third_sabb += giving.third_sabb 
        total_general_conf += giving.general_conf
        total_operation_unity += giving.operation_unity
        total_prime_radio += giving.prime_radio
        total_lunch += giving.lunch
        total_evangelism += giving.evangelism 
        total_building += giving.building 
        total_other_funds += giving.other_funds
        #print(total_tithe)
        for project in giving.projects:
            if project in project_lst:
                pass
            else:
                project_lst.append(project)
            #if project in project_lst:    
            #total += project.acct_balance 
            """Compute the total contributions and the remaining balance of a project"""
            total_contribution = sum([cont.amount for cont in project.contributions])
            total_invoices = sum([inv.amount for inv in project.invoices])
            #SEt the total amount collected for each project in the giving
            if project.transaction != None:
                total_transactions = sum([trans.amount for trans in project.transaction])#Get all money added to a project via transactions
                """Add the total contribution to the total amount collected for a project"""
                total_collected = total_contribution + total_transactions
                project.total_collected = total_collected 
                if total_collected != 0 and total_collected >= total_invoices:#Check for another requirement for this calculation
                    new_acct_balance = total_collected - total_invoices
                    project.acct_balance = new_acct_balance
                    db.session.commit()
                        # print(project.acct_balance)
                        # print(project.total_collected)
                else:
                    print('No contributions Yet')    

            else:
                if total_contribution != 0 and total_contribution >= total_invoices:#Check for another requirement for this calculation
                    new_acct_balance = total_contribution - total_invoices
                    project.acct_balance = new_acct_balance
                    project.total_collected = total_contribution
                    db.session.commit()
                        # print(project.acct_balance)
                        # print(project.total_collected)
                else:
                    print('No contribution yet') 


    for project in project_lst:
        #print(project)
        print(project.acct_balance)

    """Create a function to create a pdf report for the giving"""    
    #def pdf_report():
    pdf = FPDF()
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Report Summary', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
    
    col_width = page_width/4
    
    pdf.ln(1)
    
    th = pdf.font_size
    
    #for row in result:
    #pdf.cell(col_width, th, str(row['emp_id']), border=1)
    pdf.cell(col_width, 'Tithe', str(total_tithe), border=1)
    pdf.cell(col_width, 'Birthday', str(total_birthday), border=1)
    pdf.cell(col_width, 'Camp Meeting', str(total_camp_off), border=1)
    pdf.ln(th)
    
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=employee_report.pdf'})

        # pdf_report()


    return render_template('accounts/report.html')

    # @app.route('/pdf_test', methods=['GET', 'POST'])
    # def pdf_test():
    #     date = datetime.date.today()
    #     amount = 230000
    #     pdf = FPDF(orientation='P', unit='pt', format='A4')
    #     pdf.add_page()
    #     pdf.set_font("Times", "B", 24)
    #     pdf.cell(0, 80, "Purchase Receipt", 0, 1, "C")
    #     pdf.set_font("Times", "B", 14)
    #     pdf.cell(100, 25, "Payment Date:")
    #     pdf.set_font("Times", "", 12)
    #     pdf.cell(0, 25, "{}".format(date), 0, 1)
    #     pdf.cell(0, 5, "", 0, 1)
    #     pdf.set_font("Times", "B", 14)
    #     pdf.cell(100, 25, "Payment Total:")
    #     pdf.set_font("Times", "", 12)
    #     pdf.cell(0, 25, "${}".format(amount), 0, 1)
    #     return pdf.output(dest="S")
    #     return render_template('account/test7.html')

"""Create an excel book for the giving entries"""
@app.route('/excel_giving/<int:giving_id>', methods=['GET', 'POST'])
def excel_giving(giving_id):
    qry = db.session.query(Giving).filter(Giving.id==giving_id)#Id from the invoking object
    giving = qry.first()
    entries = giving.entries
    projects = giving.projects

        # results = []       
        # sql_query = ("SELECT * FROM entries WHERE giving_id = 'giving.id'")#select all the data
        # db2.dbcursor.execute(sql_query)
        # results = db2.dbcursor.fetchall()
    
    """create an account list t pass to the first row"""
    account_lst = []
    for entry in entries:
        print(entry.id)
        qry2 = db.session.query(Account).filter(Account.id==entry.account_id)#Id from the invoking object
        account = qry2.first()
        
        if account in account_lst:
            pass
        else:
            account_lst.append(account.name)

    print(account_lst)
    
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Giving Report')

    headers = ['Name', 'Reciept Total', 'Tithe', 'Campmeeting Offering', 'sabbath School', 'Birthday Thanks', 'Divine', '13th Sabbath', 'General Conference', 'Operation Unity', 'Prime Radio', 'Lunch', 'Evangelism', 'Building', 'Other Funds']

    sh.write(0, 0, 'Name')
    sh.write(0, 1, 'Reciept Total')
    sh.write(0, 2, 'Tithe')
    sh.write(0, 3, 'Campmeeting Offering')
    sh.write(0, 4, 'sabbath School')
    sh.write(0, 5, 'Birthday Thanks')
    sh.write(0, 6, 'Divine')
    sh.write(0, 7, '13th Sabbath')
    sh.write(0, 8, 'General Conference')
    sh.write(0, 9, 'Operation Unity')
    sh.write(0, 10, 'Prime Radio')
    sh.write(0, 11, 'Lunch')
    sh.write(0, 12, 'Evangelism')
    sh.write(0, 13, 'Building')
    sh.write(0, 14, 'Other Funds')

    
    for  column_number, project in enumerate(projects):
        sh.write(0, column_number+15, project.project_name)
        idx = 1
        for cont in project.contributions:
            if cont.giving_id == giving.id:
                #sh.write(idx+1, i, cont.amount)
                sh.write(idx, column_number+15, cont.amount)
                idx += 1



        


            # idx = 0
            # for account in account_lst:
            #     sh.write(idx+1, 0, account.name)#You can iignore the str
    
    idx = 0
            # len_lst = len(account_lst)
            # for x in enumerate(account_lst):
            #     sh.write(idx, len_lst, account.name)#You can iignore the str
                
            # for entry in entries:
            #     print(entry.id)
            #     qry2 = db.session.query(Account).filter(Account.id==entry.account_id)#Id from the invoking object
            #     account = qry2.first()
            #     sh.write(idx+1, 1, account)



    for row in entries:
        sh.write(idx+1, 0, row.user_entries.name)
        sh.write(idx+1, 1, row.reciept_total) #row['reciept_total'])
        sh.write(idx+1, 2, row.tithe) #row['tithe'])
        sh.write(idx+1, 3, row.camp_off)#row['camp_off'])
        sh.write(idx+1, 4, row.sabbath_sch)#row['sabbath_sch'])
        sh.write(idx+1, 5, row.birthday)#row['birthday'])
        sh.write(idx+1, 6, row.divine)#row['divine'])
        sh.write(idx+1, 7, row.third_sabb)#row['third_sabb'])
        sh.write(idx+1, 8, row.general_conf)#row['general_conf'])
        sh.write(idx+1, 9, row.operation_unity)#row['operation_unity'])
        sh.write(idx+1, 10, row.prime_radio)#row['prime_radio'])
        sh.write(idx+1, 11, row.lunch)#row['lunch'])
        sh.write(idx+1, 12, row.evangelism)#row['evangelism'])
        sh.write(idx+1, 13, row.building)#row['building'])
        sh.write(idx+1, 14, row.other_funds)#row['other_funds'])
        idx += 1

    workbook.save(output)
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=giving_report.xls"})



"""Create an exvel book for the giving entries"""
@app.route('/excel_test/<int:giving_id>', methods=['GET', 'POST'])
def excel_test(giving_id):
    qry = db.session.query(Giving).filter(Giving.id==giving_id)#Id from the invoking object
    giving = qry.first()
    entries = giving.entries
    projects = giving.projects
    contributions = giving.contributions
        # results = []       
        # sql_query = ("SELECT * FROM entries WHERE giving_id = 'giving.id'")#select all the data
        # db2.dbcursor.execute(sql_query)
        # results = db2.dbcursor.fetchall()
    
        # a = ['January\n','February\n','March\n','April\n','May\n','June\n']
        # book = xlwt.Workbook()
        # sheet = book.add_sheet('Test')
        # sheet.write(0,0,a)
        # book.save('Test.xls')
    """create an account list t pass to the first row"""
    account_lst = []
    for entry in entries:
        print(entry.id)
        qry2 = db.session.query(Account).filter(Account.id==entry.account_id)#Id from the invoking object
        account = qry2.first()
        
        if account in account_lst:
            pass
        else:
            account_lst.append(account)

    print(account_lst)
            
    # #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    # #add a sheet
    sh = workbook.add_sheet('Giving Report')

    headers = ['Name', 'Reciept Total', 'Tithe', 'Campmeeting Offering', 'sabbath School', 'Birthday Thanks', 'Divine', '13th Sabbath', 'General Conference', 'Operation Unity', 'Prime Radio', 'Lunch', 'Evangelism', 'Building', 'Other Funds']
    # #add headers
    project_lst = []
        # for project in projects:
        #     project_lst.append(project.project_name)

    #sh.write(0, 0, project_lst)
    # sh.write(0, 1, 'Reciept Total')
    # sh.write(0, 2, 'Tithe')
    # sh.write(0, 3, 'Campmeeting Offering')
    # sh.write(0, 4, 'sabbath School')
    # sh.write(0, 5, 'Birthday Thanks')
    # sh.write(0, 6, 'Divine')
    # sh.write(0, 7, '13th Sabbath')
    # sh.write(0, 8, 'General Conference')
    # sh.write(0, 9, 'Operation Unity')
    # sh.write(0, 10, 'Prime Radio')
    # sh.write(0, 11, 'Lunch')
    # sh.write(0, 12, 'Evangelism')
    # sh.write(0, 13, 'Building')
    # sh.write(0, 14, 'Other Funds')


        


    idx = 0
    # for account in account_lst:
    #     sh.write(idx+1, 0, account.name)#You can iignore the str
    lst = [projects]
    len_lst = len(lst)
        # i = 0
        # while i < len_lst:
        #     for project in projects:
        #         for cont in contributions:
        #             if cont.project_id == project.id:
                        
        #                 sh.write(idx+1, ++i, cont.amount) #row['reciept_total'])

        #     i += 1
    lst = [[1,2,4,5,6,8], [2,3,5,6,7,8], [94,20,45,12,89]] 
    d = {'first': 1, 'second': 2, 'third': 3}

        # for i in lst:
        #     sh.write(idx+1, 1, i)
        #     idx += 1

        # for key, val in d.items():
        #     sh.write(idx+1, 1, val)
        #     idx += 1
    i = 0
        # while i < len_lst:
    #column_number = 3         
    for  column_number, project in enumerate(projects):
        sh.write(0, column_number, project.project_name)
        idx = 1
        for cont in project.contributions:
            if cont.giving_id == giving.id:
                #sh.write(idx+1, column_number+1, cont.amount)
                sh.write(idx, column_number, cont.amount)
                """Set the column to begin from"""
                #sh.write(idx, column_number+3, cont.amount)
                idx += 1
                
        #     i += 1 
    # column_number = 1    
    # for column_number, item in enumerate(project_lst):
    #     #sh.write(row_number+1, column_number, item) 
    #     sh.write(row_number+1, column_number+1, item)                           

    #for (i == 0, i<len_lst, i++):#change this to the last number in the cell of the seet
            # for project in projects:
            #     for cont in contributions:
            #         if cont.project_id == project.id:
                        
            #             sh.write(idx+1, i, cont.amount) #row['reciept_total'])
            # #     sh.write(idx+1, 2, row.tithe) #row['tithe'])
    #     sh.write(idx+1, 3, row.camp_off)#row['camp_off'])
    #     sh.write(idx+1, 4, row.sabbath_sch)#row['sabbath_sch'])
    #     sh.write(idx+1, 5, row.birthday)#row['birthday'])
    #     sh.write(idx+1, 6, row.divine)#row['divine'])
    #     sh.write(idx+1, 7, row.third_sabb)#row['third_sabb'])
    #     sh.write(idx+1, 8, row.general_conf)#row['general_conf'])
    #     sh.write(idx+1, 9, row.operation_unity)#row['operation_unity'])
    #     sh.write(idx+1, 10, row.prime_radio)#row['prime_radio'])
    #     sh.write(idx+1, 11, row.lunch)#row['lunch'])
    #     sh.write(idx+1, 12, row.evangelism)#row['evangelism'])
    #     sh.write(idx+1, 13, row.building)#row['building'])
    #     sh.write(idx+1, 14, row.other_funds)#row['other_funds'])
    
    workbook.save(output)
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=giving_report.xls"})

    


db.create_all()
if __name__ == '__main__':
    app.run(debug=True) 
#ui.run()          
