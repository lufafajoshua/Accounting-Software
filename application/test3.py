
L = ['one','two','three','four','five','six','seven','eight','nine']
m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
n = ['one', 'thirteen', 'twenty']

x = list(zip(L,n))
print(x)

lst = ['Geeks', 'For', 'Geeks', 'is', 'portal', 'for', 'Geeks']
  
# list of int
lst2 = [11, 22, 33, 44, 55, 66, 77]

print(list(zip(lst,lst2)))


p = []
for i in m:
    s = list(zip(i))
    p.append(s)
print(p)





TABLE 1 
<table  id ="table1">
<thead>
<tr bgcolor="#f0f0f0">
<td nowrap=""><b>COLUMN_NAME</b></td>       
<td nowrap=""><b>DATA_TYPE</b></td>     
<td nowrap=""><b>IS_NULLABLE</b></td>       
<td nowrap=""><b>CHARACTER_MAXIMUM_LENGTH</b></td>      
<td nowrap=""><b>NUMERIC_PRECISION</b></td>
<td nowrap=""><b>COLUMN_KEY</b></td>
</tr>
</thead>
<tbody>
<tr>        
  <td nowrap="">CountryCode   </td>
  <td nowrap="">int   </td>
  <td nowrap="">YES   </td>
       <td nowrap="">NULL </td>
       <td nowrap="">10   </td>
  </tr>
  <tr>      
    <td nowrap="">Number   </td>
    <td nowrap="">varchar   </td>
    <td nowrap="">NO   </td>
    <td nowrap="">20   </td>
            <td nowrap="">NULL </td>
            <td nowrap="">PRI </td> 
       </tr><tr>        
    <td nowrap="">Type   </td>
    <td nowrap="">tinyint   </td>
    <td nowrap="">NO   </td>
            <td nowrap="">NULL </td>
            <td nowrap="">3   </td>
            <td nowrap="">PRI </td>     
        </tr>
    <tr>        
        <td nowrap="">Date   </td>
        <td nowrap="">smalldatetime   </td>
        <td nowrap="">NO   </td>            
        <td nowrap="">NULL </td>
        <td nowrap="">NULL </td>
    </tr>
</tbody>

</table>
<br>
<br>
TABLE 2
<table  id ="table2">
  <thead>
    <tr bgcolor="#f0f0f0">
<td nowrap=""><b>COLUMN_NAME</b></td>
<td nowrap=""><b>DATA_TYPE</b></td>
<td nowrap=""><b>IS_NULLABLE</b></td>
<td nowrap=""><b>CHARACTER_MAXIMUM_LENGTH</b></td>
<td nowrap=""><b>NUMERIC_PRECISION</b></td>
<td nowrap=""><b>COLUMN_KEY</b></td>
    </tr>
</thead>
<tbody>
    <tr>            
            <td nowrap="">CountryCode</td>
            <td nowrap="">int</td>
            <td nowrap="">NO</td>
            <td nowrap="">NULL</td>
            <td nowrap="">10</td>
            <td nowrap=""></td>
        </tr>
        <tr>    
            <td nowrap="">PhoneNumber</td>
            <td nowrap="">varchar</td>
            <td nowrap="">NO</td>
            <td nowrap="">20</td>
            <td nowrap="">NULL</td>
            <td nowrap="">PRI</td>
        </tr>
<tr>        
            <td nowrap="">Type</td>
            <td nowrap="">tinyint</td>
            <td nowrap="">NO</td>
            <td nowrap="">NULL</td>
            <td nowrap="">3</td>
            <td nowrap="">PRI</td>
        </tr>
<tr>        
            <td nowrap="">EffectiveDate</td>
            <td nowrap="">datetime</td>
            <td nowrap="">NO</td>
            <td nowrap="">NULL</td>
            <td nowrap="">NULL</td>
            <td nowrap=""></td>
        </tr>
</tbody>
</table>

<center><input type="submit" value="Compare IVR & TNS" onclick="CompareTables();" /></center>







function compareTables(){
        var t1 = document.getElementById("table1")
    var t2 = document.getElementById("table2")
var t2rows = t2.find('tbody > tr');
t1.find('tbody > tr').each(function(index){
    var t1row = $(this);
    var t2row = $(t2rows[index]);
    var t2tds = t2row.find('td');

    t1row.find('td').each(function(index){
        if($(this).text().trim() != $(t2tds[index]).text().trim() ){
            console.log('difference: table1:('+$(this).text()+')  table2:('+$(t2tds[index]).text()+')');
            //set row in error
            return;
        }
    });

});
}























Another one 

<html>
<head>
    <title>Read Data from HTML Table uisng JavaScript</title>
    <style>
        th, td, p, input {
            font:14px Verdana;
        }
        table, th, td 
        {
            border: solid 1px #DDD;
            border-collapse: collapse;
            padding: 2px 3px;
            text-align: center;
        }
        th {
            font-weight:bold;
        }
    </style>
</head>

<body>
    <table id="empTable">
        <tr>    
            <th id="id">ID</th>
                <th id="emp">Employee Name</th>
                    <th id="age">Age</th>
        </tr>
        <tr><td>01</td><td>Alpha</td><td>37</td></tr>
        <tr><td>02</td><td>Bravo</td><td>29</td></tr>
        <tr><td>03</td><td>Charlie</td><td>32</td></tr>
    </table>

    <p><select name="select" id="opt">
        <option value="">--Select a Value--</option>
        <option value="id">ID</option>
        <option value="emp">Employee Name</option>
        <option value="age">Age</option></select>
    </p>

    <input type="button" id="bt" value="Show Data" onclick="showTableData()" />
    <p id="info" style="font-style:italic;"></p>
</body>

<script>    
    function showTableData() { 
        document.getElementById('info').innerHTML = ""; 
        var myTab = document.getElementById('empTable'); 
        var opt = document.getElementById("opt").value; 
        var index = document.getElementById(opt).cellIndex; 
        
        for (i = 1; i < myTab.rows.length; i++) { 
            var objCells = myTab.rows.item(i).cells; 
            
            for (var j = index; j <= index; j++) { 
                info.innerHTML = info.innerHTML + ' ' + objCells.item(j).innerHTML; 
            } 
            
            info.innerHTML = info.innerHTML + '<br />'; 
        } 
    }
</script>
</html>