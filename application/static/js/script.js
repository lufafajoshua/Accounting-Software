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


