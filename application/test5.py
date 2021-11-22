 $(document).ready(function () {

            $('#merge').click(function(){
                merge();
            });

            function merge(){
                var el = $("#table2 thead tr:eq(0) td:eq(2)").clone();
                $("#table1 thead tr:eq(0)").append(el);

                $("#table2 thead tr:eq(1) td").each(function () {
                    $("#table1 thead tr:eq(1)").append($(this).clone());
                });

                $('#table2 tbody tr').each(function (index) {
                    $(this).find('td:nth-last-child(2), td:nth-last-child(3), td:nth-last-child(4)').each(function () {
                        $("#table1 tbody").find("tr:eq(" + index + ")").append($(this).clone());
                    });
                });
            }
            
        });







<!DOCTYPE html>
<html>

  <head>
    <link data-require="bootstrap@*" data-semver="4.0.5" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" />
    <script data-require="bootstrap@*" data-semver="4.0.5" src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/js/bootstrap.min.js"></script>
    <script data-require="jquery@*" data-semver="3.1.1" src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <link rel="stylesheet" href="style.css" />
    <script src="script.js"></script>
  </head>

  <body>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <button id="merge" class="btn btn-success">Merge</button>

                <table width="100%" class="table table-striped table-bordered table-hover" id="table1">
                    <thead>
                        <tr>
                            <td rowspan="2">Tgl. Group Temuan</td>
                            <td rowspan="2">Ket</td>
                            <td colspan="3">Temuan Pemeriksaan (TP)</td>

                        </tr>
                        <tr>
                            <td>TP s/d Bulan Lalu</td>
                            <td>TP Bulan ini</td>
                            <td>TP s/d Bulan ini</td>

                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td rowspan="2">01</td>
                            <td>Kejadian</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td></td>
                            <td></td>
                            <td></td>

                        </tr>

                        <tr>
                            <td rowspan="2">02</td>
                            <td>Kejadian</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td rowspan="2">03</td>
                            <td>Kejadian</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td rowspan="2">04</td>
                            <td>Kejadian</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>

                        <tr>
                            <td rowspan="2">05</td>
                            <td>Kejadian</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                    </tbody>
                </table>

                <!-- Table 2 -->
                <table width="100%" class="table table-striped table-bordered table-hover" id="table2">
                    <thead>
                        <tr>
                            <td rowspan="2">Tgl. Group Temuan</td>
                            <td rowspan="2">Ket</td>

                            <td colspan="3">TP yang ditindak lanjuti (TP)</td>
                            <td rowspan="2">TPB s/d Bulan Ini</td>
                        </tr>
                        <tr>
                            <td>TP s/d Bulan Lalu</td>
                            <td>TP Bulan ini</td>
                            <td>SUB TOTAL</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td rowspan="2">01</td>
                            <td>Kejadian</td>
                            <td>Row-0, Td-1</td>
                            <td>Row-0, Td-2</td>
                            <td>Row-0, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td>Row-1, Td-1</td>
                            <td>Row-1, Td-2</td>
                            <td>Row-1, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td rowspan="2">02</td>
                            <td>Kejadian</td>
                            <td>Row-2, Td-1</td>
                            <td>Row-2, Td-2</td>
                            <td>Row-2, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td>Row-3, Td-1</td>
                            <td>Row-3, Td-2</td>
                            <td>Row-3, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td rowspan="2">03</td>
                            <td>Kejadian</td>
                            <td>Row-4, Td-1</td>
                            <td>Row-4, Td-2</td>
                            <td>Row-4, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td>Row-5, Td-1</td>
                            <td>Row-5, Td-2</td>
                            <td>Row-5, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td rowspan="2">04</td>
                            <td>Kejadian</td>
                            <td>Row-6, Td-1</td>
                            <td>Row-6, Td-2</td>
                            <td>Row-6, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td>Row-7, Td-1</td>
                            <td>Row-7, Td-2</td>
                            <td>Row-7, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td rowspan="2">05</td>
                            <td>Kejadian</td>
                            <td>Row-8, Td-1</td>
                            <td>Row-8, Td-2</td>
                            <td>Row-8, Td-3</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Rp</td>
                            <td>Row-9, Td-1</td>
                            <td>Row-9, Td-2</td>
                            <td>Row-9, Td-3</td>
                            <td></td>
                        </tr>                       

                    </tbody>

                </table>

            </div>
        </div>
    </div>
  </body>

</html>







/* Styles go here */

button {
  cursor: pointer;
  margin: 5px 0;
}
