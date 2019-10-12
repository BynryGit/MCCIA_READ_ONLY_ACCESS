
$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block");

$("#file_id").change(function () {
		$(file_error).css("display", "none");
});
 
$("#save-btn").click(function(event) { 	 
	if (validateData()) {
        event.preventDefault(); 		
    	  var input = document.getElementById("file_id");  	  
		  link_file = input.files[0];

		  var formData= new FormData();		  
    	  formData.append("link_file",link_file);

        $.ajax({            
             type: "POST",
       		 url: "/mediaapp/save-new-link/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {
	                console.log('response', response);
	                if (response.success == "true") {
	                    bootbox.alert("<span class='center-block text-center'>Link created successfully</span>",function(){
                    			location.href = '/mediaapp/link-to-download/'
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
    if (checkFile("#file_id")) {
        return true;
    }
    return false;
}	 


function checkFile(file_id) {
	if ($('#file_id').val()=='') {
	     $(file_error).css("display", "block");
        $(file_error).text("Please upload Document");
        return false;
    }else{
        $(file_error).css("display", "none");
        return true;
    }
}



