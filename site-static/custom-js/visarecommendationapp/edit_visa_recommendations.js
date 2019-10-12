$("#visa_anchor").addClass("tab-active");
$("#visa_nav").addClass("active");
$("#visa_icon").addClass("icon-active");
$("#visa_active").css("display","block");



$("#drpCountry").change(function () {	  
     get_embassy_location();
});

function get_embassy_location() {
        country_id = $('#drpCountry :selected').val();
        if (country_id) {
            $.ajax({
                type: 'GET',
                url: '/visarecommendationapp/get-embassy-location/',
                data: {'country_id': country_id},
                success: function (response) {   
                  if (response.success == 'true') {  
                    console.log(response.embassy_list) 
  						  $("#drpEmbasy").html('')
  						  $("#drpEmbasy").append('<option value="">Select Embassy</option>');
                    $.each(response.embassy_list, function (index, item) {
                        data = '<option value="'+ item.id +'">'+ item.embassy_name +'</option>'
                        $("#drpEmbasy").append(data);
                    });     
                    $("#drpEmbasy").val('').change();             
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }  
      else {
      	$("#drpEmbasy").html('')      	
  			$("#drpEmbasy").append('<option value="">Select Embassy</option>');
  			$("#drpEmbasy").val('').change();
     }      
 }
 
function VisaTypeDivShow() {
        visaType=$("#VisaType").val();

        if (visaType == "Single"){
            $("#row0Div").css("display","block")
            $("#row1Div").css("display","block")
            $("#row2Div").css("display","none")
        }
        else if (visaType == "Multiple"){
        	   $("#row0Div").css("display","block")
            $("#row1Div").css("display","block")
            $("#row2Div").css("display","block")  
            $("#drpMonth").val($("#hidden_visatotalduration").val()).change()        
        }
        else{
        	   $("#row0Div").css("display","none")
            $("#row1Div").css("display","none")
            $("#row2Div").css("display","none")
        }
}
 
//$('input[name=ctl00_user_visit_duration]').change(function(){
function radioButtonChange() {
	ctl00_user_visit_duration= $('input[name=ctl00_user_visit_duration]:checked').val();
	
	if (ctl00_user_visit_duration == "ctl00_user_rdoDay"){
	    $("#txtdaysDiv").css("display","block")
	    $("#txtWeekDiv").css("display","none")
	    $("#txtMonthDiv").css("display","none")
	}
	else{
	    if (ctl00_user_visit_duration == "ctl00_user_rdoWeek"){
	        $("#txtdaysDiv").css("display","none")
	        $("#txtWeekDiv").css("display","block")
	        $("#txtMonthDiv").css("display","none")
	    }
	    else{	
	        $("#txtdaysDiv").css("display","none")
	        $("#txtWeekDiv").css("display","none")
	        $("#txtMonthDiv").css("display","block")	
	    }
	}
}

$(document).ready(function (){
	hidden_radiochoice = $("#hidden_radiochoice").val()
	if (hidden_radiochoice == 'Day') {
		$('#ctl00_user_rdoDay').attr('checked',true);
		$("#txtdays").val($("#hidden_visaduration").val()).change()
	}
	else if (hidden_radiochoice == 'Week') {
		$('#ctl00_user_rdoWeek').attr('checked',true);
		$("#txtWeek").val($("#hidden_visaduration").val()).change()
	}
	else {
		$('#ctl00_user_rdoMonth').attr('checked',true);
		$("#txtMonth").val($("#hidden_visaduration").val()).change()
	}
   VisaTypeDivShow();
   radioButtonChange(); 
});


function save_member_visa(){
	
	if (validateData()) {
        visaType=$("#VisaType").val();

		  visitDurations = ''
		  TotalvisitDurations = ''
		  radioChoices = ''
        if (visaType != '') {
        		ctl00_user_visit_duration= $('input[name=ctl00_user_visit_duration]:checked').val();

            if (ctl00_user_visit_duration == "ctl00_user_rdoDay"){
               visitDurations=($("#txtdays").val()) ;
               radioChoices = 'Day'
            }        
            else if (ctl00_user_visit_duration == "ctl00_user_rdoWeek"){
                 visitDurations= ($("#txtWeek").val());
                 radioChoices = 'Week'
            }
            else if (ctl00_user_visit_duration == "ctl00_user_rdoMonth"){
                 visitDurations= ($("#txtMonth").val());
                 radioChoices = 'Month'
            }            
            if (visaType == 'Multiple') { 
            	TotalvisitDurations=$("#drpMonth").val();
            }            
        	}
        else{
            return false;
        }

        //$('#visa_recommendations_form').serialize()

        var formData= new FormData();

        formData.append("visa_recommendation_no",$("#visa_recommendation_no").val());
        formData.append("txtRDate",$("#txtRDate").val());
        formData.append("drpCountry",$("#drpCountry").val());
        formData.append("McciaLocation",$("#McciaLocation").val());
        formData.append("drpEmbasy",$("#drpEmbasy").val());
        formData.append("txtName",$("#txtName").val());
        formData.append("txtDesg",$("#txtDesg").val());
        formData.append("txtContact",$("#txtContact").val());
        formData.append("txtEmail",$("#txtEmail").val());
        formData.append("PurposeToVisit",$("#PurposeToVisit").val());
        formData.append("txtVFDate",$("#txtVFDate").val());
        formData.append("txtVTDate",$("#txtVTDate").val());
        formData.append("txtFDate",$("#txtFDate").val());
        formData.append("VisaType",$("#VisaType").val());
        formData.append("txtCompany",$("#txtCompany").val());
        formData.append("txtAdd",$("#txtAdd").val());
        formData.append("PersonTitle",$("#PersonTitle").val());
        formData.append("visitDurations",visitDurations);
        formData.append("TotalvisitDurations",TotalvisitDurations);
        formData.append("radioChoices",radioChoices);
        formData.append("passport_no",$("#txtPassportNo").val());



        $.ajax({
                type: "POST",
                url: "/visarecommendationapp/save-edit-visa-recommendation/",
                data:formData,
                processData: false,
		 		    contentType: false,
                success: function(response) {

                if (response.success == 'true'){                      
                        bootbox.alert("<span class='center-block text-center'>Your Visa Recommendation Save Successfully</span>",function(){
                   			 $('#visa_recommendations_form').trigger("reset");
                   			 location.href="/visarecommendationapp/manage-visa/";
                        	});                   	                   	
                    }
                 else if (response.success == 'false'){   
                 		alert('Member does not exist, please contact respected office contact person')
                 }
                },
                error: function(response) {
                    console.log('Error = ',response);
                },

                beforeSend: function() {
                    $("#processing").show();
                },

                complete: function() {
                    $("#processing").hide();
                }
            });
    }

}

function validateData() {
    if (CheckCountry("#drpCountry")&CheckEmbassy("#drpEmbasy")&CheckName("#txtName")&CheckDesignation("#txtDesg")
        ) {
        return true;
    }
    return false;
}

function CheckCountry(drpCountry) {
    if ($(drpCountry).val() != '' && $(drpCountry).val() != null) {
        $("#drpCountryDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#drpCountryDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function CheckEmbassy(drpEmbasy) {
    if ($(drpEmbasy).val() != '' && $(drpEmbasy).val() != null) {
        $("#drpEmbasyDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#drpEmbasyDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function CheckName(txtName) {
    var namePattern = /[A-Za-z]+/;
    txtName = $(txtName).val()
    if (namePattern.test(txtName)) {
        $("#txtNameDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#txtNameDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function CheckDesignation(txtDesg) {
    txtDesg = $(txtDesg).val()
    if (txtDesg != '') {
        $("#txtDesgDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#txtDesgDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}


















