$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")


$(document).ready(function(){
$(".sel2").select2({
            width: '100%'
        })
  });



function validateData(){

	if(checkLast_name("#department_name"))
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("department_name",$('#department_name').val());
  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-department-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	           	  		location.href = '/backofficeapp/administrator-department-landing'
	              	}
	      			if (response.success == "false") {
							$("#error_msg").html('').text("Sorry Somthing Went Wrong")
							$("#error-modal").modal('show');
	       			}
	       			else if (response.success == 'exist'){
	       			    $("#error_msg").html('').text("department Name Already Exist")
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

function checkLast_name(department_name){
	department_name = $(department_name).val()
  	var namePattern = /[A-Za-z0-9!@#$%^&*]$/;
   if(department_name!='' & namePattern.test(department_name)){
 	$('#department_name_error').css("display", "none");
   return true;
   }else{
    $('#department_name_error').css("display", "block");
    $('#department_name_error').text("Please enter department Name");
   return false;
   }
}