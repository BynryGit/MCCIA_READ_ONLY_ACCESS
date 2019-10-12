$("#hall_booking_anchor").addClass("tab-active");
    $("#hall_booking_nav").addClass("active");
    $("#hall_booking_icon").addClass("icon-active");
    $("#hall_booking_active").css("display", "block");

    $(".sel2").select2({
        width: '100%'
    })

$(document).ready(function () {
get_event_announcement_datatable();
});

function change_data(){
get_event_announcement_datatable();
}

function get_event_announcement_datatable(){
        var table = $('#announcement_table');
	    sort_var = $('#announcement_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/hall-get-announvcement/?sort_var='+sort_var,
            "searching": true,
            "filtering": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
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
            "pageLength": 10,
        });
        $("#announcementSearch").keyup(function() {
        oTable.fnFilter($("#announcementSearch").val());
    });
}

function update_announcement_status(status, announcement_id){

    if (status == "False"){
        $("#active_deactive_event_text").html('').text('Do you want to make this announcement  Active ?');
        $("#announcement_status").val(status);
        $("#announcement_id").val(announcement_id);
    }
    else{
        $("#active_deactive_event_text").html('').text('Do you want to make this announcement  Inactive ?');
        $("#announcement_status").val(status);
        $("#announcement_id").val(announcement_id);

    }
}

function change_announcement_status(){
    var announcement_id = $("#announcement_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-hall-announcement-status/',
        data: {'announcement_id': announcement_id},
        success: function(response){
            get_event_announcement_datatable();
        }
    });
}

function edit_announcement_open(announcement_id){

$("#edit_announcement_modal").modal('show');
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-hall-announcement-details/',
                data : {
                'announcement_id':announcement_id
                },
              success: function (response) {
                     if (response.success == "true") {
                $('#edit_announcement_id').val(announcement_id);
                $('#special_announcement').val(response.abc);
                $('#select_location').val(response.location_id).trigger("change")
               }
                },
               error : function(response){
                    alert("_Error");
                }
           });
  }


function validateData(){

	if(checklocation("#select_location") && check_announcement("#special_announcement"))
	{
		return true;
	}
	return false;
}


$("#edit-announcement").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("announcement_id",$('#edit_announcement_id').val());
		formData.append("special_announcement",$('#special_announcement').val());
		formData.append("select_location",$('#select_location').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-hall-announcement-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_announcement_modal").modal('hide');
	           	  		$("#success_modal").modal('show');
	              	}
	      			if (response.success == "false") {
							$("#error-modal").modal('show');
	       			}
               },
               	beforeSend: function () {
            $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
               error : function(response){
                  	alert("_Error");
            	}
           });
  }
});


function check_announcement(special_announcement){
	special_announcement = $(special_announcement).val()
  	var namePattern = /[A-Za-z0-9]$/;
   if(special_announcement!='' & namePattern.test(special_announcement)){
 	$('#special_announcement_error').css("display", "none");
   return true;
   }else{
    $('#special_announcement_error').css("display", "block");
    $('#special_announcement_error').text("Please enter state");
   return false;
   }
}

function checklocation(select_location){
select_location = $(select_location).val()
if (select_location != ''){
    $('#select_location_error').css("display", "none");
    return true;
}else{
    $('#select_location_error').css("display", "block");
    $('#select_location_error').text("Please select Location");
    return false;
}
}