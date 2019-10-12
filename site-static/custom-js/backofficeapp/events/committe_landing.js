
$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");		

 filter_committee_table();
 
function filter_committee_table() {
  	   search_committee_text = $("#search_committee_text").val()  	     	   
  	   select_committee = $("#select_committee").val()  	     	   

 		load_events_details(search_committee_text,select_committee);
 }
 
 
 function load_events_details(search_committee_text,select_committee) {
   var committee_table =  $('#committee_table').dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-committee-datatable/?search_committee_text="+search_committee_text+'&select_committee='+select_committee,
        "searching": false,
        "6": true,
        "paging": true,
        
        "columnDefs": [
				{"targets": 0, "orderable": false , "className": "text-center"},            
            {"targets": 1, "orderable": true , "className": "text-center"},
            {"targets": 2, "orderable": false , "className": "text-center"},
            {"targets": 3, "orderable": false , "className": "text-center"},
            {"targets": 4, "orderable": false , "className": "text-center"},

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


function update_committee(status,event_id){
    if (status == "Inactive"){
        $("#active_deactive_committee_text").html('').text('Do you want to make this committee  Active ?');
        $("#committee_id").val(event_id);
    }
    else{
        $("#active_deactive_committee_text").html('').text('Do you want to make this committee  Inactive ?');
        $("#committee_id").val(event_id);
    }
}

function change_committee_status(){
    var committee_id = $("#committee_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-committee-status/',
        data: {'committee_id': committee_id},
        success: function(response){
            filter_committee_table();
        }
    });
}
