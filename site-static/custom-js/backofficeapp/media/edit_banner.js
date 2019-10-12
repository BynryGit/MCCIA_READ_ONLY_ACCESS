
$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block");

function add_new_image() { 	
   $(edit_banner).css("display", "none");
   $("#hidden_banner").val(1);
}   

$('#banner_link').keyup(function() {
    $("#banner_linkDiv").addClass("has-success").removeClass("has-error");
});
$("#event_banner").change(function () {
		$(event_banner_error).css("display", "none");
});

$("#expire_date").change(function () {
		$(expire_date_error).css("display", "none");
});
 
$("#save-btn").click(function(event) { 	 
		  //$('#submit_event').prop('disabled', true);
	if (validateData()) {
        event.preventDefault(); 		
    	  var input = document.getElementById("event_banner");  	  
		  event_banner_file = input.files[0];

		  var formData= new FormData();		  
    	  formData.append("event_banner_file",event_banner_file);
    	  formData.append("banner_link",$('#banner_link').val());
    	  formData.append("expire_date",$('#expire_date').val());
    	  formData.append("hidden_banner_val",$('#hidden_banner').val());
    	  formData.append("banner_id",$('#hidden_banner_id').val());

        $.ajax({            
             type: "POST",
       		 url: "/mediaapp/update-banner/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {
	                console.log('response', response);
	                if (response.success == "true") {
	                    bootbox.alert("<span class='center-block text-center'>Banner updated successfully</span>",function(){
                    			location.href = '/mediaapp/upload-banner/'
                       });
	                }
	                else("#errorMessage")
	            },
	            error: function(response) {
	                bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
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
    if (CheckExpireDate("#expire_date")&checkEventBanner("#event_banner")) {
        return true;
    }
    return false;
}	 

function CheckExpireDate(expire_date) {
    expire_date=$(expire_date).val()
    if (expire_date == ''){
        $(expire_date_error).css("display", "block");
        $(expire_date_error).text("Please enter Expire Date");
        return false;
    }else{
        $(expire_date_error).css("display", "none");
        return true;
    }
}

function checkEventBanner(event_banner) {
	if ($('#hidden_banner').val() == 1) {
		if ($('#event_banner').val()=='') {
		     $(event_banner_error).css("display", "block");
	        $(event_banner_error).text("Please upload Banner");
	        return false;
	    }else{
	        $(event_banner_error).css("display", "none");
	        return true;
	    }
   }
   else{
        $(event_banner_error).css("display", "none");
        return true;
    }
}



