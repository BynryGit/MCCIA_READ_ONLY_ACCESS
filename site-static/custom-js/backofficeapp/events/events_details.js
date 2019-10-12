
$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");

 select_change_event();
 
  function select_change_event() {
       select_status = $("#select_status").val()               
       committee = $("#select_committee").val()                
       events = $("#select_event").val()               
       event_type = $("#select_type").val()                
        load_events_details(select_status,committee,events,event_type);
 }
 
function clear_filter() {
    $('.select2').val('').change();
    select_change_event();
}
 
 function load_events_details(select_status,committee,events,event_type) {
    // $('#EventListTable').dataTable({
    var table = $('#EventListTable');
    var oTable = table.dataTable({
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-events-datatable/?select_status="+select_status+'&committee='+committee+'&events='+events+'&event_type='+event_type,
        "searching": false,
        "6": true,
        "paging": true,
        
        "columnDefs": [
                {"targets": 0, "orderable": false, "className": "text-center"},            
            {"targets": 1, "orderable": true , "className": "text-center"},
            {"targets": 2, "orderable": true ,"className": "text-center"},
            {"targets": 3, "orderable": false , "className": "text-center"},
            {"targets": 4, "orderable": false , "className": "text-center"},
            {"targets": 5, "orderable": false , "className": "text-center"},
            {"targets": 6, "orderable": false , "className": "text-center"},
            {"targets": 7, "orderable": false , "className": "text-center"},

        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
            { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,

        //"ordering": false, disable column ordering
        //"paging": false, disable pagination

        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [50, 100, 500],
            [50, 100, 500],
        ],
        // set the initial value
        "pageLength": 50,
    });
    // handle datatable custom tools
    $('#slab_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}

function update_event_details(status,event_id){
    if (status == "Inactive"){
        $("#active_deactive_event_text").html('').text('Do you want to make this event Active ?');
        $("#event_details_id").val(event_id);
        $("#delete_event_row").hide();
    }
    else{
        $("#active_deactive_event_text").html('').text('Do you want to delete this event. If Yes, please select a reason from below ?');
        $("#event_details_id").val(event_id);
        $("#delete_event_row").show();
    }
}

function change_event_details_status(){
    var event_details_id = $("#event_details_id").val();
    if ($("#delete_event_row").is(":visible")){
        var formData= new FormData();
        formData.append("delete_event_radio",$('input[name=delete_event_radio]:checked').val());
        formData.append("event_details_id",event_details_id);
        formData.append("check_ajax",'yes');

        $.ajax({
            type: "POST",
            url: '/backofficeapp/update-event-detail-status/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response){
                select_change_event();
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
            error: function(response){
                bootbox.alert('Sorry for inconvenience. An error occurred.');
            },
        });
    }
    else{
        var formData= new FormData();
        formData.append("event_details_id",event_details_id);
        formData.append("check_ajax",'no');
        $.ajax({
            type: "POST",
            url: '/backofficeapp/update-event-detail-status/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response){
                select_change_event();
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
            error: function(response){
                bootbox.alert('Sorry for inconvenience. An error occurred.');
            },
        });
    }
}