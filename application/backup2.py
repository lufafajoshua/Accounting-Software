
@app.route('/all_givings', methods=['GET', 'POST'])
def all_givings():
    qry = db.session.query(Giving).filter(Giving.id==1)#Id from the invoking object
    giving = qry.first()
    qry2 = db.session.query(Project).filter(Project.acct_status=='Active')#Get all the active projects
    projects = qry2.all()
    contributions = giving.contributions
    entries = giving.entries
    headers = ['ID', 'Reciept Total', 'Tithe', 'Campmeeting Offering', 'sabbath School', 'Birthday Thanks', 'Divine', '13th Sabbath', 'General Conference', 'Operation Unity', 'Prime Radio', 'Lunch', 'Evangelism', 'Building', 'Other Funds']

    values = []
    ids = []
    project_lst = []    
    for project in projects:
        
        values1 = []#Captures the individual contributions
        values2 = []#Captures the id's of the contributions for editing in the frontend
        accounts_lst = []
        
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
    for s in ids:
        print(s)
    print(accounts_lst) 
    print(project_lst)   
    df = pd.DataFrame(values)    
    trans_df = df.transpose()
    print(trans_df)
    df2 = pd.DataFrame(ids)
    trans_df2 = df2.transpose()
    print(trans_df2)
    result = df2.to_html()#Convert the dataframe into an html table
    result2 = df.to_html()
    text_file = open("pandas.html", "w")
    text_file.write(result)
    text_file.close()
    list_df = [trans_df, trans_df2]
    output = ""
    for index, df in enumerate(list_df):
        output += df.to_html() + '<br>'      

        # with open("application/templates/accounts/pandas.html", "w") as f:
        #     f.writelines(output)  
        
    return render_template('accounts/giving.html', headers=headers, entries=entries, projects=project_lst, values=values, ids=ids, contributions=contributions, result=result, accounts=accounts_lst)










#GEt the totals from all the rows in the entries table
    qry1 = "SELECT tithe, SUM(tithe) FROM entries "
    db2.dbcursor.execute(qry1)
    tithe = db2.dbcursor.fetchone()
    qry2 = "SELECT camp_off, SUM(camp_off) FROM entries "
    db2.dbcursor.execute(qry2)
    camp_off = db2.dbcursor.fetchone()
    qry3 = "SELECT sabbath_sch, SUM(sabbath_sch) FROM entries "
    db2.dbcursor.execute(qry3)
    sabbath_sch = db2.dbcursor.fetchone()
    qry4 = "SELECT birthday, SUM(birthday) FROM entries "
    db2.dbcursor.execute(qry4)
    birthday = db2.dbcursor.fetchone()
    qry5 = "SELECT divine, SUM(divine) FROM entries "
    db2.dbcursor.execute(qry5)
    divine = db2.dbcursor.fetchone()
    qry6 = "SELECT third_sabb, SUM(third_sabb) FROM entries "
    db2.dbcursor.execute(qry6)
    third_sabb = db2.dbcursor.fetchone()
    qry7 = "SELECT general_conf, SUM(general_conf) FROM entries "
    db2.dbcursor.execute(qry7)
    general_conf = db2.dbcursor.fetchone()
    qry8 = "SELECT operation_unity, SUM(operation_unity) FROM entries "
    db2.dbcursor.execute(qry8)
    operation_unity = db2.dbcursor.fetchone()
    qry9 = "SELECT prime_radio, SUM(prime_radio) FROM entries "
    qry10 = "SELECT lunch, SUM(lunch) FROM entries "
    qry11 = "SELECT evangelism, SUM(evangelism) FROM entries "
    qry12 = "SELECT building, SUM(building) FROM entries "
    qry13 = "SELECT other_funds, SUM(other_funds) FROM entries "

   