$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

function ConfigureFacilityRate(id) {
			if ($(id).prop("checked")) {			
				 id = $(id).val()		 
				 f_name = $("#f_name_"+id).val()	
	        	 data =  '<div class="col-md-12" id="FacilityRowDiv_'+ id +'">'+
		      	'<div class="col-md-1">'+
	               '<div class="form-group form-md-line-input has-success"'+
	                  'id="">'+
	                  '<label>Facility :</label>'+
	               '</div>'+
	            '</div>'+
	            '<div class="col-md-3">'+
	               '<div class="form-group form-md-line-input has-success">'+
	                  '<input type="text" class="form-control" id="f_name_'+ id +'"'+
	                     'readonly="" name="f_name_'+ id +'" value="'+ f_name +'">'+
	               '</div>'+
	            '</div>'+
	            '<div class="col-md-1">'+
	               '<div class="form-group form-md-line-input has-success"'+
	                  'id="">'+
	                  '<label>Non Member<span class="required">*</span>&nbsp&nbsp:</label>'+
	               '</div>'+
	            '</div>'+
	            '<div class="col-md-3">'+
	               '<div class="form-group form-md-line-input has-success" id="facility_nmchargeDiv_'+ id +'">'+
	                  '<input type="text" class="form-control" id="facility_nmcharge_'+ id +'" value="0" '+
	                     'name="facility_nmcharge_'+ id +'" minlength="1" maxlength="5" onkeypress="return validateFloatKeyPresss(this, event)">'+
	               '</div>'+
	            '</div>'+
	            '<div class="col-md-1">'+
	               '<div class="form-group form-md-line-input has-success"'+
	                  'id="">'+
	                  '<label>Member<span class="required">*</span>&nbsp&nbsp:</label>'+
	               '</div>'+
	            '</div>'+
	            '<div class="col-md-3">'+
	               '<div class="form-group form-md-line-input has-success"'+
	                  'id="facility_nmchargeDiv_'+ id +'" >'+
	                  '<input type="text" class="form-control" id="facility_mcharge_'+ id +'" value="0"'+
	                     'name="facility_nmcharge_'+ id +'" minlength="1" maxlength="5" onkeypress="return validateFloatKeyPresss(this, event)">'+
	               '</div>'+
	            '</div>'+
	           '</div>'
	  			$('#FacilityMainDiv').append(data)
       }		
      else {
      	id = $(id).val()	
      	$("#FacilityRowDiv_"+id ).remove()
       }	               
}


function validateData(){

	if(checkHallLocation("#select_hallLocation") & checkHallName("#select_hallName") & checkSeatingStyle("#select_seatingStyle") & checkHallCapacity("#select_hallCapacity") & checkChargesfor8hrNM("#select_chargesfor8hrNM") & checkChargesfor4hrNM("#select_chargesfor4hrNM") & checkChargesfor2hrNM("#select_chargesfor2hrNM") & checkChargesfor8hrM("#select_chargesfor8hrM") & checkChargesfor4hrM("#select_chargesfor4hrM") & checkChargesfor2hrM("#select_chargesfor2hrM") & checkChargesforExtrahrNM("#select_chargesforExtrahrNM") & checkChargesforExtrahrM("#select_chargesforExtrahrM") & check_lat() & check_long() & check_addres())
	{
		return true;
	}
	return false;
}

$("#save-continue").click(function(event)  {				
    if(validateData()){
	    var formData= new FormData();
        var chkId = '';
        var myList = new Array();
        var hallList = []

        $("input[name='select_hallFacilityEquipement']:checked").each (function() {
            chkId = $(this).val()
            myList.push(chkId)
            
            formData.append("facility_nmcharge_"+chkId,$('#facility_nmcharge_'+chkId).val());
            formData.append("facility_mcharge_"+chkId,$('#facility_mcharge_'+chkId).val());
        });
        $("input[name='select_hall_id']:checked").each (function() {
            chkId = $(this).val()
            hallList.push(chkId)
        });

        var input = document.getElementById("select_HallImage");
	    hall_file = input.files[0];

		  formData.append("hallLocation",$('#select_hallLocation').val());
        formData.append("hallName",$('#select_hallName').val());
        formData.append("hallFacility",myList);
        formData.append("hallList",hallList);
        formData.append("seatingStyle",$('#select_seatingStyle').val());
        formData.append("hallCapacity",$('#select_hallCapacity').val());
        formData.append("chargesfor8hrNM",$('#select_chargesfor8hrNM').val());
        formData.append("chargesfor8hrM",$('#select_chargesfor8hrM').val());
        formData.append("chargesfor4hrNM",$('#select_chargesfor4hrNM').val());
        formData.append("chargesfor4hrM",$('#select_chargesfor4hrM').val());
        formData.append("chargesfor2hrNM",$('#select_chargesfor2hrNM').val());
        formData.append("chargesfor2hrM",$('#select_chargesfor2hrM').val());
        formData.append("chargesforExtrahrNM",$('#select_chargesforExtrahrNM').val());
        formData.append("chargesforExtrahrM",$('#select_chargesforExtrahrM').val());
        formData.append("hallImage",hall_file);
        formData.append("openForOnline",document.getElementById('select_OpenForOnline').checked);
        formData.append("lattitude_value",$('#lattitude_value').val());
        formData.append("longitude_value",$('#longitude_value').val());
        formData.append("address",$('#address').val());
        
        formData.append("booking_start_time",$('#booking_start_time').val());
        formData.append("booking_end_time",$('#booking_end_time').val());
        $.ajax({
            type	: "POST",
            url : '/backofficeapp/save-hall-details/',
            data : formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success=='true'){
                    $("#success_modal").modal('show');
                }
                if(response.success=='alreadyExist'){
                    $("#success_modal_alreadyExist").modal('show');
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



function checkHallLocation(HallLocation){
  if($(HallLocation).val()!='Select')
   {
   $("#hallLocation_error").closest("div").removeClass('has-error').addClass('has-success')
//	$("#hallLocation_error").css("display", "none");
   return true;
   }else{
    $("#hallLocation_error").closest("div").removeClass('has-success').addClass('has-error')
//    $("#hallLocation_error").css("display", "block");
//    $("#hallLocation_error").text("Please select Hall Location");
   return false;
   }
}


function checkHallName(hallName){
  if($(hallName).val()!='' && $(hallName).val()!=null)
   {
   $("#hallName_error").closest("div").removeClass('has-error').addClass('has-success')

//   $("#hallName_error").css("display", "none");
//   console.log("hall name");
   return true;
   }else{
   $("#hallName_error").closest("div").removeClass('has-success').addClass('has-error')
//   	$("#hallName_error").css("display", "block");
//    $('#hallName_error').text("Please Enter Hall Name");
   return false;
   }
}

function checkSeatingStyle(SeatingStyle){
  if($(SeatingStyle).val()!='Select' && $(SeatingStyle).val()!=null)
   {
   $("#seatingStyle_error").closest("div").removeClass('has-error').addClass('has-success')
//   $("#seatingStyle_error").css("display", "none");
//   console.log("yseating style");
   return true;
   }else{
   $("#seatingStyle_error").closest("div").removeClass('has-success').addClass('has-error')
//   	$("#seatingStyle_error").css("display", "block");
//    $('#seatingStyle_error').text("Please Select Seating Style");
   return false;
   }
}

function checkHallCapacity(HallCapacity){
    HallCapacity = $(HallCapacity).val()
  	var namePattern =/^\d{1,5}$/;
  if(HallCapacity!='' & namePattern.test(HallCapacity)){
  $("#hallCapacity_error").closest("div").removeClass('has-error').addClass('has-success')
// 	$('#hallCapacity_error').css("display", "none");
// 	console.log("capacity");
   return true;
   }else{
   $("#hallCapacity_error").closest("div").removeClass('has-success').addClass('has-error')
//    $('#hallCapacity_error').css("display", "block");
//    $('#hallCapacity_error').text("Please enter Hall Capacity");
   return false;
   }
}

function checkChargesfor8hrNM(Chargesfor8hrNM){
	Chargesfor8hrNM = $(Chargesfor8hrNM).val()
//  	var namePattern = /^\d{1,5}$/;
  	var namePattern = /^-?\d*(\.\d+)?$/;

   if(Chargesfor8hrNM!='' & namePattern.test(Chargesfor8hrNM)){
   $("#chargesfor8hrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor8hrNM").removeClass('has-error').addClass('has-success')
// 	$('#chargesfor8hrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor8hrNM_error").closest("div").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor8hrNM").removeClass('has-success').addClass('has-error')
//    $('#chargesfor8hrNM_error').css("display", "block");
//    $('#chargesfor8hrNM_error').text("Please enter charges");
   return false;
   }
}

function checkChargesfor8hrM(Chargesfor8hrM){
	Chargesfor8hrM = $(Chargesfor8hrM).val()
//  	var namePattern = /^\d{1,5}$/;
  	var namePattern = /^-?\d*(\.\d+)?$/;

   if(Chargesfor8hrM!='' & namePattern.test(Chargesfor8hrM)){
   $("#chargesfor8hrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor8hrM").removeClass('has-error').addClass('has-success')
// 	$('#chargesfor8hrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor8hrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor8hrM").removeClass('has-success').addClass('has-error')
//    $('#chargesfor8hrM_error').css("display", "block");
//    $('#chargesfor8hrM_error').text("Please enter charges");
   return false;
   }
}

function checkChargesfor4hrNM(Chargesfor4hrNM){
	Chargesfor4hrNM = $(Chargesfor4hrNM).val()
//  	var namePattern = /^\d{1,5}$/;
    var namePattern = /^-?\d*(\.\d+)?$/;

   if(Chargesfor4hrNM!='' & namePattern.test(Chargesfor4hrNM)){
   $("#chargesfor4hrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor4hrNM").removeClass('has-error').addClass('has-success')
// 	$('#chargesfor4hrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor4hrNM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor4hrNM").removeClass('has-success').addClass('has-error')
//    $('#chargesfor4hrNM_error').css("display", "block");
//    $('#chargesfor4hrNM_error').text("Please enter charges");
   return false;
   }
}

function checkChargesfor4hrM(Chargesfor4hrM){
	Chargesfor4hrM = $(Chargesfor4hrM).val()
//  	var namePattern = /^\d{1,5}$/;
    var namePattern = /^-?\d*(\.\d+)?$/;

   if(Chargesfor4hrM!='' & namePattern.test(Chargesfor4hrM)){
   $("#chargesfor4hrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor4hrM").removeClass('has-error').addClass('has-success')
// 	$('#chargesfor4hrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor4hrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor4hrM").removeClass('has-success').addClass('has-error')
//    $('#chargesfor4hrM_error').css("display", "block");
//    $('#chargesfor4hrM_error').text("Please enter charges");
   return false;
   }
}

function checkChargesfor2hrNM(Chargesfor2hrNM){
	Chargesfor2hrNM = $(Chargesfor2hrNM).val()
//  	var namePattern = /^\d{1,5}$/;
    var namePattern = /^-?\d*(\.\d+)?$/;

   if(Chargesfor2hrNM!='' & namePattern.test(Chargesfor2hrNM)){
   $("#chargesfor2hrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor2hrNM").removeClass('has-error').addClass('has-success')
// 	$('#chargesfor2hrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor2hrNM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor2hrNM").removeClass('has-success').addClass('has-error')
//    $('#chargesfor2hrNM_error').css("display", "block");
//    $('#chargesfor2hrNM_error').text("Please enter NM charges");
   return false;
   }
}

function checkChargesfor2hrM(Chargesfor2hrM){
	Chargesfor2hrM = $(Chargesfor2hrM).val()
//  	var namePattern = /^\d{1,5}$/;
    var namePattern = /^-?\d*(\.\d+)?$/;
   if(Chargesfor2hrM!='' & namePattern.test(Chargesfor2hrM)){
   $("#chargesfor2hrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor2hrM").removeClass('has-error').addClass('has-success')
// 	$('#chargesfor2hrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor2hrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor2hrM").removeClass('has-success').addClass('has-error')
//    $('#chargesfor2hrM_error').css("display", "block");
//    $('#chargesfor2hrM_error').text("Please enter M charges");
   return false;
   }
}




function checkChargesforExtrahrNM(ChargesforExtrahrNM){
	ChargesforExtrahrNM = $(ChargesforExtrahrNM).val()
//  	var namePattern = /^\d{1,5}$/;
    var namePattern = /^-?\d*(\.\d+)?$/;
   if(ChargesforExtrahrNM!='' & namePattern.test(ChargesforExtrahrNM)){
   $("#chargesforExtrahrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesforExtrahrNM").removeClass('has-error').addClass('has-success')
// 	$('#chargesforExtrahrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesforExtrahrNM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesforExtrahrNM").removeClass('has-success').addClass('has-error')
//    $('#chargesforExtrahrNM_error').css("display", "block");
//    $('#chargesforExtrahrNM_error').text("Please enter NM charges");
   return false;
   }
}

function checkChargesforExtrahrM(ChargesforExtrahrM){
	ChargesforExtrahrM = $(ChargesforExtrahrM).val()
//  	var namePattern = /^\d{1,5}$/;
    var namePattern = /^-?\d*(\.\d+)?$/;
   if(ChargesforExtrahrM!='' & namePattern.test(ChargesforExtrahrM)){
   $("#chargesforExtrahrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesforExtrahrM").removeClass('has-error').addClass('has-success')
// 	$('#chargesforExtrahrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesforExtrahrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesforExtrahrM").removeClass('has-success').addClass('has-error')
//    $('#chargesforExtrahrM_error').css("display", "block");
//    $('#chargesforExtrahrM_error').text("Please enter M charges");
   return false;
   }
}

function check_lat(){
latitude_value = $("#lattitude_value").val()
var lat_Pattern = /^-?\d*(\.\d+)?$/;

if(latitude_value !='' & lat_Pattern.test(latitude_value)){
   $("#lattitude_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#lattitude").removeClass('has-error').addClass('has-success')
   return true;
   }else{
   $("#lattitude_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#lattitude").removeClass('has-success').addClass('has-error')
   return false;
   }
}

function check_long(){
longitude_value = $("#longitude_value").val()
var long_Pattern = /^-?\d*(\.\d+)?$/;

if(longitude_value !='' & long_Pattern.test(longitude_value)){
   $("#longitude_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#longitude").removeClass('has-error').addClass('has-success')
   return true;
   }else{
   $("#longitude_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#longitude").removeClass('has-success').addClass('has-error')
   return false;
   }
}


function check_addres(){
  if($("#address").val()!='' && $("#address").val()!=null)
   {
   $("#address").closest("div").removeClass('has-error').addClass('has-success')
//   $("#address_div").removeClass('has-error').addClass('has-success')
    return true;
   }else{
    $("#address").closest("div").removeClass('has-success').addClass('has-error')
//    $("#address_div").removeClass('has-success').addClass('has-error')
   return false;
   }

}

function get_hall_list(element){
$("#related_hall").html('')
$("#address").text('')
$(element).closest('div').removeClass('has-error').addClass('has-success')
location_id = $("#select_hallLocation").val()
if (location_id != 'Select'){
    $.ajax({
            type: "POST",
            url: "/backofficeapp/manage-get-hall-list/",
            data:{'location_id':location_id},
            success: function(response) {
                if (response.success == "true") {
                      $("#related_hall").append(response.hall_list)
                      $("#address").text(response.address)
                }

            }
        });

}
}

function validateFloatKeyPresss(obj,evt,div_id) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    var value = obj.value;
    var dotcontains = value.indexOf(".") != -1;
    if (dotcontains)
        if (charCode == 46) return false;
    if (charCode == 46) return true;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    $('#'+div_id).removeClass('has-error').addClass('has-success')
    $('#'+ div_id +'_error').closest('div').removeClass('has-error').addClass('has-success')
    return true;
}

function validateNumKeyPresss(obj,evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    var value = obj.value;
//    var dotcontains = value.indexOf(".") != -1;
//    if (dotcontains)
//        if (charCode == 46) return false;
//    if (charCode == 46) return true;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    $(obj).closest('div').removeClass('has-error').addClass('has-success')
    return true;
}


function isKeypress(evt, element){
$(element).closest('div').removeClass('has-error').addClass('has-success')
}

function selectHallLoc(element){
    $(element).closest('div').removeClass('has-error').addClass('has-success')
}

function selectSeatingStyle(){
    $("#seatingStyle").removeClass('has-error').addClass('has-success')
}



