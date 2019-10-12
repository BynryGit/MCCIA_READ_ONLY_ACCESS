$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_department_list_datatable();
 		});

function get_department_list_datatable(){

var table = $('#department_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-department-list/?sort_var='+sort_var,
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
        $('#department_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}




function change_data(){
 get_department_list_datatable();
}


function editSlabDetailsModal(department_id){
        $('#department_name_error').css("display", "none");
        $("#edit_department_detail_modal").modal('show');
        $('#department_id').val(department_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-department-detail/',
                data : {
                'department_id':department_id
                },
              success: function (response) {
              if (response.success == "true") {
                $('#department_name').val(response.abc);
              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-department").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("department_id",$('#department_id').val());
		formData.append("department_name",$('#department_name').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-department-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_department_detail_modal").modal('hide');
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

	if(checkdepartment_name("#department_name"))
	{
		return true;
	}
	return false;
}

function checkdepartment_name(department_name){
	department_name = $(department_name).val()
  	var namePattern = /[A-Za-z0-9!@#$%^&*]$/;
   if(department_name!='' & namePattern.test(department_name)){
 	$('#department_name_error').css("display", "none");
   return true;
   }else{
    $('#department_name_error').css("display", "block");
    $('#department_name_error').text("Please valid enter department");
   return false;
   }
}

function update_department_status(status, department_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this department  Active ?');
        $("#department_status").val(status);
        $("#status_department_id").val(department_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this department Inactive ?');
        $("#department_status").val(status);
        $("#status_department_id").val(department_id);
    }
}

function change_department_status(){
    var status_department_id = $("#status_department_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-department-status/',
        data: {'status_department_id': status_department_id},
        success: function(response){
            get_department_list_datatable();
        }
    });
}