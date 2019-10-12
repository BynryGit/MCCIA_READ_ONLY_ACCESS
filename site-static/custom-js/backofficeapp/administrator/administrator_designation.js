$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_designation_list_datatable();
 		});

function get_designation_list_datatable(){

var table = $('#designation_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-designation-list/?sort_var='+sort_var,
            "searching": true,
            "Filter": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2]}},
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2]}},
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2]} },
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2]} },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2]} },
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
        $('#designation_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}




function change_data(){
 get_designation_list_datatable();
}


function editSlabDetailsModal(designation_id){
        $('#designation_name_error').css("display", "none");
        $("#edit_designation_detail_modal").modal('show');
        $('#designation_id').val(designation_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-designation-detail/',
                data : {
                'designation_id':designation_id
                },
              success: function (response) {
              if (response.success == "true") {
                $('#designation_name').val(response.abc);
              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-designation").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("designation_id",$('#designation_id').val());
		formData.append("designation_name",$('#designation_name').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-designation-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_designation_detail_modal").modal('hide');
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

	if(checkdesignation_name("#designation_name"))
	{
		return true;
	}
	return false;
}

function checkdesignation_name(designation_name){
	designation_name = $(designation_name).val()
  	var namePattern = /[A-Za-z0-9!@#$%^&*]$/;
   if(designation_name!='' & namePattern.test(designation_name)){
 	$('#designation_name_error').css("display", "none");
   return true;
   }else{
    $('#designation_name_error').css("display", "block");
    $('#designation_name_error').text("Please valid enter designation");
   return false;
   }
}

function update_designation_status(status, designation_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this designation  Active ?');
        $("#designation_status").val(status);
        $("#status_designation_id").val(designation_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this designation Inactive ?');
        $("#designation_status").val(status);
        $("#status_designation_id").val(designation_id);
    }
}

function change_designation_status(){
    var status_designation_id = $("#status_designation_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-designation-status/',
        data: {'status_designation_id': status_designation_id},
        success: function(response){
            get_designation_list_datatable();
        }
    });
}