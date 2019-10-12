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

	if(checkLast_name("#designation_name"))
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("designation_name",$('#designation_name').val());
  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-designation-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	           	  		location.href = '/backofficeapp/administrator-designation-landing'
	              	}
	      			if (response.success == "false") {
							$("#error_msg").html('').text("Sorry Somthing Went Wrong")
							$("#error-modal").modal('show');
	       			}
	       			else if (response.success == 'exist'){
	       			    $("#error_msg").html('').text("designation Name Already Exist")
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

function checkLast_name(designation_name){
	designation_name = $(designation_name).val()
  	var namePattern = /[A-Za-z0-9!@#$%^&*]$/;
   if(designation_name!='' & namePattern.test(designation_name)){
 	$('#designation_name_error').css("display", "none");
   return true;
   }else{
    $('#designation_name_error').css("display", "block");
    $('#designation_name_error').text("Please enter designation Name");
   return false;
   }
}