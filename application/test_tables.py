from flask_table import Table, Col, LinkCol, ButtonCol

class Entry_Table(Table):#This will be used in creating entries or for data input
    classes = ["table", "table-hover", "table-striped", "clickable-row", "sortable"]
    myclass  = ["hover", "important"]
    id = Col('id', show=False)
    full_name = Col('Full name')
    reciept_no = Col('Receipt Number')
    #date_created = Col('Date Created')
    reciept_total = Col('Receipt Total')
    tithe = Col('Tithe')
    camp_off = Col('Camp Meeting Offering')
    sabbath_sch = Col('Sabbath School')
    birthday = Col('Birth Day')
    divine = Col('Divine')
    third_sabb = Col('Thirteenth sabbath')
    general_conf = Col('General Conference')
    operation_unity = Col('Operation Unity')
    prime_radio = Col('Prime radio')
    lunch = Col('Lunch')
    evangelism = Col('Evangelism')
    building = Col('Local Church Building')
    other_funds = Col('Other Funds')

class Project_table(Table):
    classes = ["table", "table-hover", "table-striped", "clickable-row", "sortable"]
    myclass  = ["hover", "important"]
    id = Col('id', show=False)
    project_name = Col('Name')
    #date_created = Col('Date Created')
    project_type = Col('Type')
    Owner = Col('Owner')
    acct_balance = Col('Account Balance')
    acct_status = Col('Status')

class Contribution_table(Table):
    classes = ["table", "table-hover", "table-striped", "clickable-row", "sortable"]
    myclass  = ["hover", "important"]
    id = Col('id', show=False)
    amount = Col('Amount')#THis will display the amount collected from a particular contribution

    


