

$("#VisaType").change(function(){

        visaType=$("#VisaType").val();

        if (visaType == "Single"){

            $("#singleEntry").css("display","block")
            $("#multiEntry").css("display","none")
        }
        else if (visaType == "Multiple"){
            $("#singleEntry").css("display","block")
            $("#multiEntry").css("display","block")
        }
        else{
            $("#singleEntry").css("display","none")
            $("#multiEntry").css("display","none")
        }

});


$('input[name=ctl00_user_visit_duration]').change(function(){


ctl00_user_visit_duration= $('input[name=ctl00_user_visit_duration]:checked').val();


if (ctl00_user_visit_duration == "ctl00_user_rdoDay"){
    $("#txtdays").css("display","block")
    $("#txtWeek").css("display","none")
    $("#txtMonth").css("display","none")
}
else{
    if (ctl00_user_visit_duration == "ctl00_user_rdoWeek"){
        $("#txtdays").css("display","none")
        $("#txtWeek").css("display","block")
        $("#txtMonth").css("display","none")
    }
    else{

        $("#txtdays").css("display","none")
        $("#txtWeek").css("display","none")
        $("#txtMonth").css("display","block")

    }
}

});


function save_member_visa(){
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
        var input = document.getElementById("txtPassportCopy");
        file = input.files[0];
        var formData= new FormData();

        formData.append("passportDoc",file);
        formData.append("membershipId",$("#membershipId").val());
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
        formData.append("PassportCopyFlag",$('input[name=PassportCopy]:checked').val());
        formData.append("PersonTitle",$("#PersonTitle").val());
        formData.append("visitDurations",visitDurations);
        formData.append("TotalvisitDurations",TotalvisitDurations);
        formData.append("radioChoices",radioChoices);
        formData.append("passport_no",$("#txtPassportNo").val());



        $.ajax({
                type: "POST",
                url: "/visarecommendationapp/save-visa-recommendation-detail/",
                data:formData,
                processData: false,
		 		contentType: false,
                success: function(response) {

                if (response.success == 'true'){                      
                        bootbox.alert("<span class='center-block text-center'>Your Visa Recommendation Save Successfully</span>",function(){
                   			 $('#visa_recommendations_form').trigger("reset");
                   			 location.href="/hallbookingapp/hallbooking-landing/";
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


function reset_form(){
    location.reload();
    $('#visa_recommendations_form').trigger("reset");
}


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
     }      
 }
 
 function show_passport_copy(){
		 PassportCopy= $('input[name=PassportCopy]:checked').val();
		 if (PassportCopy == 'YES') {
		 		$("#passportDiv").css("display","block")
		 }
		 else {
		 	$("#passportDiv").css("display","none")
		 }
}            
            
            
            
            
