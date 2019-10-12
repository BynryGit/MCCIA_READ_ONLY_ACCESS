$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");


$(document).ready(function(){
$(".sel2").select2({
            width: '100%'
        })
  });

function validateData(){

	if(checklocation("#select_location") && check_announcement("#special_announcement"))
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("select_location",$('#select_location').val());
		formData.append("special_announcement",$('#special_announcement').val());
  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-hall-announcement/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	           	  		location.href = '/backofficeapp/special-announcement'
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

function check_announcement(special_announcement){
	special_announcement = $(special_announcement).val()
  	var namePattern = /[A-Za-z0-9]$/;
   if(special_announcement!='' & namePattern.test(special_announcement)){
 	$('#special_announcement_error').css("display", "none");
   return true;
   }else{
    $('#special_announcement_error').css("display", "block");
    $('#special_announcement_error').text("Please enter announcement");
   return false;
   }
}

function checklocation(select_location){
select_location = $(select_location).val()
if (select_location != ''){
    $('#select_location_error').css("display", "none");
    return true;
}else{
    $('#select_location_error').css("display", "block");
    $('#select_location_error').text("Please select Location");
    return false;
}
}