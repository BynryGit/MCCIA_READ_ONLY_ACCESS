
$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block");

 change_event();
 
  function change_event() {
  	   select_status = $("#select_status").val()  	     	   
 		load_link_datatable(select_status);
 }
 
function clear_filter() {
    $('.select2').val('').change();
    change_event();
}
 
 function load_link_datatable(select_status) {
    $('#LinkListTable').dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/mediaapp/get-link-datatable/?select_status="+select_status,
        "searching": false,
        "6": true,
        "paging": true,
        
        "columnDefs": [
				{"targets": 0, "orderable": false , "className": "text-center"},            
            {"targets": 1, "orderable": false , "className": "text-center"},
            {"targets": 2, "orderable": false , "className": "text-center"},
            {"targets": 3, "orderable": false , "className": "text-center"},
            {"targets": 4	, "orderable": false , "className": "text-center"},


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

function update_link(status,link_id){
    if (status == "Inactive"){
        $("#active_deactive_link_text").html('').text('Do you want to make this Link  Active ?');
        $("#link_id").val(link_id);
    }
    else{
        $("#active_deactive_link_text").html('').text('Do you want to make this Link  Inactive ?');
        $("#link_id").val(link_id);
    }
}

function change_link_status(){
    var link_id = $("#link_id").val();
    $.ajax({
        type: "GET",
        url: '/mediaapp/update-link-status/',
        data: {'link_id': link_id},
        success: function(response){
            change_event();
        }
    });
}


function copy_function(copyText) {
	$("#copy_text").val(copyText);
	var copyText1 = document.getElementById("copy_text")
	copyText1.removeAttribute("type", "hidden");
	var copyText1 = document.getElementById("copy_text")
	copyText1.select();
	document.execCommand("copy");
	copyText1.setAttribute("type", "hidden");
	toastr.success("Copied");

}