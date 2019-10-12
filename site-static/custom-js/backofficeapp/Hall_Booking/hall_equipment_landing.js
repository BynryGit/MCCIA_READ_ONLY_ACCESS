$("#hall_booking_anchor").addClass("tab-active");
    $("#hall_booking_nav").addClass("active");
    $("#hall_booking_icon").addClass("icon-active");
    $("#hall_booking_active").css("display", "block");

$(document).ready(function () {
	get_equipment_datatable();
});

function change_data(){
	get_equipment_datatable();
}

function get_equipment_datatable(){
        var table = $('#equipment_table');
	    sort_var = $('#sortby :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/load-hall-equipment-table/?sort_var='+sort_var,
            "searching": true,
            "filtering": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false,"className": "text-center"},
                {"targets": 1, "orderable": false,"className": "text-center"},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
                {"targets": 4, "orderable": false,"className": "text-center"},
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
        $("#txtSearch").keyup(function() {
        oTable.fnFilter($("#txtSearch").val());
    });
}

function update_equipment_status(status, equipment_id){
    if (status == "False"){
        $("#active_deactive_equipment_text").html('').text('Do you want to make this Equipment Active ?');
        $("#equipment_status").val(status);
        $("#equipment_id").val(equipment_id);
    }
    else{
        $("#active_deactive_equipment_text").html('').text('Do you want to make this Equipment Inactive ?');
        $("#equipment_status").val(status);
        $("#equipment_id").val(equipment_id);
    }
}

 toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-top-center",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

function change_equipment_status(){
    var equipment_id = $("#equipment_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-hall-equipment-status/',
        data: {'equipment_id': equipment_id},
        success: function(response){
        	   toastr.success("Equipment Updated Successfully");
            get_equipment_datatable();
        }
    });
}

function edit_equipment_open(equipment_id){
$("#edit_equipment_modal").modal('show');
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-hall-equipment-details/',
                data : {
                'equipment_id':equipment_id
                },
              success: function (response) {
                    if (response.success == "true") {
			                $('#edit_equipment_id').val(equipment_id);
			                $('#equipment_name').val(response.equipment_name);
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


$("#edit-equipment").click(function(event)  {
	event.preventDefault();
	$("#equipment_nameDiv").addClass("has-success").removeClass("has-error");
	if ($("#equipment_name").val() != ''){
	   var formData= new FormData();
		formData.append("equipment_id",$('#edit_equipment_id').val());
		formData.append("equipment_name",$('#equipment_name').val());

  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-edit-hall-equipment/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
               success: function (response) {
	              if(response.success == "true"){
	                  $("#edit_equipment_modal").modal('hide');
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
  else {
  		$("#equipment_nameDiv").addClass("has-error").removeClass("has-success");
  }
});

