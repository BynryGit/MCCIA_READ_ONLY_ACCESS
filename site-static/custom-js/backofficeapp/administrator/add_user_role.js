$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

$("#save-role").click(function(event)  {

    if(validateRole("#user_role_name")){
        var prv = check_privilage()
        if (prv == false){
         return false;
	}
	event.preventDefault();
	var checkboxValues = []
	checkboxValues = $('.privillages:checked').map(function() {
			    return $(this).val();
			}).get();

	var formData= new FormData();

	formData.append("user_role_name",$('#user_role_name').val());
	formData.append("user_role_desc",$('#user_role_desc').val());
	formData.append("privilege_list",checkboxValues);
	 $.ajax({
			  type	: "POST",
			   url : '/backofficeapp/save-user-role-details/',
	 			data : formData,
				cache: false,
		      processData: false,
		 		contentType: false,

	        success: function (response) {
	           if(response.success=='true'){
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

function validateRole(user_role){

	user_name = $(user_role).val()

   if($(user_role).val()!=''){

 	$(user_role).parent().children('.error').css("display", "none");
   return true;
   }else{

    $(user_role).parent().children('.error').css("display", "block");
    $(user_role).parent().children('.error').text("Please enter Role Name");
   return false;
   }
}


$("#ckbCheckAll").click(function () {
    $(".privillages").prop('checked', $(this).prop('checked'));
});