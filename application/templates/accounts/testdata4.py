<div class="printer-type">
<table width="580" border="0" class="printer-row">
  <tr>
    <td>&nbsp;</td>
    <td>8X10 in</td>
    <td>10X12 in</td>
    <td>8X10 in Memmo</td>
    <td>10X12 in Memmo</td>
    <td>11X14 in</td>
    <td>14X14 in</td>
    <td>14X17 in</td>
    <td>Total sheets/year</td>
  </tr>
  <tr>
    <td>Item 5700</td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>Item 5700</td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>FUJI DRYPIX 400</td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>AGFA Drystar 3000</td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td><input type="text" class="txtfld" placeholder="edit"></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>Total sheets/year</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
</table>
</div>
#html






 $('.txtfld').bind({
            keyup:function(){ 
         //total calculation
                    $(".printer-type tr:not(:first, last) td:last-child").text(function () {
                        var totalVal = 0;
                        $(this).prevAll().each(function () {
                            totalVal += parseInt($(this).children('.txtfld').val()) || 0;
                            //totalVal += parseInt( );
                        });
                        return totalVal;
                    });

                    $(".printer-type tr:last td").text(function (i) {
                        var totalVal = 0;
                        $(this).parent().prevAll().find("td:nth-child(" + (++i) + ")").each(function () {
                            totalVal += parseInt($(this).children('.txtfld').val()) || 0;
                            $(".printer-type tr:last td:first").text('Total sheets/year');
                        });
                        return totalVal;

                    });
					
					var count=0
					for(i=1;i<$('tr').length;i++){
						var trs=parseInt($('tr:eq('+i+')').find('td:last').text())
						count+=trs
					}
					$(".printer-type tr:last td:last").text(count)
                 
            }
        });







.txtfld{ width:50px;}
.printer-row{border-collapse: collapse;}
.printer-row td{border:1px solid #ccc;}























#Another code


<table>
    <thead>
        <tr>
            <th>MAX ATK</th>
            <th>MAX DEF</th>
            <th>MAX HP</th>
            <th>Overall</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="combat">8170</td>
            <td class="combat">6504</td>
            <td class="combat">6050</td>
            <td class="total-combat"></td>
        </tr>
        <tr>
            <td class="combat">8500</td>
            <td class="combat">10200</td>
            <td class="combat">7650</td>
            <td class="total-combat"></td>
        </tr>
        <tr>
            <td class="combat">9185</td>
            <td class="combat">7515</td>
            <td class="combat">9185</td>
            <td class="total-combat"></td>
        </tr>
    </tbody>
</table>






##Javascript
$(document).ready(function () {
    //iterate through each row in the table
    $('tr').each(function () {
        //the value of sum needs to be reset for each row, so it has to be set inside the row loop
        var sum = 0
        //find the combat elements in the current row and sum it 
        $(this).find('.combat').each(function () {
            var combat = $(this).text();
            if (!isNaN(combat) && combat.length !== 0) {
                sum += parseFloat(combat);
            }
        });
        //set the value of currents rows sum to the total-combat element in the current row
        $('.total-combat', this).html(sum);
    });
});








##
body {
    background: black;
    color: #d5d4d4;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12px;
    margin: 0;
    overflow-x: auto;
    padding: 30px;
}
table {
    background: #030303;
    border-collapse: collapse;
    border: 1px #393939 solid;
    color: #d5d4d4;
    margin: 1em 1em 1em 0;
}
thead {
    border-collapse: collapse;
    color: #d5d4d4;
}
th, td {
    border: 1px #aaa solid;
    padding: 0.2em;
}