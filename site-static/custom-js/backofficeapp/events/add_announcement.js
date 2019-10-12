$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block")
$(document).ready(function(){
});



function validateData(){

	if(checkLast_name("#category_descriptions") && check_date("#end_date"))
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("category_descriptions",($('#category_descriptions').val()).trim());
		formData.append("end_date",($('#end_date').val()));
  			$.ajax({
				  type	: "POST",
				   url : '/backofficeapp/save-announcement-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
	           	  		location.href = '/backofficeapp/event-announcement'
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

function checkLast_name(category_descriptions){
	category_descriptions = $(category_descriptions).val()

   if(category_descriptions!=''){
 		$('#category_descriptions_error').css("display", "none");
   	return true;
   }else{
    	$('#category_descriptions_error').css("display", "block");
    	$('#category_descriptions_error').text("Please enter announcement");
   	return false;
   }
}


function validateIntKeyPress(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}

function check_date(end_date){
end_date_val = $(end_date).val()
if (end_date_val != ''){
    $("#release_date_error").css("display", "none");
    return true;
}else{
    $("#release_date_error").css("display", "block");
    $("#release_date_error").text("Please select End Date");
    return false;
}
}
