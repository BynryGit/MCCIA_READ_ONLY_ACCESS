
    $("#administration_anchor").addClass("tab-active");
		$("#admin_nav").addClass("active");
        $("#administration_icon").addClass("icon-active");
        $("#administration_active").css("display","block");
        $("#admin_nav").addClass("active");
        
        
        $(document).ready(function(){
$(".sel2").select2({
            width: '100%'
        })
  });


        
function validateData(){

	if(checkFirst_name("#First_name")&checkLast_name("#Last_name")&checkNumber("#phone_no")&checkEmail("#Username")&checkrole("#role")&checkcity("#city")&checkpassword("#password"))
	{
		return true;	
	}
	return false;
}

$("#save-continue").click(function(event)  {

	event.preventDefault();  

	if(validateData()){		
	
		var password = $('#password').val();
 		var re_password = $('#re-password').val();
	   if (password != re_password) {

	 			 $('#confirmpas_err').css("display", "block");
             $('#confirmpas_err').text("Password don't match");
    
 				return false;	
	 		}
	
	   var formData= new FormData();

		formData.append("First_name",$('#First_name').val());
		formData.append("Last_name",$('#Last_name').val());
		formData.append("phone_no",$('#phone_no').val());    
		formData.append("Username",$('#Username').val());    
		formData.append("role",$('#role').val()); 
		formData.append("city",$('#city').val()); 
		formData.append("password",$('#password').val());
	
  			$.ajax({
  				  
				  type	: "POST",
				   url : '/add-new-user/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,                       
              success: function (response) {
	 		  	 	  if (response.success == 'Expired') {		
 		  			   location.href = '/backoffice/?status=Expired'
 		  		      }              
	              if(response.success=='true'){
	           	  		$("#success_modal").modal('show');
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


function checkFirst_name(First_name){

	First_name = $(First_name).val()   
  	var namePattern = /[A-Za-z]$/;
   
   if(First_name!='' & namePattern.test(First_name)){
   
   

 	$('#first_name_error').css("display", "none");
   return true;
   }else{
    $('#first_name_error').css("display", "block");
    $('#first_name_error').text("Please enter valid Code");
   return false; 
   }
}
function checkLast_name(Last_name){
	Last_name = $(Last_name).val()   
  	var namePattern = /[A-Za-z]$/;
   if(Last_name!='' & namePattern.test(Last_name)){
 	$('#last_name_error').css("display", "none");
   return true;
   }else{
    $('#last_name_error').css("display", "block");
    $('#last_name_error').text("Please enter valid Membership Description");
   return false; 
   }
}

function checkNumber(phone_no){
	phoneno = $(phone_no).val()     
   var phoneNumberPattern = /^[789]\d{9}$/;  
   if(phoneNumberPattern.test(phoneno)){
 	$(phone_no).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(phone_no).parent().children('.error').css("display", "block");
    $(phone_no).parent().children('.error').text("Please enter valid Contact No");
   return false; 
   }
}


function checkEmail(Username){
	Email = $(Username).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
 
   if(namePattern.test(Email)){
   
     $('#email_err').css("display", "none");
		return true;   
   }else{
 	$('#email_err').css("display", "block");
   $('#email_err').text("Please enter valid Email");
   return false; 
   }
}
	


function checkrole(role){



  if($(role).val()!='' && $(role).val()!=null)
   {

    $(role).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(role).parent().children('.error').css("display", "block");
    $(role).parent().children('.error').text("Please select Role");
   return false; 
   }
}


function checkcity(city){



  if($(city).val()!='' && $(city).val()!=null)
   {

    $(city).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(city).parent().children('.error').css("display", "block");
    $(city).parent().children('.error').text("Please select City");
   return false; 
   }
}

function checkpassword(password){
 passw = $(password).val()
 var paswd=  /^[a-zA-Z0-9!@#$%^&*]{6,15}$/;

	if($(password).val()!='' && paswd.test(passw))
   {
    $( password).parent().children('.error').css("display", "none");
   return true;
   }else{
    $( password).parent().children('.error').css("display", "block");
    $( password).parent().children('.error').text("Password should be more than 6 digits");
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
