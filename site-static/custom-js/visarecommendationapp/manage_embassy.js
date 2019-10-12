$("#visa_anchor").addClass("tab-active");
$("#visa_nav").addClass("active");
$("#visa_icon").addClass("icon-active");
$("#visa_active").css("display","block");	

 filter_embassy_table();
 
function filter_embassy_table() {
  	   search_embassy_text = $("#search_embassy_text").val()  	     	   
  	   select_embassy = $("#select_embassy").val()  	     	   

 		load_embassy_details(search_embassy_text,select_embassy);
 }
 
 
 function load_embassy_details(search_embassy_text,select_embassy) {
   var embassy_table =  $('#embassy_table').dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/visarecommendationapp/get-embassy-datatable/?search_embassy_text="+search_embassy_text+'&select_embassy='+select_embassy,
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


function update_embassy(status,embassy_id){
    if (status == "Inactive"){
        $("#active_deactive_embassy_text").html('').text('Do you want to make this Embassy  Active ?');
        $("#embassy_id").val(embassy_id);
    }
    else{
        $("#active_deactive_embassy_text").html('').text('Do you want to make this Embassy  Inactive ?');
        $("#embassy_id").val(embassy_id);
    }
}

function change_embassy_status(){
    var embassy_id = $("#embassy_id").val();
    $.ajax({
        type: "GET",
        url: '/visarecommendationapp/update-embassy-status/',
        data: {'embassy_id': embassy_id},
        success: function(response){
            filter_embassy_table();
        }
    });
}
