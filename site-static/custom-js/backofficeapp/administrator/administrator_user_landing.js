$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

$(document).ready(function(){
    get_user_detail_list_datatable();
});

function get_user_detail_list_datatable(){
var table = $('#user_detail_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-user-detail-list/?sort_var='+sort_var,
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
                {"targets": 6, "orderable": false,"className": "text-center"},
                {"targets": 7, "orderable": false,"className": "text-center"},
                {"targets": 8, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7]} },
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7]}  },
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7]}  },
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7]}  },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7]}  },
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
        $("#userSearch").keyup(function() {
        oTable.fnFilter($("#userSearch").val());
    });
        $('#user_detail_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });
}


function change_data(){
 get_user_detail_list_datatable();
}

function add_new_function(selected_checkbox_length){

checkboxAllValues = $('.privillages').map(function() {
						    return $(this).val();
}).get();

if (checkboxAllValues.length == selected_checkbox_length){
    $(".ckbCheckAll_priv").prop('checked', true);
}


// start:check membership priviledge
checkAll_memValues = $('.privillages_mem:checked').map(function() {
    return $(this).val();
}).get();

All_memValues = $('.privillages_mem').map(function() {
    return $(this).val();
}).get();

if (checkAll_memValues.length == All_memValues.length){
    $(".checkAll_mem").prop('checked', true);
}
//End:check membership priviledge


// start:check Hall priviledge
checkAll_hallValues = $('.privillages_hall:checked').map(function() {
    return $(this).val();
}).get();

All_hallValues = $('.privillages_hall').map(function() {
    return $(this).val();
}).get();

if (checkAll_hallValues.length == All_hallValues.length){
    $(".checkAll_hall").prop('checked', true);
}
//End:check Hall priviledge


// start:check Event priviledge
checkAll_eventValues = $('.privillages_event:checked').map(function() {
    return $(this).val();
}).get();

All_adminValues = $('.privillages_event').map(function() {
    return $(this).val();
}).get();

if (checkAll_eventValues.length == All_adminValues.length){
    $(".checkAll_event").prop('checked', true);
}
//End:check Event priviledge

// start:check Visa priviledge
checkAll_visaValues = $('.privillages_visa:checked').map(function() {
    return $(this).val();
}).get();

All_adminValues = $('.privillages_visa').map(function() {
    return $(this).val();
}).get();

if (checkAll_visaValues.length == All_adminValues.length){
    $(".checkAll_visa").prop('checked', true);
}
//End:check Visa priviledge

// start:check Publication priviledge
checkAll_publicationValues = $('.privillages_publication:checked').map(function() {
    return $(this).val();
}).get();

All_adminValues = $('.privillages_publication').map(function() {
    return $(this).val();
}).get();

if (checkAll_publicationValues.length == All_adminValues.length){
    $(".checkAll_publication").prop('checked', true);
}
//End:check Publication priviledge


// start:check Admin priviledge
checkAll_adminValues = $('.privillages_admin:checked').map(function() {
    return $(this).val();
}).get();

All_adminValues = $('.privillages_admin').map(function() {
    return $(this).val();
}).get();

if (checkAll_adminValues.length == All_adminValues.length){
    $(".checkAll_admin").prop('checked', true);
}
//End:check Admin priviledge
return true
}



function edit_user_detail_modal(user_detail_id){
        $('#user_data').trigger("reset");
        $('#user_detail_name_error').css("display", "none");
        $('#user_detail_id').val(user_detail_id);
        $("#edit_user_detail_modal").modal('show');
//        $("#checkbox1_16").prop('checked', true);

        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-user-detail/',
                data : {
                'user_detail_id':user_detail_id
                },
              success: function (response) {
              if (response.success == "true") {
                var selected_checkbox_length;
		     		  	selected_checkbox_length = (response.id_list).length;
                        userDetail = response.user_Detail
		     		  	var checkboxAllValues = []

		     		  	$.each(response.id_list, function( index, value ) {
                          $("#checkbox1_"+ value).prop('checked',true);
                        });
                        add_new_function(selected_checkbox_length)
		     		  	$("#user_name").val(userDetail.name);
		     		  	$('#select_dept').val(userDetail.department_id).trigger("change")
		     		  	$('#select_desig').val(userDetail.designation_id).trigger("change")
		     		  	$("#user_email").val(userDetail.email);
		     		  	$("#user_contact").val(userDetail.contact_no);
		     		  	$("#user_contact").val(userDetail.contact_no);
		     		  	$("#user_username").val(userDetail.username);
              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-user-detail").click(function(event)  {
    user_detail_id=$('#user_detail_id').val();
    if(validateData()){
        event.preventDefault();
        var checkboxValues = []
	    checkboxValues = $('.privillages:checked').map(function() {
			    return $(this).val();
			}).get();

        var formData= new FormData();
        formData.append("user_detail_id",user_detail_id);
        formData.append("user_name",$('#user_name').val());
        formData.append("select_dept",$('#select_dept').val());
        formData.append("select_desig",$('#select_desig').val());
        formData.append("user_email",$('#user_email').val());
        formData.append("user_contact",$('#user_contact').val());
        formData.append("user_username",$('#user_username').val());
        formData.append("user_password",$('#user_password').val());
        formData.append("privilege_list",checkboxValues);
  			$.ajax({
				 type:"POST",
				 url : '/backofficeapp/save-edit-user-detail/',
				 data : formData,
				 cache: false,
		         processData: false,
		    	 contentType: false,
                 success: function (response) {	          
	             if (response.success == "true") {
	             	     $("#edit_user_detail_modal").modal('hide');
	                    bootbox.alert("<span class='center-block text-center'>User information Updated Successfully</span>",function(){
                    			location.href = '/backofficeapp/administrator-user-landing/'
                       });
	              }	  
                 else if (response.success == "exist") {
                        $("#user-modal").modal('show');
                 }else{
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
//    if(checkName("#user_name") & checkUsertype("#select_user_type") &checkDept("#select_dept") & checkDesignation("#select_desig") & checkRole("#select_role") & checkEmail("#user_email") & checkContactno("#user_contact") & checkUsername("#user_username") & checkpassword("#user_password")){
    if(checkName("#user_name") & checkDept("#select_dept") & checkDesignation("#select_desig") & checkEmail("#user_email") & checkContactno("#user_contact") & checkUsername("#user_username") & checkpassword("#user_password")){
        return true
    }else if(check_privilage()){
        return true
    }
    else{
        return false
        }
}

function check_privilage(){
			var checkboxValues1 = []
			checkboxValues1 = $('.privillages:checked').map(function() {
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

function checkName(check_name){
	check_name = $(check_name).val()
  	var namePattern = /[a-zA-Z]$/;
   if(check_name!='' & namePattern.test(check_name)){
 	$('#user_name_error').css("display", "none");
   return true;
   }else{
    $('#user_name_error').css("display", "block");
    $('#user_name_error').text("Please enter Name");
   return false;
   }
}

function checkUsertype(select_user_type){
    if($(select_user_type).val()!='' && $(select_user_type).val()!=null){
        $('#select_user_type_error').css("display", "none");
        return true;
    }else{
        $('#select_user_type_error').css("display", "block");
        $('#select_user_type_error').text("Please select Type");
        return false;
    }
}

function checkDept(select_dept){
   if($(select_dept).val()!='' && $(select_dept).val()!=null)
   {

    $('#select_dept_error').css("display", "none");
   return true;
   }else{
    $('#select_dept_error').css("display", "block");
    $('#select_dept_error').text("Please select Department");
   return false;
   }

}

function checkDesignation(select_desig){
   if($(select_desig).val()!='' && $(select_desig).val()!=null)
   {

    $('#select_desig_error').css("display", "none");
   return true;
   }else{
    $('#select_desig_error').css("display", "block");
    $('#select_desig_error').text("Please select Designation");
   return false;
   }

}

function checkRole(select_role){
   if($(select_role).val()!='' && $(select_role).val()!=null)
   {
    $('#select_role_error').css("display", "none");
   return true;
   }else{
    $('#select_role_error').css("display", "block");
    $('#select_role_error').text("Please select Role");
   return false;
   }

}

function checkEmail(user_email){
	Email = $(user_email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;

   if(namePattern.test(Email)){
     $('#user_email_error').css("display", "none");
		return true;
   }else{
 	$('#user_email_error').css("display", "block");
    $('#user_email_error').text("Please enter valid Email");
    return false;
   }
}

function checkContactno(user_contact){
    phoneno = $(user_contact).val()
    var check_no = /^[0-9]{10,30}$/;
    var phoneNumberPattern = /^[789]\d{11}$/;
    if(check_no.test(phoneno)){
//    if($(user_contact).val()!='' && $(user_contact).val()!=null){
        $('#user_contact_error').css("display", "none");
        return true;
    }else{
        $('#user_contact_error').css("display", "block");
        $('#user_contact_error').text("Please enter valid Contact No");
    return false;
   }
}

function checkUsername(user_username){
    if($(user_username).val()!='' && $(user_username).val()!=null){
            $('#user_username_error').css("display", "none");
            return true;
        }else{
            $('#user_username_error').css("display", "block");
            $('#user_username_error').text("Please enter valid Contact No");
        return false;
    }
}

function checkpassword(user_password){
    passw = ($(user_password).val()).trim()
//    var paswd=  /^[a-zA-Z0-9!@#$%^&*]{6,15}$/;
    var paswd=  /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,15}$/;

    if(($(user_password).val()).trim() == ''){
        $(user_password).val('')
        return true
    }
    if($(user_password).val()!='' && paswd.test(passw)){
        $('#user_password_error').css("display", "none");
        return true;
    }else{
        $('#user_password_error').css("display", "block");
        $('#user_password_error').text("Must contain at least one number,one letter and one special character, and at least 6 or more characters");
    return false;
    }
}

function isNumberKey(evt, element) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) ||  charCode == 46 )
     return false;

  return true;
}

function update_user_detail_status(status, user_detail_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this User Active ?');
        $("#user_detail_status").val(status);
        $("#status_user_detail_id").val(user_detail_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this User Inactive ?');
        $("#user_detail_status").val(status);
        $("#status_user_detail_id").val(user_detail_id);
    }
}

function change_user_detail_status(){
    var status_user_detail_id = $("#status_user_detail_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-user-detail-status/',
        data: {'status_user_detail_id': status_user_detail_id},
        success: function(response){
            get_user_detail_list_datatable();
        }
    });
}

function check_for_all(this_obj){

if ($(this_obj).prop('checked')){
        checkboxAllValues = $('.privillages').map(function() {
                                return $(this_obj).val();
    }).get();

    checkboxcheckedValues = $('.privillages:checked').map(function() {
                                return $(this_obj).val();
    }).get();

    if (checkboxAllValues.length == checkboxcheckedValues.length){
        $(".ckbCheckAll_priv").prop('checked', true);
    }

}else{
    $(".ckbCheckAll_priv").prop('checked', false);
}

}

$("#CheckAll").click(function () {
    $(".privillages").prop('checked', $(this).prop('checked'));
    $(".checkAll_mem").prop('checked', $(this).prop('checked'));
    $(".checkAll_hall").prop('checked', $(this).prop('checked'));
    $(".checkAll_event").prop('checked', $(this).prop('checked'));
    $(".checkAll_visa").prop('checked', $(this).prop('checked'));
    $(".checkAll_admin").prop('checked', $(this).prop('checked'));
    $(".checkAll_publication").prop('checked', $(this).prop('checked'));
});

$("#ckbCheckAll_mem").click(function () {
    $(".privillages_mem").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});

$("#ckbCheckAll_hall").click(function () {
    $(".privillages_hall").prop('checked', $(this).prop('checked'));
    check_for_all(this)

});
$("#ckbCheckAll_event").click(function () {
    $(".privillages_event").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});
$("#ckbCheckAll_visa").click(function () {
    $(".privillages_visa").prop('checked', $(this).prop('checked'));
    check_for_all(this)

});
$("#ckbCheckAll_admin").click(function () {
    $(".privillages_admin").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});
$("#ckbCheckAll_publication").click(function () {
    $(".privillages_publication").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});

function check_for_indv_all(prev_module,prev_check_module){

checkboxAllValues = $('.' + prev_module).map(function() {
                                return $(this_obj).val();
    }).get();

    checkboxcheckedValues = $('.prev_module:checked').map(function() {
                                return $(this_obj).val();
    }).get();

    if (checkboxAllValues.length == checkboxcheckedValues.length){
        $("."+ prev_check_module).prop('checked', true);
    }

}

$("#ckbCheckAll_mem").click(function () {
    $(".privillages_mem").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});

$("#ckbCheckAll_hall").click(function () {
    $(".privillages_hall").prop('checked', $(this).prop('checked'));
    check_for_all(this)

});
$("#ckbCheckAll_event").click(function () {
    $(".privillages_event").prop('checked', $(this).prop('checked'));
    check_for_all(this)

});
$("#ckbCheckAll_admin").click(function () {
    $(".privillages_admin").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});
$("#ckbCheckAll_publication").click(function () {
    $(".privillages_publication").prop('checked', $(this).prop('checked'));
    check_for_all(this)
});

function check_for_indv_all(prev_module,prev_check_module){

    checkboxAllValues = $('.' + prev_module).map(function() {
                                return $(this).val();
    }).get();

    checkboxcheckedValues = $('.'+prev_module+':checked').map(function() {
                                return $(this).val();
    }).get();

    if (checkboxAllValues.length == checkboxcheckedValues.length){
        $("."+ prev_check_module).prop('checked', true);
    }else{
         $("."+ prev_check_module).prop('checked', false);
    }
}


$(".privillages_mem").click(function () {
    check_for_indv_all('privillages_mem','checkAll_mem')
    check_for_all(this)
});

$(".privillages_hall").click(function () {
    check_for_indv_all('privillages_hall','checkAll_hall')
    check_for_all(this)
});

$(".privillages_event").click(function () {
    check_for_indv_all('privillages_event','checkAll_event')
    check_for_all(this)
});

$(".privillages_visa").click(function () {
    check_for_indv_all('privillages_visa','checkAll_visa')
    check_for_all(this)
});

$(".privillages_admin").click(function () {
    check_for_indv_all('privillages_admin','checkAll_admin')
    check_for_all(this)
});
$(".privillages_publication").click(function () {
    check_for_indv_all('privillages_publication','checkAll_publication')
    check_for_all(this)
});
$(".privillages_dash").click(function () {
    check_for_all(this)
});