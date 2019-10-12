$(document).ready(function(){
    $('#inddiv').css('display','block')
    $('#compdiv').css('display','none')
    $("#membership_div").css("display","none")
    $('#org_name_inpu_div_comp').css('display','none')
    $('#org_name_inpu_div_ind').css('display','block')
    $("#org_name_select2_div_comp").css("display","none")
    $("#org_name_select2_div_ind").css("display","none")
    get_hall_location();
    $.ajax({
             type: 'GET',
             url: '/backofficeapp/get-program-details/',
             data: {'event_detail_id': $("#hidden_eventdetails_id").val()},
             success: function (response) {   
               if (response.success == 'true') {                              
                 $('#program_detail_id').html(response.event_description_indetails);
               }                    
             },
             error: function (response) {
                 alert("Error!");
             },
         });
});

function get_hall_location() {
        event_id = $('#hidden_eventdetails_id').val();
        if (event_id) {
            $.ajax({
                type: 'GET',
                url: '/eventsapp/get-hall-location/',
                data: {'event_id': event_id},
                success: function (response) {   
                  if (response.success == 'true') {  
                     // reset_map(response.locations);
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }      
 } 

//var map = null;
//function reset_map(locations){
//       if (map == null){
//	   map = new Maplace({
//   	       show_markers: true,
//   	       controls_on_map: false,
//  	       locations: locations,
//
//	   }).Load();
//        } else {
//           show_markers: false,
//           map.SetLocations(locations,true);
//        }
//    }

function get_nonmem_detail() {
    $("#non_member_id").val('');
    $("#address").val('');
    $("#ContactPerson").val('');
    $("#contact_person_email_id").val('');

    if ($("#Organizationname").val()) {
    $.ajax({
        type: "GET",
        url: "/eventsapp/get-non-member-detail/",
        data: {"non_mem_id": $("#Organizationname").val()},
        success: function(response){
            if (response.success == 'true'){
                $("#non_member_id").val(response.non_mem_id);
                $("#address").val(response.address);
                $("#contact_person_email_id").val(response.mail_id);
            }
        }
    });
  }
}

function get_nonmem_detail_comp() {
    $("#non_member_id").val('');
    $("#address").val('');
    $("#ContactPerson").val('');
    $("#contact_person_email_id").val('');

    if ($("#Organizationnamecomp").val()) {
    $.ajax({
        type: "GET",
        url: "/eventsapp/get-non-member-detail/",
        data: {"non_mem_id": $("#Organizationnamecomp").val()},
        success: function(response){
            if (response.success == 'true'){
                $("#non_member_id").val(response.non_mem_id);
                $("#address").val(response.address);
                $("#contact_person_email_id").val(response.mail_id);
            }
        }
    });
  }
}

function save_event_details(){
      window.scrollTo(0, 500);
		member_type = $("input[name='radiobtn-1']:checked").val();		 
		hidden_eventdetails_id = $("#hidden_eventdetails_id").val();
		non_member_id = $("#non_member_id").val();
		if (validateData()) {  

        $.ajax({        			
                type: "POST",
                url: "/eventsapp/save-event-details/",
                data:$('#event_details_form').serialize()+ '&member_type=' + member_type + '&hidden_eventdetails_id=' + hidden_eventdetails_id + '&non_member_id='+non_member_id,
                success: function(response) {
                  if (response.success == 'true'){                       
                   		$("#nonmem_div").css("display","none");
                   		$("#confirm_div").css("display","block");
                   		$("#head_div").css("display","none");
                   		$("#hidden_event_reg_id").val(response.event_reg_id);
                   		
                   		$("#confirm_reg_no").text(response.reg_no);
                   		$("#confirm_membership_no").text(response.membership_no_val);
                   		if (member_type =='member') {
                   		        enroll_type = $("input[name='enroll_type']:checked").val();
                   		        if (enroll_type=='IN'){
                   		            $("#confirm_org_name").text($("#selectOrganizationname option:selected").text());
                   		        }
                   		        else{
                   		            $("#confirm_org_name").text($("#selectOrganizationnamecomp option:selected").text());

                   		          }
                   	       }
                   		else {
                   		    enroll_type = $("input[name='enroll_type']:checked").val();
                   		        if (enroll_type=='IN'){
                   		             $("#confirm_org_name").text($("#Organizationname option:selected").text());
                   		        }
                   		        else{
                   		             $("#confirm_org_name").text($("#Organizationnamecomp option:selected").text());
                   		        }
                   		}
                   		$("#confirm_enrolled").text($("#enroll_type").val());
                   		$("#confirm_address").text($("#address").val());
                   		$("#confirm_contact_person").text($("#ContactPerson").val());
                   		$("#confirm_email").text($("#contact_person_email_id").val());
                   		$("#confirm_contact_no").text($("#contact_person_number").val());
                   		$("#confirm_no_part").text($("#industry_participant").val());
                   		// $("#confirm_payable_amt").text($("#hidden_payable_amount").val());
                   		// $("#confirm_discount").text($("#hidden_discount_part").val());
                  
							   $.each(response.event_part_list, function (index, item) {                        
		                        data  =  '<tr>'+
													'<td align="center">'+parseInt(index+1)+'</td><td>'+item.event_user_name+'</td><td>'+item.email_id+'</td><td>'+item.contact_no+'</td><td>'+item.designation+'</td><td>'+item.department+'</td>'+
													'</tr>'							         
							    		$('#confirm_participant_table').append(data)            
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
	
    if (CheckOrganizationName()&&CheckEmailId()&&CheckMobileNo()&&CheckOfficeNo()&&CheckPAN()&&CheckNoOfParticipant()&&CheckGST()) {
        if ($('input[name=correspondence_GST]:checked').val() == 'on' && $('input[name=UnderProcess]:checked').val() == 'on'){
        	toastr.error("<span class='center-block text-center'>Select only one option for GST</span>")
        	return false;
        }   
        return true;
    }
    return false;
}

function CheckOrganizationName() {	 
	   member_type = $("input[name='radiobtn-1']:checked").val();
	   if (member_type == 'non_member') {
	   	   // Organizationname = document.getElementById("Organizationname").getAttribute("aria-invalid")
	   	   Organizationname = $("#Organizationname").val()
	   		if (Organizationname != 'true' & Organizationname != null){
	   			return true;
	   		}else {return false; }
	   }
	   else {
	   	  // selectOrganizationname = document.getElementById("selectOrganizationname").getAttribute("aria-invalid")
	   	  selectOrganizationname = $("#selectOrganizationname").val()
	   	  if (selectOrganizationname != 'true' & selectOrganizationname != null){
	   			return true;
	   		}else {return false;}
		}	  			
}


//function CheckAddress() {
//	   // address = document.getElementById("address").getAttribute("aria-invalid")
//	   address = $("#address").val()
//	   if (address != 'true' & address != null) {
//			return true;
//	   }
//	   else {
//	   	return false;
//		}
//}
function CheckEmailId() {
	   // email_id = document.getElementById("contact_person_email_id").getAttribute("aria-invalid")
	   email_id = $("#contact_person_email_id").val()
	   if (email_id != 'true' & email_id != null) {
			return true;
	   }
	   else {
	   	return false;
		}	  			
}
function CheckMobileNo() {
	   // contact_person_number = document.getElementById("contact_person_number").getAttribute("aria-invalid")
	   contact_person_number = $("#contact_person_number").val()
	   if (contact_person_number != 'true' & contact_person_number != null) {
			return true;
	   }
	   else {
	   	return false;
		}	  			
}
function CheckOfficeNo() {
	   // contact_office_number = document.getElementById("contact_office_number").getAttribute("aria-invalid")
	   contact_office_number = $("#contact_office_number").val()
	   if (contact_office_number != null) {
	   	return true;
	   }
	   else if (contact_office_number == 'false') {
			return true;
	   }
	   else {
	   	return false;
		}	  			
}

function CheckPAN() {
		if ($('input[name=CorrespondencePanCheck]:checked').val() == 'on'){
				return true;
				
		}else {
			var panVal = $('#CorrespondencePan').val();
			var regpan = /^([a-zA-Z]{5})(\d{4})([a-zA-Z]{1})$/;
			if(regpan.test(panVal)){
			   return true;
			}else{
				return false;
			}
		}				
}

function CheckGST() {
		if ($('input[name=correspondence_GST]:checked').val() == 'on'){
				return true;
				
		}else if ($('input[name=UnderProcess]:checked').val() == 'on'){
				return true;
		}
		else {
			var gst_no = $("#CorrespondenceGSTText").val();
			var regpan = /^([a-zA-Z0-9]){15}?$/;
			if(regpan.test(gst_no)){
			   return true;
			}else{
				return false;
			}
		}				
}

// function CheckGST() {
// 		if ($('input[name=correspondence_GST]:checked').val() == 'Applicable'){
// 				gst_no = $("#CorrespondenceGSTText").val();
// 				if (gst_no != '') {
// 					return true;
// 				}
// 				else {
// 					return false;
// 				}
// 		}else {
// 			return true;			
// 		}				
// }

function CheckNoOfParticipant() {
	industry_participant_count = $("#industry_participant").val()
	if (industry_participant_count) {
		   check_flag = 1
			for (i = 0; i < parseInt(industry_participant_count); i++) {
			
			      firstname = $("#firstname_"+i).val();
					if (firstname == '') {
							check_flag = 0
					}
					Designation = $("#Designation_"+i).val();
					if (Designation == '') {
							check_flag = 0
					}
					email = $("#email_"+i).val();
					if (email == '') {
							check_flag = 0
					}
					ContactNumber = $("#ContactNumber_"+i).val();
					if (ContactNumber == '') {
							check_flag = 0
					}														
         }
    if (check_flag == 1) {
    	  return true;
    	}
    else {
    	return false;
    }	
	}
	else {
		return false;
	}
}

toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-top-center",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}


function open_discount_div() {
	$("#promocode_div1").css("display","none")
	$("#promocode_div2").css("display","block")
}
function remove_discount_div() {
	$("#promocode_div1").css("display","block")
	$("#promocode_div2").css("display","none")
}

function append_part_div(){
	if($("#industry_participant").val() == ''){
		$("#participant_data_div").hide();
	}
	else{
		$("#participant_data_div").show();
	}
	industry_participant_count = $("#industry_participant").val()
	$("#same_as_above").css("display","none")
	if (industry_participant_count) {
   $("#same_as_above").css("display","block")
	member_type = $("input[name='radiobtn-1']:checked").val();
	enroll_type = $("input[name='enroll_type']:checked").val();

	organization_id = $('#selectOrganizationname').val();
	organization_id = $('#selectOrganizationnamecomp').val();
	if (member_type == 'member') {		
		if (enroll_type == 'IN'){
        	organization_id = $('#selectOrganizationname').val();
        }
        else {
                organization_id = $('#selectOrganizationnamecomp').val();
        }

	}

	$.ajax({        			
          type: "GET",
          url: "/eventsapp/get-total-event-amount/",
          data:{'organization_id':organization_id,'state_id':$('#state_id').val(),'eventdetails_id':$('#hidden_eventdetails_id').val(),'industry_participant_count':industry_participant_count,'member_type':member_type,'enroll_type':enroll_type},
          success: function(response) {
				
            if (response.success == 'true'){	
            		$('#total_fees').text('')
   					$('#total_fees').append('<i class="fa fa-inr"></i> ')
						$('#total_fees').append(response.total_fees)
						$('#hidden_total_fees').val(response.total_fees)	
						$('#participant_div').html('')					
						
						$('#total_gst').text('')
   					$('#total_gst').append('<i class="fa fa-inr"></i> ')
						$('#total_gst').append(response.add_gst)
						$('#hidden_total_gst').val(response.add_gst)	
						
						$('#discount_part').text('')
   					$('#discount_part').append('<i class="fa fa-inr"></i> ')
						$('#discount_part').append(response.total_discount)					
		
						$('#hidden_discount_part').val(response.total_discount)							
						$('#payable_amount').text('')
   					$('#payable_amount').append('<i class="fa fa-inr"></i> ')
						$('#payable_amount').append(response.total_payable_amount)
						$('#hidden_payable_amount').val(response.total_payable_amount)
						$("#participant_data").find("tr:not(:first)").remove();
					   for (i = 0; i < parseInt(industry_participant_count); i++) {

					   		$("#participant_data_body").append('<tr>'+
			                 '<td class="has-success text-overflow: ellipsis;" width="5px"><label class="text-dark " id= "participant_id" for="participant_id">'+(i+1)+'</label></td>'+
			                 '<td class="has-success text-overflow: ellipsis;" width="25px" style="word-wrap: break-word"><div class="validateField mandatory"><input type="text" class="form-control validateRequired validateAlphaonly" name="firstname_'+i+'" id="firstname_'+i+'" maxlength="50"></td>'+
			                 '<td class="has-success text-overflow: ellipsis;" width="25px" style="word-wrap: break-word"><div class="validateField mandatory"><input type="text" class="form-control  validateRequired validateEmail" name="email_'+i+'" id="email_'+i+'" maxlength="50"></div></td>'+
			                 '<td class="has-success text-overflow: ellipsis;" width="15px" style="word-wrap: break-word"><div class="validateField mandatory"><input type="text" class="form-control validateRequired validateNumber validateMobileNoLimit" name="ContactNumber_'+i+'" id="ContactNumber_'+i+'" maxlength="10"></div></td>'+
			                 '<td class="has-success text-overflow: ellipsis;" width="20px" style="word-wrap: break-word"><div class="validateField mandatory"><input type="text" class="form-control validateRequired validateAlphaonly" name="Designation_'+i+'" id="Designation_'+i+'" maxlength="50"></div></td>'+                                             
			                 '<td class="has-success text-overflow: ellipsis;" style="word-wrap: break-word"><div class="validateField mandatory"><input type="text" class="form-control validateRequired validateAlphaonly" name="Department'+i+'" id="Department'+i+'" maxlength="50"></div></td>'+                                             
			                 '</tr>'
			                 );

					                //      data = 	'<label class="col-md-2 control-label" for="Name">Name<span'+
					                //                         ' class="mandatory">*</span></label>'+
					
					                //                '<div class="col-md-4">'+
					                //                      '<div class="validateField">'+
					                //                         '<input type="text" class="form-control validateRequired validateAlphaonly"'+
					                //                                'name="firstname_'+i+'" id="firstname_'+i+'" maxlength="50">'+
					                //                     '</div>'+
					                //                 '</div>'+
					                //                 '<label class="col-md-2 control-label" for="Designation ">Designation<span'+
					                //                         ' class="mandatory">*</span> </label>'+
					
					                //                 '<div class="col-md-4">'+
					                //                     '<div class="validateField">'+
					                //                         '<input type="text" class="form-control validateRequired validateAlphaonly"'+
					                //                                'name="Designation_'+i+'" id="Designation_'+i+'" maxlength="50">'+
					                //                     '</div>'+
					                //                 '</div>'+
					                //                 '<label class="col-md-2 control-label" for="Designation ">Email Id.<span'+
					                //                         ' class="mandatory">*</span></label>'+
					
					                //                 '<div class="col-md-4">'+
					                //                     '<div class="validateField">'+
					                //                         '<input type="text" class="form-control  validateRequired validateEmail"'+
					                //                                'name="email_'+i+'" id="email_'+i+'" maxlength="50">'+
					                //                     '</div>'+
					                //                 '</div>'+
					                //                 '<label class="col-md-2 control-label" for="Contact No">Mobile No<span'+
					                //                         ' class="mandatory">*</span></label>'+
					
					                //                 '<div class="col-md-4">'+
					                //                     '<div class="validateField">'+
					                //                         '<input type="text"'+
					                //                                'class="form-control validateRequired validateNumber validateMobileNoLimit"'+
					                //                                'name="ContactNumber_'+i+'" id="ContactNumber_'+i+'" maxlength="10">'+
					                //                     '</div>'+
					                //                 '</div>'
					                // $('#participant_div').append(data)

					    }
					    if ($('input[name=same_as_above_check]:checked').val() == 'on'){
								$('#firstname_0').val($('#ContactPerson').val())					                                
								$('#email_0').val($('#contact_person_email_id').val())					                                
								$('#ContactNumber_0').val($('#contact_person_number').val())
						}
						else{
								$('#firstname_0').val('')					                                
								$('#email_0').val('')					                                
								$('#ContactNumber_0').val('')
						}
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
   else {
   	$('#participant_div').html('')
   	$('#total_fees').text('')
   	$('#total_fees').append('<i class="fa fa-inr"></i> ')
		$('#total_fees').append(0)
		$('#hidden_total_fees').val(0)	
		
		$('#total_gst').text('')
		$('#total_gst').append('<i class="fa fa-inr"></i> ')
		$('#total_gst').append(0)
		$('#hidden_payable_amount').val(0)	
	
		
		$('#discount_part').text('')
		$('#discount_part').append('<i class="fa fa-inr"></i> ')
		$('#discount_part').append(0)
		$('#discount_per_id').text('')
		//$('#discount_per_id').append(0)
		//$('#discount_per_id').append('%')
		$('#hidden_discount_part').val(0)	
		
		$('#payable_amount').text('')
		$('#payable_amount').append('<i class="fa fa-inr"></i> ')
		$('#payable_amount').append(0)
		$('#hidden_payable_amount').val(0)												
   }
}

function get_total_count() {
	industry_participant_count = $("#industry_participant").val()
	member_type = $("input[name='radiobtn-1']:checked").val();
    enroll_type = $("input[name='enroll_type']:checked").val();

	$.ajax({        			
          type: "GET",
          url: "/eventsapp/get-total-event-amount/",
          data:{'state_id':$('#state_id').val(),'eventdetails_id':$('#hidden_eventdetails_id').val(),'industry_participant_count':industry_participant_count,'member_type':member_type,'enroll_type':enroll_type},
          success: function(response) {
				
            if (response.success == 'true'){	
            
            		$('#total_fees').text('')
   					$('#total_fees').append('<i class="fa fa-inr"></i> ')
						$('#total_fees').append(response.total_fees)
						$('#hidden_total_fees').val(response.total_fees)	
						
						$('#total_gst').text('')
   					$('#total_gst').append('<i class="fa fa-inr"></i> ')
						$('#total_gst').append(response.add_gst)
						$('#hidden_total_gst').val(response.add_gst)	
						
						$('#discount_part').text('')
   					$('#discount_part').append('<i class="fa fa-inr"></i> ')
						$('#discount_part').append(response.total_discount)
						$('#hidden_discount_part').val(response.total_discount)	
						
						$('#payable_amount').text('')
   					$('#payable_amount').append('<i class="fa fa-inr"></i> ')
						$('#payable_amount').append(response.total_payable_amount)
						$('#hidden_payable_amount').val(response.total_payable_amount)	
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

$('#same_as_above_check').change(function(){
	if ($('input[name=same_as_above_check]:checked').val() == 'on'){
			$('#firstname_0').val($('#ContactPerson').val())					                                
			$('#email_0').val($('#contact_person_email_id').val())					                                
			$('#ContactNumber_0').val($('#contact_person_number').val())
	}
	else{
			$('#firstname_0').val('')					                                
			$('#email_0').val('')					                                
			$('#ContactNumber_0').val('')
	}
});

	
//function change_div(){
//	member_type = $("input[name='radiobtn-1']:checked").val();
//	if (member_type == 'member') {
//	    $("#industry_participant").val('').change();
//	    $('#participant_div').html('')
//		$("#org_name_inpu_div").css("display","none")
//		$("#org_name_select2_div").css("display","block")
//		$("#membership_div").css("display","block")
//        $('#org_name_inpu_div_comp').css('display','none')
//        $('#org_name_inpu_div_ind').css('display','none')
//	}
//	else {
//		$("#industry_participant").val('').change();
//		$('#participant_div').html('')
//		$("#org_name_inpu_div").css("display","block")
//		$("#org_name_select2_div").css("display","none")
//		$("#membership_div").css("display","none")
//	}
//}

$('#CorrespondencePanCheck').change(function(){
if ($('input[name=CorrespondencePanCheck]:checked').val() == 'on'){
$("#CorrespondencePan").removeClass('validateRequired');
$("#CorrespondencePan-error").text('');
$("#CorrespondencePan").val('')
$("#CorrespondencePan").closest('div').removeClass('has-error');
document.getElementById("CorrespondencePan").readOnly = true;
}
else{
$("#CorrespondencePan").addClass('validateRequired');
document.getElementById("CorrespondencePan").readOnly = false;
}
});



$('#correspondence_GST').change(function(){
	// alert('correspondence_GST')
	// alert($('input[name=correspondence_GST]:checked').val())
	// alert($('input[name=UnderProcess]:checked').val())
	if ($('input[name=correspondence_GST]:checked').val() == 'on'){
		$('#CorrespondenceGSTText').removeClass('validateRequired')
		$("#CorrespondencePan-error").text('');
		$("#CorrespondenceGSTText").val('')
		$("#CorrespondenceGSTText").closest('div').removeClass('has-error');
		document.getElementById("CorrespondenceGSTText").readOnly = true;
	}
	
	else{
		if ($('input[name=UnderProcess]:checked').val() == 'on'){
		$('#CorrespondenceGSTText').removeClass('validateRequired')
		$("#CorrespondencePan-error").text('');
		$("#CorrespondenceGSTText").val('')
		$("#CorrespondenceGSTText").closest('div').removeClass('has-error');
		document.getElementById("CorrespondenceGSTText").readOnly = true;
		}
		else{
		$("#CorrespondenceGSTText").addClass('validateRequired');
		document.getElementById("CorrespondenceGSTText").readOnly = false;
	}
	}
	
});


$('#UnderProcess').change(function(){
	// alert('UnderProcess')
	// alert($('input[name=correspondence_GST]:checked').val())
	// alert($('input[name=UnderProcess]:checked').val())
	if ($('input[name=UnderProcess]:checked').val() == 'on'){
		$('#CorrespondenceGSTText').removeClass('validateRequired')
		$("#CorrespondencePan-error").text('');
		$("#CorrespondenceGSTText").val('')
		$("#CorrespondenceGSTText").closest('div').removeClass('has-error');
		document.getElementById("CorrespondenceGSTText").readOnly = true;
	}
	
	else{
		if ($('input[name=correspondence_GST]:checked').val() == 'on'){
		$('#CorrespondenceGSTText').removeClass('validateRequired')
		$("#CorrespondencePan-error").text('');
		$("#CorrespondenceGSTText").val('')
		$("#CorrespondenceGSTText").closest('div').removeClass('has-error');
		document.getElementById("CorrespondenceGSTText").readOnly = true;
		}
		else{
		$("#CorrespondenceGSTText").addClass('validateRequired');
		document.getElementById("CorrespondenceGSTText").readOnly = false;
		}
	}
	
});
// $('input[name=correspondence_GST]').change(function(){


//     gstValue= $('input[name=correspondence_GST]:checked').val();
//     if ( gstValue == "Applicable"){
//     $("#GSTField").css('display','block');
//     $('#CorrespondenceGSTText').addClass('validateRequired')
//     }
//     else{
//     $("#GSTField").css('display','none');
//     $('#CorrespondenceGSTText').removeClass('validateRequired')
//     }

// });


function confirm_save_event_details() {
        mail_radio=$('input[name=radiobtn-3]:checked').val()
        event_reg_id = $('#hidden_event_reg_id').val();
        if (event_reg_id) {
            $.ajax({
                type: 'GET',
                url: '/eventsapp/confirm-event-registration/',
                data: {'event_reg_id': event_reg_id,'confirm_mail':mail_radio},
                success: function (response) {   
                  if (response.success == 'true') {                                                                 
                            bootbox.alert("<span class='center-block text-center'>Event Registration added successfully</span>",function(){
                   			 location.href = '/eventsapp/events-home/'
                   	});
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }      
 } 
 
function get_membership_no() {
        organization_id = $('#selectOrganizationname').val();
        if (organization_id) {
            $.ajax({
                type: 'GET',
                url: '/eventsapp/get-membership-no/',
                data: {'organization_id': organization_id},
                success: function (response) {   
                  if (response.success == 'true') { 
                  	
                  	$("#membership_id").text(response.member_associate_no)
                  	$("#address").text(response.correspond_address)   
                  	$("#ContactPerson").val(response.contact_person)    
                  	$("#contact_person_email_id").val(response.email_id)  
                  	$("#contact_person_number").val(response.mobile_no)   
                  	$("#CorrespondencePan").val(response.pan_no)   
                  	$("#CorrespondenceGSTText").val(response.gst_no)                                   
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }   
        else {
        	$("#membership_id").text('')
      }   
 }

function get_membership_no_comp() {
        organization_id = $('#selectOrganizationnamecomp').val();
        if (organization_id) {
            $.ajax({
                type: 'GET',
                url: '/eventsapp/get-membership-no/',
                data: {'organization_id': organization_id},
                success: function (response) {
                  if (response.success == 'true') {

                  	$("#membership_id").text(response.member_associate_no)
                  	$("#address").text(response.correspond_address)
                  	$("#ContactPerson").val(response.contact_person)
                  	$("#contact_person_email_id").val(response.email_id)
                  	$("#contact_person_number").val(response.mobile_no)
                  }
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }
        else {
        	$("#membership_id").text('')
      }
 }


$('input[name=medium]').change(function(){
    mediumValue= $('input[name=medium]:checked').val();
    if (mediumValue == "2"){
    $("#social_medium_div").css('display','block');
    $('#CorrespondenceGSTText').addClass('validateRequired')
    }
    else{
    $("#social_medium_div").css('display','none');
    $('#CorrespondenceGSTText').removeClass('validateRequired')
    }
});


function change_ind(){
    member_type = $("input[name='radiobtn-1']:checked").val();
	if (member_type == 'member') {
	    $("#org_name_select2_div_ind").val('').change();
	    $('#participant_div').html('')
	    $("#membership_id").change();
	    $("#industry_participant").val('').change();
	    $("#address").val('').change();
	    $("#ContactPerson").val('').change();
	    $("#contact_person_number").val('').change();
	    $("#contact_person_email_id").val('').change();
		$("#membership_div").css("display","block")
		$('#inddiv').css('display','block')
        $('#compdiv').css('display','none')
        $('#org_name_inpu_div_comp').css('display','none')
        $('#org_name_inpu_div_ind').css('display','none')
        $("#org_name_select2_div_comp").css("display","none")
        $("#org_name_select2_div_ind").css("display","block")
        $('#Organizationname').removeClass('validateRequired')
        $('#Organizationnamecomp').removeClass('validateRequired')
        $('#selectOrganizationname').addClass('validateRequired')
        $('#selectOrganizationnamecomp').removeClass('validateRequired')
	}
	else {
	    $("#org_name_inpu_div_ind").val('').change();
	    $('#participant_div').html('')
	    $("#industry_participant").val('').change();
	    $("#address").val('').change();
	     $("#ContactPerson").val('').change();
	    $("#contact_person_number").val('').change();
	    $("#contact_person_email_id").val('').change();
        $('#inddiv').css('display','block')
        $('#compdiv').css('display','none')
        $("#membership_div").css("display","none")
        $('#org_name_inpu_div_comp').css('display','none')
        $('#org_name_inpu_div_ind').css('display','block')
        $("#org_name_select2_div_comp").css("display","none")
        $("#org_name_select2_div_ind").css("display","none")
        $('#Organizationname').addClass('validateRequired')
        $('#Organizationnamecomp').removeClass('validateRequired')
        $('#selectOrganizationname').removeClass('validateRequired')
        $('#selectOrganizationnamecomp').removeClass('validateRequired')
	}

}

function change_comp(){
    member_type = $("input[name='radiobtn-1']:checked").val();
	if (member_type == 'member') {
	    $("#org_name_select2_div_comp").val('').change();
	    $('#participant_div').html('')
	    $("#industry_participant").val('').change();
	    $("#address").val('').change();
	    $("#ContactPerson").val('').change();
	    $("#contact_person_number").val('').change();
	    $("#membership_id").change();
	    $("#contact_person_email_id").val('').change();
		$("#membership_div").css("display","block")
		$('#inddiv').css('display','none')
        $('#compdiv').css('display','block')
        $('#org_name_inpu_div_comp').css('display','none')
        $('#org_name_inpu_div_ind').css('display','none')
        $("#org_name_select2_div_comp").css("display","block")
        $("#org_name_select2_div_ind").css("display","none")
        $('#Organizationname').removeClass('validateRequired')
        $('#Organizationnamecomp').removeClass('validateRequired')
        $('#selectOrganizationname').removeClass('validateRequired')
        $('#selectOrganizationnamecomp').addClass('validateRequired')
	}
	else {
	    $("#org_name_inpu_div_comp").val('').change();
	    $("#address").val('').change();
	     $("#ContactPerson").val('').change();
	    $("#contact_person_number").val('').change();
	    $("#industry_participant").val('').change();
	    $("#contact_person_email_id").val('').change();
	    $('#participant_div').html('')
        $('#inddiv').css('display','none')
        $('#compdiv').css('display','block')
        $("#membership_div").css("display","none")
        $('#org_name_inpu_div_comp').css('display','block')
        $('#org_name_inpu_div_ind').css('display','none')
        $("#org_name_select2_div_comp").css("display","none")
        $("#org_name_select2_div_ind").css("display","none")
        $('#Organizationname').removeClass('validateRequired')
        $('#Organizationnamecomp').addClass('validateRequired')
        $('#selectOrganizationname').removeClass('validateRequired')
        $('#selectOrganizationnamecomp').removeClass('validateRequired')

	}

}
