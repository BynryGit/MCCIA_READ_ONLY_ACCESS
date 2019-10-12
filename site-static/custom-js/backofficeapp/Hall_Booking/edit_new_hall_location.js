$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display", "block");

$("#edit_hall_location").click(function (event) {
	event.preventDefault();
	if (validateData()) {
		$.ajax({
			type: "POST",
			url: '/backofficeapp/edit-save-hall-location/',
			data: $("#edit_hall_location_form").serialize(),
			success: function (response) {
				if (response.success == 'true') {
					$("#success_modal").modal('show');
				}else if (response.success == "Alreadyexist") {
				    $("#error_msg").text("Location Already Exist")
					$("#error-modal").modal('show');
				}else {
				    $("#error_msg").text("Sorry Something Went Wrong")
					$("#error-modal").modal('show');
				}
			},
			beforeSend: function () {
				$("#processing").css('display', 'block');
			},
			complete: function () {
				$("#processing").css('display', 'none');
			},
			error: function (response) {
				alert("_Error");
			}
		});
	}
});


function validateData() {
	if (checkhall_location("#edit_hall_location_detail") & check_terms_condition("#edit_terms_condition") & check_contact_person1("#edit_contact_person1") &
		check_deposit("#edit_deposit") & check_hall_rent_on_holiday("#edit_hall_rent_holiday") & check_deposit_factor_on_holiday("#edit_deposit_holiday_factor") & check_hall_address("#edit_address") ) {
		return true;
	}
	return false;
}

function checkhall_location(edit_hall_location_detail) {
	var namePattern = /[A-Za-z]+/;
	edit_hall_location_detail = $(edit_hall_location_detail).val()
	if (namePattern.test(edit_hall_location_detail)) {
	    $("#edit_hall_location_error").closest("div").removeClass('has-error').addClass('has-success')
//		$(edit_hall_location_error).css("display", "none");
		return true;
	} else {
	    $("#edit_hall_location_error").closest("div").removeClass('has-success').addClass('has-error')
//		$(edit_hall_location_error).css("display", "block");
//		$(edit_hall_location_error).text("Please enter Location name");
		return false;
	}
}



function check_terms_condition(edit_terms_condition) {
	if ($(edit_terms_condition).val() != '' && $(edit_terms_condition).val() != null) {
	    $("#edit_terms_condition_error").closest("div").removeClass('has-error').addClass('has-success')
//		$("#edit_terms_condition_error").css("display", "none");
		return true;
	} else {
	    $("#edit_terms_condition_error").closest("div").removeClass('has-success').addClass('has-error')
//		$("#edit_terms_condition_error").css("display", "block");
//		$("#edit_terms_condition_error").text("Please enter terms and condition");
		return false;
	}
}

function check_deposit(edit_deposit) {
	var namePattern = /^\d+(\.\d{1,2})?$/
	edit_deposit = $(edit_deposit).val()
	if (namePattern.test(edit_deposit)) {
	    $("#edit_deposit_error").closest("div").removeClass('has-error').addClass('has-success')
//		$(edit_deposit_error).css("display", "none");
		return true;
	} else {
	    $("#edit_deposit_error").closest("div").removeClass('has-success').addClass('has-error')
//		$(edit_deposit_error).css("display", "block");
//		$(edit_deposit_error).text("Please enter deposit amount");
		return false;
	}
}


function check_contact_person1(edit_contact_person1) {
	if ($(edit_contact_person1).val() != '' && $(edit_contact_person1).val() != null) {
	    $("#edit_contact_person1_error").closest("div").removeClass('has-error').addClass('has-success')
//		$("#edit_contact_person1_error").css("display", "none");
		return true;
	} else {
	    $("#edit_contact_person1_error").closest("div").removeClass('has-success').addClass('has-error')
//		$("#edit_contact_person1_error").css("display", "block");
//		$("#edit_contact_person1_error").text("Please select Contact person 1");
		return false;
	}
}


function check_hall_rent_on_holiday(edit_hall_rent_holiday) {
	var namePattern = /^\d+(\.\d{1,2})?$/
	edit_hall_rent_holiday = $(edit_hall_rent_holiday).val()
	if (namePattern.test(edit_hall_rent_holiday)) {
	    $("#edit_hall_rent_holiday_error").closest("div").removeClass('has-error').addClass('has-success')
//		$("#edit_hall_rent_holiday_error").css("display", "none");
		return true;
	} else {
	    $("#edit_hall_rent_holiday_error").closest("div").removeClass('has-success').addClass('has-error')
//		$("#edit_hall_rent_holiday_error").css("display", "block");
//		$("#edit_hall_rent_holiday_error").text("Please enter hall rent on holiday");
		return false;
	}
}

function check_deposit_factor_on_holiday(edit_deposit_holiday_factor) {
	var namePattern = /^\d+(\.\d{1,2})?$/
	deposit_factor = $(edit_deposit_holiday_factor).val()
	if (namePattern.test(deposit_factor)) {
	    $("#edit_deposit_holiday_factor_error").closest("div").removeClass('has-error').addClass('has-success')
//		$("#edit_hall_rent_holiday_error").css("display", "none");
		return true;
	} else {
	    $("#edit_deposit_holiday_factor_error").closest("div").removeClass('has-success').addClass('has-error')
//		$("#edit_hall_rent_holiday_error").css("display", "block");
//		$("#edit_hall_rent_holiday_error").text("Please enter hall rent on holiday");
		return false;
	}
}

function check_hall_address(address){
  if($(address).val()!='' && $(address).val()!=null)
   {
   $("#edit_address").closest("div").removeClass('has-error').addClass('has-success')
//	$("#hall_location_error").css("display", "none");
    return true;
   }else{
    $("#edit_address").closest("div").removeClass('has-success').addClass('has-error')
//    $("#hall_location_error").css("display", "block");
//    $("#hall_location_error").text("Please enter hall location");
   return false;
   }
}


function isNumberKey(evt, element){
  check_value=$(element).val()
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode > 47 && charCode < 58)){
  $(element).closest('div').removeClass('has-error').addClass('has-success')
  return true;
  }
  return false;
}


function isnotNumberKey(evt, element) {
	check_value = $(element).val()
	var charCode = (evt.which) ? evt.which : evt.keyCode;
	if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) || charCode == 46)
		return true;
	return false;
}


function isKeypress(evt, element){
$(element).closest('div').removeClass('has-error').addClass('has-success')
}

function selectcontactperson(element){
    $(element).closest('div').removeClass('has-error').addClass('has-success')
}

function locisnotNumberKey(evt, element){
  check_value=$(element).val()
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) ||  charCode == 46 ){
    $(element).closest('div').removeClass('has-error').addClass('has-success')
    return true;
  }
  return false;
}

function validateFloatKeyPresss(evt,obj) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    var value = obj.value;
    var dotcontains = value.indexOf(".") != -1;
    if (dotcontains)
        if (charCode == 46) return false;
    if (charCode == 46) return true;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    $(obj).closest('div').removeClass('has-error').addClass('has-success')
    return true;
}