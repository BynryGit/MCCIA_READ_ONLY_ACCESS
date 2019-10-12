$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_state_list_datatable();
 		});

function get_state_list_datatable(){

var table = $('#state_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-state-list/?sort_var='+sort_var,
            "searching": true,
            "Filter": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false},
                {"targets": 2, "orderable": false},
                {"targets": 3, "orderable": false,"className": "text-center"},
                {"targets": 4, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
            ],

            // setup responsive extension: http://datatables.net/extensions/responsive/
            responsive: false,

            //"ordering": false, disable column ordering
            //"paging": false, disable pagination

            "order": [
                [0, 'asc']
            ],

            "lengthMenu": [
                // change per page values here
                [10, 25, 50, 100],
                [10, 25, 50, 100]
            ],
            // set the initial value
            "pageLength": 10,


        });
        $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

        // handle datatable custom tools
        $('#state_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}




function change_data(){
 get_state_list_datatable();
}


function editSlabDetailsModal(state_id){
        $('#state_name_error').css("display", "none");
        $("#edit_state_detail_modal").modal('show');
        $('#state_id').val(state_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-state-detail/',
                data : {
                'state_id':state_id
                },
              success: function (response) {
              if (response.success == "true") {
                $('#state_name').val(response.abc);
                $('#select_country').val(response.country_id).trigger("change")

              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-state").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("state_id",$('#state_id').val());
		formData.append("state_name",$('#state_name').val());
		formData.append("country_id",$('#select_country').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-state-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_state_detail_modal").modal('hide');
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

	if(checkcountry("#select_country") && checkstate_name("#state_name"))
	{
		return true;
	}
	return false;
}

function checkstate_name(state_name){
	state_name = $(state_name).val()
  	var namePattern = /[A-Za-z]$/;
   if(state_name!='' & namePattern.test(state_name)){
 	$('#state_name_error').css("display", "none");
   return true;
   }else{
    $('#state_name_error').css("display", "block");
    $('#state_name_error').text("Please valid enter state");
   return false;
   }
}

function update_state_status(status, state_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this state  Active ?');
        $("#state_status").val(status);
        $("#status_state_id").val(state_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this state Inactive ?');
        $("#state_status").val(status);
        $("#status_state_id").val(state_id);
    }
}

function change_state_status(){
    var status_state_id = $("#status_state_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-state-status/',
        data: {'status_state_id': status_state_id},
        success: function(response){
            get_state_list_datatable();
        }
    });
}

function checkcountry(country){
country = $(country).val()
if (country != ''){
    $('#country_error').css("display", "none");
    return true;
}else{
    $('#country_error').css("display", "block");
    $('#country_error').text("Please select country");
    return false;
}
}