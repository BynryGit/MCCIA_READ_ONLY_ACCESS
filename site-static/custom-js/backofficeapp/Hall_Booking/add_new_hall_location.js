$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

$(document).ready(function(){
    $("#timepicker2").timepicker({
        defaultTime: false,
        disableFocus: false,
        disableMousewheel: false,
        isOpen: false,
        minuteStep: 15,
        modalBackdrop: false,
        orientation: { x: 'auto', y: 'auto'},
        secondStep: 15,
        showSeconds: false,
        showInputs: true,
        showMeridian: true,
        template: 'dropdown',
        appendWidgetTo: 'body',
        showWidgetOnAddonClick: true
    });
});


$("#submit_new_hall_location").click(function(event) {

        event.preventDefault();

        if(validateData()){
        $.ajax({
            type: "POST",
            url: '/backofficeapp/save-new-hall-location/',
            data: $("#add_new_hall_location_form").serialize(),
            success: function(response) {
                if (response.success == 'true') {
                    $("#success_modal").modal('show');
                }
                if (response.success == 'alreadyExist') {
                    $("#alreadyExist").modal('show');
                }
                if (response.success == "false") {
                    $("#error-modal").modal('show');
                }s
            },
            beforeSend: function() {
//                $("#processing").css('display', 'block');
            },
            complete: function() {
//                $("#processing").css('display', 'none');
            },
            error: function(response) {
                alert("_Error");
            }
        });

        }
});

function validateData(){
	if(checkhall_location("#hall_location") & check_terms_condition("#terms_condition") & check_contact_person1("#contact_person1") &
    check_deposit("#deposit")& check_hall_rent_on_holiday("#hall_rent_holiday") & check_hall_address("#address"))
	{
		return true;
	}
	return false;
}

function checkhall_location(hall_location){
  if($(hall_location).val()!='' && $(hall_location).val()!=null)
   {
   $("#hall_location_error").closest("div").removeClass('has-error').addClass('has-success')
//	$("#hall_location_error").css("display", "none");
    return true;
   }else{
    $("#hall_location_error").closest("div").removeClass('has-success').addClass('has-error')
//    $("#hall_location_error").css("display", "block");
//    $("#hall_location_error").text("Please enter hall location");
   return false;
   }
}

function check_hall_address(address){
  if($(address).val()!='' && $(address).val()!=null)
   {
   $("#address").closest("div").removeClass('has-error').addClass('has-success')
//	$("#hall_location_error").css("display", "none");
    return true;
   }else{
    $("#address").closest("div").removeClass('has-success').addClass('has-error')
//    $("#hall_location_error").css("display", "block");
//    $("#hall_location_error").text("Please enter hall location");
   return false;
   }
}


function check_terms_condition(terms_condition){
  if($(terms_condition).val()!='' && $(terms_condition).val()!=null)
   {
   $("#terms_condition_error").closest("div").removeClass('has-error').addClass('has-success')
//	$("#terms_condition_error").css("display", "none");
    return true;
   }else{
   $("#terms_condition_error").closest("div").removeClass('has-success').addClass('has-error')
//    $("#terms_condition_error").css("display", "block");
//    $("#terms_condition_error").text("Please enter terms and condition");
   return false;
   }
}

function check_contact_person1(contact_person1){
  if($(contact_person1).val()!='' && $(contact_person1).val()!=null)
   {
    $("#contact_person1_error").closest("div").removeClass('has-error').addClass('has-success')
//	$("#contact_person1_error").css("display", "none");
    return true;
   }else{
   $("#contact_person1_error").closest("div").removeClass('has-success').addClass('has-error')
//    $("#contact_person1_error").css("display", "block");
//    $("#contact_person1_error").text("Please select Contact person 1");
   return false;
   }
}





function check_deposit(deposit) {
    var namePattern = /^\d+(\.\d{1,2})?$/
    deposit = $(deposit).val()
    if (namePattern.test(deposit)) {
        $("#deposit_error").closest("div").removeClass('has-error').addClass('has-success')
//        $(deposit_error).css("display", "none");
        return true;
    } else {
        $("#deposit_error").closest("div").removeClass('has-success').addClass('has-error')
//        $(deposit_error).css("display", "block");
//        $(deposit_error).text("Please enter deposit amount");
        return false;
    }
}


function check_hall_rent_on_holiday(hall_rent_holiday) {
    var namePattern = /^\d+(\.\d{1,2})?$/
    hall_rent_holiday = $(hall_rent_holiday).val()
    if (namePattern.test(hall_rent_holiday)) {
        $("#hall_rent_holiday_error").closest("div").removeClass('has-error').addClass('has-success')
//        $(hall_rent_holiday_error).css("display", "none");
        return true;
    } else {
        $("#hall_rent_holiday_error").closest("div").removeClass('has-success').addClass('has-error')
//        $(hall_rent_holiday_error).css("display", "block");
//        $(hall_rent_holiday_error).text("Please enter hall rent on holiday");
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

function isnotNumberKey(evt, element){
  check_value=$(element).val()
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) ||  charCode == 46 )
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
    alert(value);
    var dotcontains = value.indexOf(".") != -1;
    if (dotcontains)
        if (charCode == 46) return false;
    if (charCode == 46) return true;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    $(obj).closest('div').removeClass('has-error').addClass('has-success')
    return true;
}

