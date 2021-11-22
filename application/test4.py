import pandas as pd

lst = []
a = [('a', [5,7,8,4,0]), ('b', [2,3,5,0,9]), ('c', [0,6,7,10,3])]
b = [('e', 2), ('f', 1), ('g', 3)]

p = []
q = []
for x in a:
    #for y in b:
    print(x[0], x[1])
    p.append(x[0])
    
    q.append(x[1])
    print(q)
    for y in x[1]:
        print(y)
print(p)        
print(q)
new = [[row[i] for row in q] for i in range(len(q[1]))]
print(new)







sql_query = ("SELECT * FROM account_projects")#select all the data
db2.dbcursor.execute(sql_query)
results = db2.dbcursor.fetchall()
account_ids = []
for row in results:
    accounts = row[2]
    account_ids.append(accounts)
for x in account_ids:#Get the id of the specified project
        #print(account_project)
        if x == project.id:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
            sql_query2 = "DELETE FROM account_projects WHERE project_id='%s'" %project.id
            db2.dbcursor.execute(sql_query2)
            db2.commit_db() 










sql_query = ("SELECT * FROM account_projects")#select all the data
    db2.dbcursor.execute(sql_query)
    results = db2.dbcursor.fetchall()
    account_projects = []
    for row in results:
        projects = row[1]
        account_projects.append(projects)
        print(account_projects)
    if account:
        print(account.accountprojects)    
        """Delete all contributions with the given account"""        
        for cont in contributions:
            if cont.account_id == account.id:
                db.session.delete(cont)
                db.session.commit() 
        """Delete all account projects with the account_id of the account being deleted"""
        for account_project in account_projects:
            #print(account_project)
            if account_project == account.id:
                sql_query2 = "DELETE FROM account_projects WHERE account_id='%s'" %account.id
                db2.dbcursor.execute(sql_query2)
                db2.commit_db() 