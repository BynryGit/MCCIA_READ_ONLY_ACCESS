$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");


$(document).ready(function (){
 select_status = $("#select_status").val()
 select_HallLocation = $("#select_HallLocation").val()
 load_manage_halls_landing_table(select_status,select_HallLocation);
});


function change_status(){
 select_status = $("#select_status").val()
 select_HallLocation = $("#select_HallLocation").val()
 load_manage_halls_landing_table(select_status,select_HallLocation);
 }




$("#save_new_holiday").click(function(event) {
        $.ajax({
            type: "POST",
            url: '/backofficeapp/save-new-holiday/',
            data: $("#add_new_holiday_form").serialize(),
            success: function(response) {
                if (response.success == 'true') {
                    $("#success_modal").modal('show');
                }
                if (response.success == "false") {
                    $("#error-modal").modal('show');
                }
            },
            beforeSend: function() {
                $("#processing").css('display', 'block');
            },
            complete: function() {
                $("#processing").css('display', 'none');
            },
            error: function(response) {
                alert("_Error");
            }
        });
});

function change_filterData(){
 select_status = $("#select_status").val()
 select_HallLocation = $("#select_HallLocation").val()
 load_manage_halls_landing_table(select_status,select_HallLocation);
}

function load_manage_halls_landing_table(select_status,select_HallLocation){
var oTable = $('#manage_halls_landing_table').dataTable({
	
				"processing": true,
            "serverSide": true,
            "destroy": true,
            "searching": true,
            "filtering": true,
            "ordering": true,

            "ajax": "/backofficeapp/get-manage-halls-datatable/?select_status="+select_status+"&select_location="+select_HallLocation,
            "paging": true,
            "columnDefs": [
                {"targets": 1, "orderable": false, "className": "text-center"},
                {"targets": 2, "orderable": false, "className": "text-center"},
                {"targets": 3, "orderable": false, "className": "text-center"},
                {"targets": 4, "orderable": false, "className": "text-center"},
                {"targets": 5, "orderable": false, "className": "text-center"},
                {"targets": 6, "orderable": false, "className": "text-center"},
                {"targets": 7, "orderable": false, "className": "text-center"},
                {"targets": 8, "orderable": false, "className": "text-center"},
                {"targets": 9, "orderable": false, "className": "text-center"},
                {"targets": 10, "orderable": false, "className": "text-center"},

            ],
        // setup responsive extension: http://datatables.net/extensions/responsive/
            responsive: false,
            buttons: [
                {extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'pdf', className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'excel', className: 'btn yellow btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'csv', className: 'btn purple btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
            ],

        //"ordering": false, disable column ordering
        //"paging": false, disable pagination

            "order": [
                [1, 'asc']
            ],

            "lengthMenu": [
            // change per page values here
                 [10, 25, 50, 100],
                 [10, 25, 50, 100],
            ],
        // set the initial value
            "pageLength": 10,
        });
         $('#manage_halls_landing_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#manage_halls_landing_table').DataTable().button(action).trigger();
        });

        $("#txtSearch").keyup(function() {
            oTable.fnFilter($("#txtSearch").val());
        });
}

function update_hall_details(status,hall_id){
    if (status == "Inactive"){
        $("#active_deactive_hall_text").html('').text('Do you want to make this Hall  Active ?');
        $("#hall_id").val(hall_id);
    }
    else{
        $("#active_deactive_hall_text").html('').text('Do you want to make this Hall Inactive ?');
        $("#hall_id").val(hall_id);
    }
}



function change_hall_status(){
    var hall_id = $("#hall_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-hall-status/',
        data: {'hall_id': hall_id},
        success: function(response){
        change_status();
        }
    });
}



$("#edit_new_holiday").click(function(event) {
        $.ajax({
            type: "POST",
            url: '/backofficeapp/edit-new-holiday/',
            data: $("#edit_holiday_form").serialize(),
            success: function(response) {
                if (response.success == 'true') {
                    $("#success_modal").modal('show');
                }
                if (response.success == "false") {
                    $("#error-modal").modal('show');
                }
            },
            beforeSend: function() {
                $("#processing").css('display', 'block');
            },
            complete: function() {
                $("#processing").css('display', 'none');
            },
            error: function(response) {
                alert("_Error");
            }
        });
});
