

class Account(db.Model):#This is the admins model.py file
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=False, nullable=False)
    password = db.Column(db.String, index=False, nullable=False)  

    def __repr__(self):
        return '<Account {}>'.format(self.username)      







@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    #This methid uses the form-data directly from the login.html file not from the defined wtf forms in forms.py file 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #account = Account()#Query the account object directly without assigning it to a variable
        qry = db.session.query(Account).filter(id==id).filter(Account.username.contains(username)).filter(Account.password.contains(password))
        #Query the database to see if the account exists
        existing_account = qry.first()
        if existing_account:
            session['loggedin'] = True
            session['id'] = existing_account.id
            session['username'] = existing_account.username
            msg = 'successfully logged in' 
            return redirect('home.html')
        else:
            msg = 'Invalid username or password!'
            #return redirect('login') redirect back to the login page
    return render_template('login.html', msg=msg)         

def save_user(account, form, new=False):# This view is to save the new user for the system
    account.username = form.username.data
    account.password = form.password.data
    if new:
        db.session.add(account)
        db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AdminForm(request.form)
    username = form.username.data
    password = form.password.data
    password1 = form.password1.data
    msg = ''
    if request.method == 'POST' and form.validate():
        account = Account()
        #Query the database and retrieve an account with similar data and if it exists, display errors
        qry = db.session.query(Account).filter(id==id).filter(Account.username.contains(username)).filter(Account.password.contains(password))
        existing_account = qry.first()
        if existing_account:
            msg = 'Account already exists'
        # elif not re.match(r'[A-Za-z0-9]+', username):#Validate username to use only numbers and letters
    #       msg = 'User name must contain only letters and numbers'#Dont forget to check how to validate frontend fields with re.match 
        elif password != password1:#authenticate password validation
            msg = 'Passwords didnt match'    
        else:  
            save_user(account, form, new=True)  
            msg = 'Successfully registered' 
    
    elif request.method == 'POST':
        msg = 'Please Fill in the form'
    return render_template('register.html', form=form, msg=msg)    
