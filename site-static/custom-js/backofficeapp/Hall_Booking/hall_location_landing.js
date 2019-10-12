
$(document).ready(function(e){

    $("#hall_booking_anchor").addClass("tab-active");
    $("#hall_booking_nav").addClass("active");
    $("#hall_booking_icon").addClass("icon-active");
    $("#hall_booking_active").css("display", "block");

    $(".sel2").select2({
        width: '100%'
    });

    change_status();

});



function change_status(){
 select_status = $("#select_status").val()
 load_hall_location(select_status);

}

function load_hall_location(select_status){
var oTable = $('#hall_location_details').dataTable({
//        "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": "/backofficeapp/get-hall-location-data/?select_status="+select_status,
            "searching": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": true, "className": "text-center"},
                {"targets": 1, "orderable": false, "className": "text-center"},
                {"targets": 2, "orderable": false, "className": "text-center"},
                {"targets": 3, "orderable": false, "className": "text-center"},
                {"targets": 4, "orderable": false, "className": "text-center"},
                {"targets": 5, "orderable": false, "className": "text-center"},
            ],

            responsive: false,

            "order": [[1, 'asc']],

            "lengthMenu": [[10, 25, 50, 100],[10, 25, 50, 100]],

            "pageLength": 10,

        });

        $("#locationSearch").keyup(function() {
        oTable.fnFilter($("#locationSearch").val());
    });


}

function update_location_details(status,location_id){
    if (status == "Inactive"){
        $("#active_deactive_location_text").html('').text('Do you want to make this Hall Location Active ?');
        $("#hall_location_id").val(location_id);
    }
    else{
        $("#active_deactive_location_text").html('').text('Do you want to make this Hall Location Inactive ?');
        $("#hall_location_id").val(location_id);
    }
}

function change_location_details_status(){
    var hall_location_id = $("#hall_location_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-location-detail-status/',
        data: {'hall_location_id': hall_location_id},
        success: function(response){
            change_status();
        }
    });
}





function clearFunction() {
$("#locationSearch").val('')
$('.select2').val('All').change();
load_hall_location(select_status);
}




