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


import datetime 
import dateutil.relativedelta
d = datetime.datetime.strptime("2021-09-01", "%Y-%m-%d") 
d2 = d - dateutil.relativedelta.relativedelta(months=1)
print(d2)
print(d2.month)

today = datetime.date.today()
print(today.month)



total = sum([item.product.price * item.quantity for item in self.items.all()])
