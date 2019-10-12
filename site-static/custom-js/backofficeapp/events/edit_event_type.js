
$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");  


$('#event_type').keyup(function() {
    $("#event_typeDiv").addClass("has-success").removeClass("has-error");
});

 $("#update-continue").click(function(event) { 	 	
	if (validateData()) {
        event.preventDefault(); 
		  
		  var formData= new FormData();		  
    	  formData.append("type_id",$('#hidden_type_id').val());
    	  formData.append("event_type",$('#event_type').val());

        $.ajax({            
             type: "POST",
       		 url: "/backofficeapp/update-event-type-form/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {
	                console.log('response', response);
	                if (response.success == "true") {
	                    bootbox.alert("<span class='center-block text-center'>Event Type updated successfully</span>",function(){
                    			location.href = '/backofficeapp/add-event-type/'
                       });
	                }	                
	                else("#errorMessage")
	            },
	            error: function(response) {
	            	console.log('response', response);
	                bootbox.alert("<span class='center-block text-center'>Email Id already exist</span>");
	            },
	            beforeSend: function() {
	//                $("#processing").show();
	            },
	            complete: function() {
	//                $("#processing").hide();
	            }
        });   
    }  
});
function validateData() {
    if (CheckEventType("#event_type")) {
        return true;
    }
    return false;
}

function CheckEventType(event_type) {
    var namePattern = /[A-Za-z]+/;
    event_type = $(event_type).val()
    if (namePattern.test(event_type)) {
        $("#event_typeDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#event_typeDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}





