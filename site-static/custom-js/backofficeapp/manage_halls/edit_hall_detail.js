$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");


$(document).ready(function (){
$('.' + 'viewcheckbox').prop("checked", false);
$('.' + 'viewcheckbox').closest('span').removeClass('checked');

hall_detail_id= $("#hall_detail_id").val()

$.ajax({
        type: "GET",
        url: '/backofficeapp/hall-equipment-list/?hall_detail_id='+hall_detail_id,
       success: function(response) {

            console.log('response', response.selectHallEquipment);
               $.each(response.selectHallEquipment, function(index, value) {
                    $('.view' + value).prop("checked", true);
                    $('.view' + value).closest('span').addClass('checked');
                });

                $.each(response.selectHall, function(index, value) {
                    $('#checkbox1_' + value).prop("checked", true);
                    $('#checkbox1_' + value).closest('span').addClass('checked');
                });

        },
        });



});


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
	                  '<input type="text" class="form-control" id="facility_mcharge_'+ id +'" value="0" '+
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

//$(".rootView").change(function() {
//    var className = $(this).attr('class').split(' ');
//    if (this.checked) {
//        $('.' + className[1]).prop("checked", true);
//        $('.' + className[1]).closest('span').addClass('checked');
//    } else {
//        $('.' + className[1]).prop("checked", false);
//        $('.' + className[1]).closest('span').removeClass('checked');
//    }
//});
////////////////////////////////////// Edit hall Details//////////////////


function validateDataEdit(){
//return true

	if(checkEditHallLocation("#edit_hallLocation") & checkEditHallName("#edit_hallName") & checkEditSeatingStyle("#edit_seatingStyle") & checkEditHallCapacity("#edit_hallCapacity") & checkEditChargesfor8hrNM("#edit_chargesfor8hrNM") & checkEditChargesfor4hrNM("#edit_chargesfor4hrNM") & checkEditChargesfor2hrNM("#edit_chargesfor2hrNM") & checkEditChargesfor8hrM("#edit_chargesfor8hrM") & checkEditChargesfor4hrM("#edit_chargesfor4hrM") & checkEditChargesfor2hrM("#edit_chargesfor2hrM") & checkEditChargesforExtrahrNM("#edit_chargesforExtrahrNM") & checkEditChargesforExtrahrM("#edit_chargesforExtrahrM")  & check_lat() & check_long() & check_addres())
	{
		return true;
	}
	return false;
}

$("#edit-continue").click(function(event)  {
    event.preventDefault();
	if(validateDataEdit()){
        var formData= new FormData();
        var chkId = '';
        var myList = new Array();
        var hallList = [];

        $("input[name='edit_hallFacilityEquipement']:checked").each ( function() {
            chkId = $(this).val()
            myList.push(chkId)
            
            formData.append("facility_nmcharge_"+chkId,$('#facility_nmcharge_'+chkId).val());
            formData.append("facility_mcharge_"+chkId,$('#facility_mcharge_'+chkId).val());
        });

        $("input[name='select_hall_id']:checked").each ( function() {
            chkId = $(this).val()
            hallList.push(chkId)
        });
        var input = document.getElementById("edit_HallImage");
        hall_file = input.files[0]
        formData.append("hall_detail_id",$('#hall_detail_id').val());
        formData.append("hallLocation",$('#edit_hallLocation').val());
        formData.append("hallName",$('#edit_hallName').val());
        formData.append("hallFacility",myList);
        formData.append("hallList",hallList);
        formData.append("seatingStyle",$('#edit_seatingStyle').val());
        formData.append("hallCapacity",$('#edit_hallCapacity').val());
        formData.append("chargesfor8hrNM",$('#edit_chargesfor8hrNM').val());
        formData.append("chargesfor8hrM",$('#edit_chargesfor8hrM').val());
        formData.append("chargesfor4hrNM",$('#edit_chargesfor4hrNM').val());
        formData.append("chargesfor4hrM",$('#edit_chargesfor4hrM').val());
        formData.append("chargesfor2hrNM",$('#edit_chargesfor2hrNM').val());
        formData.append("chargesfor2hrM",$('#edit_chargesfor2hrM').val());
        formData.append("chargesforExtrahrNM",$('#edit_chargesforExtrahrNM').val());
        formData.append("chargesforExtrahrM",$('#edit_chargesforExtrahrM').val());
        formData.append("hallImage",hall_file);
        formData.append("openForOnline",document.getElementById('edit_OpenForOnline').checked);
        formData.append("lattitude_value",$('#lattitude_value').val());
        formData.append("longitude_value",$('#longitude_value').val());
        formData.append("address",$('#address').val());
        formData.append("image_flag",$('#image_flag').val());
        formData.append("booking_start_time",$('#booking_start_time').val());
        formData.append("booking_end_time",$('#booking_end_time').val());
        $.ajax({
            type	: "POST",
            url : '/backofficeapp/edit-hall-details/',
            data : formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {

            if(response.success=='true'){
                $("#success_modal").modal('show');
            }
            else if (response.success == "false") {
                $("#error_msg").text("Sorry Something went wrong")
                $("#error-modal").modal('show');
            }
            else if (response.success == "Exist") {
                $("#error_msg").text("Hall Already Exists")
                $("#error-modal").modal('show');
            }else{
                $("#error_msg").text("Sorry Something went wrong")
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

function checkEditHallLocation(HallLocation){
  if($(HallLocation).val()!='Select')
   {
   $("#edithallLocation_error").closest("div").removeClass('has-error').addClass('has-success')
//	$("#edithallLocation_error").css("display", "none");
//	console.log("loc")
   return true;
   }else{
   $("#edithallLocation_error").closest("div").removeClass('has-success').addClass('has-error')
//    $("#edithallLocation_error").css("display", "block");
//    $("#edithallLocation_error").text("Please select Hall Location");
   return false;
   }
}


function checkEditHallName(hallName){
  if($(hallName).val()!='' && $(hallName).val()!=null)
   {
   $("#edithallName_error").closest("div").removeClass('has-error').addClass('has-success')
//   $("#edithallName_error").css("display", "none");
   console.log("hallName")
   return true;
   }else{
    $("#edithallName_error").closest("div").removeClass('has-success').addClass('has-error')
//   	$("#edithallName_error").css("display", "block");
//    $('#edithallName_error').text("Please Enter Hall Name");
   return false;
   }
}


//function checkEditHallFacility(){
//
//         var anyBoxesChecked = false;
//
//    var anyBoxesChecked = false;
//    $("input[name='select_hallFacilityEquipement']:checked").each ( function() {
//               anyBoxesChecked = true;
//          });
//
//    if (anyBoxesChecked == false) {
//        $("#edithallFacility_error").css("display", "block");
//        $('#edithallFacility_error').text("Please Select Atleast One Option");
//      return false;
//    }else{
//    console.log("checkEditHallFacility");
//    return true
//    }
//
//}



function checkEditSeatingStyle(SeatingStyle){
console.log($(SeatingStyle).val()!='Select' && $(SeatingStyle).val()!=null);
  if($(SeatingStyle).val()!='Select' && $(SeatingStyle).val()!=null)
   {
   $("#seatingStyle").removeClass('has-error').addClass('has-success')
//   $("#editseatingStyle_error").css("display", "none");
//   console.log("checkEditHallFacility");
   return true;

   }else{
        $("#seatingStyle").removeClass('has-success').addClass('has-error')
//   alert("seating error");
//   	$("#editseatingStyle_error").css("display", "block");
//    $('#editseatingStyle_error').text("Please Select Seating Style");
   return false;
   }
}

function checkEditHallCapacity(HallCapacity){
    HallCapacity = $(HallCapacity).val()
  	var namePattern = /^\d{1,5}$/;
  if(HallCapacity!='' & namePattern.test(HallCapacity)){
  $("#edithallCapacity_error").closest("div").removeClass('has-error').addClass('has-success')
// 	$('#edithallCapacity_error').css("display", "none");
   return true;
   }else{
    $("#edithallCapacity_error").closest("div").removeClass('has-success').addClass('has-error')
//    $('#edithallCapacity_error').css("display", "block");
//    $('#edithallCapacity_error').text("Please enter Hall Capacity");
   return false;
   }
}

function checkEditChargesfor8hrNM(Chargesfor8hrNM){
	Chargesfor8hrNM = $(Chargesfor8hrNM).val()
  	var namePattern = /^\d{1,5}$/;

   if(Chargesfor8hrNM!='' & namePattern.test(Chargesfor8hrNM)){
   $("#chargesfor8hrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor8hrNM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesfor8hrNM_error').css("display", "none");
   return true;
   }else{
    $("#chargesfor8hrNM_error").closest("div").closest("div").removeClass('has-success').addClass('has-error')
    $("#chargesfor8hrNM").removeClass('has-success').addClass('has-error')
//    $('#editchargesfor8hrNM_error').css("display", "block");
//    $('#editchargesfor8hrNM_error').text("Please enter charges");
   return false;
   }
}

function checkEditChargesfor8hrM(Chargesfor8hrM){
	Chargesfor8hrM = $(Chargesfor8hrM).val()
  	var namePattern = /^\d{1,5}$/;

   if(Chargesfor8hrM!='' & namePattern.test(Chargesfor8hrM)){
    $("#chargesfor8hrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor8hrM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesfor8hrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor8hrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor8hrM").removeClass('has-success').addClass('has-error')

//    $('#editchargesfor8hrM_error').css("display", "block");
//    $('#editchargesfor8hrM_error').text("Please enter charges");
   return false;
   }
}

function checkEditChargesfor4hrNM(Chargesfor4hrNM){
	Chargesfor4hrNM = $(Chargesfor4hrNM).val()
  	var namePattern = /^\d{1,5}$/;
   if(Chargesfor4hrNM!='' & namePattern.test(Chargesfor4hrNM)){
    $("#chargesfor4hrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor4hrNM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesfor4hrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor4hrNM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor4hrNM").removeClass('has-success').addClass('has-error')
//    $('#editchargesfor4hrNM_error').css("display", "block");
//    $('#editchargesfor4hrNM_error').text("Please enter charges");
   return false;
   }
}

function checkEditChargesfor4hrM(Chargesfor4hrM){
	Chargesfor4hrM = $(Chargesfor4hrM).val()
  	var namePattern = /^\d{1,5}$/;

   if(Chargesfor4hrM!='' & namePattern.test(Chargesfor4hrM)){
   $("#chargesfor4hrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor4hrM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesfor4hrM_error').css("display", "none");
   return true;
   }else{
    $("#chargesfor4hrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor4hrM").removeClass('has-success').addClass('has-error')
//    $('#editchargesfor4hrM_error').css("display", "block");
//    $('#editchargesfor4hrM_error').text("Please enter charges");
   return false;
   }
}

function checkEditChargesfor2hrNM(Chargesfor2hrNM){
	Chargesfor2hrNM = $(Chargesfor2hrNM).val()
  	var namePattern = /^\d{1,5}$/;
   if(Chargesfor2hrNM!='' & namePattern.test(Chargesfor2hrNM)){
   $("#chargesfor2hrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor2hrNM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesfor2hrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor2hrNM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor2hrNM").removeClass('has-success').addClass('has-error')
//    $('#editchargesfor2hrNM_error').css("display", "block");
//    $('#editchargesfor2hrNM_error').text("Please enter charges");
   return false;
   }
}

function checkEditChargesfor2hrM(Chargesfor2hrM){
	Chargesfor2hrM = $(Chargesfor2hrM).val()
  	var namePattern = /^\d{1,5}$/;

   if(Chargesfor2hrM!='' & namePattern.test(Chargesfor2hrM)){
   $("#chargesfor2hrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesfor2hrM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesfor2hrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesfor2hrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesfor2hrM").removeClass('has-success').addClass('has-error')
//    $('#editchargesfor2hrM_error').css("display", "block");
//    $('#editchargesfor2hrM_error').text("Please enter charges");
   return false;
   }
}




function checkEditChargesforExtrahrNM(ChargesforExtrahrNM){
	ChargesforExtrahrNM = $(ChargesforExtrahrNM).val()
  	var namePattern = /^\d{1,5}$/;

   if(ChargesforExtrahrNM!='' & namePattern.test(ChargesforExtrahrNM)){
   $("#chargesforExtrahrNM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesforExtrahrNM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesforExtrahrNM_error').css("display", "none");
   return true;
   }else{
   $("#chargesforExtrahrNM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesforExtrahrNM").removeClass('has-success').addClass('has-error')
//    $('#editchargesforExtrahrNM_error').css("display", "block");
//    $('#editchargesforExtrahrNM_error').text("Please enter charges");
   return false;
   }
}

function checkEditChargesforExtrahrM(ChargesforExtrahrM){
	ChargesforExtrahrM = $(ChargesforExtrahrM).val()
  	var namePattern = /^\d{1,5}$/;

   if(ChargesforExtrahrM!='' & namePattern.test(ChargesforExtrahrM)){
   $("#chargesforExtrahrM_error").closest("div").removeClass('has-error').addClass('has-success')
   $("#chargesforExtrahrM").removeClass('has-error').addClass('has-success')
// 	$('#editchargesforExtrahrM_error').css("display", "none");
   return true;
   }else{
   $("#chargesforExtrahrM_error").closest("div").removeClass('has-success').addClass('has-error')
   $("#chargesforExtrahrM").removeClass('has-success').addClass('has-error')
//    $('#editchargesforExtrahrM_error').css("display", "block");
//    $('#editchargesforExtrahrM_error').text("Please enter charges");
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


function get_hall_list(){
$("#related_hall").html('')
location_id = $("#edit_hallLocation").val()
hall_detail_id= $("#hall_detail_id").val()
if (location_id != ''){
    $.ajax({
            type: "POST",
            url: "/backofficeapp/edit-manage-get-hall-list/",
            data:{'location_id':location_id,'hall_detail_id':hall_detail_id},
            success: function(response) {
                if (response.success == "true") {
                      $("#related_hall").append(response.hall_list)
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


function isKeypress(evt, element){
$(element).closest('div').removeClass('has-error').addClass('has-success')
}

function selectHallLoc(element){
    $(element).closest('div').removeClass('has-error').addClass('has-success')
}

function selectSeatingStyle(){
    $("#seatingStyle").removeClass('has-error').addClass('has-success')
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

function myFunction(obj){
if ($(obj).val() != ''){
    $("#image_flag").val("change")
}else{
    $("#image_flag").val("removed")
}

}