CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `users` (`id`, `username`, `name`) VALUES
(8, 'Batosai23', 'Batosai Ednalan'),
(9, 'caite', 'Caite Ednalan'),
(11, 'NarutoUzumaki', 'Naruto Uzumaki'),
(12, 'SasukeUchiha', 'Sasuke Uchiha');

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;


#app.py
from flask import Flask, request, render_template, jsonify
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql
  
app = Flask(__name__)
    
mysql = MySQL()
   
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
  
@app.route('/')
def home():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from users order by id")
        userslist = cursor.fetchall()
        return render_template('index.html',userslist=userslist)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
 
@app.route("/update",methods=["POST","GET"])
def update():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            field = request.form['field'] 
            value = request.form['value']
            editid = request.form['id']
             
            if field == 'username':
               sql = "UPDATE users SET username=%s WHERE id=%s"
            if field == 'name':        
                sql = "UPDATE users SET name=%s WHERE id=%s"
 
            data = (value, editid)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            success = 1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
  
if __name__ == "__main__":
    app.run()





//templates/index.html
<!doctype html>
<html>
<head>
<title>Live Editable Table using Python Flask Mysql and Jquery Ajax</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />    
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<script type='text/javascript'>
$(document).ready(function(){
  
 // Show Input element
 $('.edit').click(function(){
  $('.txtedit').hide();
  $(this).next('.txtedit').show().focus();
  $(this).hide();
 });
 
 // Save data
 $(".txtedit").focusout(function(){
   
  // Get edit id, field name and value
  var id = this.id;
  var split_id = id.split("_");
  var field_name = split_id[0];
  var edit_id = split_id[1];
  var value = $(this).val();
   
  // Hide Input element
  $(this).hide();
 
  // Hide and Change Text of the container with input elmeent
  $(this).prev('.edit').show();
  $(this).prev('.edit').text(value);
 
  $.ajax({
   url: '/update',
   type: 'post',
   data: { field:field_name, value:value, id:edit_id },
   success:function(response){
      if(response == 1){ 
         console.log('Save successfully'); 
      }else{ 
         console.log("Not saved.");  
      }
   }
  });
  
 });
 
});
</script>
</head>
<body >
<div class="container" >
    <div class="row" style="padding:50px;">
        <p><h1>Live Editable Table using Python Flask Mysql and Jquery Ajax</h1></p>
        <table width='100%' border='0'>
         <tr>
          <th width='10%'>ID</th>
          <th width='40%'>Username</th>
          <th width='40%'>Name</th>
         </tr>
         {% for row in userslist %}    
         <tr>
          <td>{{row.id}}</td>
          <td> 
            <div class='edit' > {{row.username}}</div> 
            <input type='text' class='txtedit' value='{{row.username}}' id='username_{{row.id}}' >
          </td>
          <td> 
           <div class='edit' >{{row.name}} </div> 
           <input type='text' class='txtedit' value='{{row.name}}' id='name_{{row.id}}' >
          </td>
         </tr>
         {% endfor %} 
        </table>
   </div>
</div>
<style>
.edit{
 width: 100%;
 height: 25px;
}
.editMode{
 border: 1px solid black;
}
table {
 border:3px solid lavender;
 border-radius:3px;
}
table tr:nth-child(1){
 background-color:#4285f4;
}
table tr:nth-child(1) th{
 color:white;
 padding:10px 0px;
 letter-spacing: 1px;
}
table td{
 padding:10px;
}
table tr:nth-child(even){
 background-color:lavender;
 color:black;
}
.txtedit{
 display: none;
 width: 99%;
 height: 30px;
}
</style>
</body>
</html>  


#####Different code for date filtering
qry = DBSession.query(User).filter(
        and_(User.birthday <= '1988-01-17', User.birthday >= '1985-01-17'))
# or same:
qry = DBSession.query(User).filter(User.birthday <= '1988-01-17').\
        filter(User.birthday >= '1985-01-17')



Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])        
