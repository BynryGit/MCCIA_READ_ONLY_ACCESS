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

	if(checkcountry("#select_country") && checkLast_name("#state_name"))
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("state_name",$('#state_name').val());
		formData.append("country_id",$('#select_country').val());
  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-state-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	           	  		location.href = '/backofficeapp/administrator-state-landing'
	              	}
	      			if (response.success == "false") {
							$("#error-modal").modal('show');
	       			}
	       			else if (response.success == 'exist'){
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

function checkLast_name(state_name){
	state_name = $(state_name).val()
  	var namePattern = /[A-Za-z]$/;
   if(state_name!='' & namePattern.test(state_name)){
 	$('#state_name_error').css("display", "none");
   return true;
   }else{
    $('#state_name_error').css("display", "block");
    $('#state_name_error').text("Please enter state");
   return false;
   }
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