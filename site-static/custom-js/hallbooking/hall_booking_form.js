$( document ).ready(function() {
    $("#online_payment_note_div").hide();
//    $("#offline_payment_note").show();
    $("#conform_id").show();
    $("#payment_id").hide();
});

//if($('#hall_booking_form_div').is(':visible')){

history.pushState(null, null, location.href);
window.onpopstate = function (e) {
    bootbox.confirm({
        closeButton: false,
        message: "You will lost all your booking data. Do you wish to continue ?",
        buttons: {
            confirm: {label: 'Yes', className: 'btn-success'},
            cancel: {label: 'No', className: 'btn-danger'}
        },
        callback: function (result) {
            if (result){
                location.href = '/hallbookingapp/open-hallbooking-page/';
            }
            else{
                history.go(1);
            }
        }
    });
};

//$(function() {
//    if (window.history && window.history.pushState) {
//        window.history.pushState('', null, './');
//        $(window).on('popstate', function() {
//            // alert('Back button was pressed.');
//            document.location.href = '#';
//
//        });
//    }
//});



var member_status = ''
var key_number = 1;
//var booking_id = '';
var location_id = ''
$(document).ready(function(e){
    member_status = "nm";
    check_member(member_status);       
	 $('#CompanyIndividualName').attr('autocomplete', 'off');
	 $('#company_list').attr('autocomplete', 'off');	 	    
});

function get_hall_of_location(location_id){
if (location_id != ''){
$('.nav-pills li.active').removeClass('active');
$("#locationlistID_"+ location_id).addClass('active')
$("#location_name_h2").text(($("#locationlistID_"+ location_id).text()).trim())
$("#hall_detail_list").html('')

// Add Halls to Check Availability List
$("#selectHallName").html('').append('<option>Select Hall</option>');
$('#hall_event_calendar').fullCalendar('destroy');

$.ajax({
        type: "POST",
        url: "/hallbookingapp/get-hall-detail-location/",
        data: {"location_id": location_id},
        success: function(response){
            if (response.success == 'true'){
                data = ''
                contactperson_div=''
                contact_div=''                
                $("#hall_time").html('').append('Halls are available from '+ response.hall_start_time + ' to '+ response.hall_end_time);
                tool_tip_div='<div class="tooltip fade bottom in" role="tooltip" id="tooltip144349" style="top: 30px; left: -15px; display: block;">'+
                                '<div class="tooltip-arrow" style="left: 50%;"></div>'+
                                '<div class="tooltip-inner">Video</div>'+
                                '</div>'
                tool_tip_div=''
                $.each(response.contact_data, function(i,contact_user){
                    contactperson_div = contactperson_div + '<div class="caption" style="margin-bottom:5px;">'+
                    '<p>'+
                        '<img src="/static/assets/images/icons/contact-person-icon-white.png"/> <strong>'+contact_user.name+'</strong><br/>'+
                        '<img src="/static/assets/images/icons/phone-icon-white.png"/> Phone:'+contact_user.phone+'<br/>'+
                        '<img src="/static/assets/images/icons/email-icon-white.png"/> Email: <a href="mailto:'+contact_user.email+'">'+contact_user.email+'</a>'+
                    '</p>'+
                  '</div>'
                });
                contact_div='<div class="col-lg-3 col-md-4 col-sm-12 col-xs-12">'+
                                '<div class="hallBookingContactPerson">'+
                                    '<h4>Contact Person:</h4>'+contactperson_div +
                                '</div>'+
                                '<div class="hallBookingAvailability">'+
                                    '<a type="button" onclick="check_hall_availbility_status();">Check Hall Availability <i class="fa fa-calendar-check-o" aria-hidden="true"></i></a>'+
                                '</div>'+

                                '<div class="hallBookingLinks">'+
                                    '<ul>'+
                                        '<li><a href="/hallbookingapp/terms-condition/">Terms and Conditions</a></li>'+
                                        '<li><a href="/hallbookingapp/terms-condition/">Cancellation Policy</a></li>'+
                                    '</ul>'+
                                '</div>'+
                            '</div>'

                $.each(response.hall_data, function(index, item){
                    var li_equip_var1=''
                    if (item.paid_facility_list !='') {
                    	  li_equip_var1 = li_equip_var1 + '<div class="row">' +
                    	  												'<div class="col-lg-12">'+
                    	  												 '<span>Facilities on Additional Payment</span>'+
                    	  												   '<ul class="facilities">' 
	                    $.each(item.paid_facility_list, function(i, euipment){
	                                    if (euipment == 'Video Conferencing'){
	                                        li_equip_var1 = li_equip_var1 + '<li>'+  
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f" src="/static/assets/images/icons/video-icon.png" alt="" title="" data-toggle="tooltip" data-placement="bottom" data-original-title="Video Conferencing">'+
	                                        '</li>' + tool_tip_div
	                                    }else if (euipment == 'Audio Conferencing'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f" class="pqrq" src="/static/assets/images/icons/audio-icon.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="Audio Conferencing">'+
	                                        '</li>'+ tool_tip_div
	                                    }else if (euipment == 'Podium'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f" class="pqrq" src="/static/assets/images/icons/podium.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="Podium">'+
	                                        '</li>'+ tool_tip_div
	                                    }else if (euipment == 'Wi-Fi'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/wifi-icon.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="Wi-Fi">'+
	                                        '</li>'+ tool_tip_div
	                                    }else if (euipment == 'Projector'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/projector.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="Projector">'+
	                                        '</li>'+ tool_tip_div
	                                    }else if (euipment == 'PA System'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/pa_system.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="PA System">'+
	                                        '</li>'+ tool_tip_div
	                                    }
	                                    else if (euipment == 'Dias'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/dias.jpeg" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="Dias">'+
	                                        '</li>'+ tool_tip_div
	                                    }
	                                    else if (euipment == 'Air Conditioner'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/air.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="Air Conditioner">'+
	                                        '</li>'+ tool_tip_div
	                                    }
	                                    else if (euipment == 'White Board with Marker'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/whiteboard.jpg" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="White Board with Marker">'+
	                                        '</li>'+ tool_tip_div
	                                    }
	                                    else if (euipment == 'LAN'){
	                                        li_equip_var1 = li_equip_var1 +'<li>'+
	                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/plug_lan.png" alt="" title=""'+
	                                             'data-toggle="tooltip" data-placement="bottom"'+
	                                             'data-original-title="LAN">'+
	                                        '</li>'+ tool_tip_div
	                                    }
	 
	                    });
	                    li_equip_var1 = li_equip_var1 + '</ul>'+
                                           '</div>'+
                                         '</div>'	                    
	                 }
                    
                    var li_equip_var2=''
                    if (item.free_facility_list !='') {
                    	  li_equip_var2 = li_equip_var2 + '<div class="row">' +
                    	  												'<div class="col-lg-12">'+
                    	  												 '<span>Included in Hall Rental</span>'+
                    	  												   '<ul class="facilities">' 
                    $.each(item.free_facility_list, function(i, euipment){
                                    if (euipment == 'Video Conferencing'){
                                        li_equip_var2 = li_equip_var2 + '<li>'+  
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f" src="/static/assets/images/icons/video-icon.png" alt="" title="" data-toggle="tooltip" data-placement="bottom" data-original-title="Video Conferencing">'+
                                        '</li>' + tool_tip_div
                                    }else if (euipment == 'Audio Conferencing'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f" class="pqrq" src="/static/assets/images/icons/audio-icon.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="Audio Conferencing">'+
                                        '</li>'+ tool_tip_div
                                    }else if (euipment == 'Podium'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f" class="pqrq" src="/static/assets/images/icons/podium.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="Podium">'+
                                        '</li>'+ tool_tip_div
                                    }else if (euipment == 'Wi-Fi'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/wifi-icon.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="Wi-Fi">'+
                                        '</li>'+ tool_tip_div
                                    }else if (euipment == 'Projector'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/projector.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="Projector">'+
                                        '</li>'+ tool_tip_div
                                    }else if (euipment == 'PA System'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/pa_system.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="PA System">'+
                                        '</li>'+ tool_tip_div
                                    }
                                    else if (euipment == 'Dias'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/dias.jpeg" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="Dias">'+
                                        '</li>'+ tool_tip_div
                                    }
                                    else if (euipment == 'Air Conditioner'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/air.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="Air Conditioner">'+
                                        '</li>'+ tool_tip_div
                                    }
                                    else if (euipment == 'White Board with Marker'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/whiteboard.jpg" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="White Board with Marker">'+
                                        '</li>'+ tool_tip_div
                                    }
                                    else if (euipment == 'LAN'){
                                        li_equip_var2 = li_equip_var2 +'<li>'+
                                            '<img style="margin-top: 5px;width: 26px;border-radius: 50%;border: 2px solid #8d8e8f"  src="/static/assets/images/icons/plug_lan.png" alt="" title=""'+
                                             'data-toggle="tooltip" data-placement="bottom"'+
                                             'data-original-title="LAN">'+
                                        '</li>'+ tool_tip_div
                                    }
 
                    });
                     li_equip_var2 = li_equip_var2 + '</ul>'+
                                           '</div>'+
                                         '</div>'	
                 }

                    var li_charge_var=''
                    $.each(item.hall_charges, function(i, charge){
                        li_charge_var = li_charge_var + '<li>'+
                            '<div class="hallDetails">'+
                                '<h4>'+i+' HRS.</h4>'+
                                '<p>'+
                                    '<span>M:'+charge[0]+'</span>'+
                                    '<span>NM:'+charge[1]+'</span>'+
                                '</p>'+
                            '</div>'+
                        '</li>'
                    });
                    var a = ''
                    if (response.user_type == 'backoffice'){
                        var a = '<a type="submit" class="btn btn-default subbtn" onclick="show_hall_booking_form('+ item.id + ",'" + item.hall_name+"'"+')">Book Now</a>'
                    }
                    else{
                    	if (response.book_now_flag == 1) {
                        	var a = '<a style="display: block;" type="submit" class="btn btn-default subbtn" onclick="show_hall_booking_form('+ item.id + ",'" + item.hall_name+"'"+')">Book Now</a>'
                        }
                        else {
                        	var a = '<a style="display: none;" type="submit" class="btn btn-default subbtn" onclick="show_hall_booking_form('+ item.id + ",'" + item.hall_name+"'"+')">Book Now</a>'
                        }
                    }          

                    var start_time_id = "start_time_"+item.id;                    
                    var end_time_id = "end_time_"+item.id;                    

                    data = data + '<div class="hallBookingListing">'+
                        '<div class="row">'+
                            '<div class="col-md-12 col-sm-12 col-xs-12">'+
                                '<h4> <span>'+item.hall_name+'</span>'+
                                    '<div class="Formbuttons">'+
                                    a+                                                                                
                                        '<input type="text" id="' + start_time_id + '" value="' + item.start_time + '" hidden>'+
                                        '<input type="text" id="' + end_time_id + '" value="' + item.end_time + '" hidden>'+
                                    '</div>'+
                                '</h4>'+
                            '</div>'+
                            '<div class="col-md-12 col-sm-12 col-xs-12">'+
                                '<div class="media">'+
                                    '<div class="media-left">'+
                                        '<img class="media-object" src='+ item.hall_imag +' alt="hall-bookings-img">'+
                                    '</div>'+
                                    '<div class="media-body">'+
                                        '<div class="row">'+
                                            '<div class="col-lg-3 col-md-6 col-sm-3 col-xs-3 hallDetailsPoints">'+
                                                '<h5>'+ item.capacity +'<span>Seating</span></h5>'+
                                            '</div>'+
                                            '<div class="col-lg-3 col-md-6 col-sm-3 col-xs-3 hallDetailsPoints">'+
                                                '<h5>'+ item.seating_style +'<span>Seating Style</span></h5>'+
                                            '</div>'+
                                            '<div class="col-lg-6 col-md-12 col-sm-6 col-xs-6 hallDetailsFacilitiesPoints">'+                                            
                                                li_equip_var1 +
                                                li_equip_var2 +                                                
                                            '</div>'+
                                        '</div>'+
                                        '<div class="row">'+
                                            '<div class="col-md-12">'+
                                                '<ul class="hallDetailsList">'+li_charge_var+'</ul>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'

                    // Add Halls to Check Availability List
                    $("#selectHallName").append('<option value="' + item.id + '">' + item.hall_name + '</option>');
                });

                final_div = '<div class="col-lg-9 col-md-8 col-sm-12 col-xs-12">'+
                data + '</div>'+ contact_div

                $("#hall_detail_list").append(final_div)
                $('[data-toggle="tooltip"]').tooltip();
            }

        }
    });

}
}
// On Login Modal Hide - Change to Non-Member Form
$('#memberLoginModal').on('hidden.bs.modal', function () {
    $("#radiobtn1").prop("checked", true);
    member_status = "nm";
    check_member(member_status);
})


//function check_member(check_value){
//    if (check_value == 'nm'){
//        member_status = "nm";
//        if ($("#check_user").val() == "False"){
//            $("#nonmember_note").show();
//            $("#nonmember_list").show();
//            $("#address").val('');
//            $("#member_note").hide();
//            $("#membership_row").hide();
//            $("#member_note2").hide();
//            $("#member_list").css("display", "none");
//            $("#CompanyIndividualName").addClass('validateRequired');
//        }
//        else{
//            $("#nonmember_note").show();
//            $("#nonmember_list").show();
//
//            $("#address").val('');
//            $("#company_list").prop("selectedIndex", 0);
//            $("#member_note").hide();
//            $("#membership_row").hide();
//            $("#member_note2").hide();
//            $("#member_list").css("display", "none");
//            $("#CompanyIndividualName").addClass('validateRequired');
//        }
//    }
//    else if (check_value == 'm'){
//        member_status = "m";
//        if ($("#check_user").val() == "False"){
//            get_membership_no($("#company_list").val());
//            $("#nonmember_note").hide();
//            $("#nonmember_list").hide();
//
//            $("#address").val('');
//            $("#member_note").show();
//            $("#membership_row").show();
//            $("#member_note2").show();
//            $("#member_list").css("display", "block");
//            $("#CompanyIndividualName").removeClass('validateRequired');
//        }
//        else{
//            $("#memberLoginModal").modal('show');
//        }
//
//    }
//    else{
//        member_status = "nm";
//        $("#nonmember_note").show();
//        $("#nonmember_list").show();
//
//        $("#address").val('');
//        $("#company_list").prop("selectedIndex", 0);
//        $("#member_note").hide();
//        $("#membership_row").hide();
//        $("#member_note2").hide();
//        $("#member_list").css("display", "none");
//        $("#CompanyIndividualName").addClass('validateRequired');
//    }
//}


function check_member(check_value){
    if ($("#user_type").val() == 'backoffice'){
        member_status = "nm";
        $("#user_detail_id").removeClass('validateRequired');
        $("#membership_no").removeClass('validateRequired');
        $("#address").removeClass('validateRequired');
        $("#ContactPerson").removeClass('validateRequired');
        $("#Designation").removeClass('validateRequired');
        $("#Tel").removeClass('validateRequired');
        $("#CompanyIndividualName").removeClass('validateRequired');
        $("#Mobile").removeClass('validateRequired');
        $("#email").removeClass('validateRequired');
        $("#nonmember_div").removeClass('validateRequired');
        $("#member_note").hide();
        $("#membership_row").hide();
        $("#member_note2").hide();
        $("#member_list").css("display", "none");
        $("#company_list").removeClass("validateRequired");
    }
    else  {
         $("#company_list").val('').change();
         $("#CompanyIndividualName").val('').change();
        if (check_value == 'nm'){
            member_status = "nm";
            getNonmemberData();
            $("#nonmember_note").show();
            $("#nonmember_list").show();
            $("#address").val('');
            $("#member_note").hide();
            $("#membership_row").hide();
            $("#member_note2").hide();
            $("#member_list").css("display", "none");
            $("#company_list").prop("selectedIndex", 0);
            $("#company_list").removeClass("validateRequired");
            $("#company_list").parent().removeClass("has-error");
            $("#CompanyIndividualName").addClass('validateRequired');

        }
        else if (check_value == 'm'){
            member_status = "m";
            get_membership_no();
            $("#nonmember_note").hide();
            $("#nonmember_list").hide();
            $("#address").val('');
            $("#member_note").show();
            $("#membership_row").show();
            $("#member_note2").show();
            $("#member_list").css("display", "block");
            $("#company_list").addClass("validateRequired");
            $("#CompanyIndividualName").removeClass('validateRequired');
            $("#CompanyIndividualName").parent().removeClass("has-error");
        }
        else {
            member_status = "nm";
            $("#nonmember_note").show();
            $("#nonmember_list").show();
            $("#address").val('');
            $("#company_list").prop("selectedIndex", 0);
            $("#member_note").hide();
            $("#membership_row").hide();
            $("#member_note2").hide();
            $("#member_list").css("display", "none");
            $("#company_list").removeClass("validateRequired");
            $("#company_list").parent().removeClass("has-error");
            $("#CompanyIndividualName").addClass('validateRequired');
        }
        }
}


function getNonmemberData() {
	 $("#user_track_id").val('');
    $("#address").val('');
    $("#ContactPerson").val('');
    $("#Designation").val('');
    $("#Tel").val('');
    $("#Mobile").val('');
    $("#GSTIN").val('');
    $("#email").val('');
    $("#NatureoftheEvent").val('');
    if ($("#CompanyIndividualName").val()) {
    $.ajax({
        type: "GET",
        url: "/hallbookingapp/get-non-member-detail/",
        data: {"non_mem_id": $("#CompanyIndividualName").val()},
        success: function(response){
            if (response.success == 'true'){
                $("#user_track_id").val(response.user_track_id);
                $("#address").val(response.address);
				    $("#ContactPerson").val(response.contact_person);
				    $("#Designation").val(response.designation);
				    $("#Tel").val(response.mobile_no);
				    $("#Mobile").val(response.mobile_no);
				    if (response.gst != 'None'){
				        $("#GSTIN").val(response.gst);
				    }
				    $("#email").val(response.email);
            }
        }
    });
  }
}


// Reset Button Code
$("#reset_btn").click(function(){
    $("#CompanyIndividualName").val('').change();
    $("#company_list").val('').change();
    $("#address").val('');
    $("#ContactPerson").val('');
    $("#Designation").val('');
    $("#Tel").val('');
    $("#Mobile").val('');
    $("#TelR").val('');
    $("#email").val('');
    $("#NatureoftheEvent").val('');
    $("#FromDate").val('');
    $("#ToDate").val('');
    $("#time_table_body").html('');
    $("#time_slot_row").hide();
    $("#company_list").prop("selectedIndex", 0);
    $("#membership_no").text('');

});


// Get Membership Number & address on Company Change
function get_membership_no(){
	 mem_id = $("#company_list").val()
	 $("#user_track_id").val('');
    $("#address").val('');
    $("#ContactPerson").val('');
    $("#Designation").val('');
    $("#Tel").val('');
    $("#Mobile").val('');
    $("#GSTIN").val('');
    $("#email").val('');
    $("#NatureoftheEvent").val('');
    $("#membership_no").text('');
	 if (mem_id) {
	    $.ajax({
	        type: "GET",
	        url: "/hallbookingapp/get-member-detail/",
	        data: {"mem_id": mem_id},
	        success: function(response){
	            if (response.success == 'true'){
	                $("#user_track_id").val(response.user_track_id);
	                $("#address").val(response.address);
	                $("#membership_no").text(response.membership_no);
					    $("#ContactPerson").val(response.contact_person);
					    $("#Designation").val(response.designation);
					    $("#Tel").val(response.mobile_no);
					    $("#Mobile").val(response.mobile_no);
					    $("#GSTIN").val(response.gst);
					    $("#email").val(response.email);
	            }
	        }
	    });
   }
//    $("#membership_no").text('I9887');
}



// Animate To Error Field in Hall Booking Form
$("#submit_btn, #re_enter_btn").click(function(){

	if (member_status == "nm"){
		//$("#company_list").removeClass('validateRequired');
		//$("#member_div").removeClass().addClass("validateField has-success");
		if ($("#CompanyIndividualName").val() != ''){
			$("#CompanyIndividualName").removeClass('validateRequired');
			$("#nonmember_div").removeClass().addClass("validateField has-success");
	    }
	    else {
	        if ($("#user_type").val() == 'backoffice'){
	            $("#CompanyIndividualName").removeClass('validateRequired');
                $("#nonmember_div").removeClass("validateField has-error");
	        }
	        else{
                $("#CompanyIndividualName").removeClass('validateRequired').addClass('validateRequired');
                $("#nonmember_div").removeClass().addClass("validateField has-error");
	        }
	    }
	}
	else{
		if ($("#company_list").val() != ''){
			$("#company_list").removeClass('validateRequired');
			$("#member_div").removeClass().addClass("validateField has-success");
	    }
	    else {
			$("#company_list").removeClass('validateRequired').addClass('validateRequired');
			$("#member_div").removeClass().addClass("validateField has-error");
	    }
	}

   /*if (member_status == "nm"){
		if ($("#CompanyIndividualName").val() != ''){
			$("#CompanyIndividualName").removeClass('validateRequired');
			$("#nonmember_div").removeClass().addClass("validateField has-success");
	    }
	    else {
			$("#CompanyIndividualName").removeClass('validateRequired').addClass('validateRequired');
			if ($("#CompanyIndividualName").val() == ''){
				$("#nonmember_div").removeClass().addClass("validateField has-error");
			}
			else{
				$("#nonmember_div").removeClass().addClass("validateField has-success");
			}
	    }
	}
	else{
		if ($("#__searchit2").val() != ''){
			$("#company_list").removeClass('validateRequired');
			$("#member_div").removeClass().addClass("validateField has-success");
	    }
	    else {
			$("#company_list").removeClass('validateRequired').addClass('validateRequired');
			if ($("#company_list").val() == ''){
				$("#member_div").removeClass().addClass("validateField has-error");
			}
			else{
				$("#member_div").removeClass().addClass("validateField has-success");
			}
	    }
	} */
    if ($("form > div .has-error").length > 0){
        $('html, body').animate({
            scrollTop: $("form > div .has-error").first().offset().top - 150
        }, 1000);
        $("#time_slot_row").hide();
        $("#time_table_body").html('');
        $("#time_note_div").html('');
    }
    else {
    	  window.scrollTo(0, 1200);
    }
});



// Add Time Slot table
function add_table(){
    start_date = $("#FromDate").val();
    end_date = $("#ToDate").val();

    formsubmit = document.getElementById('submit_btn')
    console.log(formsubmit.classList);
    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false;
    }
    else{
        if (start_date && end_date){
            $("#time_slot_row").show();
            $("#time_table_body").html('');
            $("#submit_btn").hide();
            $("#re_enter_btn").show();
            $("#time_note_div").html('');

            $.ajax({
                type: "POST",
                url: "/hallbookingapp/get-slot-table/",
                data: {"start_date": start_date, "end_date": end_date,
                        "check_user": member_status, "hall_id": $("#hall_id").val()},
                success: function(response){
                    if (response.success == 'true'){
                        $.each(response.output_list, function(index, item){
                            if (item.status == "YES" && item.type == "National Holiday"){
                                $("#time_table_body").append('<tr style="background-color: #ffdcd0;">'+
                                                '<td class="col-md-2">'+
                                                '<label name="from_date_list1[]">'+ item.date +'</label>'+
                                                '<input type="text" name="from_date_list[]" value='+ item.formatted_date +' hidden>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="00" name="from_hour_list[]" readonly />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="00" name="from_minute_list[]" readonly />'+
                                                    '<select disabled class="form-control time-table-select" name="from_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_hour_list[]" readonly />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_minute_list[]" readonly />'+
                                                    '<select disabled class="form-control time-table-select" name="to_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-2">' + item.type + '</td>'+
                                            '</tr>');
                            }
                            else if (item.status == "YES" && item.type == "MCCIA Holiday" && item.is_booking_available == 'True'){
                                $("#time_table_body").append('<tr style="background-color: #dcd0ff;">'+
                                                '<td class="col-md-2">'+
                                                '<label name="from_date_list1[]">'+ item.date +'</label>'+
                                                '<input type="text" name="from_date_list[]" value='+ item.formatted_date +' hidden>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="00" name="from_hour_list[]" />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="00" name="from_minute_list[]" />'+
                                                    '<select class="form-control time-table-select" name="from_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_hour_list[]" />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_minute_list[]" />'+
                                                    '<select class="form-control time-table-select" name="to_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-2">' + item.type + '</td>'+
                                            '</tr>');
                            }
                            else if (item.status == "YES" && item.type == "MCCIA Holiday" && item.is_booking_available == 'False'){
                                $("#time_table_body").append('<tr style="background-color: #dcd0ff;">'+
                                                '<td class="col-md-2">'+
                                                '<label name="from_date_list1[]">'+ item.date +'</label>'+
                                                '<input type="text" name="from_date_list[]" value='+ item.formatted_date +' hidden>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="00" name="from_hour_list[]" readonly />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="00" name="from_minute_list[]" readonly />'+
                                                    '<select disabled class="form-control time-table-select" name="from_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_hour_list[]" readonly />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_minute_list[]" readonly />'+
                                                    '<select disabled class="form-control time-table-select" name="to_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-2">' + item.type + '</td>'+
                                            '</tr>');
                            }
                            else{
                                $("#time_table_body").append('<tr>'+
                                                '<td class="col-md-2">'+
                                                '<label name="from_date_list[]">'+ item.date +'</label>'+
                                                '<input type="text" name="from_date_list[]" value='+ item.formatted_date +' hidden>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="from_hour_list[]" />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="from_minute_list[]" />'+
                                                    '<select class="form-control time-table-select" name="from_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
                                                '<td class="col-md-4">'+
                                                    '<input type="number" class="form-control time-table-input" placeholder="HH"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_hour_list[]" />'+
                                                    '<input type="number" class="form-control time-table-input" value="00" placeholder="MM"'+
                                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                           'min="0" name="to_minute_list[]" />'+
                                                    '<select class="form-control time-table-select" name="to_period_list[]" style="display: inline-block; width: 25%;">'+
                                                        '<option value="AM">AM</option>'+
                                                        '<option value="PM">PM</option>'+
                                                    '</select>'+
                                                '</td>'+
    //                                            '<td class="col-md-3">'+
    //                                                '<select name="demo[]" class="my_multi_select form-control" multiple="multiple">'+
    //                                                '</select>'+
    //                                            '</td>'+
                                                '<td class="col-md-4">NO</td>'+
                                            '</tr>');
                            }

                        });

    //                     Hall Equipment Multiselect Dropdown

    //                    $('.my_multi_select').multiselect({
    //                        placeholder: 'None Selected',
    //                    });
    //
    //                    $('select[name="demo[]"]').each(function(index, item){
    //                        $.each(response.hall_equipment_list, function(rindex, ritem){
    //                            var data = '<option value="'+ ritem.id +'">'+ritem.hall_equipment +'</option>'
    //                            $(item).append(data);
    //                        });
    //                    });

                        $("#continue_btn").hide();
                        $("#re_enter_btn").show();
                        $("#time_confirm_row").show();
                        $("#confirm_booking_btn").show();
                    }
                }
            });
        }
    }



}

// Save Hall Booking
function save_booking(){
    var booking_data = {}
    var start_time = Date.parse('10:00 AM');
    var end_time = Date.parse('04:00 PM');
    var today_date = new Date();

    $.each($("#time_table_body tr"), function(tindex, titem){
        $(titem).css("background-color", "initial");
    });

    if (validate_time()){
        if (check_availability()){
            bootbox.confirm({
                message: "Do you want to book more hall?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
//                    if (result){
                        $('#company_list').removeAttr("disabled");
                        user_track_id = $('#user_track_id').val();
								if (member_status=='nm') {
									company_name_text = $("#CompanyIndividualName option:selected").text()
								}
								else if (member_status=='m') {
									company_name_text = $("#company_list option:selected").text()
							   }

							   $("#company_name_text_div").css("display", "block");
                        $("#CompanyIndividualNameDiv").val(company_name_text);
                        $("#nonmember_list").css("display", "none");
                        $("#member_list").css("display", "none");

                        $.ajax({
                            type: "POST",
                            url: "/hallbookingapp/save-temp-booking-data/",
                            async: false,
                            data: $('#check_hall_booking_form, #check_hall_form').serialize() + "&member_status="+member_status +"&booking_id="+booking_id +"&is_continue="+result +"&user_track_id="+user_track_id +"&company_name_text="+company_name_text,
                            success: function(response){
//                                $('#company_list').attr("disabled", true);
                                if (response.success=='true'){
                                    booking_id = response.booking_id

                                    if (response.member_status == 'm'){
                                         $("#non_member_radio").hide()
                                    }else{
                                         $("#member_radio").hide()
                                    }
                                    $("#non_member_radio").hide();
                                    $("#member_radio").hide();

                                    $("#hall_booking_landing_div").show();
                                    $("#location_div").show();
                                    $("#hall_booking_form_div").hide();
                                    $("#FromDate").val('');
                                    $("#ToDate").val('');
                                    $("#time_slot_row").css("display", "none");
                                    $("#confirm_booking_btn").hide();
//                                    $("#submit_btn").hide();
                                    $("#CompanyIndividualName").attr("readonly", true);
                                    $("#GSTIN").attr("readonly", true);
                                    $("#address").attr("readonly", true);
                                    $("#email").attr("readonly", true);
                                    $('#company_list').attr("disabled", true);
                                    $("#booking_id").val(response.booking_id)

                                }else if (response.success == 'false'){
                                   window.location.href = '/hallbookingapp/hall-booking-confirm/'+ response.booking_id + '/'
                                }else{
                                    bootbox.alert("<span class='center-block text-center'>Sorry for inconvenience. An error occurred</span>")
                                }

                            },
                            error: function(response){
                                console.log("HSTBDE = ",response);
                                alert("Sorry for inconvenience. An error occurred");
//                                window.location.href = '/hallbookingapp/open-hallbooking-page/'
                            }
                        });

//                        window.location.href = '/hallbookingapp/open-hallbooking-page/'
//                    }
//                    else{
//                        var key = 'data'+key_number.toString();
//                        booking_data[key] = create_data_object();
//                        localStorage.setItem("data_obj"+key_number.toString(), JSON.stringify(booking_data));
//                        key_number = key_number + 1;
//
//                        // Get Data object and send it to Server
//                        var data_list = []
//                        var archive = {}, // Notice change here
//                        keys = Object.keys(localStorage),
//                        i = keys.length;
//
//                        while ( i-- ) {
//                            archive[ keys[i] ] = localStorage.getItem( keys[i] );
//                        }
//
//                        last_index = keys.length;
//                        var iterate_index = last_index;
//
//                        while (iterate_index != 0){
//                            var stored_data = localStorage.getItem("data_obj"+iterate_index);
//                            myObject = JSON.parse(stored_data);
//                            show_data = myObject['data'+iterate_index]
//
//                            data_list.push(show_data);
//                            iterate_index = iterate_index - 1;
//                        }
//
//                        var formData = new FormData();
//                        formData.append("data_list", JSON.stringify(data_list));
//
//                        // Ajax Call to get Payment Data
//                        $.ajax({
//                            type: "POST",
//                            url: "/hallbookingapp/hall-booking-confirm/",
//                            data: formData,
//                            processData: false,
//                            contentType: false,
//                            success: function(response){
//                                if (response.success == 'true'){
//
//                                }
//                                else{
//                                    alert('Error Occurred');
//                                }
//                            }
//                        });
////                        window.open('/hallbookingapp/hall-booking-confirm/', "_self");
//                    }
                }
            });

        }
        else{
            console.log('no done');
        }
    }
}


// Validate Time Slot
function validate_time(){
    $("#time_note_div").html('');
    from_hour_array = $('[name="from_hour_list[]"]');
    from_minute_array = $('[name="from_minute_list[]"]');
    to_hour_array = $('[name="to_hour_list[]"]');
    to_minute_array = $('[name="to_minute_list[]"]');
    from_period_array = $('[name="from_period_list[]"]');
    to_period_array = $('[name="to_period_list[]"]');
    var str1 = $("#start_time_"+$("#hall_id").val()).val();
    var str2 = $("#end_time_"+$("#hall_id").val()).val();
    var flag_one = true; // To Check Hall Start & End Time
    var flag_two = true; // To Check Input Start & End Time
    var flag_three = true; // To Check if From & To are equal

    for (i=0; i<from_hour_array.length; i++){
        if ( !$(from_hour_array[i]).is('[readonly]')){
            if ($(from_hour_array[i]).val() != ''){
                var from_time = Date.parse(str1);
                var to_time = Date.parse(str2);
                if ($(from_hour_array[i]).val() == 12 && $(from_period_array[i]).val() == 'PM'){
                    var input_from_time = new Date();
                    input_from_time.setHours($(from_hour_array[i]).val());
                    input_from_time.setMinutes($(from_minute_array[i]).val());
                }
                else{
                    if ($(from_hour_array[i]).val() == 12 && $(from_period_array[i]).val() == 'AM'){
                        flag_one = false;
                    }
                    var input_from_time = Date.parse($(from_hour_array[i]).val()+':'+ $(from_minute_array[i]).val() + ' '+ $(from_period_array[i]).val());
                }
                if ($(to_hour_array[i]).val() == 12 && $(to_period_array[i]).val() == 'PM'){
                    var input_to_time = new Date();
                    input_to_time.setHours($(to_hour_array[i]).val());
                    input_to_time.setMinutes($(to_minute_array[i]).val());
                }
                else{
                    if ($(to_hour_array[i]).val() == 12 && $(to_period_array[i]).val() == 'AM'){
                        flag_one = false;
                    }
                    var input_to_time = Date.parse($(to_hour_array[i]).val()+':'+ $(to_minute_array[i]).val() + ' '+ $(to_period_array[i]).val());
                }
                if (input_from_time < input_to_time){
                    if (input_from_time >= from_time && input_to_time <= to_time){
                    }
                    else{
                        flag_one = false;
                    }
                }
                else{
                    flag_three = false;
                    flag_one = true;
                }

                if (parseInt($(from_hour_array[i]).val()) > 12){
                    flag_two = false;
                }

                if (parseInt($(to_hour_array[i]).val()) > 12){
                    flag_two = false;
                }

                if ($(from_minute_array[i]).val().trim() == "00" || $(from_minute_array[i]).val().trim() == "30"){
                }
                else{
                    flag_two = false;
                }

                if ($(to_minute_array[i]).val().trim() == "00" || $(to_minute_array[i]).val().trim() == "30"){
                }
                else{
                    flag_two = false;
                }
            }
            else{
                flag_two = false;
            }
        }
    }
    if (flag_two != true){
        $("#time_table").after('<div id="time_note_div"><label>Please enter valid time in 12 Hour Format (HH:MM eg. 05:00 PM) & in multiple of 30 minutes.</label></div>');
        return flag_two;
    }
    else if (flag_one != true){
        $("#time_table").after('<div id="time_note_div"><label>Please ensure that Booking Time is between '+str1+' '+str2+'</label></div>');
        return flag_one;
    }
    else if (flag_three != true){
        $("#time_table").after('<div id="time_note_div"><label>Please ensure that From Time must be less than To Time & should have 1 hour difference.</label></div>');
        return flag_three;
    }
    else if (flag_one == true && flag_two == true && flag_three == true){
        return flag_one;
    }
}



// Check Availability
function check_availability(){
    var date_list = []
    var from_period_array = []
    var to_period_array = []
    var from_hour_list = []
    var to_hour_list = []
    var from_minute_list = []
    var to_minute_list = []

    $.each($("#time_table_body tr"), function(tindex, titem){
        if ($(titem).find("td:last").text() == "NO"){
            console.log('---',typeof($(titem).find("td:nth-child(1) > input").val()))
            date_list.push($(titem).find("td:nth-child(1) > input").val());
            from_hour_list.push($(titem).find("td:nth-child(2) > input:nth-child(1)").val().trim());
            from_minute_list.push($(titem).find("td:nth-child(2) > input:nth-child(2)").val().trim());
            from_period_array.push($(titem).find("td:nth-child(2) > select").val());
            to_hour_list.push($(titem).find("td:nth-child(3) > input:nth-child(1)").val().trim());
            to_minute_list.push($(titem).find("td:nth-child(3) > input:nth-child(2)").val().trim());
            to_period_array.push($(titem).find("td:nth-child(3) > select").val());
        }
    });

    var availData = new FormData();
    var flag = true;

    availData.append("hall_id", $("#hall_id").val());
    availData.append("date_list", date_list);
    availData.append("from_period", from_period_array);
    availData.append("to_period", to_period_array);
    availData.append("from_hour_list", from_hour_list);
    availData.append("to_hour_list", to_hour_list);
    availData.append("from_minute_list", from_minute_list);
    availData.append("to_minute_list", to_minute_list);
    
    $.ajax({
        type: "POST",
        async: false,
        url: '/hallbookingapp/check-availability/',
        data: $('#check_hall_form').serialize() + "&hall_id="+$("#hall_id").val(),

        success: function(response){
            if ((response.slot_not_avail_list).length > 0){
                $.each($("#time_table_body tr td input"), function(tindex, titem){
                    $.each(response.slot_not_avail_list, function (rindex, ritem) {
                        if ($(titem).val() == ritem.date){
                            $(titem).closest("tr").css("background-color", "red");
                            flag = false;
                        }
                    });
                });
            }
        },
        error: function(response){
            console.log('Error = ',response);
        }
    });
    if (flag != false){
        return true;
    }
    else{
        $("#time_table").after('<div id="time_note_div"><label>Hall is not available for the highlighted time slot and There is 1 hr gap in between 2 Hall schedules.</label></div>');
        return false;
    }
}



// Create Data Booking Object
function create_data_object(){

    var date_list = []
    var from_hour_list = []
    var to_hour_list = []
    var from_minute_list = []
    var to_minute_list = []
    var from_period_array = []
    var to_period_array = []
    start_date = $("#FromDate").val();
    end_date = $("#ToDate").val();

    start_date = start_date.split("/");
    end_date = end_date.split("/");

    start_date = new Date(start_date[2],start_date[0]-1,start_date[1]);
    end_date = new Date(end_date[2],end_date[0]-1,end_date[1]);

    for (var i=0; start_date <= end_date; start_date.setDate(start_date.getDate() + 1), i++) {
        date_list.push(new Date(start_date));
    }

    from_period_array.push($('[name="from_period_list[]"]').map(function () {return this.value;}).get());
    to_period_array.push($('[name="to_period_list[]"]').map(function () {return this.value;}).get());

    if ($("#company_list").val() != ''){
        var add_data = new FormData();
        add_data.append("company_name", $("#company_list option:selected").text());
        add_data.append("address", $("#address").val());
        add_data.append("contact_person", $("#ContactPerson").val());
        add_data.append("designation", $("#Designation").val());
        return {
            "company_name": $("#company_list option:selected").text(),
            "address":$("#address").val(),
            "contact_person":$("#ContactPerson").val(),
            "designation":$("#Designation").val(),
            "mobile":$("#Mobile").val(),
            "tel_o":$("#Tel").val(),
            "tel_r":$("#TelR").val(),
            "email":$("#email").val(),
            "event_nature":$("#NatureoftheEvent").val(),
            "date_list": date_list,
            "from_hour": $('input[name="from_hour_list[]"]').map(function () {return this.value;}).get(),
            "to_hour": $('input[name="to_hour_list[]"]').map(function () {return this.value;}).get(),
            "from_minute": $('input[name="from_minute_list[]"]').map(function () {return this.value;}).get(),
            "to_minute": $('input[name="to_minute_list[]"]').map(function () {return this.value;}).get(),
            "from_period": from_period_array,
            "to_period": to_period_array,
            "hall_id": $("#hall_id").val(),
            "hall_name": $("#hall_name").val(),
            "company_id": $("#company_list").val(),
            "key_number": key_number
        }
    }
    else{
        return {
            "company_name": $("#CompanyIndividualName").val(),
            "address":$("#address").val(),
            "contact_person":$("#ContactPerson").val(),
            "designation":$("#Designation").val(),
            "mobile":$("#Mobile").val(),
            "tel_o":$("#Tel").val(),
            "tel_r":$("#TelR").val(),
            "email":$("#email").val(),
            "event_nature":$("#NatureoftheEvent").val(),
            "date_list": date_list,
            "from_hour": $('input[name="from_hour_list[]"]').map(function () {return this.value;}).get(),
            "to_hour": $('input[name="to_hour_list[]"]').map(function () {return this.value;}).get(),
            "from_minute": $('input[name="from_minute_list[]"]').map(function () {return this.value;}).get(),
            "to_minute": $('input[name="to_minute_list[]"]').map(function () {return this.value;}).get(),
            "from_period": from_period_array,
            "to_period": to_period_array,
            "hall_id": $("#hall_id").val(),
            "hall_name": $("#hall_name").val(),
            "company_id": 'None',
            "key_number": key_number
        }
    }
}                


// Call this function on click of additional facility icon
function additional_facility(myResponse, user_type_val){ 
    $("#time_note").html("")
    $("#facility_charges").html("");
    $("#total_charges").html("");
    hall_id_val = myResponse
    user_type = user_type_val
    date_obj_val = date_obj
    holiday = holiday_val
    $('.extra_facility').on('click', function(e) {
        var holiday = $(this).closest("tr").find('td:eq(3)').text();
        var date_val = $(this).closest("tr").find('td:eq(0) > input').val(); 
        var from_time_hrs = $(this).closest("tr").find('td:nth-child(2) > input:nth-child(1)').val();
        var from_time_minute = $(this).closest("tr").find('td:nth-child(2) > input:nth-child(2)').val();
        var from_time_period = $(this).closest("tr").find('td:nth-child(2) > select').val();
        var to_time_hrs = $(this).closest("tr").find('td:nth-child(3) > input:nth-child(1)').val();
        var to_time_minute = $(this).closest("tr").find('td:nth-child(3) > input:nth-child(2)').val();
        var to_time_period = $(this).closest("tr").find('td:nth-child(3) > select').val();
        if (validate_time_for_additional_facility(from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period)){
            if (availability_for_additional_facility(date_val,holiday,from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period,avail_booking)){
            $.ajax({
            type: "GET",
            url: '/hallbookingapp/additional-facility-details/?from_hour=' + from_time_hrs +'&to_hour='+to_time_hrs +'&from_minute='+from_time_minute + '&to_minute=' + to_time_minute + '&hall_id=' + hall_id_val+'&NatureoftheEvent='+ $("#NatureoftheEvent").val() +'&fromdate=' +$('#FromDate').val() +'&todate=' + $('#ToDate').val() + '&companyindividualname=' +$('#CompanyIndividualName').val() +'&date_value='+date_val,
            data: {
                "from_hour": from_time_hrs,
                "to_hour": to_time_hrs,
                "from_minute": from_time_minute,
                "to_minute": to_time_minute,
                'from_period' : from_time_period,
                'to_period' : to_time_period,
                "hall_id":myResponse,
                "user_type_val" : user_type_val,
                "date_value" : date_val,
            },

            success: function(response){
               if (response.success == 'true'){
                $('#add_extra_hour_facility_modal').modal('show');
                $('#hall_name_modal1').text(response.hall_name);
                $('#company_name_modal1').text(response.company_name_val);
                $('#nature_of_event_modal1').text(response.event_nature);
                // $('#event_date_modal1').text(response.event_date);
                $('#booking_from_time_modal1').text(response.booking_from_time);
                $('#booking_from_to_modal1').text(response.booking_to_time); 
                $('#hall_booking_date').val(date_val);
                $('#hall_name_modal2').val(response.hall_name);
                $('#company_name_modal2').val(response.company_name_val);
                $('#nature_of_event_modal2').val(response.event_nature);
                $('#event_date_modal2').val(response.event_date);
                $('#booking_from_time_modal2').val(response.booking_from_time);
                $('#booking_from_to_modal2').val(response.booking_to_time);                  
                $("#hall_charges").text(response.hall_rent);
                $("#hall_charges_rent").val(response.hall_rent);
                $("#hall_id1").val(response.hall_detail_id);
                $("#additional_facility_table").find("tr:not(:first)").remove();
                
                $.each(response.hall_equipment, function (index, item) {
                $("#from_hour_main").val(item.from_hour);
                $("#from_minute_main").val(item.from_minute);
                $("#from_period_main").val(item.from_period);
                $("#to_hour_main").val(item.to_hour);
                $("#to_minute_main").val(item.to_minute);
                $("#to_period_main").val(item.to_period);
                if(item.hall_rate != 0){
                $("#extra_hour_facility_body").append('<tr>'+               
                 '<td class="has-success"><label class="col-md-4 text-dark extra_facility_values" id= "facilities_id" for="facilities_id">'+item.facility_list+'</label></td>'+
                 '<td class="has-success"><label class="col-md-4 text-dark extra_facility_values" id="hall_rate" for="hall_rate">'+item.hall_rate+'</label></td>'+                                            
                 '<td class="has-success"><input type="number" class="form-control time-table-input " placeholder="HH"'+
                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                           'min="0" name="from_hour[]"  onInput="extra_facility_values(this)" />'+
                                    '<input type="number" class="form-control time-table-input extra_facility_values(this)" value="00" placeholder="MM"'+
                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                           'min="0" name="from_minute[]" onInput="extra_facility_values(this)" />'+
                                    '<select class="extra_facility_values form-control time-table-select " name="from_period[]" style="display: inline-block; width: 25%;" onchange="extra_facility_values(this)">'+
                                        '<option value="AM">AM</option>'+
                                        '<option value="PM">PM</option>'+
                                    '</select>'+ 
                                    '</td>'+                                           
                 '<td class="has-success"><input type="number" class="form-control time-table-input extra_facility_values" placeholder="HH"'+
                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                           'min="0" name="to_hour[]" onInput="extra_facility_values(this)" />'+
                                    '<input type="number" class="form-control time-table-input extra_facility_values" value="00" placeholder="MM"'+
                                           'maxlength="2" style="display: inline-block; width: 25%;"'+
                                           'min="0" name="to_minute[]" onInput="extra_facility_values(this)" />'+
                                    '<select class="extra_facility_values form-control time-table-select" name="to_period[]" style="display: inline-block; width: 25%;" onchange="extra_facility_values(this)">'+
                                        '<option value="AM">AM</option>'+
                                        '<option value="PM">PM</option>'+
                                    '</select>'+  
                                    '</td>'+       
                 '<td class="has-success"><label class="col-md-3 text-dark extra_facility_values"></label></td>'+                                             
                 '</tr>');
            }
            });
         }
    },
        beforeSend: function() {
            $("#processing").css('display', 'block');
        },
        complete: function() {
            $("#processing").css('display', 'none');
        },
            error: function(response){
                console.log('Error = ',response);
            }
        });
        }
        else{
            $("#add_extra_hour_facility_modal").modal('hide');
            return false;
        }
        }else{
            $("#add_extra_hour_facility_modal").modal('hide');
            return false;
        }
    });
}


// Validate time when we click on additional facility icon
function validate_time_for_additional_facility(from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period){
    $("#time_note_div").html('');
    facility_from_hour = from_time_hrs;
    facility_from_minute = from_time_minute;
    facility_to_hour = to_time_hrs;
    facility_to_minute = to_time_minute;
    facility_from_period = from_time_period;
    facility_to_period = to_time_period;
    var str1 = $("#start_time_"+$("#hall_id").val()).val();
    var str2 = $("#end_time_"+$("#hall_id").val()).val();
    var flag_one = true; // To Check Hall Start & End Time
    var flag_two = true; // To Check Input Start & End Time
    var flag_three = true; // To Check if From & To are equal
        if (facility_from_hour != ''){
            var from_time = Date.parse(str1);
            var to_time = Date.parse(str2);
            if (facility_from_hour == 12 && facility_from_period == 'PM'){
                var input_from_time = new Date();
                input_from_time.setHours(facility_from_hour);
                input_from_time.setMinutes(facility_from_minute);
                input_from_time.setSeconds(00);

            }
            else{
                if (facility_from_hour == 12 && facility_from_period == 'AM'){
                    flag_one = false;
                }
                var input_from_time = Date.parse(facility_from_hour+':'+ facility_from_minute + ' '+ facility_from_period);
            }
            if (facility_to_hour == 12 && facility_to_period == 'PM'){
                var input_to_time = new Date();
                input_to_time.setHours(facility_to_hour);
                input_to_time.setMinutes(facility_to_minute);
                input_to_time.setSeconds(00)
            }
            else{
                if (facility_to_hour == 12 && facility_to_period == 'AM'){
                    flag_one = false;
                }
                var input_to_time = Date.parse(facility_to_hour+':'+ facility_to_minute + ' '+ facility_to_period);
            }
            if (input_from_time < input_to_time){
                if (input_from_time >= from_time && input_to_time <= to_time){
                }
                else{
                    flag_one = false;
                }
            }
            else{
                flag_three = false;
                flag_one = true;
            }

            if (parseInt(facility_from_hour) > 12){
                flag_two = false;
            }

            if (parseInt(facility_to_hour) > 12){
                flag_two = false;
            }

            if (facility_from_minute == "00" || facility_from_minute == "30"){
            }
            else{
                flag_two = false;
            }

            if (facility_to_minute == "00" || facility_to_minute == "30"){
            }
            else{
                flag_two = false;
            }
        }
        else{
            flag_two = false;
        }
    if (flag_two != true){
        $("#time_table").after('<div id="time_note_div"><label>Please enter valid time in 12 Hour Format (HH:MM eg. 05:00 PM) & in multiple of 30 minutes.</label></div>');
        return flag_two;
    }
    else if (flag_one != true){
        $("#time_table").after('<div id="time_note_div"><label>Please ensure that Booking Time is between '+str1+' '+str2+'</label></div>');
        return flag_one;
    }
    else if (flag_three != true){
        $("#time_table").after('<div id="time_note_div"><label>Please ensure that From Time must be less than To Time & should have 1 hour difference.</label></div>');
        return flag_three;
    }
    else if (flag_one == true && flag_two == true && flag_three == true){
        return flag_one;
    }
}


// Check Availability when we click on additional facility icon
function availability_for_additional_facility(date_val,holiday,from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period,avail_booking){
    var date_list = []
    var from_period_array = []
    var to_period_array = []
    var from_hour_list = []
    var to_hour_list = []
    var from_minute_list = []
    var to_minute_list = []
    // var date = new Date(date_val);
    // var dd = date.getDate(); 
    // var mm = date.getMonth() + 1; 
    // var yyyy = date.getFullYear(); 
    // if (dd < 10) { 
    //     dd = '0' + dd; 
    // } 
    // if (mm < 10) { 
    //     mm = '0' + mm; 
    // } 
    // var date_value = dd + '/' + mm + '/' + yyyy;   
    
    date_list.push(date_val);
    from_hour_list.push(from_time_hrs.trim());
    from_minute_list.push(from_time_minute.trim());
    from_period_array.push(from_time_period);
    to_hour_list.push(to_time_hrs.trim());
    to_minute_list.push(to_time_minute.trim());
    to_period_array.push(to_time_period);
    
    var availData = new FormData();
    var flag = true;
    availData.append("hall_id", $("#hall_id").val());
    availData.append("from_date_list[]", date_list);
    availData.append("from_period_list[]", from_period_array);
    availData.append("to_period_list[]", to_period_array);
    availData.append("from_hour_list[]", from_hour_list);
    availData.append("to_hour_list[]", to_hour_list);
    availData.append("from_minute_list[]", from_minute_list);
    availData.append("to_minute_list[]", to_minute_list);    
    $.ajax({
        type: "POST",
        async: false,
        url: '/hallbookingapp/check-availability/',
        processData: false,
        contentType: false,
        data: availData,
        success: function(response){
            if ((response.slot_not_avail_list).length > 0){
                $.each($("#time_table_body tr td input"), function(tindex, titem){
                    $.each(response.slot_not_avail_list, function (rindex, ritem) {
                        if ($(titem).val() == ritem.date){
                            $(titem).closest("tr").css("background-color", "red");
                            flag = false;
                        }                        
                    });
                });
            }            
        },
        beforeSend: function() {
            $("#processing").css('display', 'block');
        },
        complete: function() {
            $("#processing").css('display', 'none');
        },
        error: function(response){
            console.log('Error = ',response);
        }
    });
    if (flag != false){
        return true;
    }
    else{
        $("#time_table").after('<div id="time_note_div"><label>Hall is not available for the highlighted time slot.</label></div>');
        return false;
    }
}



// Call this function when we type time in the facility from & to time fields
function extra_facility_values(p_one){ 
    total_amt = 0
    $("#time_note").html("")
    from_time_hrs = $(p_one).closest("tr").find("td:nth-child(3) > input:nth-child(1)").val();
    from_time_minute = $(p_one).closest("tr").find("td:nth-child(3) > input:nth-child(2)").val();
    from_time_period = $(p_one).closest("tr").find("td:nth-child(3) > select").val();
    to_time_hrs = $(p_one).closest("tr").find("td:nth-child(4) > input:nth-child(1)").val();
    to_time_minute = $(p_one).closest("tr").find("td:nth-child(4) > input:nth-child(2)").val(); 
    to_time_period =$(p_one).closest("tr").find("td:nth-child(4) > select").val();
    rate = $(p_one).closest("tr").find("td:eq(1) label").text();  
    var result = extra_facility_values_validation(from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period,rate)
    if (result[1]){        
        calculate_amount();
    }
}


// Function to calculate amount of Additional Facilities
function calculate_amount(){
    var facility_charges = 0;
    $("#additional_facility_table > tbody  > tr").each(function(e){
        var from_time_hrs = $(this).closest("tr").find("td:nth-child(3) > input:nth-child(1)").val();        
        var from_time_minute = $(this).closest("tr").find("td:nth-child(3) > input:nth-child(2)").val();
        var from_time_period = $(this).closest("tr").find("td:nth-child(3) > select").val();
        var to_time_hrs = $(this).closest("tr").find("td:nth-child(4) > input:nth-child(1)").val();
        var to_time_minute = $(this).closest("tr").find("td:nth-child(4) > input:nth-child(2)").val();
        var to_time_period =$(this).closest("tr").find("td:nth-child(4) > select").val();
        var rate = $(this).closest("tr").find("td:eq(1) label").text();

        var validation_output = extra_facility_values_validation(from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period,rate)
        if (validation_output[1]){
            var input_from_time = validation_output[0]['input_from_time'];
            var input_to_time = validation_output[0]['input_to_time'];  
            var res = Math.abs(input_to_time - input_from_time) / 1000;
            var hours = Math.floor(res / 3600) % 24;        
            var minutes = hours*(1000 * 60 * 60);
            var amount = hours * rate;
            $(this).closest("tr").find("td:eq(4)").text(amount);
            facility_charges = parseFloat(facility_charges) + parseFloat(amount)            
            total_amt = facility_charges + parseFloat($("#hall_charges_rent").val());
            $("#facility_charges").text(facility_charges);                
            $("#total_charges").text(total_amt);                 
        }
        else{
            return false;
        }
    });
}


// Facility from & to time validation function
function extra_facility_values_validation(from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period,rate){
    $("#time_note").val("");
    var temp = ''
    var str1 = $("#start_time_"+$("#hall_id").val()).val();
    var str2 = $("#end_time_"+$("#hall_id").val()).val();
    var from_hour_main = $("#from_hour_main").val();
    var from_minute_main = $("#from_minute_main").val();
    var from_period_main = $("#from_period_main").val();
    var to_hour_main = $("#to_hour_main").val();
    var to_minute_main = $("#to_minute_main").val();
    var to_period_main = $("#to_period_main").val();
    var hall_rate = $("#hall_charges_rent").val();
    var from_time = Date.parse(str1);
    var to_time = Date.parse(str2);
    var flag_one = true; // To Check Hall Start & End Time
    var flag_two = true; // To Check Input Start & End Time
    var flag_three = true; // To Check if From & To are equal or From < To
    var flag_four = true; // Input time is between Main From and To time 

    if (from_time_hrs != '' && to_time_hrs != '' && from_time_minute != '' && to_time_minute != ''){
        if (from_hour_main == 12 && from_period_main == 'PM'){
            var main_input_from_time = new Date();
            main_input_from_time.setHours(from_hour_main);
            main_input_from_time.setMinutes(from_minute_main);
            main_input_from_time.setSeconds(00);
        }
        else{
            if (from_hour_main == 12 && from_period_main == 'AM'){
                flag_one = false;
            }
            var main_input_from_time = Date.parse(from_hour_main+':'+ from_minute_main + ' '+ from_period_main);
            
        }
        if (to_hour_main == 12 && to_period_main == 'PM'){
            var main_input_to_time = new Date();
            main_input_to_time.setHours(to_hour_main);
            main_input_to_time.setMinutes(to_minute_main);
            main_input_to_time.setSeconds(00);
        }
        else{
            if (to_hour_main == 12 && to_period_main == 'AM'){
                flag_one = false;
            }
            var main_input_to_time = Date.parse(to_hour_main+':'+ to_minute_main + ' '+ to_period_main);
        }
        if (from_time_hrs == 12 && from_time_period == 'PM'){
            var input_from_time = new Date();
            input_from_time.setHours(from_time_hrs);
            input_from_time.setMinutes(from_time_minute);
            input_from_time.setSeconds(00);
            }
        else{
            if (from_time_hrs == 12 && from_time_period == 'AM'){
                flag_one = false;
            }
            var input_from_time = Date.parse(from_time_hrs+':'+ from_time_minute + ' '+ from_time_period);
            }
        if (to_time_hrs == 12 && to_time_period == 'PM'){
            var input_to_time = new Date();
            input_to_time.setHours(to_time_hrs);
            input_to_time.setMinutes(to_time_minute);
            input_to_time.setSeconds(00);

        }
        else{
            if (to_time_hrs == 12 && to_time_period == 'AM'){
                flag_one = false;
            }
            var input_to_time = Date.parse(to_time_hrs+':'+ to_time_minute + ' '+ to_time_period);
        }

        if (main_input_from_time <= input_from_time  && main_input_to_time >=input_to_time ){
            if (input_from_time < input_to_time){    
            }
            else{
                flag_three = false;                
            }

        }
        else{
            flag_four = false;
        }

        if (parseInt(from_time_hrs) > 12){
            flag_two = false;
        }
        if (parseInt(to_time_hrs) > 12){
            flag_two = false;
        }

        if (from_time_minute == "00" || from_time_minute == "30"){
        }
        else{
            flag_two = false;
        }

        if (to_time_minute == "00" || to_time_minute == "30"){
        }
        else{
            flag_two = false;
        }

        var time_result = {
            'input_from_time' : input_from_time,
            'input_to_time' : input_to_time,
            'main_input_from_time':main_input_from_time,
            'main_input_to_time':main_input_to_time
            }

        if (flag_two != true){
            $("#time_note").html('<b>Please enter valid time in 12 Hour Format (HH:MM eg. 05:00 PM) & in multiple of 30 minutes.</b>');
            temp = flag_two;

        }
        else if (flag_one != true){
            $("#time_note").html('<b>Please ensure that Booking Time is between '+str1+' and '+str2+'</b>');
            temp = flag_one;

        }
        else if (flag_three != true){
            $("#time_note").html('<b>Please ensure that From Time must be less than To Time & should have 1 hour difference.</b>');
            temp = flag_three;

        }
        else if(flag_four != true){
            $("#time_note").html('<b>From Time and To Time is Should Between '+from_hour_main+' '+from_period_main+''+' and '+to_hour_main+' '+to_period_main+'</b> ');
            temp = flag_four;

        }
        else if (flag_one == true && flag_two == true && flag_three == true && flag_four == true){
            temp = flag_one;
            return [time_result , temp];
        }   
    }
    else{  
        return ['dd', false];
    }

}



var facility_data_list = []
function submit_extra_facility(){
    var booking_date_val = $('#hall_booking_date').val();
    var current_datetime = booking_date_val.split("/");    
    var booking_date = new Date(current_datetime[2], current_datetime[1]-1, current_datetime[0]);    
    var hall_id = $("#hall_id1").val();
    var from_hour_main = $("#from_hour_main").val()
    var from_minute_main =$("#from_minute_main").val()
    var from_period_main =$("#from_period_main").val()
    var to_hour_main = $("#to_hour_main").val()
    var to_minute_main = $("#to_minute_main").val()
    var to_period_main = $("#to_period_main").val()
    
    $("#additional_facility_table > tbody  > tr").each(function(e){
        var from_time_hrs = $(this).closest("tr").find("td:nth-child(3) > input:nth-child(1)").val();        
        var from_time_minute = $(this).closest("tr").find("td:nth-child(3) > input:nth-child(2)").val();
        var from_time_period = $(this).closest("tr").find("td:nth-child(3) > select").val();
        var to_time_hrs = $(this).closest("tr").find("td:nth-child(4) > input:nth-child(1)").val();
        var to_time_minute = $(this).closest("tr").find("td:nth-child(4) > input:nth-child(2)").val();
        var to_time_period =$(this).closest("tr").find("td:nth-child(4) > select").val();
        var facility_rate = $(this).closest("tr").find("td:eq(1) label").text();
        var facility_name = $(this).closest("tr").find("td:eq(0) label").text();
        date_values = create_time_object(from_hour_main,from_minute_main,from_period_main,to_hour_main,to_minute_main,to_period_main,from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period)
        input_from_time = date_values.input_from_time
        input_to_time = date_values.input_to_time
        main_input_from_time = date_values.main_input_from_time
        main_input_to_time = date_values.main_input_to_time
        flag_one = 1
        if(from_time_hrs != '' && from_time_minute != '' && from_time_period != '' && to_time_hrs != '' && to_time_minute != '' && to_time_period != ''){
            if (facility_data_list.length > 0) {
                 $.each(facility_data_list, function(index, item){
                   // console.log('item = ', item);    
                    if(item['hall_id'] == parseInt(hall_id) && item['booking_date'].getTime() === booking_date.getTime()){
                        console.log('hall_id and date matched');
                        if(item['booking_from_time'].getTime() === main_input_from_time.getTime() && item['booking_to_time'].getTime() === main_input_to_time.getTime()){
                            console.log('from and to time matched');
                            if(item['facility_name'] == facility_name){
                                console.log('facility matched');
                            item['facility_from_time'] = input_from_time
                            item['facility_to_time'] = input_to_time
                            item['facility_rate'] = facility_rate
                        }
                        else{
                            flag_one = "update"
                            console.log('facility NOT matched');
                            temp_obj = {
                                'hall_id' :parseInt(hall_id),
                                'booking_date' :booking_date,
                                'booking_from_time':main_input_from_time,
                                'booking_to_time':main_input_to_time,
                                'facility_from_time':input_from_time,
                                'facility_to_time':input_to_time,
                                'facility_name':facility_name,
                                'facility_rate':facility_rate,
                            }

                            // facility_data_list.push(temp_obj)
                        }
                        }
                        else{
                            flag_one = "update"
                            console.log('from and to time NOT matched')
                            temp_obj = {
                                'hall_id' :parseInt(hall_id),
                                'booking_date' :booking_date,
                                'booking_from_time':main_input_from_time,
                                'booking_to_time':main_input_to_time,
                                'facility_from_time':input_from_time,
                                'facility_to_time':input_to_time,
                                'facility_name':facility_name,
                                'facility_rate':facility_rate,
                            }
                            // facility_data_list.push(temp_obj)
                        }
                    }                        
                        else{
                            flag_one = "update"
                            console.log('hall_id and date NOT matched');
                            temp_obj = {
                            'hall_id' :parseInt(hall_id),
                            'booking_date' :booking_date,
                            'booking_from_time':main_input_from_time,
                            'booking_to_time':main_input_to_time,
                            'facility_from_time':input_from_time,
                            'facility_to_time':input_to_time,
                            'facility_name':facility_name,
                            'facility_rate':facility_rate,
                        }
                        // facility_data_list.push(temp_obj)
                        }

                    });
                 }
            else{
                console.log('FIRST ADD');
                temp_obj = {
                    'hall_id' :parseInt(hall_id),
                    'booking_date' :booking_date,
                    'booking_from_time':main_input_from_time,
                    'booking_to_time':main_input_to_time,
                    'facility_from_time':input_from_time,
                    'facility_to_time':input_to_time,
                    'facility_name':facility_name,
                    'facility_rate':facility_rate,
                }
                
            }
            if(flag_one == "update"){
                facility_data_list.push(temp_obj)
                console.log('--------1----temp_obj----------',temp_obj)
            }
            else{
                facility_data_list.push(temp_obj)
                console.log('----------temp_obj------------',temp_obj)
            }
        console.log('-------------facility_data_list------------------',facility_data_list)
    //     console.log('-------------flag_one------------------',flag_one)
    //     if (flag_one == "update"){
    //     var my_array = facility_data_list
    //     var start_index = 0
    //     var start_index1 = 1
    //     var start_index3 = 3
    //     var number_of_elements_to_remove = 1;
    //     var removed_elements = my_array.splice(start_index, number_of_elements_to_remove,temp_obj);
    //     var removed_element = removed_elements.splice(start_index1, number_of_elements_to_remove,temp_obj);
    // }
    //     console.log('--------removed_elements--------',removed_elements);
    //     console.log('--------removed_element--------',removed_element);
    //     console.log('--------my_array--------',my_array);
        //["tennis", "golf"]
        // if(flag_one = =1 || flag_two = 2 || flag_three = 3 ||  flag_four = 4 ){ 
        // if(flag_one == 2){
        // facility_data_list.push(temp_obj1)
        // }
        // if(flag_two == 3){
        //     facility_data_list.push(temp_obj2)}
        // if(flag_three == 4){
        //     facility_data_list.push(temp_obj3)}
        // if(flag_four == 5)
        //     facility_data_list.push(temp_obj4)
        // }
        }

    });
        $.ajax({
                type: "POST",
                // async: false,
                url: '/hallbookingapp/additional-facility-details-values/',
                data: {facility_data_list :facility_data_list},
                success: function(response){
                    if(response.success == 'true'){
                        bootbox.alert("successfull add")
                    $('#add_extra_hour_facility_modal').modal('hide');
                    }
                },
                beforeSend: function() {
                    $("#processing").css('display', 'block');
                },
                complete: function() {
                    $("#processing").css('display', 'none');
                },
                error: function(response){
                    console.log('Error = ',response);
                }
            });
}



function create_time_object(from_hour_main,from_minute_main,from_period_main,to_hour_main,to_minute_main,to_period_main,from_time_hrs,from_time_minute,from_time_period,to_time_hrs,to_time_minute,to_time_period){

if (from_hour_main == 12 && from_period_main == 'PM'){
            var main_input_from_time = new Date();
            main_input_from_time.setHours(from_hour_main);
            main_input_from_time.setMinutes(from_minute_main);
            main_input_from_time.setSeconds(00);
        }
        else{
            if (from_hour_main == 12 && from_period_main == 'AM'){
                flag_one = false;
            }
            var main_input_from_time = Date.parse(from_hour_main+':'+ from_minute_main + ' '+ from_period_main);
            
        }
        if (to_hour_main == 12 && to_period_main == 'PM'){
            var main_input_to_time = new Date();
            main_input_to_time.setHours(to_hour_main);
            main_input_to_time.setMinutes(to_minute_main);
            main_input_to_time.setSeconds(00);
        }
        else{
            if (to_hour_main == 12 && to_period_main == 'AM'){
                flag_one = false;
            }
            var main_input_to_time = Date.parse(to_hour_main+':'+ to_minute_main + ' '+ to_period_main);
        }
        if (from_time_hrs == 12 && from_time_period == 'PM'){
            var input_from_time = new Date();
            input_from_time.setHours(from_time_hrs);
            input_from_time.setMinutes(from_time_minute);
            input_from_time.setSeconds(00);
            }
        else{
            if (from_time_hrs == 12 && from_time_period == 'AM'){
                flag_one = false;
            }
            var input_from_time = Date.parse(from_time_hrs+':'+ from_time_minute + ' '+ from_time_period);
            }
        if (to_time_hrs == 12 && to_time_period == 'PM'){
            var input_to_time = new Date();
            input_to_time.setHours(to_time_hrs);
            input_to_time.setMinutes(to_time_minute);
            input_to_time.setSeconds(00);

        }
        else{
            if (to_time_hrs == 12 && to_time_period == 'AM'){
                flag_one = false;
            }
            var input_to_time = Date.parse(to_time_hrs+':'+ to_time_minute + ' '+ to_time_period);
        }
        var time_result = {
            'input_from_time' : input_from_time,
            'input_to_time' : input_to_time,
            'main_input_from_time':main_input_from_time,
            'main_input_to_time':main_input_to_time
            }

            return time_result;
}


function online_payment(){
    $("#online_payment_note_div").show();
    $("#payment_id").show();
    $("#conform_id").hide();
    $("#offline_payment_note").hide();
}

function offline_payment(){
    $("#conform_id").show();
    $("#payment_id").hide();
    $("#online_payment_note_div").hide();
    $("#offline_payment_note").show();
}

function pay_online(){
    $("#online_payment_model").modal('show');
    $("#conform_id").hide();
    $("#offline_payment_note").hide();
}