
class AllocateTransaction(db.Model):
    __tablename__ = 'allocated'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, default=0) 
    field = db.Column(db.String(120), index=False)  
    today = datetime.date.today()
    date_created = db.Column(db.DateTime, index=False, nullable=False, default=today)
    authorizer = db.Column(db.String(120), index=False)# Person authorising the transaction
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('member_account.id'))
    giving_id = db.Column(db.Integer, db.ForeignKey('giving.id'))







@app.route('/edit_allocate/<int:id>', methods=['GET', 'POST'])
def edit_allocate(id):
    qry = db.session.query(Account).filter(Account.id==id)
    account = qry.first() 
    #Select the giving that is being contributed to
    #Display the currently created givings 
    #Redirect to another page to select the field and set the amount
    form = SelectForm(request.form)
    #Select the most current givings to select from, set the ordering of the choices
    form.giving.choices = [(d.id, d.date_created) for d in Giving.query.all()]
    if request.method == 'POST':
        selected_giving = Giving.query.get(form.giving.data)
        giving = selected_giving
        #Return redirect to the 
        return redirect(url_for('edit_allocate_money', account_id=account.id, giving_id=giving.id))
    return render_template('accounts/edit-allocate.html', form=form, account=account)   


"""Edit allocated money from the account"""

#You have the account and the giving being allocated money to.
@app.route('/edit_allocate_money/<int:account_id>')
@app.route('/edit_allocate_money/<int:account_id>/<int:giving_id>', methods=['GET', 'POST'])
def edit_allocate_money(account_id, giving_id):
        
    qry = db.session.query(Giving).filter(Giving.id==giving_id)#Get all the active projects
    giving = qry.first()
    qry2 = db.session.query(Account).filter(Account.id==account_id)#Get all the active projects
    account = qry2.first()
    print(account.acct_balance)
    #Get the entry in giving entries where the account is the one selected
    qry3 = db.session.query(Entry).filter(id==id).filter(Entry.account_id==account.id).filter(Entry.giving_id==giving.id)
    entry = qry3.first()
    print(entry.id)
    qry4 = db.session.query(AllocateTransaction).filter(id==id).filter(AllocateTransaction.account_id==account.id).filter(AllocateTransaction.giving_id==giving.id).filter(AllocateTransaction.entry_id==entry.id)
    transaction = qry4.first()
    form  = AllocateForm(request.form)
    amount = form.amount.data#incase of erors use form.data['search] after passing the request.form argument in the form instatiation
    msg = ''
    headers = ['ID', 'Reciept Total', 'Tithe', 'Campmeeting Offering', 'sabbath School', 'Birthday Thanks', 'Divine', '13th Sabbath', 'General Conference', 'Operation Unity', 'Prime Radio', 'Lunch', 'Evangelism', 'Building', 'Other Funds']
    
    if request.method == 'POST':
        if account.acct_balance != 0 and amount <= account.acct_balance:
            if form.data['select'] == 'Tithe' and transaction.field=='tithe':
                #Create a variable to store the original amount as it is entered
                current_balance = account.acct_balance + entry.tithe
                print(current_balance)
                new = form.amount.data
                transaction.amount = amount 
                new_balance = current_balance - amount
                #new_balance = account.acct_balance - amount
                print(new_balance)
                entry.tithe = new
                account.acct_balance = new_balance
                #db.session.add(entry)
                #db.session.add(account)
                db.session.commit()   
            elif form.data['select'] == 'Campmeeting Offering' and transaction.field=='camp_off':
                new = entry.camp_off + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.camp_off = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Sabbath School' and transaction.field=='sabbath_sch':
                new = entry.sabbath_sch + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.sabbath_sch = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Birthday Thanks' and transaction.field=='birthday':
                new = entry.birthday + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.birthday = new
                account.acct_balance = new_balance
                db.session.add(entry)
                db.session.add(account)
                db.session.commit()      
            elif form.data['select'] == 'Divine' and transaction.field=='divine':
                new = entry.divine + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.divine = new
                account.acct_balance = new_balance
                db.session.commit()     
            elif form.data['select'] == 'Thirteenth sabbath' and transaction.field=='third_sabb':
                new = entry.third_sabb + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.third_sabb = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'General Conference' and transaction.field=='general_conf':
                new = entry.general_conf + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.general_conf = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Operation Unity' and transaction.field=='operation_unity':
                new = entry.operation_unity + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.operation_unity = new
                account.acct_balance = new_balance
                db.session.commit()   
            elif form.data['select'] == 'Prime Radio' and transaction.field=='prime_radio':
                new = entry.prime_radio + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.prime_radio = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Lunch' and transaction.field=='lunch':
                new = entry.lunch + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.lunch = new
                account.acct_balance = new_balance
                db.session.commit()   
            elif form.data['select'] == 'Evangelism' and transaction.field=='evangelism':
                new = entry.evangelism + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.evangelism = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Building' and transaction.field=='building':
                new = entry.building + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.building = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Other Funds' and transaction.field=='other_funds':
                new = entry.other_funds + form.amount.data 
                transaction.amount = amount
                new_balance = account.acct_balance - amount
                entry.other_funds = new
                account.acct_balance = new_balance
                db.session.commit()  
            else:
                #Return message that the field doesnt exist
                msg = 'Cant finish that operation '
        else:
            msg = 'Your account balance is low to complete operation'        
    

    return render_template('accounts/editallocate.html', account=account, headers=headers, giving=giving, entry=entry,form=form, msg=msg)#return to the admit process

@app.route('/allocate/<int:id>', methods=['GET', 'POST'])
def allocate(id):
    #Get the account allocating the money and then redirect to the selct page to get the project
    qry = db.session.query(Account).filter(Account.id==id)
    account = qry.first() 

    #Select the giving that is being contributed to
    #Display the currently created givings 
    #Redirect to another page to select the field and set the amount
    form = SelectForm(request.form)
    #Select the most current givings to select from, set the ordering of the choices
    form.giving.choices = [(d.id, d.date_created) for d in Giving.query.all()]
    if request.method == 'POST':
        selected_giving = Giving.query.get(form.giving.data)
        giving = selected_giving
        #Return redirect to the 
        return redirect(url_for('allocate_money', account_id=account.id, giving_id=giving.id))
    return render_template('accounts/allocate.html', form=form, account=account)   

#You have the account and the giving being allocated money to.
@app.route('/allocate_money/<int:account_id>')
@app.route('/allocate_money/<int:account_id>/<int:giving_id>', methods=['GET', 'POST'])
def allocate_money(account_id, giving_id):
    #Get the account along with the giving being allocated money
    #Get the entry that belongs to that account

    qry = db.session.query(Giving).filter(Giving.id==giving_id)#Get all the active projects
    giving = qry.first()
    qry2 = db.session.query(Account).filter(Account.id==account_id)#Get all the active projects
    account = qry2.first()
    print(account.acct_balance)
    #Get the entry in giving entries where the account is the one selected
    qry3 = db.session.query(Entry).filter(id==id).filter(Entry.account_id==account.id).filter(Entry.giving_id==giving.id)
    entry = qry3.first()
    print(entry.id)
    form  = AllocateForm(request.form)
    amount = form.amount.data#incase of erors use form.data['search] after passing the request.form argument in the form instatiation
    msg = ''
    #Validate that the account doesnt have a zero balance and that the amount is less than or equal to the account balance
    if request.method == 'POST':
        transaction = AllocateTransaction()
        if account.acct_balance != 0 and amount <= account.acct_balance:
            if form.data['select'] == 'Tithe':
                #current_balance = account.acct_balance + entry.tithe
                #print(current_balance)
                transaction.amount = form.amount.data
                transaction.field = 'tithe'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.tithe + form.amount.data 
                #new_balance = current_balance - amount
                new_balance = account.acct_balance - amount
                print(new_balance)
                entry.tithe = new
                account.acct_balance = new_balance
                #db.session.add(entry)
                #db.session.add(account)
                db.session.commit()   
            elif form.data['select'] == 'Campmeeting Offering':
                """Create a transaction for the money being allocated a field"""    
                transaction.amount = form.amount.data
                transaction.field = 'camp_off'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit()     

                new = entry.camp_off + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.camp_off = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Sabbath School':

                transaction.amount = form.amount.data
                transaction.field = 'sabbath_sch'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit()     

                new = entry.sabbath_sch + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.sabbath_sch = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Birthday Thanks':

                
                transaction.amount = form.amount.data
                transaction.field = 'birthday'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.birthday + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.birthday = new
                account.acct_balance = new_balance
                db.session.add(entry)
                db.session.add(account)
                db.session.commit()      
            elif form.data['select'] == 'Divine':

                transaction.amount = form.amount.data
                transaction.field = 'divine'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.divine + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.divine = new
                account.acct_balance = new_balance
                db.session.commit()     
            elif form.data['select'] == 'Thirteenth sabbath':

                transaction.amount = form.amount.data
                transaction.field = 'third_sabb'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.third_sabb + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.third_sabb = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'General Conference':

                transaction.amount = form.amount.data
                transaction.field = 'general_conf'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 


                new = entry.general_conf + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.general_conf = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Operation Unity':

                transaction.amount = form.amount.data
                transaction.field = 'operation_unity'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.operation_unity + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.operation_unity = new
                account.acct_balance = new_balance
                db.session.commit()   
            elif form.data['select'] == 'Prime Radio':

                transaction.amount = form.amount.data
                transaction.field = 'prime_radio'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.prime_radio + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.prime_radio = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Lunch':

                transaction.amount = form.amount.data
                transaction.field = 'lunch'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.lunch + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.lunch = new
                account.acct_balance = new_balance
                db.session.commit()   
            elif form.data['select'] == 'Evangelism':

                transaction.amount = form.amount.data
                transaction.field = 'evangelism'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.evangelism + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.evangelism = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Building':

                transaction.amount = form.amount.data
                transaction.field = 'building'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.building + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.building = new
                account.acct_balance = new_balance
                db.session.commit()  
            elif form.data['select'] == 'Other Funds':

                transaction.amount = form.amount.data
                transaction.field = 'other_funds'
                transaction.entry_id = entry.id
                transaction.giving_id = giving.id
                transaction.account_id = account.id
                db.session.add(transaction)
                db.session.commit() 

                new = entry.other_funds + form.amount.data 
                new_balance = account.acct_balance - amount
                entry.other_funds = new
                account.acct_balance = new_balance
                db.session.commit()  
            else:
                #Return message that the field doesnt exist
                msg = 'Cant finish that operation '
        else:
            msg = 'Your account balance is low to complete operation'        
    
    return render_template('accounts/allocate-money.html', account=account, giving=giving, form=form, msg=msg)#return to the admit process




@app.route('/allocations/<int:account_id>', methods=['GET', 'POST'])
def my_allocations(account_id):
    qry = db.session.query(Account).filter(Account.id==account_id)#Get all the active projects
    account = qry2.first()

    allocations = account.allocations
    entries = []

    return render_template('accounts/allocations', allocations=allocations)











ns)        
        
        """Compute the total contributions and the remaining balance of a project"""
        total_contribution = sum([cont.amount for cont in project_contributions])
        total_invoices = sum([inv.amount for inv in project_invoices])
        #SEt the total amount collected for each project in the giving
        if project.transaction != None:
            total_transactions = sum([trans.amount for trans in project_transactions])#Get all money added to a project via transactions
            """Add the total contribution to the total amount collected for a project"""
            total_collected = total_contribution + total_transactions
            project.total_collected = total_collected 
            if total_collected != 0 and total_collected >= total_invoices:#Check for another requirement for this calculation
                new_acct_balance = total_collected - total_invoices
                project.acct_balance = new_acct_balance
                db.session.commit()
            else:
                print('No contributions Yet')    

        else:
            if total_contribution != 0 and total_contribution >= total_invoices:#Check for another requirement for this calculation
                new_acct_balance = total_contribution - total_invoices
                project.acct_balance = new_acct_balance
                project.total_collected = total_contribution
                db.session.commit()
            else:
                print('No contribution yet')    

        """Get the project account balance and deduct the project invoices"""
        total_invoices = sum([inv.amount for inv in project_invoices])
        if total_contribution != 0 and total_contribution >= total_invoices:#Check for another requirement for this calculation
            new_acct_balance = total_contribution - total_invoices
            project.acct_balance = new_acct_balance
            db.session.commit()
            print('Total cotribution:', total_contribution)
            print(project.acct_balance)
        else:#Return a message that the account has not 
            print("You dont have enough money")
        print('Total cotribution:', total_contribution)
        print(project.acct_balance)  



"""Backup for view_project view or function"""

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

