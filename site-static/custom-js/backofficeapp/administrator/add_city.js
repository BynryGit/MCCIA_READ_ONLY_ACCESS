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

	if(checkstate("#select_state") && checkLast_name("#city_name"))
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("city_name",$('#city_name').val());
		formData.append("state_id",$('#select_state').val());
  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-city-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	           	  		location.href = '/backofficeapp/administrator-city-landing'
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

function checkLast_name(city_name){
	city_name = $(city_name).val()
  	var namePattern = /[A-Za-z]$/;
   if(city_name!='' & namePattern.test(city_name)){
 	$('#city_name_error').css("display", "none");
   return true;
   }else{
    $('#city_name_error').css("display", "block");
    $('#city_name_error').text("Please enter city");
   return false;
   }
}

function checkstate(state){
state = $(state).val()
if (state != ''){
    $('#state_error').css("display", "none");
    return true;
}else{
    $('#state_error').css("display", "block");
    $('#state_error').text("Please select State");
    return false;
}
}