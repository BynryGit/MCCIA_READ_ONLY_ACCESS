
$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");		

 filter_type_table();
 
function filter_type_table() {
  	   search_type_text = $("#search_type_text").val()  	     	   
  	   select_type = $("#select_type").val()  	     	   

 		load_type_details(search_type_text,select_type);
 }
 
 
 function load_type_details(search_type_text,select_type) {
   var event_type_table =  $('#event_type_table').dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-event-type-datatable/?search_type_text="+search_type_text+'&select_type='+select_type,
        "searching": false,
        "6": true,
        "paging": true,
        
        "columnDefs": [
				{"targets": 0, "orderable": false , "className": "text-center"},            
            {"targets": 1, "orderable": true , "className": "text-center"},
            {"targets": 2, "orderable": false , "className": "text-center"},
            {"targets": 3, "orderable": false , "className": "text-center"},

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
} 


function update_event_type(status,type_id){
    if (status == "Inactive"){
        $("#active_deactive_type_text").html('').text('Do you want to make this Event Type  Active ?');
        $("#type_id").val(type_id);
    }
    else{
        $("#active_deactive_type_text").html('').text('Do you want to make this Event Type  Inactive ?');
        $("#type_id").val(type_id);
    }
}

function change_type_status(){
    var type_id = $("#type_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-event-type-status/',
        data: {'type_id': type_id},
        success: function(response){
            filter_type_table();
        }
    });
}
