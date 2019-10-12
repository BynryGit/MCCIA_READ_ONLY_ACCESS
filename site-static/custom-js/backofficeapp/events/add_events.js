
$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");  


function add_new_row(){	
        $("#promocode_body").append('<tr >'+
            '<td class="has-success">'+'<input type="text"  name="min" class="form-control">'+'</td>'+
            '<td class="has-success">'+'<input style="text-transform: uppercase" type="text" name="max" class="form-control" >'+'</td>'+
            '<td class="has-success">'+'<input onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57" type="text" name="rate" class="form-control">'+'</td>'+
            '<td class="has-success">'+'<input onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57" type="text" name="ed" class="form-control">'+'</td>'+
            '<td class="has-success">'+'<button class="delete btn btn-danger btn-circle" onclick="deleteRow(this)" type="button"><i class="fa fa-trash-o" ></i></button>'+'</td>'+
            '</tr>');
}

function deleteRow(row) {
    $(row).closest("tr").remove();
}    
    
$('input[name="checkbox1_1"]').click(function () {
	   $("#early_member_charges").val(0)
	   $("#early_non_member_charges").val(0)
	   $("#early_date").val('')
		if ($('#checkbox1_1').prop("checked")) {
			$("#early_bird_div").css("display", "block");
     	}
     	else {
   		$("#early_bird_div").css("display", "none");  		
	   }	 
});

$('input[name="checkbox2_2"]').click(function () {

		if ($('#checkbox2_2').prop("checked")) {
			$("#promo_btn_div").css("display", "block");
			$("#promo_table_div").css("display", "block");
			$("#select_other").val('Yes').change();
     	}
     	else {
   		$("#promo_btn_div").css("display", "none");
			$("#promo_table_div").css("display", "none");  		
			$("#select_other").val('No').change();
	   }	 
});

function change_other_charge() {
if($("#select_other").val() == 'Yes'){
	$("#other_charges_div1").css("display", "block");
	$("#other_charges_div2").css("display", "block");
}
else {
	$("#other_charges_div1").css("display", "none");
	$("#other_charges_div2").css("display", "none");
}
}

$("#select_committee").change(function () {	  
	  $("#select_committeeDiv").addClass("has-success").removeClass("has-error");
     get_contact_person();
});

$("#select_contact1").change(function () {
	  if ($('#select_contact1 :selected').val() !='') {
		  $("#select_contact1Div").addClass("has-success").removeClass("has-error");
	 }
});
$("#select_priority").change(function () {
		  $("#select_priorityDiv").addClass("has-success").removeClass("has-error");
});
$("#select_event_type").change(function () {
		  $("#select_event_typeDiv").addClass("has-success").removeClass("has-error");
});
$("#select_criteria").change(function () {
		  $("#select_criteriaDiv").addClass("has-success").removeClass("has-error");
});
$("#select_payment").change(function () {
		  $("#select_paymentDiv").addClass("has-success").removeClass("has-error");
});
$('#event_title').keyup(function() {
    $("#event_titleDiv").addClass("has-success").removeClass("has-error");
});
$('#event_location').keyup(function() {
    $("#event_locationDiv").addClass("has-success").removeClass("has-error");
});
$("#from_date").change(function () {
		$(from_date_error).css("display", "none");
});

$("#to_date").change(function () {
		$(to_date_error).css("display", "none");
});

$("#registr_start_date").change(function () {
		$(registr_start_date_error).css("display", "none");
});
$("#registr_end_date").change(function () {
		$(registr_end_date_error).css("display", "none");
});
$("#release_date").change(function () {
		$(release_date_error).css("display", "none");
});
$('#for_whom').keyup(function() {
    $("#for_whomdiv").addClass("has-success").removeClass("has-error");
});
$('#organised_by').keyup(function() {
    $("#organised_bydiv").addClass("has-success").removeClass("has-error");
});
$('#event_objective').keyup(function() {
    $("#event_objectivediv").addClass("has-success").removeClass("has-error");
});
$('#member_charges').keyup(function() {
    $("#member_chargesDiv").addClass("has-success").removeClass("has-error");
});
$('#non_member_charges').keyup(function() {
    $("#nonmember_chargesDiv").addClass("has-success").removeClass("has-error");
});
$('#othercharge_name').keyup(function() {
    $("#otherDiv1").addClass("has-success").removeClass("has-error");
});
$('#othercharge_amt').keyup(function() {
    $("#otherDiv2").addClass("has-success").removeClass("has-error");
});
$("#event_banner").change(function () {
		$(event_banner_error).css("display", "none");
});
$("#sponsor_banner").change(function () {
		$(sponsor_banner_error).css("display", "none");
});
$('#meta_title').keyup(function() {
    $("#meta_titleDiv").addClass("has-success").removeClass("has-error");
});
$('#meta_keyword').keyup(function() {
    $("#meta_keywordDiv").addClass("has-success").removeClass("has-error");
});
$('#meta_description').keyup(function() {
    $("#meta_descriptionDiv").addClass("has-success").removeClass("has-error");
});
$('#meta_key_phrase').keyup(function() {
    $("#meta_key_phraseDiv").addClass("has-success").removeClass("has-error");
});
$("#event_location").change(function () {
		$("#event_locationDiv").addClass("has-success").removeClass("has-error");
});
$("#select_hall_id").change(function () {
		$("#select_hall_locationDiv").addClass("has-success").removeClass("has-error");
});
$('#other_location_address').keyup(function() {
    $("#other_location_addressDiv").addClass("has-success").removeClass("has-error");
});
$('#early_member_charges').keyup(function() {
    $("#early_member_chargesDiv").addClass("has-success").removeClass("has-error");
});
$('#early_non_member_charges').keyup(function() {
    $("#early_nonmember_chargesDiv").addClass("has-success").removeClass("has-error");
});
$("#early_date").change(function () {
		$(early_date_error).css("display", "none");
});

function entry_criteria() {
	select_criteria = $("#select_criteria").val()
	$("#member_charges").val(0);
   $("#non_member_charges").val(0);
	if (select_criteria == '0') {
		 $("#select_payment").val(0).change();
		 $('#member_charges').attr('readonly', true);
		 $('#non_member_charges').attr('readonly', true);
	}
	else if (select_criteria == '1') {
		$("#select_payment").val(1).change();
		$('#member_charges').attr('readonly', false);
		$('#non_member_charges').attr('readonly', false);
	}
	else if (select_criteria == '2') {
		$("#select_payment").val(0).change();
		$('#member_charges').attr('readonly', true);
		$('#non_member_charges').attr('readonly', true);
	}
	else {
		$("#select_payment").val('').change();
		$('#member_charges').attr('readonly', false);
		$('#non_member_charges').attr('readonly', false);
   }
}

function get_hall_name() {
	     $("#select_hall_locationDiv").css("display","block");	
     	  $("#gmapDiv").css("display","block");
     	  $("#otherLocationDiv").css("display","none");
        event_location_id = $('#event_location :selected').val();
        if (event_location_id != '' & event_location_id != 'other') {
            $.ajax({
                type: 'GET',
                url: '/backofficeapp/get-hall-name/',
                data: {'event_location_id': event_location_id},
                success: function (response) {   
                  if (response.success == 'true') {   
  						  $("#select_hall_id").html('').select2({data: [{id: ' ', text: 'Select Hall'}]});
                    $.each(response.hall_name_list, function (index, item) {
                        data = '<option value="'+ item.id +'">'+ item.hall_name +'</option>'
                        $("#select_hall_id").append(data);
                    });                  
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }  
     else if (event_location_id == '') {
      	$("#select_hall_id").html('').select2({data: [{id: ' ', text: 'Select Hall'}]});
     }      
     else if (event_location_id == 'other') {
     		$("#select_hall_id").html('').select2({data: [{id: ' ', text: 'Select Hall'}]});
     		$("#select_hall_locationDiv").css("display","none");	
     		$("#gmapDiv").css("display","none");	
     		$("#otherLocationDiv").css("display","block");	
     }
 }

function get_hall_location() {
        select_hall_id = $('#select_hall_id').val();
        reset_map('');
        if (select_hall_id != 'all') {
            $.ajax({
                type: 'GET',
                url: '/backofficeapp/get-hall-location/',
                data: {'hall_id': select_hall_id},
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
 
function get_contact_person() {
        commitee_id = $('#select_committee :selected').val();
        if (commitee_id) {
            $.ajax({
                type: 'GET',
                url: '/backofficeapp/get-contact-person/',
                data: {'commitee_id': commitee_id},
                success: function (response) {   
                  if (response.success == 'true') {                              
                    $('#select_contact1').val(response.contact_person_obj1).change();
                    $('#select_contact2').val(response.contact_person_obj2).change();
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }  
      else {
      	$('#select_contact1').val('').change();
      	$('#select_contact2').val('').change();
     }      
 }
 
 function upload_event_banner() {
 	
 	var input = document.getElementById("event_banner");  	  
	event_file = input.files[0];

   var formData= new FormData();		  
   formData.append("event_file",event_file);
   $.ajax({            
             type: "POST",
       		 url: "/backofficeapp/upload-event-banner/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {	                
	                if (response.success == "true") {
	                	console.log('response', response);
	                }
	                else("#errorMessage")
	            },
	            error: function(response) {
	                bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
	            },
	            beforeSend: function() {
	//                $("#processing").show();
	            },
	            complete: function() {
	//                $("#processing").hide();
	            }
        });
 }
 
  function upload_sponsor_banner() {
 	
 	var input = document.getElementById("sponsor_banner");  	  
	sponsor_file = input.files[0];

   var formData= new FormData();		  
   formData.append("sponsor_file",sponsor_file);
   $.ajax({            
             type: "POST",
       		 url: "/backofficeapp/upload-sponsor-banner/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {	                
	                if (response.success == "true") {
	                	console.log('response', response);
	                }
	                else("#errorMessage")
	            },
	            error: function(response) {
	                bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
	            },
	            beforeSend: function() {
	//                $("#processing").show();
	            },
	            complete: function() {
	//                $("#processing").hide();
	            }
        });
 }

 $("#preview-continue").click(function(event) {
//     alert($("#event_objective").val());
//	alert($("#event_objective").text()) ;
  	if (validateData()) {
  		var a = $('#sponsor_banner_div1').html();
  		if (doc_length == 0) {
  			$("#sponsor_banner_preview_div").css("display","none");
  		}
		else {
			$("#sponsor_banner_preview_div").css("display","block");
			var b = $('#sponsor_banner_div2').html(a);
		}

  		//{ 
	   $("#main_div").css("display", "none");
		$("#preview_div").css("display", "block");	
	 	$("#preview_committee").val($("#select_committee").find("option:selected").text())
	 	$("#preview_event_title").val($("#event_title").val())
	 	$("#preview_contact_person1").val($("#select_contact1").find("option:selected").text())
	 	$("#preview_contact_person2").val($("#select_contact2").find("option:selected").text())
	 	$("#preview_for_whom").text($("#for_whom").val())
	 	$("#preview_organised_by").text($("#organised_by").val())
	 	$("#preview_event_objective").text($("#event_objective").val())
	 	$("#preview_location").val($("#event_location").val())
	 	$("#preview_event_type").val($("#select_event_type").find("option:selected").text())
	 	$("#preview_entry_criteria").val($("#select_criteria").find("option:selected").text())
	 	$("#preview_from_date").val($("#from_date").val())
	 	$("#preview_to_date").val($("#to_date").val())
	 	$("#preview_member_charge").val($("#member_charges").val())
	 	$("#preview_nonmember_charge").val($("#non_member_charges").val())	 
	 	
	 	
	 	$.ajax({
                type: 'GET',
                url: '/backofficeapp/get-banner-file/',
                data: {},
                success: function (response) {   
                  if (response.success == 'true') {                              
                    var preview_event_banner = document.getElementById("preview_event_banner");
    					  preview_event_banner.src = response.event_docs_address; 
                  }                    
                },
                error: function (response) {
                    alert("Error!");
                },
      });
    }
});

 $("#cancel_preview").click(function(event) {
 	$("#main_div").css("display", "block");
	$("#preview_div").css("display", "none");
  });

 $("#submit_event").click(function(event) { 	 
		  //$('#submit_event').prop('disabled', true);
        event.preventDefault(); 
			
    	  var input = document.getElementById("event_banner");  	  
		  event_file = input.files[0];
		  
		  //var input = document.getElementById("sponsor_banner");  	  
		 //sponsor_file = input.files[0];
		  
		  var formData= new FormData();
		  
    	  formData.append("event_file",event_file);
    	  formData.append("attachments",$('#attachments').val());
    	      	 
    	  formData.append("select_committee",$('#select_committee').val());
    	  formData.append("select_contact1",$('#select_contact1').val());
    	  formData.append("select_contact2",$('#select_contact2').val());
    	  formData.append("select_priority",$('#select_priority').val());
    	  formData.append("select_event_type",$('#select_event_type').val());
        formData.append("oter_select_event_type",$('#other_event').val());
    	  formData.append("select_criteria",$('#select_criteria').val());
    	  formData.append("select_payment",$('#select_payment').val());
    	  formData.append("select_entry_level",$('#select_entry_level').val());
    	  formData.append("select_event_sponsored",$('#select_event_sponsored').val());
    	  // formData.append("expected_capacity",$('#expected_capacity').val());
    	  formData.append("event_title",$('#event_title').val());
    	  formData.append("hall_id",$('#select_hall_id').val());
    	  formData.append("other_location_address",$('#other_location_address').val());
    	  formData.append("from_date",$('#from_date').val());
    	  formData.append("to_date",$('#to_date').val());
    	  formData.append("registr_start_date",$('#registr_start_date').val());
    	  formData.append("registr_end_date",$('#registr_end_date').val());
    	  formData.append("release_date",$('#release_date').val());
    	  formData.append("for_whom",$('#for_whom').val());
    	  formData.append("organised_by",$('#organised_by').val());
    	  formData.append("event_objective",$('#event_objective').val());
    	  formData.append("member_charges",$('#member_charges').val());
    	  formData.append("non_member_charges",$('#non_member_charges').val());
    	  
    	  formData.append("disc_part_count1",$('#disc_part_count1').val());
    	  formData.append("disc_perct1",$('#disc_perct1').val());
    	  formData.append("disc_part_count2",$('#disc_part_count2').val());
    	  formData.append("disc_perct2",$('#disc_perct2').val());
    	  formData.append("disc_part_count3",$('#disc_part_count3').val());
    	  formData.append("disc_perct3",$('#disc_perct3').val());
    	      	  
    	  formData.append("expected_member",$('#expected_member').val());
    	  // formData.append("expected_nonmember",$('#expected_nonmember').val());
    	  // formData.append("expected_freemember",$('#expected_freemember').val());
    	  // formData.append("expected_sponsmember",$('#expected_sponsmember').val());    	  
    	  formData.append("othercharge_name",$('#othercharge_name').val());
    	  formData.append("othercharge_amt",$('#othercharge_amt').val());
    	  
    	  formData.append("is_early_bird",$('#checkbox1_1').prop("checked"));
		  formData.append("early_member_charges",$('#early_member_charges').val());
		  formData.append("early_non_member_charges",$('#early_non_member_charges').val());
		  formData.append("early_bird_date",$('#early_date').val());    	  
    	  
    	  
    	  formData.append("meta_title",$('#meta_title').val());
    	  formData.append("meta_keyword",$('#meta_keyword').val());
    	  formData.append("meta_description",$('#meta_description').val());
    	  formData.append("meta_key_phrase",$('#meta_key_phrase').val());
    	  formData.append("program_detail_id",$('#summernote_1').code());
    	  
    	  
    	  var promocode_list1 = new Array();
    	  var promocode_list2 = new Array();
    	  var promocode_list3 = new Array();
    	  var promocode_list4 = new Array();
    	   $("#promocode_body").find('tr').each(function () {
    	   	    var sub_list =new Array();
                check_row=$(this)
                to_whom = check_row.find("td:eq(0) input[type='text']").val()
                promocode = check_row.find("td:eq(1) input[type='text']").val()
                discount = check_row.find("td:eq(2) input[type='text']").val()
                charges = check_row.find("td:eq(3) input[type='text']").val() 
                
                promocode_list1.push(to_whom)
                promocode_list2.push(promocode)
                promocode_list3.push(discount)
                promocode_list4.push(charges)
                
			 });
			 formData.append("promocode_list1",promocode_list1);
			 formData.append("promocode_list2",promocode_list2);
			 formData.append("promocode_list3",promocode_list3);
			 formData.append("promocode_list4",promocode_list4);




        $.ajax({            
             type: "POST",
       		 url: "/backofficeapp/save-new-event/",
       		 data : formData,
				 cache: false,
		       processData: false,
		 		 contentType: false, 
             success: function(response) {
	                console.log('response', response);
	                if (response.success == "true") {
	                    bootbox.alert("<span class='center-block text-center'>Event added successfully</span>",function(){
                    			location.href = '/backofficeapp/event-details/'
                       });
	                }
	                else("#errorMessage")
	            },
	            error: function(response) {
	                bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
	            },
	            beforeSend: function() {
	                $("#processing").css('display','block');
	            },
	            complete: function() {
	                $("#processing").css('display','none');
	            }
        });     
});
function validateData() {
    if (CheckCommittee("#select_committee")&CheckPerson1("#select_contact1")&CheckPriority("#select_priority")&CheckEventType("#select_event_type")&CheckEventlevel("#select_entry_level")
        &CheckEventCriteria("#select_criteria")&CheckPayment("#select_payment")&checkEventTitle("#event_title")&checkEventLocation("#event_location")
        &CheckFromDate("#from_date")&CheckToDate("#to_date")&CheckRegistraStartDate("#registr_start_date")&CheckRegistraEndDate("#registr_end_date")
        &CheckReleaseDate("#release_date")&CheckPromoCodeRows()
        &CheckForWhom("#for_whom")&CheckOrganisedBy("#organised_by")&CheckEventObjective("#event_objective")&checkMemberCharges("#member_charges")&checkNonMemberCharges("#non_member_charges")
        &checkifOther("#select_other")&checkifEarlyBird()&checkEventBanner("#event_banner")&checkSponsorBanner("#sponsor_banner")
        &CheckMetaTitle("#meta_title")&CheckMetaKeyword("#meta_keyword")&CheckMetaDescription("#meta_description")&CheckMetaKeyPhrase("#meta_key_phrase") ) {
        return true;
    }
    return false;
}

function CheckPromoCodeRows() {
	 if ($('#checkbox2_2').prop("checked")) {
	 	      check_promo_flag = true;
				$("#promocode_body").find('tr').each(function () {
                check_row=$(this)
                check_row.find("td:eq(0)").addClass("has-success").removeClass("has-error");
                check_row.find("td:eq(1)").addClass("has-success").removeClass("has-error");
                check_row.find("td:eq(2)").addClass("has-success").removeClass("has-error");
                check_row.find("td:eq(3)").addClass("has-success").removeClass("has-error");
                
                to_whom = check_row.find("td:eq(0) input[type='text']").val().trim()
                var namePattern = /[A-Za-z]+/;
					 if (!namePattern.test(to_whom)) {
					 	  check_row.find("td:eq(0)").addClass("has-error").removeClass("has-success");
					     check_promo_flag = false;
					 }                
                promocode = check_row.find("td:eq(1) input[type='text']").val().trim()
                if (promocode == '') {
					 	  check_row.find("td:eq(1)").addClass("has-error").removeClass("has-success");
					     check_promo_flag = false;
					 }                                                
                discount = check_row.find("td:eq(2) input[type='text']").val().trim()
                if (!$.isNumeric(discount)){
					 	  check_row.find("td:eq(2)").addClass("has-error").removeClass("has-success");
					     check_promo_flag = false;
					 }                                
                charges = check_row.find("td:eq(3) input[type='text']").val().trim() 
                if (!$.isNumeric(charges)){
					 	  check_row.find("td:eq(3)").addClass("has-error").removeClass("has-success");
					     check_promo_flag = false;
					 }
                
			 });
			 return check_promo_flag;
    }
    else {
   		return true;	
	 }	
}
			 
			 
function CheckCommittee(select_committee) {
    if ($(select_committee).val() != '' && $(select_committee).val() != null) {
        $("#select_committeeDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_committeeDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckPerson1(select_contact1) {
    if ($(select_contact1).val() != '' && $(select_contact1).val() != null) {
        $("#select_contact1Div").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_contact1Div").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckPriority(select_priority) {
    if ($(select_priority).val() != '' && $(select_priority).val() != null) {
        $("#select_priorityDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_priorityDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckEventType(select_event_type) {
    if ($(select_event_type).val() != '' && $(select_event_type).val() != null) {
        $("#select_event_typeDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_event_typeDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckEventlevel(select_entry_level) {
    if ($(select_entry_level).val() != '' && $(select_entry_level).val() != null) {
        $("#select_entry_leveldiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_entry_leveldiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function CheckEventCriteria(select_criteria) {
    if ($(select_criteria).val() != '' && $(select_criteria).val() != null) {
        $("#select_criteriaDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_criteriaDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckPayment(select_payment) {
    if ($(select_payment).val() != '' && $(select_payment).val() != null) {
        $("#select_paymentDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#select_paymentDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function checkEventTitle(event_title) {
    var namePattern = /[A-Za-z]+/;
    event_title = $(event_title).val()
    if (namePattern.test(event_title)) {
        $("#event_titleDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#event_titleDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function checkEventLocation(event_location) {
	if ($(event_location).val() == '') {
		$("#event_locationDiv").addClass("has-error").removeClass("has-success");
        return false;
	}
	else if ($(event_location).val() == 'other') {
		    var namePattern = /[A-Za-z]+/;
		    other_location_address = $("#other_location_address").val()
		    if (namePattern.test(other_location_address)) {
		        $("#other_location_addressDiv").addClass("has-success").removeClass("has-error");
		        return true;
		    } else {
		        $("#other_location_addressDiv").addClass("has-error").removeClass("has-success");
		        return false;
		    } 
	}	
   else if ($(event_location).val() != '' && $(event_location).val() != null) {
        $("#event_locationDiv").addClass("has-success").removeClass("has-error");        
        if ($("#select_hall_id").val() != ' ' && $("#select_hall_id").val() != null) {
	        $("#select_hall_locationDiv").addClass("has-success").removeClass("has-error");
	        return true;
	     } else {
	        $("#select_hall_locationDiv").addClass("has-error").removeClass("has-success");
	        return false;
	     }
    }
}

function CheckFromDate(from_date) {
    from_date=$(from_date).val()
    if (from_date == ''){
        $(from_date_error).css("display", "block");
        $(from_date_error).text("Please enter From Date");
        return false;
    }else{
        $(from_date_error).css("display", "none");
        return true;
    }
}
function CheckToDate(to_date) {
    to_date=$(to_date).val()
    if (to_date == ''){
        $(to_date_error).css("display", "block");
        $(to_date_error).text("Please enter To Date");
        return false;
    }else{    	
    	  // FROM DATE
    	  from_date=$("#from_date").val()    
    	  if (from_date != '') {	      	  
	    	  start_date=from_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_start_date=start_date[0].split(" ");// we get => [04,July,2018]
	    	  new_start_time=start_date[1].split(":");// we get => [06,08]	    	   
	    	  month_list = ['January','February','March','April','May','June','July','August','September','October','November','December'];    	       
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);
	    	  st_dt = new Date(new_start_date[2],month_list.indexOf(new_start_date[1]),new_start_date[0],new_start_time[0],new_start_time[1])
	    	  
	    	  //END DATE
	    	  to_date=$("#to_date").val()
	    	  end_date=to_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_end_date=end_date[0].split(" ");// we get => [04,July,2018]
	    	  new_end_time=end_date[1].split(":");// we get => [06,08]	    	   
	    	  month_list = ['January','February','March','April','May','June','July','August','September','October','November','December'];    	       
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);	    	  
	    	  ed_dt = new Date(new_end_date[2],month_list.indexOf(new_end_date[1]),new_end_date[0],new_end_time[0],new_end_time[1])
	
	    	  if (st_dt > ed_dt) {
	    	  		$(to_date_error).css("display", "block");
        			$(to_date_error).text("Please enter 'To Date' greater than 'From Date'");
       			return false;
	    	  }
	    	  else if (st_dt < ed_dt) {
	    	  		$(to_date_error).css("display", "none");
        			return true;
	    	  }
	    	  else {
	    	  		$(to_date_error).css("display", "block");
        			$(to_date_error).text("'To Date' and 'From Date' can't be equal");
       			return false;
	    	  }
    	  }
    	  else {
        $(to_date_error).css("display", "none");
        return true;
       }
    }
}
function CheckRegistraStartDate(registr_start_date) {
    registr_start_date=$(registr_start_date).val()
    if (registr_start_date == ''){
        $(registr_start_date_error).css("display", "block");
        $(registr_start_date_error).text("Please enter Registration Start Date");
        return false;
    }else{
      
        from_date=$("#from_date").val()    
        registr_start_date=$("#registr_start_date").val()    
    	  if (from_date != '') {	    	 

	    	  new_reg_start_date=registr_start_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_start_date=new_reg_start_date[0].split(" ");// we get => [04,July,2018]
	    	  new_start_time=new_reg_start_date[1].split(":");// we get => [06,08]	    	   
	    	  month_list = ['January','February','March','April','May','June','July','August','September','October','November','December'];    	       
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);
	    	  reg_st_dt = new Date(new_start_date[2],month_list.indexOf(new_start_date[1]),new_start_date[0],new_start_time[0],new_start_time[1])	    	 	   

	    	  
	    	  //From DATE
	    	  from_date=$("#from_date").val()    		    	  
	    	  new_from_date=from_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_start_date=new_from_date[0].split(" ");// we get => [04,July,2018]
	    	  new_start_time=new_from_date[1].split(":");// we get => [06,08]	    	  	   
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);	    	  
	    	  from_dt = new Date(new_start_date[2],month_list.indexOf(new_start_date[1]),new_start_date[0],new_start_time[0],new_start_time[1])

	    	  if (reg_st_dt > from_dt) {
	    	  		$(registr_start_date_error).css("display", "block");
        			$(registr_start_date_error).text("Please enter 'Registration Start Date' smaller than 'From Date'");
       			return false;
	    	  }
	    	  else if (reg_st_dt < from_dt) {
	    	  		$(registr_start_date_error).css("display", "none");
        			return true;
	    	  }
	    	  else {
	    	  		$(registr_start_date_error).css("display", "block");
        			$(registr_start_date_error).text("'Registration Start Date' and 'From Date' can't be equal");
       			return false;
	    	  }
    	  }
    	  else {
        $(registr_start_date_error).css("display", "none");
        return true;
       }             
    }
}
function CheckRegistraEndDate(registr_end_date) {
    registr_end_date=$(registr_end_date).val()
    if (registr_end_date == ''){
        $(registr_end_date_error).css("display", "block");
        $(registr_end_date_error).text("Please enter Registration End Date");
        return false;
    }else{
    	
    	  to_date=$("#to_date").val()    
        registr_start_date=$("#registr_start_date").val()    
    	  if (to_date != '' & registr_start_date!= '') {	 	    	  
	    	  month_list = ['January','February','March','April','May','June','July','August','September','October','November','December'];    	       
	    	  
	    	  //Registration End DATE
	    	  new_reg_end_date=registr_end_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_end_date=new_reg_end_date[0].split(" ");// we get => [04,July,2018]
	    	  new_end_time=new_reg_end_date[1].split(":");// we get => [06,08]	    	   
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);
	    	  reg_end_dt = new Date(new_end_date[2],month_list.indexOf(new_end_date[1]),new_end_date[0],new_end_time[0],new_end_time[1])	    	 	   
	    	  
	    	  
	    	  //to DATE   	 	    	  
	    	  to_date1=to_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_to_date=to_date1[0].split(" ");// we get => [04,July,2018]
	    	  new_to_time=to_date1[1].split(":");// we get => [06,08]	    	  	    	  
	    	  to_dt = new Date(new_to_date[2],month_list.indexOf(new_to_date[1]),new_to_date[0],new_to_time[0],new_to_time[1])
	    	 	    	  
	    	  //Registration Start DATE
	    	  new_reg_start_date=registr_start_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_start_date=new_reg_start_date[0].split(" ");// we get => [04,July,2018]
	    	  new_start_time=new_reg_start_date[1].split(":");// we get => [06,08]	    	   
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);
	    	  reg_start_dt = new Date(new_start_date[2],month_list.indexOf(new_start_date[1]),new_start_date[0],new_start_time[0],new_start_time[1])	    	 	   
	    	  

	    	  if (reg_end_dt > to_dt) {
	    	  		$(registr_end_date_error).css("display", "block");
        			$(registr_end_date_error).text("Please enter 'Registration End Date' smaller than 'To Date'");
       			return false;
	    	  }
	    	  else if (reg_end_dt < reg_start_dt) {
	    	  		$(registr_end_date_error).css("display", "block");
        			$(registr_end_date_error).text("Please enter 'Registration End Date' greater than 'Registration Start Date'");
       			return false;
	    	  }
	    	  else if (reg_end_dt <= to_dt & reg_end_dt > reg_start_dt) {
	    	  		$(registr_end_date_error).css("display", "none");
        			return true;
	    	  }
	    	  else {
	    	  		$(registr_end_date_error).css("display", "block");
        			$(registr_end_date_error).text("'Registration End Date' can't be equal with Registration Start Date");
       			return false;
	    	  }
    	  }
    	  else {
        $(registr_end_date_error).css("display", "none");
        return true;
       }
    }
}
function CheckReleaseDate(release_date) {
    release_date=$(release_date).val()
    if (release_date == ''){
        $(release_date_error).css("display", "block");
        $(release_date_error).text("Please enter Release Date");
        return false;
    }else{
    	      	  
    	  registr_start_date=$("#registr_start_date").val()    
    	  if (registr_start_date != '') {	 
	    	   
	    	  month_list = ['January','February','March','April','May','June','July','August','September','October','November','December'];    	       
	    	  
	    	  //Release DATE
	    	  new_release_date=release_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_start_release_date=new_release_date[0].split(" ");// we get => [04,July,2018]
	    	  new_start_release_time=new_release_date[1].split(":");// we get => [06,08]	    	   
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);
	    	  release_dt = new Date(new_start_release_date[2],month_list.indexOf(new_start_release_date[1]),new_start_release_date[0],new_start_release_time[0],new_start_release_time[1])	    	 	   
	    	  
	    	  
	    	  //Registration Start DATE
	    	  new_reg_start_date=registr_start_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	    	  new_start_date=new_reg_start_date[0].split(" ");// we get => [04,July,2018]
	    	  new_start_time=new_reg_start_date[1].split(":");// we get => [06,08]	    	   
	    	  // new Date(Year, Month, Date, Hr, Min, Sec);
	    	  reg_start_dt = new Date(new_start_date[2],month_list.indexOf(new_start_date[1]),new_start_date[0],new_start_time[0],new_start_time[1])	    	 	   
	    	  ////////////	    	 
	
	    	  if (reg_start_dt < release_dt) {
	    	  		$(release_date_error).css("display", "block");
        			$(release_date_error).text("Please enter 'Release Date' smaller than 'Registration Start Date'");
       			return false;
	    	  }
	    	  else if (reg_start_dt >= release_dt) {
	    	  		$(release_date_error).css("display", "none");
        			return true;
	    	  }
	    	  else {
	    	  		$(release_date_error).css("display", "none");
        			return true;
	    	  }
    	  }
    	  else {
        $(release_date_error).css("display", "none");
        return true;
       }                     
    }
}

function CheckForWhom(for_whom) {
    var namePattern = /[A-Za-z]+/;
    for_whom = $(for_whom).val()
    if (namePattern.test(for_whom)) {
        $("#for_whomdiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#for_whomdiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckOrganisedBy(organised_by) {
    var namePattern = /[A-Za-z]+/;
    organised_by = $(organised_by).val()
    if (namePattern.test(organised_by)) {
        $("#organised_bydiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#organised_bydiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckEventObjective(event_objective) {
    var namePattern = /[A-Za-z]+/;
    event_objective = $(event_objective).val()
    if (namePattern.test(event_objective)) {
        $("#event_objectivediv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#event_objectivediv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function checkMemberCharges(member_charges) {
    member_charges=$(member_charges).val()
    
    if ($.isNumeric(member_charges)){
    	  $("#member_chargesDiv").addClass("has-success").removeClass("has-error");        
        return true;        
    }else{
    	  $("#member_chargesDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function checkNonMemberCharges(non_member_charges) {
    non_member_charges=$(non_member_charges).val()
    if ($.isNumeric(non_member_charges)){
    	  $("#nonmember_chargesDiv").addClass("has-success").removeClass("has-error");        
        return true;              
    }else{
    	  $("#nonmember_chargesDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function checkifOther(select_other) {
	select_other = $(select_other).val()
	if (select_other == 'No') {
		$("#otherDiv1").addClass("has-success").removeClass("has-error");        
		$("#otherDiv2").addClass("has-success").removeClass("has-error");        
      return true;
	}
	else {
		if ($("#othercharge_name").val() == '' & $("#othercharge_amt").val() == '') {
			$("#otherDiv1").addClass("has-error").removeClass("has-success");
			$("#otherDiv2").addClass("has-error").removeClass("has-success");
			return false;
		}
		else if ($("#othercharge_name").val() == '' & $("#othercharge_amt").val() != '') {
			$("#otherDiv1").addClass("has-error").removeClass("has-success");
			$("#otherDiv2").addClass("has-success").removeClass("has-error");
			return false;
		} 
		else if ($("#othercharge_name").val() != '' & $("#othercharge_amt").val() == '') {
			$("#otherDiv1").addClass("has-success").removeClass("has-error");
			$("#otherDiv2").addClass("has-error").removeClass("has-success");
			return false;
		}     
		else {
			$("#otherDiv1").addClass("has-success").removeClass("has-error");        
			$("#otherDiv2").addClass("has-success").removeClass("has-error");        
      	return true;
		}
	}
}

function checkifEarlyBird() {
	select_other = $(select_other).val()
	if ($('#checkbox1_1').prop("checked")) {
			 check_flag = true;
			 member_charges=$("#early_member_charges").val()
		    if (!$.isNumeric(member_charges)){
		    	  $("#early_member_chargesDiv").addClass("has-error").removeClass("has-success");  
		    	  check_flag = false;
		    }
		    
		    non_member_charges=$("#early_non_member_charges").val()
		    if (!$.isNumeric(non_member_charges)){
		    	  $("#early_nonmember_chargesDiv").addClass("has-error").removeClass("has-success");  
		    	  check_flag = false;
		    }
		    
		    early_date=$(early_date).val()
			 if (early_date == ''){
				        $(early_date_error).css("display", "block");
				        $(early_date_error).text("Please enter Early Bird Date");
				        check_flag = false;
		    }    
    		return check_flag
	}
	else {
      return true;
	}
}


function checkEventBanner(event_banner) {
	if ($('#event_banner').val()=='') {
	     $(event_banner_error).css("display", "block");
        $(event_banner_error).text("Please Select Event Banner");
        return false;
    }else{
        $(event_banner_error).css("display", "none");
        return true;
    }
}
function checkSponsorBanner(sponsor_banner) {
	return true;	
	if (doc_length == 0) {
	     $(error_dropzone).css("display", "block");
        $(error_dropzone).text("Please Select Sponsor Banner");
        return false;
    }else{
        $(error_dropzone).css("display", "none");
        return true;
    }
}
function CheckMetaTitle(meta_title) {
    var namePattern = /[A-Za-z]+/;
    meta_title = $(meta_title).val()
    if (namePattern.test(meta_title)) {
        $("#meta_titleDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#meta_titleDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}     
function CheckMetaKeyword(meta_keyword) {
    var namePattern = /[A-Za-z]+/;
    meta_keyword = $(meta_keyword).val()
    if (namePattern.test(meta_keyword)) {
        $("#meta_keywordDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#meta_keywordDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckMetaDescription(meta_description) {
    var namePattern = /[A-Za-z]+/;
    meta_description = $(meta_description).val()
    if (namePattern.test(meta_description)) {
        $("#meta_descriptionDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#meta_descriptionDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckMetaKeyPhrase(meta_key_phrase) {
    var namePattern = /[A-Za-z]+/;
    meta_key_phrase = $(meta_key_phrase).val()
    if (namePattern.test(meta_key_phrase)) {
        $("#meta_key_phraseDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#meta_key_phraseDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function disable_end_date() {
	from_date=$("#from_date").val() 
	start_date=from_date.split("-"); //04 July 2018 - 06:08 Split by '-'
	new_start_date=start_date[0].split(" ");// we get => [04,July,2018]	    	  
	$('#to_date').datetimepicker('remove');
	$("#to_date").datetimepicker({format: 'dd MM yyyy - hh:ii'});
	month_list = ['January','February','March','April','May','June','July','August','September','October','November','December'];	
	ss = new_start_date[2]+'-'+(month_list.indexOf(new_start_date[1])+1)+'-'+new_start_date[0] //2018-07-07
	$('#to_date').datetimepicker('setStartDate',ss);
}


////////////////////////////////// NEW DROPZONE ///////////////////////////
var uploaded_file_mb = 0;
var uploaded_file1_mb = 0;
var uploaded_file2_mb = 0;
var doc_length = 0
Dropzone.options.myAwesomeDropzone3 = {
    autoProcessQueue: true,
    uploadMultiple: true,
    paramName: "file",
    //maxFiles: 10,
    maxFilesize: 0.3,
    method: 'post',
    parallelUploads: 1,
    url: '/backofficeapp/upload-sponsor-images/',
    dictDefaultMessage: "Drop or Browse up to 10 images (1MB or higher in size)",
    addRemoveLinks: true,
    acceptedFiles: "",
    acceptedFiles: "image/jpeg,image/png,image/gif,.pdf,.PDF",
    dictInvalidFileType: 'This file type is not supported.',
    dictMaxFilesExceeded: "You can not upload more than 10 images.",

    init: function() {
        var myDropzone = this;
        var reordered_array = new Array();
        var temp_image_files = new Array();
        this.on("sending", function() {
            return false;
        });

        /*this.on("totaluploadprogress", function (file,progress,bytesSent) {
            uploaded_file1_mb = parseInt(bytesSent)/(1024*1024);
            uploaded_file_mb = parseFloat(uploaded_file1_mb) + parseFloat(uploaded_file2_mb)+ parseFloat(display_image_size);;
            $("#progress_bar").val(parseFloat(uploaded_file_mb));
            if(uploaded_file_mb > 100){
                $("#error-modal1").modal('show');
                $("#error-message1").text("Uploaded file size exceeds limit of 100 MB");
            }
            progrss_count = parseFloat(uploaded_file_mb).toFixed(2) + "/100 MB"
            $(".progress_count").text(progrss_count);
            var alreadyUploadedTotalSize = getTotalPreviousUploadedFilesSize(bytesSent);
        });*/


        this.on("addedfile", function(file, response) {
            $(".txt_dropzone3").text("");
            if (this.files.length) {
                var i, len, pre;
                for (i = 0, len = this.files.length; i < len - 1; i++) {
                    if (this.files[i].name == file.name && this.files[i].size == file.size && this.files[i].lastModifiedDate.toString() == file.lastModifiedDate.toString()) {
                        this.removeFile(file);
                        //return (pre = file.previewElement) != null ? pre.parentNode.removeChild(file.previewElement) : void 0;
                    }
                }
            }
            temp_image_files.push(file);
        });

        this.on("success", function(files, response) {
            doc_length = doc_length + 1;
            $('#attachment').val($('#attachment').val() + "," + response.attachid);
            $('a .dz-remove').attr('href', '/remove-advert-image/?image_id=' + response.attachid);
            reordered_array.push(response.attachid);
            $('#attachment').val(reordered_array);
            $('#attachments').val(reordered_array);
        });

        this.on("removedfile", function(file) {
            deleting_image_id = reordered_array[temp_image_files.indexOf(file)];
            $.ajax({
                url: "/backofficeapp/remove-sponsor-images/?image_id=" + deleting_image_id,
                success: function(result) {
                    doc_length = doc_length - 1;
                    arr = $('#attachment').val();
                    arr = arr.split(',');
                    console.log('Before Id Remove : ' + arr);
                    arr = jQuery.grep(arr, function(value) {
                        return value != deleting_image_id;
                    });
                    console.log('After Id Remove : ' + arr);
                    $('#attachment').val(arr);
                }
            });
            arr = $('#attachments').val();
            arr = arr.split(',');
            arr = jQuery.grep(arr, function(value) {
                return value != deleting_image_id;
            });

            $('#attachments').val(arr);
            var index = myDropzone.files.length;
            var temp_image_id = reordered_array[temp_image_files.indexOf(file)];

            reordered_array = jQuery.grep(reordered_array, function(value) {
                return value != temp_image_id;
            });

            temp_image_files = jQuery.grep(temp_image_files, function(value) {
                return value != file;
            });
            $('#attachments').val(reordered_array);
            if (myDropzone.files.length == 0) {
                $(".txt_dropzone3").text("Click or drag and drop to upload documents");
            }
        });

        this.on("maxfilesexceeded", function(file) {
            this.removeFiles(file);
            $('#lbl_upl').css("color", "red");
        });

        function getTotalPreviousUploadedFilesSize(bytesSent) {
            var totalSize = 0;
            var image_space = bytesSent;
            $("#image_space").val(image_space);
        }
    }
}

function event_type_change(){
  if($("#select_event_type").val() == 8){
  $("#other_event_div").show()
}
else{
  $("#other_event_div").hide()
}
}
