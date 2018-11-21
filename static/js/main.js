$(document).ready(function() {
    var table=$('#mpgtable').DataTable();

    function tableupdate(updatedCell,updatedRow,oldValue){
        console.log("Data: "+updatedRow.data());

    }
    table.MakeCellsEditable({
        "onUpdate":tableupdate,
        "columns":[1,2],
        "confirmationButton":true
    });

} );