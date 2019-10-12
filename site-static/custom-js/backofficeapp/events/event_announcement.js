$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block")
 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_event_announcement_datatable();
 		});

function get_event_announcement_datatable(){

var table = $('#slab_details');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-event-detail/?sort_var='+sort_var,
            "searching": true,
            "filtering": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false},
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
        $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });
}




function change_data(){

 sort_var = $('#slab_filter :selected').val();
 get_event_announcement_datatable();
}


function editSlabDetailsModal(event_id){

$("#edit_slab_details_modal").modal('show');
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-event-announcement-details/',
                data : {
                'event_id':event_id
                },
              success: function (response) {
                     if (response.success == "true") {
                $('#event_id').val(event_id);
                $('#category_descriptions').val(response.abc);
                $('#end_date').val(response.end_date);
                $('#end_date_hidden').val(response.end_date);
               }
                },
               error : function(response){
                    alert("_Error");
                }
           });
  }

$('#end_date').change(function(){
end_date=$("#end_date").val()
if (end_date == ''){
    $("#end_date").val($('#end_date_hidden').val())
}
});


$("#edit-slab").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("event_id",$('#event_id').val());
		formData.append("category_descriptions",$('#category_descriptions').val());
		formData.append("end_date",$('#end_date').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-event-announcement-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_slab_details_modal").modal('hide');
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

function validateData(){

	if(checkslab_name("#category_descriptions"))
	{
		return true;
	}
	return false;
}

function checkslab_name(category_descriptions){
	category_descriptions = $(category_descriptions).val()

   if(category_descriptions!=''){
 	$('#category_descriptions_error').css("display", "none");
    return true;
   }else{
    $('#category_descriptions_error').css("display", "block");
    $('#category_descriptions_error').text("Please enter announcement");
   return false;
   }
}

function update_mem_cat(status, event_id){
    if (status == "False"){
        $("#active_deactive_event_text").html('').text('Do you want to make this announcement  Active ?');
        $("#event_announcement_status").val(status);
        $("#event_announcement_id").val(event_id);
    }
    else{
        $("#active_deactive_event_text").html('').text('Do you want to make this announcement  Inactive ?');
        $("#event_announcement_status").val(status);
        $("#event_announcement_id").val(event_id);
    }
}

function change_mem_cat_status(){
    var event_announcement_id = $("#event_announcement_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-event-announcement-status/',
        data: {'event_announcement_id': event_announcement_id},
        success: function(response){
            get_event_announcement_datatable();
        }
    });
}

function checkval(){
alert("hii");}