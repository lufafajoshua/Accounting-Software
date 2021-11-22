from flask_table import Table, Col, LinkCol, ButtonCol

class Search_Results(Table):
    classes = ["table", "table-hover", "table-striped", "clickable-row", "sortable"]
    myclass  = ["hover", "important"]
    id = Col('id', show=False)
    full_name = Col('Full name')#Applying bootstrap to flask table
    gender = Col('Gender') 
    date_added = Col('Date Added', show=False)
    telephone_no = Col('Telephone No')#create a telephone form class which ths value subclasses 
    address = Col('Address', show=False) 
    a_o_residence = Col('Area of Residence') 
    d_o_birth = Col('Date Of Birth', show=False)#this stores the date of birth
    age = Col('Age', show=False)# I have disabled the table property to show the age field while displaying the search results 
    m_status = Col('Marital Status', show=False) 
    no_children = Col('Number of children', show=False) #number of children
    occupation = Col('Occupation', show=False) 
    l_o_educ = Col('Level of Education', show=False)#You Can show them if the user is convienient
    p_o_work = Col('Place of work', show=False)#place of work
    employer = Col('Employer', show=False)  
    nationality = Col('Nationality', show=False)
    tribe = Col('Tribe', show=False)
    clan = Col('Clan', show=False)
    ch_born = Col('Church born or not', show=False) 
    f_faith = Col('former Faith', show=False) # this is the former faith
    d_o_baptism = Col('Date Of Baptism', show=False)#date of baptism
    ch_of_baptism = Col('Church of baptism', show=False)#chrch of baptism
    ch_family = Col('church family')
    l_o_AY = Col('level of AY progression', show=False)
    lang_spoken = Col('Languages Spoken', show=False)#languages spoken
    skills = Col('Skills', show=False)#skills obtained by the member, text datatype
    inc_projects = Col('Income Generating Projects', show=False) #income generating projects, text 
    hobbies = Col('Hobbies', show=False)# text
    ch_programs = Col('Church Programs To Improve Upon', show=False)#ch programs to improve upon
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))#connect the edit function to the frontend with this column 
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
    profile = LinkCol('View Profile', 'view_profile', url_kwargs=dict(id='id'))

class ALL_Data(Table):#Table to display all available members in the database
    classes = ["table", "table-hover", "table-striped", "clickable-row", "sortable"]
    id = Col('id', show=False)
    full_name = Col('Full name')#Applying bootstrap to flask table
    gender = Col('Gender')
    a_o_residence = Col('Area of Residence') 
    ch_family = Col('church family')

class All_Departments(Table):#Table to display all available members in the database
    classes = ["table", "table-hover", "clickable-row", "sortable"]
    id = Col('id', show=False)
    name = Col('Name')
    department = LinkCol('View Department', 'department', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit', 'edit_department', url_kwargs=dict(id='id'))

class TimeTable(Table):#This will use dynamic creation of the table
    id = Col('id', show=False)
    church_name = Col('Name')
    #let the date label be passed from a select field and be supplied  by the user and should reflect the dates ie 01/01/10 
    date = Col('Date')#The date will nest another table that includes the activity and the person to runt that activity

class ActivityTable(Table):#This will be nested with the date column in the Time table
    #id = Col('id', show=False)
    activity = Col('Name')#The name of the activity 
    incharge = Col('Name')#The name of the person in charge

class Family_Results(Table):
    id = Col('id', show=False)
    classes = ["table", "table-hover", "table-striped", "clickable-row", "sortable"]
    myclass  = ["hover", "important"]
    full_name = Col('Full name')#Applying bootstrap to flask table
    gender = Col('Gender') 
    telephone_no = Col('Telephone No')#create a telephone form class which ths value subclasses 
    a_o_residence = Col('Area of Residence', show=False)  
    ch_family = Col('church family')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))#connect the edit function to the frontend with this column 
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
    profile = LinkCol('View Profile', 'view_profile', url_kwargs=dict(id='id'))

class All_Accounts(Table):
    id = Col('id', show=False)
    name = Col('Name')
    #account = LinkCol('View Account', 'view_account', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit', 'edit_account', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_account', url_kwargs=dict(id='id'))
    deposit_project = LinkCol('Contribute', 'deposit_project', url_kwargs=dict(id='id'))
    #allocate = LinkCol('Allocate', 'allocate', url_kwargs=dict(id='id'))
    deposit = LinkCol('Deposit', 'deposit', url_kwargs=dict(id='id'))
    view = LinkCol('View Account', 'view_account', url_kwargs=dict(account_id='id'))


class All_Projects(Table):
    id = Col('id', show=False)
    project_name = Col('Name') 
    edit = LinkCol('Edit', 'edit_project', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_project', url_kwargs=dict(id='id'))
    view = LinkCol('View Project', 'view_project', url_kwargs=dict(id='id'))
    invoice = LinkCol('Create Invoice', 'create_invoice', url_kwargs=dict(project_id='id'))

    #Delete , edit, View and add a project 


class All_Givings(Table):
    id = Col('id', show=False)
    date_created = Col('Date Created') 
    edit = LinkCol('Edit', 'edit_project', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_project', url_kwargs=dict(id='id'))
    view = LinkCol('View Giving', 'view_giving', url_kwargs=dict(giving_id='id'))
   