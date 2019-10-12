$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");

$(document).ready(function () {
select_status = $("#select_status").val()
start_date = $("#from_date").val()
end_date = $("#to_date").val()
delete_event_table(select_status,start_date,end_date);
});

function filter(){
       select_status = $("#select_status").val()
        start_date = $("#from_date").val()
        end_date = $("#to_date").val()

 	   delete_event_table(select_status,start_date,end_date);
}

function clear_filter() {
        $("#filter_div").load(" #filter_div");
        setTimeout(function () {
            $('.select2').select2();
            test();
            filter();
        }, 1000);
}
function test(){
var date_input=$('.dateField'); //our date input has the name "date"
		var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
		date_input.datepicker({
			format: 'dd/mm/yyyy',
			container: container,
			todayHighlight: true,
			autoclose: true,
		})
		}

function delete_event_table(select_status,start_date,end_date){
    var table = $('#DeleteEventListTable');
    var oTable = table.dataTable({
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-delete-events/?select_status="+select_status+"&start_date="+start_date+"&end_date="+end_date,
        "searching": true,
        "Filter": true,
        "ordering": true,
        "paging": true,
        "columnDefs": [
            {"targets": 0, "orderable": false,"className": "text-center"},
            {"targets": 1, "orderable": false,"className": "text-center"},
            {"targets": 2, "orderable": false,"className": "text-center"},
            {"targets": 3, "orderable": false,"className": "text-center"},
            {"targets": 4, "orderable": false,"className": "text-center"},
            {"targets": 5, "orderable": false,"className": "text-center"},
            {"targets": 6, "orderable": false,"className": "text-center"},
            {"targets": 7, "orderable": false,"className": "text-center"},
        ],
        buttons: [
            {extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6]}},
            {extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6]}},
            {extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6]}},
            {extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6]}},
            {extend: 'csv', className: 'btn purple btn-outline ',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6]}},
        ],

        responsive: false,
        "order": [
            [0, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [10, 25, 50, 100],
            [10, 25, 50, 100]
        ],
        // set the initial value
        "pageLength": 10,
    });
    $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

     $('#slab_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}

function update_mem_cat(status, event_id){
    if (status == "False"){
        $("#active_deactive_event_text").html('').text('Do you want to Activate this Event ?');
    }
    else{
        $("#active_deactive_event_text").html('').text('Do you want to Deactivate this Event ?');

    }

     $("#event_announcement_status").val(status);
     $("#event_id").val(event_id);
}

function change_mem_cat_status(){
    var event_id = $("#event_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/action-delete-event/',
        data: {'event_id': event_id},
        success: function(response){
            delete_event_table(select_status,start_date,end_date);
        }
    });
}
