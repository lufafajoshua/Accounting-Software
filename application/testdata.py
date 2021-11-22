from wtforms.form import Form
from wtforms.fields import FieldList, FormField, IntegerField, BooleanField, StringField
from jinja2 import Template

from flask_table import Table, Col

from bs4 import BeautifulSoup


def pretty_html(html):
    return BeautifulSoup(html, 'html.parser').prettify()


class InputGridRecordForm(Form):
    """A form for entering inputgrid record row data"""
    id = IntegerField('Continent Record ID')
    select = BooleanField('Select')
    stringcol1 = StringField('String Col #1')
    intcol1 = IntegerField('Int Col #1')

class InputGridTableForm(Form):
    """A form for one or more InputGridRecords"""
    gridtblrecords = FieldList(FormField(InputGridRecordForm), min_entries=1)

def from_template(form):
    template = '''
    <table>
        <tbody>
            {{ form.csrf_token }}
            {% for grid_record in form.gridtblrecords %}
                <tr>
                    {% for field in grid_record %}
                        <td>{{ field() }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>'''
    return pretty_html(Template(template, autoescape=True).render(form=form))

def from_flask_table(form):
    class MyTable(Table):
        id = Col('ID')
        select = Col('Select')
        stringcol1 = Col('Stringcol1')
        intcol1 = Col('Intcol1')

        def thead(self):
            # No thead because there was none in the example
            return ''

    return pretty_html(
        Template(r'{{ table }}', autoescape=True).render(table=MyTable(form.gridtblrecords))
    )

form = InputGridTableForm()
html_from_template = from_template(form)
html_from_flask_table = from_flask_table(form)

print ('From template:')
print ('==============')
print (html_from_template)

print ('From flask_table:')
print ('=================')
print (html_from_flask_table)

print ('=================')

if html_from_template == html_from_flask_table:
    print ('All matches')
else:
    print ('Not the same')







    # from werkzeug.datastructures import MultiDict

    # @blueprint.route('/list/inputgrid', methods=['GET', 'POST'])
    # def list_inputgrid():
    #     """workout the basic input grid."""
    #     records = InputGrid1.query.order_by('id').all()
    #     data = {'gridtblrecords': records}
    #     form = InputGridTableForm(request.form, data=MultiDict(data))

    #     return render_template('inputgrid.html', form=form)


#app.py
from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from datetime import datetime
  
app = Flask(__name__)
  
app.secret_key = "caircocoders-ednalan-2020"
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testingdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
  
@app.route('/')
def main():
    return redirect('/useradmin')
    
@app.route('/useradmin')
def useradmin():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM employee")
    employee = cur.fetchall()
    return render_template('useradmin.html', employee=employee)
 
@app.route('/updateemployee', methods=['POST'])
def updateemployee():
        pk = request.form['pk']
        name = request.form['name']
        value = request.form['value']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if name == 'name':
           cur.execute("UPDATE employee SET name = %s WHERE id = %s ", (value, pk))
        elif name == 'email':
           cur.execute("UPDATE employee SET email = %s WHERE id = %s ", (value, pk))
        elif name == 'phone':
           cur.execute("UPDATE employee SET phone = %s WHERE id = %s ", (value, pk))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
             
if __name__ == '__main__':
    app.run(debug=True)


//templates/useradmin.html
<html>
  <head>
    <meta name="viewport" content="width=device-width">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>DataTable Inline Editing using Python Flask MySQLdb jquery ajax and X-Editable</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />
        <script src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.10.12/js/dataTables.bootstrap.min.js"></script>  
        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/dataTables.bootstrap.min.css" />
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/css/bootstrap-editable.css" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/js/bootstrap-editable.js"></script>
<script type="text/javascript" language="javascript">
$(document).ready(function(){
    var dataTable = $('#sample_data').DataTable();
    $('#sample_data').editable({
        container:'body',
        selector:'td.name',
        url:'/updateemployee',
        title:'Name',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
 
    $('#sample_data').editable({
        container:'body',
        selector:'td.email',
        url:'/updateemployee',
        title:'Email',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
 
    $('#sample_data').editable({
        container:'body',
        selector:'td.phone',
        url:'/updateemployee',
        title:'Phone',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
}); 
</script>
    </head>
    <body>
        <div class="container">
            <h3 align="center">DataTable Inline Editing using Python Flask MySQLdb jquery ajax and X-Editable</h3>
            <br />
            <div class="panel panel-default">
                <div class="panel-heading">DataTable</div>
                <div class="panel-body">
                    <div class="table-responsive">
                        <table id="sample_data" class="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in employee %}
                                <tr>
                                    <td data-pk="{{row.id}}">{{row.id}}</td>
                                    <td data-name="name" class="name" data-type="text" data-pk="{{row.id}}">{{row.name}}</td>
                                    <td data-name="email" class="email" data-type="text" data-pk="{{row.id}}">{{row.email}}</td>
                                    <td data-name="phone" class="phone" data-type="text" data-pk="{{row.id}}">{{row.phone}}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <br />
        <br />
    </body>
</html>





?






#app.py
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
  
app = Flask(__name__)
         
app.secret_key = "caircocoders-ednalan"
         
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testingdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
      
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM topphpframework ORDER BY id ASC")
    topphpframework = cur.fetchall() 
    return render_template('index.html', topphpframework=topphpframework)
     
@app.route("/ajax",methods=["POST","GET"])
def ajax():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    if request.method == 'POST':
        getid = request.form['id']
        getname = request.form['name']
        print(getid)
        cur.execute("UPDATE topphpframework SET name = %s WHERE id = %s ", [getname, getid])
        mysql.connection.commit()       
        cur.close()
    return jsonify('Record updated successfully')
 
if __name__ == "__main__":
    app.run(debug=True)


//templates/index.html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Python Flask Table Edit using jquery ajax andd mysql Database</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
<style>
body
{
font-family:Arial, Helvetica, sans-serif;
font-size:16px;
}
.head
{
background-color:#333;
color:#FFFFFF
}
.edit_tr:hover
{
background:url(/static/img/edit.png) right no-repeat #80C8E5;
cursor:pointer;
}
.editbox
{
display:none
}
.editbox
{
font-size:16px;
width:270px;
background-color:#ffffcc;
border:solid 1px #000;
padding:4px;
}
td
{
padding:10px;
}
th
{
font-weight:bold;
text-align:left;
padding:4px;
}
</style>
<script type="text/javascript">
$(document).ready(function() {
  $(".edit_tr").click(function() {
    var ID=$(this).attr('id');
    $("#first_"+ID).hide();
    $("#first_input_"+ID).show();
  }).change(function(){
      var ID=$(this).attr('id');
      var first=$("#first_input_"+ID).val();
      var dataString = 'id='+ ID +'&name='+first;
      $("#first_"+ID).html('<img src="/staticf/img/loader.gif" />');
      if(first.length>0){
        $.ajax({
          type: "POST",
          url: "/ajax",
          data: dataString,
          cache: false,
          success: function(html)
          {
            $("#first_"+ID).html(first);
          }
        });
      }else{
        alert('Enter something.');
      }
  });
    
  $(".editbox").mouseup(function() {
   return false
  });
  $(document).mouseup(function() {
      $(".editbox").hide();
      $(".text").show();
  });
});
</script>
</head>
<body>
<center><p><h1>Python Flask Table Edit using jquery ajax and mysql Database</h1></p></center>
<div style="margin:0 auto; width:350px; padding:10px; background-color:#fff;"> 
<table width="100%" border="0">
 <tr class="head">
 <th>PHP Frameworks</th>
 </tr>
 {% for row in topphpframework %}
  <tr id="{{row.id}}" bgcolor="#f2f2f2" class="edit_tr">
    <td width="50%" class="edit_td">
    <span id="first_{{row.id}}" class="text">{{row.name}}</span>
    <input type="text" name="name" value="{{row.name}}" class="editbox" id="first_input_{{row.id}}" />
    </td>
  </tr>
  {% endfor %}
</table>
</div>
</body>
</html>

