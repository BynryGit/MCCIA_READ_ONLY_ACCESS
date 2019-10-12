$("#visa_anchor").addClass("tab-active");
$("#visa_nav").addClass("active");
$("#visa_icon").addClass("icon-active");
$("#visa_active").css("display","block");	



$("#embassy_name").keyup(function () {
		  $("#embassy_nameDiv").addClass("has-success").removeClass("has-error");
});
$("#city_name").keyup(function () {
		  $("#city_nameDiv").addClass("has-success").removeClass("has-error");
});
$("#embassy_address").keyup(function () {
		  $("#embassy_addressDiv").addClass("has-success").removeClass("has-error");
});
$("#select_country").change(function () {	  
	  $("#select_countryDiv").addClass("has-success").removeClass("has-error");
});


 $("#update-continue").click(function(event) { 
	if (validateData()) {
		  $('#save-continue').prop('disabled', true);
        event.preventDefault(); 
		  
		  var formData= new FormData();
		  
    	  formData.append("embassy_id",$('#hidden_embassy_id').val());
    	  formData.append("embassy_name",$('#embassy_name').val());
    	  formData.append("city_name",$('#city_name').val());
    	  formData.append("embassy_address",$('#embassy_address').val());
    	  formData.append("select_country",$('#select_country').val());

        $.ajax({            
             type: "POST",
       		 url: "/visarecommendationapp/update-embassy-form/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {
	                console.log('response', response);
	                if (response.success == "true") {
	                    bootbox.alert("<span class='center-block text-center'>Embassy updated successfully</span>",function(){
                    			location.href = '/visarecommendationapp/manage-embassy/'
                       });
	                }	                
	                else("#errorMessage")
	            },
	            error: function(response) {
	            	console.log('response', response);
	                bootbox.alert("<span class='center-block text-center'>Error</span>");
	            },
	            beforeSend: function() {
	                $("#processing").show();
	            },
	            complete: function() {
	                $("#processing").hide();
	            }
        });   
    }  
});
function validateData() {
    if (CheckEmbassyName("#embassy_name")&CheckCity("#city_name")&CheckAddress("#embassy_address")&CheckCountry("#select_country")) {
        return true;
    }
    return false;
}

function CheckEmbassyName(embassy_name) {
    var namePattern = /[A-Za-z]+/;
    embassy_name = $(embassy_name).val()
    if (namePattern.test(embassy_name)) {

        $("#embassy_nameDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#embassy_nameDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckCity(city_name) {
    var namePattern = /[A-Za-z]+/;
    city_name = $(city_name).val()
    if (namePattern.test(city_name)) {
        $("#city_nameDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#city_nameDiv").addClass("has-error").removeClass("has-success");
        return false;
    }

}
function CheckAddress(embassy_address) {
    var namePattern = /[A-Za-z]+/;
    embassy_address = $(embassy_address).val()
    if (namePattern.test(embassy_address)) {
        $("#embassy_addressDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else {
        $("#embassy_addressDiv").addClass("has-error").removeClass("has-success");
	     return false;
    }
}
function CheckCountry(select_country) {
    if ($(select_country).val() != '' && $(select_country).val() != null) {
        $("#select_countryDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_countryDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}




