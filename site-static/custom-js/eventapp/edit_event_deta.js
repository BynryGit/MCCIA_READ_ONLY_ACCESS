$(document).ready(function(){
    get_hall_location();
    append_part_div();
});

function get_hall_location() {
        event_reg_id = $('#hidden_eventreg_id').val();
        if (event_reg_id) {
            $.ajax({
                type: 'GET',
                url: '/eventsapp/get-edit-hall-location/',
                data: {'event_reg_id': event_reg_id},
                success: function (response) {   
                  if (response.success == 'true') {                                                                 
                     reset_map(response.locations);
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }      
 } 

var map = null;
function reset_map(locations){
       if (map == null){
	   map = new Maplace({
   	       show_markers: true,
   	       controls_on_map: false,
  	       locations: locations,

	   }).Load();
        } else {
           show_markers: false,
           map.SetLocations(locations,true);
        }
    }
    
function save_event_details(){
	if (validateData()) { 
        $.ajax({        			
                type: "POST",
                url: "/eventsapp/save-edit-event/",
                data:$('#event_details_form').serialize(),
                success: function(response) {
                  if (response.success == 'true'){
   							//window.open('/backofficeapp/event-registrations/');      							
   							 bootbox.alert("<span class='center-block text-center'>Action against event added successfully</span>",function(){
                   				 location.href = '/eventsapp/events-home/'
                   		});          	                        
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
    if (CheckOrganisationName("#Organizationname")&CheckSelectOrganisationName("#selectOrganizationname")&CheckAddress("#address")
        &CheckContactPerson("#ContactPerson")&CheckEmailId("#contact_person_email_id")&CheckMobileNo("#contact_person_number")&CheckNoOfParticipant("#hidden_industry_participant")) {
        return true;
    }
    return false;
}

function CheckOrganisationName(Organizationname) {
	if ($("#hidden_is_member_flag").val() == 'False'){
	    if ($(Organizationname).val() != '') {
	        return true;
	    } else {
	        return false;
	    }
   }
   else {
   	return true;
  }
}

function CheckSelectOrganisationName(Organizationname) {
	if ($("#hidden_is_member_flag").val() == 'True'){
	    if ($(selectOrganizationname).val() != '') {
	        return true;
	    } else {
	        return false;
	    }
   }
   else {
   	return true;
  }
}

function CheckAddress(address) {
	if ($(address).val() != '') {
	        return true;
	    } else {
	        return false;
  }
}
function CheckContactPerson(ContactPerson) {
	if ($(ContactPerson).val() != '') {
	        return true;
	    } else {
	        return false;
  }
}
function CheckEmailId(contact_person_email_id) {
	if ($(contact_person_email_id).val() != '') {
	        return true;
	    } else {
	        return false;
  }
}
function CheckMobileNo(contact_person_number) {
	if ($(contact_person_number).val() != '') {
	        return true;
	    } else {
	        return false;
  }
}

function CheckNoOfParticipant(hidden_industry_participant) {	
		industry_participant_count = $("#hidden_industry_participant").val()	
		check_flag_part = 0
		for (i = 0; i < parseInt(industry_participant_count); i++) {
			if ($('#firstname_'+i).val() == '') {
					check_flag_part = 1
			}
			if ($('#Designation_'+i).val() == '') {
					check_flag_part = 1
			}		                  				                                
		 }		
		 
		 if (check_flag_part == 0) {
	        return true;
	    } else {
	        return false;
  }	    
}


function append_part_div(){
	industry_participant_count = $("#industry_participant").val()
	$.ajax({        			
          type: "GET",
          url: "/eventsapp/get-participant-details/",
          data:{'eventreg_id':$('#hidden_eventreg_id').val()},
          success: function(response) {
				
            if (response.success == 'true'){	           
						$('#participant_div').html('')					  					    
					   $.each(response.participant_list, function (index, item) {
                        
                        data = 	'<label class="col-md-2 control-label" for="Name">Name<span'+
					                                        ' class="mandatory">*</span></label>'+
					
					                               '<div class="col-md-4">'+
					                                     '<div class="validateField">'+
					                                        '<input type="text" class="form-control validateRequired validateAlphaonly"'+
					                                               'name="firstname_'+index+'" id="firstname_'+index+'" maxlength="50" value="'+item.event_user_name+'">'+   
					                                    '</div>'+
					                                '</div>'+
					                                '<label class="col-md-2 control-label" for="Designation ">Designation<span'+
					                                        ' class="mandatory">*</span> </label>'+
					
					                                '<div class="col-md-4">'+
					                                    '<div class="validateField">'+
					                                        '<input type="text" class="form-control validateRequired validateAlphaonly"'+
					                                               'name="Designation_'+index+'" id="Designation_'+index+'" maxlength="50" value="'+item.designation+'">'+
					                                    '</div>'+
					                                '</div>'+
					                                '<label class="col-md-2 control-label" for="Designation ">Email Id.</label>'+
					
					                                '<div class="col-md-4">'+
					                                    '<div class="validateField">'+
					                                        '<input type="text" class="form-control  validateEmail"'+
					                                               'name="email_'+index+'" id="email_'+index+'" maxlength="50" value="'+item.email_id+'">'+
					                                    '</div>'+
					                                '</div>'+
					                                '<label class="col-md-2 control-label" for="Contact No">Mobile No</label>'+
					
					                                '<div class="col-md-4">'+
					                                    '<div class="validateField">'+
					                                        '<input type="text"'+
					                                               'class="form-control validateNumber validateMobileNoLimit"'+
					                                               'name="ContactNumber_'+index+'" id="ContactNumber_'+index+'" maxlength="10" value="'+item.contact_no+'">'+
					                                    '</div>'+
					                                '</div>'+
					                                '<input type="hidden"'+
					                                               'name="hidden_participant_'+index+'" id="hidden_participant_'+index+'" value="'+item.id+'">'
					                $('#participant_div').append(data)
					                
                    });                                        
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










