
// Highlight Hall Booking Menu Item
$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

$(document).ready(function(e){
    load_hall_cancel_policy_table();
});

// Load Cancellation Policy Data Table
function load_hall_cancel_policy_table(){
    var oTable = $('#cancel_policy_table').dataTable({
//        "processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-hall-cancel-policy-table/",
        "searching": false,
        "paging": true,
        "columnDefs": [
            {"targets": 0, "orderable": true, "className": "text-center"},
            {"targets": 1, "orderable": false, "className": "text-center"},
            {"targets": 2, "orderable": false, "className": "text-center"},
            {"targets": 3, "orderable": false, "className": "text-center"},
            {"targets": 4, "orderable": false, "className": "text-center"},
        ],

        responsive: false,

        "order": [[1, 'asc']],

        "lengthMenu": [[10, 25, 50, 100, -1],[10, 25, 50, 100, 'All']],

        "pageLength": 10,

    });

//    $("#locationSearch").keyup(function() {
//        oTable.fnFilter($("#locationSearch").val());
//    });
    $('#cancel_policy_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}

// Save New Cancellation Policy
function save_new_policy(){
    $.ajax({
        type: "POST",
        url: '/backofficeapp/save-new-cancel-policy/',
        data: $("#add_policy_form").serialize(),
        success: function(response) {
            if (response.success == 'true') {
                bootbox.alert('Cancellation policy added successfully.');
                setTimeout(function(){ location.reload('/'); }, 1000);
            }
            if (response.success == 'alreadyExist') {
                $("#alreadyExist").modal('show');
            }
            if (response.success == "false") {
                bootbox.alert('Sorry for inconvenience. An error occurred.');
            }
        },
        beforeSend: function() {
            $("#processing").css('display', 'block');
        },
        complete: function() {
            $("#processing").css('display', 'none');
        },
        error: function(response) {
            bootbox.alert('Sorry for inconvenience. An error occurred.');
            console.log('SHCPE = ',response);
        }
    });
}