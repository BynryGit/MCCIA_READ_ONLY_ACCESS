
$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");  


$("#committee_name").keyup(function () {
		  $("#committee_nameDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman1_name").keyup(function () {
		  $("#chairman1_nameDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman1_company").keyup(function () {
		  $("#chairman1_companyDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman1_designation").keyup(function () {
		  $("#chairman1_designationDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman1_email").keyup(function () {
		  $("#chairman1_emailDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman1_mobile").keyup(function () {
		  $("#chairman1_mobileDiv").addClass("has-success").removeClass("has-error");
});
$('#chairman1_telephone').keyup(function() {
    $("#chairman1_telephoneDiv").addClass("has-success").removeClass("has-error");
});
$('#chairman1_address').keyup(function() {
    $("#chairman1_addressDiv").addClass("has-success").removeClass("has-error");
});

$("#chairman2_name").keyup(function () {
		  $("#chairman2_nameDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman2_company").keyup(function () {
		  $("#chairman2_companyDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman2_designation").keyup(function () {
		  $("#chairman2_designationDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman2_email").keyup(function () {
		  $("#chairman2_emailDiv").addClass("has-success").removeClass("has-error");
});
$("#chairman2_mobile").keyup(function () {
		  $("#chairman2_mobileDiv").addClass("has-success").removeClass("has-error");
});
$('#chairman2_telephone').keyup(function() {
    $("#chairman2_telephoneDiv").addClass("has-success").removeClass("has-error");
});
$('#chairman2_address').keyup(function() {
    $("#chairman2_addressDiv").addClass("has-success").removeClass("has-error");
});
$("#select_office_incharge1").change(function () {	  
	  $("#select_office_incharge1Div").addClass("has-success").removeClass("has-error");
});

function isNumberKey(evt, element){
  check_value=$(element).val()
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) ||  charCode == 46 )
     return false;
  return true;
}

 $("#save-continue").click(function(event) { 	 	
	if (validateData()) {
		  $('#save-continue').prop('disabled', true);
        event.preventDefault(); 
		  
		  var formData= new FormData();
		  
    	  formData.append("committee_name",$('#committee_name').val());
    	  formData.append("chairman1_name",$('#chairman1_name').val());
    	  formData.append("chairman1_company",$('#chairman1_company').val());
    	  formData.append("chairman1_designation",$('#chairman1_designation').val());
    	  formData.append("chairman1_email",$('#chairman1_email').val());
    	  formData.append("chairman1_mobile",$('#chairman1_mobile').val());
    	  formData.append("chairman1_telephone",$('#chairman1_telephone').val());
    	  formData.append("chairman1_address",$('#chairman1_address').val());
    	  formData.append("chairman2_name",$('#chairman2_name').val());
    	  formData.append("chairman2_company",$('#chairman2_company').val());
    	  formData.append("chairman2_designation",$('#chairman2_designation').val());
    	  formData.append("chairman2_email",$('#chairman2_email').val());
    	  formData.append("chairman2_mobile",$('#chairman2_mobile').val());
    	  formData.append("chairman2_telephone",$('#chairman2_telephone').val());
    	  formData.append("chairman2_address",$('#chairman2_address').val());
    	  formData.append("office_incharge1",$('#select_office_incharge1').val());
    	  formData.append("office_incharge2",$('#select_office_incharge2').val());

        $.ajax({            
             type: "POST",
       		 url: "/backofficeapp/save-new-committee/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {
	                console.log('response', response);
	                if (response.success == "true") {
	                    bootbox.alert("<span class='center-block text-center'>Committee added successfully</span>",function(){
                    			location.href = '/backofficeapp/add-committee/'
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
    if (CheckCommittee("#committee_name")&CheckChairman1Name("#chairman1_name")&CheckCompany1Name("#chairman1_company")
    &CheckDesignation1("#chairman1_designation")&validateEmail1("#chairman1_email")&checkMobileNo1("#chairman1_mobile")&checkTelePhoneNo1("#chairman1_telephone")
    &CheckAddress1("#chairman1_address")&CheckChairman2Name("#chairman2_name")&CheckCompany2Name("#chairman2_company")
    &CheckDesignation2("#chairman2_designation")&validateEmail2("#chairman2_email")&checkMobileNo2("#chairman2_mobile")&checkTelePhoneNo2("#chairman2_telephone")
    &CheckAddress2("#chairman2_address")&CheckOfficeIncharge1("#select_office_incharge1")) {
        return true;
    }
    return false;
}

function CheckCommittee(committee_name) {
    var namePattern = /[A-Za-z]+/;
    committee_name = $(committee_name).val()
    if (namePattern.test(committee_name)) {
        $("#committee_nameDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#committee_nameDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}


function CheckChairman1Name(chairman1_name) {
    var namePattern = /[A-Za-z]+/;
    chairman1_name = $(chairman1_name).val()
    if (chairman1_name!= '') {
	    if (namePattern.test(chairman1_name)) {
	        $("#chairman1_nameDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman1_nameDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	}
	else {
		$("#chairman1_nameDiv").addClass("has-success").removeClass("has-error");
	   return true;
	}
}

function CheckCompany1Name(chairman1_company) {
    var namePattern = /[A-Za-z]+/;
    chairman1_company = $(chairman1_company).val()
    if (chairman1_company!= '') {
	    if (namePattern.test(chairman1_company)) {
	        $("#chairman1_companyDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman1_companyDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	}
	else {
		$("#chairman1_companyDiv").addClass("has-success").removeClass("has-error");
	   return true;
	}
}

function CheckDesignation1(chairman1_designation) {
    var namePattern = /[A-Za-z]+/;
    chairman1_designation = $(chairman1_designation).val()
    if (chairman1_designation!= '') {
	    if (namePattern.test(chairman1_designation)) {
	        $("#chairman1_designationDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman1_designationDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	}
	else {
		$("#chairman1_designationDiv").addClass("has-success").removeClass("has-error");
	   return true;
	}
}


function validateEmail1(chairman1_email) {
    chairman1_email = $(chairman1_email).val()  
    if (chairman1_email) {  
	    var filter = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	    if (filter.test(chairman1_email)) {
	        $("#chairman1_emailDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman1_emailDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
    }
    else {
    	$("#chairman1_emailDiv").addClass("has-success").removeClass("has-error");
	   return true;
    }
}

function checkMobileNo1(chairman1_mobile) {
    chairman1_mobile = $(chairman1_mobile).val()
    if (chairman1_mobile) {
	    var phoneNumberPattern = /^[789]\d{9}$/;
	    //var phoneNumberPattern = /^\d{10}$/;
	    if (phoneNumberPattern.test(chairman1_mobile)) {
	        $("#chairman1_mobileDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman1_mobileDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	 }
	 else {
	 	$("#chairman1_mobileDiv").addClass("has-success").removeClass("has-error");
	   return true;
	 }
}

function checkTelePhoneNo1(chairman1_telephone) {
    chairman1_telephone = $(chairman1_telephone).val()
    var phoneNumberPattern = /^[0]\d{10,11}$/;
    if (chairman1_telephone == '') {
        $("#chairman1_telephoneDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else if (phoneNumberPattern.test(chairman1_telephone)) {
        $("#chairman1_telephoneDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else {
        $("#chairman1_telephoneDiv").addClass("has-error").removeClass("has-success");
	     return false;
    }
}

function CheckAddress1(chairman1_address) {
    var namePattern = /[A-Za-z]+/;
    chairman1_address = $(chairman1_address).val()
    if (chairman1_address == '') {
        $("#chairman1_addressDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else if (namePattern.test(chairman1_address)) {
        $("#chairman1_addressDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else {
        $("#chairman1_addressDiv").addClass("has-error").removeClass("has-success");
	     return false;
    }
}



function CheckChairman2Name(chairman2_name) {
    var namePattern = /[A-Za-z]+/;
    chairman2_name = $(chairman2_name).val()
    if (chairman2_name!= '') {
	    if (namePattern.test(chairman2_name)) {
	        $("#chairman2_nameDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman2_nameDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	}
	else {
		$("#chairman2_nameDiv").addClass("has-success").removeClass("has-error");
	   return true;
	}
}

function CheckCompany2Name(chairman2_company) {
    var namePattern = /[A-Za-z]+/;
    chairman2_company = $(chairman2_company).val()
    if (chairman2_company!= '') {
	    if (namePattern.test(chairman2_company)) {
	        $("#chairman2_companyDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman2_companyDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	}
	else {
		$("#chairman2_companyDiv").addClass("has-success").removeClass("has-error");
	   return true;
	}
}

function CheckDesignation2(chairman2_designation) {
    var namePattern = /[A-Za-z]+/;
    chairman2_designation = $(chairman2_designation).val()
    if (chairman2_designation!= '') {
	    if (namePattern.test(chairman2_designation)) {
	        $("#chairman2_designationDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman2_designationDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	}
	else {
		$("#chairman2_designationDiv").addClass("has-success").removeClass("has-error");
	   return true;
	}
}


function validateEmail2(chairman2_email) {
    chairman2_email = $(chairman2_email).val()  
    if (chairman2_email) {  
	    var filter = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	    if (filter.test(chairman2_email)) {
	        $("#chairman2_emailDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman2_emailDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
    }
    else {
    	$("#chairman2_emailDiv").addClass("has-success").removeClass("has-error");
	   return true;
    }
}

function checkMobileNo2(chairman2_mobile) {
    chairman2_mobile = $(chairman2_mobile).val()
    if (chairman2_mobile) {
	    var phoneNumberPattern = /^[789]\d{9}$/;
	    //var phoneNumberPattern = /^\d{10}$/;
	    if (phoneNumberPattern.test(chairman2_mobile)) {
	        $("#chairman2_mobileDiv").addClass("has-success").removeClass("has-error");
	        return true;
	    } else {
	        $("#chairman2_mobileDiv").addClass("has-error").removeClass("has-success");
	        return false;
	    }
	 }
	 else {
	 	$("#chairman2_mobileDiv").addClass("has-success").removeClass("has-error");
	   return true;
	 }
}

function checkTelePhoneNo2(chairman2_telephone) {
    chairman2_telephone = $(chairman2_telephone).val()
    var phoneNumberPattern = /^[0]\d{10,11}$/;
    if (chairman2_telephone == '') {
        $("#chairman2_telephoneDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else if (phoneNumberPattern.test(chairman2_telephone)) {
        $("#chairman2_telephoneDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else {
        $("#chairman2_telephoneDiv").addClass("has-error").removeClass("has-success");
	     return false;
    }
}

function CheckAddress2(chairman2_address) {
    var namePattern = /[A-Za-z]+/;
    chairman2_address = $(chairman2_address).val()
    if (chairman2_address == '') {
        $("#chairman2_addressDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else if (namePattern.test(chairman2_address)) {
        $("#chairman2_addressDiv").addClass("has-success").removeClass("has-error");
	     return true;
    } else {
        $("#chairman2_addressDiv").addClass("has-error").removeClass("has-success");
	     return false;
    }
}

function CheckOfficeIncharge1(select_office_incharge1) {
    if ($(select_office_incharge1).val() != '' && $(select_office_incharge1).val() != null) {
        $("#select_office_incharge1Div").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_office_incharge1Div").addClass("has-error").removeClass("has-success");
        return false;
    }
}




