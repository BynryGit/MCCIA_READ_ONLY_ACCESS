$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");


$(document).ready(function (){
 select_status = $("#select_status").val()
 load_holidays_landing(select_status);

});


function change_status(){
 select_status = $("#select_status").val()
 load_holidays_landing(select_status);
}




$("#save_new_holiday").click(function(event) {
    var holiday_date_flag = false;

    var holiday_date = $("#holiday_date").val()
    if (holiday_date != ''){
        $("#errorHolidayDate").addClass("has-success").removeClass("has-error");
        $("#holiday_date_error").css("display", "none");
    }
    else{
        $("#holiday_date_error").css("display", "block");
        $('#holiday_date_error').text("Please Select Date");
        $("#errorHolidayDate").addClass("has-error").removeClass("has-success");
        holiday_date_flag = true;
    }

    if ($("#HolidayType").val() != ''){
        $("#errorHolidayType").addClass("has-success").removeClass("has-error");
        $("#holiday_type_error").css("display", "none");
    }
    else{
        $("#holiday_type_error").css("display", "block");
        $('#holiday_type_error').text("Please Select Holiday Type");
        $("#errorHolidayType").addClass("has-error").removeClass("has-success");
        holiday_date_flag = true;
    }

    if ($("#bookingavailable").val() != ''){
        $("#errorholidayavailable").addClass("has-success").removeClass("has-error");
        $("#booking_available_error").css("display", "none");
    }
    else{
        $("#booking_available_error").css("display", "block");
        $('#booking_available_error').text("Select booking Available");
        $("#errorholidayavailable").addClass("has-error").removeClass("has-success");
        holiday_date_flag = true;
    }

    if (holiday_date_flag != false){
        return false;
    }
    else{
            $.ajax({
            type: "POST",
            url: '/backofficeapp/save-new-holiday/',
            data: $("#add_new_holiday_form").serialize(),
            success: function(response) {
                if (response.success == 'true') {
                    $("#success_modal").modal('show');
                }
                if (response.success == 'alreadyExist') {
                    $("#success_modal_alreadyExist").modal('show');
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
        }
});

function load_holidays_landing(select_status){
var oTable = $('#holiday_landing_table').dataTable({
        "processing": true,
            "serverSide": true,
            "ordering":true,
            "destroy": true,
            "ajax": "/backofficeapp/get-holiday-data/?select_status="+select_status,
            "searching": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false, "className": "text-center"},
                {"targets": 2, "orderable": false, "className": "text-center"},
                {"targets": 3, "orderable": false, "className": "text-center"},
                {"targets": 4, "orderable": false, "className": "text-center"},

            ],
        // setup responsive extension: http://datatables.net/extensions/responsive/
            responsive: false,
            buttons: [
                {extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'pdf', className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'excel', className: 'btn yellow btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'csv', className: 'btn purple btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
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
         $('#holiday_landing_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#holiday_landing_table').DataTable().button(action).trigger();
        });

        $("#searchHolidayDate").keyup(function() {
            oTable.fnFilter($("#searchHolidayDate").val());
        });
}


function update_holiday_details(status,holiday_id){
    if (status == "Inactive"){
        $("#active_deactive_holiday_text").html('').text('Do you want to make this Holiday  Active ?');
        $("#hall_holiday_id").val(holiday_id);
    }
    else{
        $("#active_deactive_holiday_text").html('').text('Do you want to make this Holiday Inactive ?');
        $("#hall_holiday_id").val(holiday_id);
    }
}

function change_holiday_status(){
    var hall_holiday_id = $("#hall_holiday_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-holiday-status/',
        data: {'hall_holiday_id': hall_holiday_id},
        success: function(response){
        change_status();
        }
    });
}

$("#edit_new_holiday").click(function(event) {

var holiday_date_flag = false;

    var holiday_date = $("#edit_holiday_date").val()
    if (holiday_date != ''){
        $("#errorEditHolidayDate").addClass("has-success").removeClass("has-error");
        $("#editholiday_date_error").css("display", "none");
    }
    else{
        $("#editholiday_date_error").css("display", "block");
        $('#editholiday_date_error').text("Please Select Date");
        $("#errorEditHolidayDate").addClass("has-error").removeClass("has-success");
        holiday_date_flag = true;
    }
    if ($("#booking_available_edit").val() != ''){
        $("#errorholidayavailableedit").addClass("has-success").removeClass("has-error");
        $("#booking_available_error_edit").css("display", "none");
    }
    else{
        $("#booking_available_error_edit").css("display", "block");
        $('#booking_available_error_edit').text("Select booking Available");
        $("#errorholidayavailableedit").addClass("has-error").removeClass("has-success");
        holiday_date_flag = true;
    }

    if (holiday_date_flag != false){
        return false;
    }
    else{
        $.ajax({
            type: "POST",
            url: '/backofficeapp/edit-new-holiday/',
            data: $("#edit_holiday_form").serialize(),
            success: function(response) {
                if (response.success == 'true') {
                    $("#success_modal").modal('show');
                }
                if (response.success == 'alreadyExist') {
                    $("#success_modal_alreadyExist").modal('show');
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
        }
});

$("#holiday_date").change(function(){
    $("#errorHolidayDate").addClass("has-success").removeClass("has-error");
    $("#holiday_date_error").css("display", "none");
});

$("#edit_holiday_date").change(function(){
    $("#errorEditHolidayDate").addClass("has-success").removeClass("has-error");
    $("#editholiday_date_error").css("display", "none");
})

$("#bookingavailable").change(function(){
    $("#errorholidayavailable").addClass("has-success").removeClass("has-error");
    $("#booking_available_error").css("display", "none");
});

$("#booking_available_edit").change(function(){
    $("#errorholidayavailableedit").addClass("has-success").removeClass("has-error");
    $("#booking_available_error_edit").css("display", "none");
})
$("#HolidayType").change(function(){
    $("#errorHolidayType").addClass("has-success").removeClass("has-error");
    $("#holiday_type_error").css("display", "none");
});

$("#HolidayTypeEdit").change(function(){
    $("#errorHolidayTypeEdit").addClass("has-success").removeClass("has-error");
    $("#booking_available_error_edit").css("display", "none");
})