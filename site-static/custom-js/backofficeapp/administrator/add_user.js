$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

$("#save-role").click(function(event)  {
    if(validateData()){
        event.preventDefault();
        var checkboxValues = []
	    checkboxValues = $('.privillages:checked').map(function() {
			    return $(this).val();
			}).get();

        var formData= new FormData();
        formData.append("user_name",$('#user_name').val());
//        formData.append("select_user_type",$('#select_user_type').val());
        formData.append("select_dept",$('#select_dept').val());
        formData.append("select_desig",$('#select_desig').val());
//        formData.append("select_role",$('#select_role').val());
        formData.append("user_email",$('#user_email').val());
        formData.append("user_contact",$('#user_contact').val());
        formData.append("user_username",$('#user_username').val());
        formData.append("user_password",$('#user_password').val());
        formData.append("privilege_list",checkboxValues);
        $.ajax({
                type: "POST",
                url : '/backofficeapp/save-user-details/',
                data : formData,
                cache: false,
                processData: false,
                contentType: false,
                success: function (response) {
                    if(response.success=='true'){
                            $("#success_modal").modal('show');
                    }else if (response.success == "false"){
                            $("#error-modal").modal('show');
                    }else if (response.success == "exist"){
                        $("#error-modal").modal('show')
                        $("#error_msg").text("Username Already Exist")
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
            $('#user_username_error').text("Please enter valid username");
        return false;
    }
}

function checkpassword(user_password){
    passw = $(user_password).val()
//    var paswd=  /^[a-zA-Z0-9!@#$%^&*]{6,15}$/;
    var paswd=  /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,15}$/;

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

function checkrole(role){
  if($(role).val()!='' && $(role).val()!=null)
   {

    $(role).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(role).parent().children('.error').css("display", "block");
    $(role).parent().children('.error').text("Please select Role");
   return false;
   }
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
    $(".ckbCheckAll_publication").prop('checked', $(this).prop('checked'));
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
    check_for_indv_all('privillages_publication','ckbCheckAll_publication')
    check_for_all(this)
});

$(".privillages_dash").click(function () {
    check_for_all(this)
});





