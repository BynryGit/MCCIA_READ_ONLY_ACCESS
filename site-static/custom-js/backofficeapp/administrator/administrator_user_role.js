$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

$(document).ready(function(){
    get_user_role_list_datatable();
});

function get_user_role_list_datatable(){
var table = $('#user_role_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-user-role-list/?sort_var='+sort_var,
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
                {"targets": 5, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
            ],

            responsive: false,

            "order": [
                [0, 'asc']
            ],

            "lengthMenu": [
                [10, 25, 50, 100],
                [10, 25, 50, 100]
            ],
            "pageLength": 10,


        });
        $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });
        $('#user_role_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}


function change_data(){
 get_user_role_list_datatable();
}


function edit_user_role_modal(user_role_id){
        $('#user_role_name_error').css("display", "none");
        $('#user_role_id').val(user_role_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-user-role-detail/',
                data : {
                'user_role_id':user_role_id
                },
              success: function (response) {
              if (response.success == "true") {
                var selected_checkbox_length;
		     		  	selected_checkbox_length = (response.user_data.final_list).length;

		     		  	var checkboxAllValues = []

						checkboxAllValues = $('.privillagesModel:checked').map(function() {
						    return $(this).val();
						}).get();

						if (checkboxAllValues.length == selected_checkbox_length){
							$(".ckbCheckAll_priv").prop('checked', $(this).prop('checked'));
						}

		     		  	$("#role_name").text(response.user_data.role);
		     		  	$("#user_role_desc").text(response.user_data.role_description);
		     		  	$("#role_append").html(response.user_data.final_list);

						$("#edit_user_role_detail_modal").modal('show');
              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-user-role").click(function(event)  {
    user_role_id=$('#user_role_id').val();
    var prv = check_privilage()
    if (prv == false){
     return false;
    }
	event.preventDefault();
	var checkboxValues = []
	checkboxValues = $('.privillagesModel:checked').map(function() {
			    return $(this).val();
			}).get();
    var formData= new FormData();
	event.preventDefault();
		formData.append("user_role_id",user_role_id);
        formData.append("user_role_desc",$('#user_role_desc').val());
        formData.append("privilege_list",checkboxValues);
  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-user-role-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){

	                    $("#edit_user_role_detail_modal").modal('hide');
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
});

function update_user_role_status(status, user_role_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this User Role  Active ?');
        $("#user_role_status").val(status);
        $("#status_user_role_id").val(user_role_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this User Role Inactive ?');
        $("#user_role_status").val(status);
        $("#status_user_role_id").val(user_role_id);
    }
}

function change_user_role_status(){
    var status_user_role_id = $("#status_user_role_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-user-role-status/',
        data: {'status_user_role_id': status_user_role_id},
        success: function(response){
            get_user_role_list_datatable();
        }
    });
}


$("#ckbCheckAll").click(function () {
    $(".privillagesModel").prop('checked', $(this).prop('checked'));
});


function check_privilage(){
			var checkboxValues1 = []
			checkboxValues1 = $('.privillagesModel:checked').map(function() {
			    return $(this).val();
			}).get();

			if (checkboxValues1.length == 0){
				$("#priv_err").css("display", "block");
				$("#priv_err").text("Please select at least 1 Privilege");
			   return false;
			}else{
				$("#priv_err").css("display", "none");
				return true;
			}
}