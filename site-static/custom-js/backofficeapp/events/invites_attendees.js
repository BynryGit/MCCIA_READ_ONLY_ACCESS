$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");

$(document).ready(function(){
  	   select_event = $("#select_event").val()
 	   load_events_details(select_event);
});

function filter(){
  	   select_event = $("#select_event").val()
  	   load_events_details(select_event);
}

function clear_filter() {
       $("#select_event").val('All').trigger('change.select2');
       select_event = $('#select_event').val()
       load_events_details(select_event);
}

function ChangeToEvent() {
	if ($("#select_onspot_event").val()) {
		$('#submit_onspot_btn').attr('href','/eventsapp/events-details/?event_detail_id='+$("#select_onspot_event").val());
	}
	else {
		$('#submit_onspot_btn').attr('href','#');
	}
}

function load_events_details(select_event) {
var table = $('#InvitesAttendeesTable');
var oTable = table.dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-invites-attendees-datatable/?select_event="+select_event,
        "searching": true,
        "paging": true,
        "columnDefs": [
			{"targets": 0, "orderable": true, "className": "text-center"},
            {"targets": 1, "orderable": true},
            {"targets": 2, "orderable": true},
            {"targets": 3, "orderable": false},
            {"targets": 4, "orderable": false},
            {"targets": 5, "orderable": false, "className": "text-center"},
            {"targets": 6, "orderable": false, "className": "text-center"},
            {"targets": 7, "orderable": false, "className": "text-center"},

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
            //  [10, 20, 50],
            //  [10, 20, 50]
            [10, 20, 50 ,100,-1],
            [10, 20, 50 ,100,'All']
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

    // handle datatable custom tools

    $('#slab_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}


function update_event_details(){
    var invites_approve_ids = [];
    var attendees_approve_ids = [];
    $('.check_invites:checkbox:checked').each(function () {
        invites_approve_ids.push($(this).val());
    });
    $('.check_attendees:checkbox:checked').each(function () {
        attendees_approve_ids.push($(this).val());
    });
    if (invites_approve_ids == '' && attendees_approve_ids == '') {
        bootbox.alert("Please Select Invites Or Attendees");
        return false;
    }
    else{
        $.ajax({
            type: "GET",
            url: '/backofficeapp/update-invites-attendees-details/',
            data: {'invites_id_list': invites_approve_ids,'attendees_id_list':attendees_approve_ids},
            success: function(response){
                if(response.success=='true'){
                    bootbox.alert("Invites / Attendees updated successfully");
                    filter();
                }
                if(response.success=='false'){
                    bootbox.alert("Sorry for inconvenience. An error occurred.");
                }
            },
            beforeSend: function () {
             $("#processing").show();
             },
            complete: function () {
             $("#processing").hide();
            },
            error: function(response){
             console.log('IAUE = ', response);
            }
        });
  	 }
}