
$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block");

 change_event();
 
  function change_event() {
  	   select_status = $("#select_status").val()  	     	   
 		load_events_banner(select_status);
 }
 
function clear_filter() {
    $('.select2').val('').change();
    change_event();
}
 
 function load_events_banner(select_status) {
    $('#BannerListTable').dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/mediaapp/get-banner-datatable/?select_status="+select_status,
        "searching": false,
        "6": true,
        "paging": true,
        
        "columnDefs": [
				{"targets": 0, "orderable": false , "className": "text-center"},            
            {"targets": 1, "orderable": false , "className": "text-center"},
            {"targets": 2, "orderable": false , "className": "text-center" },
            {"targets": 3, "orderable": false , "className": "text-center"},
            {"targets": 4, "orderable": false , "className": "text-center"},
            {"targets": 5, "orderable": false , "className": "text-center"},


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

function update_banner(status,banner_id){
    if (status == "Inactive"){
        $("#active_deactive_banner_text").html('').text('Do you want to make this Banner  Active ?');
        $("#banner_id").val(banner_id);
    }
    else{
        $("#active_deactive_banner_text").html('').text('Do you want to make this Banner  Inactive ?');
        $("#banner_id").val(banner_id);
    }
}

function change_banner_status(){
    var banner_id = $("#banner_id").val();
    $.ajax({
        type: "GET",
        url: '/mediaapp/update-banner-status/',
        data: {'banner_id': banner_id},
        success: function(response){
            change_event();
        }
    });
}
