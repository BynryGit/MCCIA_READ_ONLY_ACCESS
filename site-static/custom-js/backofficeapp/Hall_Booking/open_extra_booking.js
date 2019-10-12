

$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

var sum = 0;
var total_rent = 0;
var gst = 0;
var total_payable = 0;
var deposit = 0;
var last_index = 0;
var data_list = [];

// Cancel Single Booking Modal - Get Basic Booking Detail
function cancelBookingDetail(id, row){
    $("#cancel_booking_detail_id").val(id);
    $.ajax({
	        type: "POST",
	        url: "/backofficeapp/get-hall-booking-details/",
	        data: {'booking_detail_id':id},

	        success: function(response){
	            if (response.success == 'true'){
                    $('#cancel_hall_name_modal').text(response.hall_name);
                    $('#cancel_company_name_modal').text(response.company_name);
                    $('#cancel_nature_of_event_modal').text(response.event_nature);
                    $('#cancel_event_date_modal').text(response.event_date);
                    $('#cancel_booking_from_time_modal').text(response.booking_from_time);
                    $('#cancel_booking_from_to_modal').text(response.booking_to_time);
	            }
	            else{
	                bootbox.alert('Sorry for inconvenience. An error occurred');
	            }
	        },
	        beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
	        error: function(response){
	            console.log('ECHB = ', response);
	            bootbox.alert('Sorry for inconvenience. An error occurred');
	        }
	    });
}

// Submit Cancel Single Booking Request
$("#cancel_booking_btn").click(function(e){
	e.preventDefault();
  hall_shifting_id = $('#checkbox_checked:checked').val();
	if ($("#cancel_date").val() == '' || $("#cancel_remark").val() == ''){
	    bootbox.alert('Please enter all required fields.');
	    return false;
	}
    var formData= new FormData();

    formData.append("booking_detail_id", $('#cancel_booking_detail_id').val());
    formData.append("cancel_date", $("#cancel_date").val());
    formData.append("cancel_type", $("#cancel_type").val());
    formData.append("cancel_remark", $("#cancel_remark").val());
    formData.append("hall_shifting", hall_shifting_id);

    $.ajax({
        type: "POST",
        url: '/backofficeapp/cancel-booking-detail/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            if(response.success=='true'){
                $("#cancel_booking_modal").modal('hide');
                $("#cancel_date").val('');
                $("#cancel_remark").val('');
                $("#cancel_type").val(0).change();
                bootbox.alert('Booking cancelled successfully');
                setTimeout(function(){ location.reload() }, 2000);
            }
            else{
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#cancel_date").val('');
                $("#cancel_remark").val('');
                $("#cancel_type").val(0).change();
            }
        },
        beforeSend: function () {
            $("#processing").css('display','block');
        },
        complete: function () {
            $("#processing").css('display','none');
        },
       error : function(response){
            console.log("ErroSP = ",response);
            bootbox.alert('Sorry for inconvenience. An error occurred');
            $("#cancel_booking_modal").modal('hide');
            $("#cancel_date").val('');
            $("#cancel_remark").val('');
            $("#cancel_type").val(0).change();
        }
   });
});


// Cancel All Hall Booking
$("#cancel_all_booking_btn").click(function(e){
  hall_shifting_id = $('#checkbox_checked1:checked').val();
    if ($("#booking_cancel_date").val() == '' || $("#booking_cancel_remark").val() == ''){
	    bootbox.alert('Please enter all required fields.');
	    return false;
	     }
    var formData= new FormData();

    formData.append("booking_id", $('#booking_id').val());
    formData.append("cancel_date", $("#booking_cancel_date").val());
    formData.append("cancel_type", $("#booking_cancel_type").val());
    formData.append("cancel_remark", $("#booking_cancel_remark").val());
    formData.append("hall_shifting", hall_shifting_id);
    formData.append("hall_rent_val", $("#hall_rent").val());

    $.ajax({
        type: "POST",
        url: '/backofficeapp/cancel-hall-booking/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            if(response.success=='true'){
                $("#cancel_all_booking_modal").modal('hide');
                $("#booking_cancel_date").val('');
                $("#booking_cancel_remark").val('');
                $("#booking_cancel_type").val(0).change();
                bootbox.alert('Booking cancelled successfully');
                setTimeout(function(){ location.reload() }, 2000);
            }
            else{
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#booking_cancel_date").val('');
                $("#booking_cancel_remark").val('');
                $("#booking_cancel_type").val(0).change();
            }
        },
        beforeSend: function () {
            $("#processing").css('display','block');
        },
        complete: function () {
            $("#processing").css('display','none');
        },
       error : function(response){
            console.log("ErroSP = ",response);
            bootbox.alert('Sorry for inconvenience. An error occurred');
            $("#cancel_all_booking_modal").modal('hide');
            $("#booking_cancel_date").val('');
            $("#booking_cancel_remark").val('');
            $("#booking_cancel_type").val(0).change();
        }
    });
});


// Clear content on Modal close / hide
$('#cancel_booking_modal').on('hidden.bs.modal', function (e) {
    $("#cancel_date").val('');
    $("#cancel_remark").val('');
    $("#cancel_type").val(0).change();
});

$('#cancel_all_booking_modal').on('hidden.bs.modal', function (e) {
    $("#booking_cancel_date").val('');
    $("#booking_cancel_remark").val('');
    $("#booking_cancel_type").val(0).change();
});


function addExtraHourPayment(id, row){
	       $("#booking_detail_id").val(id);
	        $("#extra_amt").val('');
          var starttimeval = new Date();
          var endtimeval = new Date();
          var start = "08.00 AM";
          var end = "10.00 PM"
          starttimeval.setTime(start);
          endtimeval.setTime(end);
		    $.ajax({
	        type: "POST",
	        url: "/backofficeapp/get-hall-booking-details/",
	        data: {'booking_detail_id':id ,'start_time_val':starttimeval,'end_time_val':endtimeval},
	
	        success: function(response){
	            if (response.success == 'true'){
							$('#hall_name_modal').text(response.hall_name);
							$('#company_name_modal').text(response.company_name);
							$('#nature_of_event_modal').text(response.event_nature);
							$('#event_date_modal').text(response.event_date);
							$('#booking_from_time_modal').text(response.booking_from_time);
							$('#booking_from_to_modal').text(response.booking_to_time);					
							$("#facility_table").find("tr:not(:first)").remove();
							if (response.check_extra_pre_hour_flag == 0) {
								$("#extra_hour_body").append('<tr>'+
	                             '<td class="has-success"><input disabled="" type="text" class="form-control" value="Extra Hall Pre Hour"></td>'+
	                             '<td class="has-success"><input  value="0" onkeyup="get_net_amount();" onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"  type="text" class="form-control" maxlength="3"></td>'+	                                          
	                             '<td class="has-success"><input disabled="" value="'+response.extra_hall_price+'"  type="text" class="form-control" ></td>'+	                                          
	                             '<td class="has-success"><input disabled="" value="0"  type="text" class="form-control" ></td>'+	                                          
	                             '<td class="has-success"><input disabled="" value="'+response.discount_per+'"  type="text" class="form-control" ></td>'+	                                          
	                             '<td class="has-success"><input disabled="" value="0"  type="text" class="form-control"></td>'+                                          
	                         '</tr>');
              }
              if (response.check_extra_hour_flag == 0) {
                $("#extra_hour_body").append('<tr>'+
                               '<td class="has-success"><input disabled="" type="text" class="form-control" value="Extra Hall Post Hour"></td>'+
                               '<td class="has-success"><input  value="0" onkeyup="get_net_amount();" onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"  type="text" class="form-control" maxlength="3"></td>'+                                            
                               '<td class="has-success"><input disabled="" value="'+response.extra_hall_price+'"  type="text" class="form-control" ></td>'+                                           
                               '<td class="has-success"><input disabled="" value="0"  type="text" class="form-control" ></td>'+                                           
                               '<td class="has-success"><input disabled="" value="'+response.discount_per+'"  type="text" class="form-control" ></td>'+                                           
                               '<td class="has-success"><input disabled="" value="0"  type="text" class="form-control"></td>'+                                          
                           '</tr>');
                    }
                         
							$.each(response.facility_list, function (index, item) {
                        $("#extra_hour_body").append('<tr>'+
                             '<td class="has-success"><input disabled="" type="text" class="form-control" value="'+item.facility_name+'"  ></td>'+
                             '<td class="has-success"><input  value="'+item.hour_used+'" onkeyup="get_net_amount();" onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"  type="text" class="form-control" maxlength="3"></td>'+	                                          
                             '<td class="has-success"><input disabled=""  value="'+item.facility_rate+'"  type="text" class="form-control" ></td>'+	                                          
                             '<td class="has-success"><input disabled=""  value="'+item.amount+'" type="text" class="form-control" ></td>'+	                                          
                             '<td class="has-success"><input disabled=""  value="'+item.discount_per+'"  type="text" class="form-control" ></td>'+	                                          
                             '<td class="has-success"><input disabled=""  value="'+item.net_amount+'" type="text" class="form-control"></td>'+                                          
                         '</tr>');
                         
                    }); 
                    
						$("#extra_hour_body").append('<tr>'+
                          '<td class="has-success"><input placeholder="Extra Charge" value="'+response.extra_broken_detail+'" type="text" class="form-control"  type="text" maxlength="25"></td>'+	                             	                                          
                          '<td class="has-success"><input value="NA" disabled="" value="NA"  type="text" class="form-control" ></td>'+	                                          
                          '<td class="has-success"><input disabled="" value="NA"  type="text" class="form-control" ></td>'+	                                          
                          '<td class="has-success"><input disabled="" value="NA"  type="text" class="form-control" ></td>'+	                                          
                          '<td class="has-success"><input disabled="" value="NA"   type="text" class="form-control"></td>'+
                          '<td class="has-success"><input  value="'+response.extra_broken_charge+'"  onkeyup="get_net_amount();" onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"  type="text" class="form-control"></td>'+                                          
                      '</tr>');
	            }
	            else{
	                bootbox.alert('Sorry for inconvenience. An error occurred');
	            }
	        },
	        error: function(response){
	            console.log('ECHB = ', response);
	            bootbox.alert('Sorry for inconvenience. An error occurred');
	        }
	    });
}


function get_net_amount() {
	total_amt = 0
	$("#facility_table").find('tr').each(function () {
                check_row=$(this)                               
                hrs_used = check_row.find("td:eq(1) input[type='text']").val()
               if ($.isNumeric(hrs_used)){
               	if (hrs_used != 0) {
               		rate = check_row.find("td:eq(2) input[type='text']").val() 
               		discount_rate = check_row.find("td:eq(4) input[type='text']").val()     
               		
               		amount = hrs_used * rate             
               		net_amount = amount - amount*(discount_rate/100);
               		total_amt = total_amt + net_amount
               		               	
               		check_row.find("td:eq(3) input[type='text']").val(amount)
               		check_row.find("td:eq(5) input[type='text']").val(net_amount)
             	  	}   
             	  	else {
             	  		check_row.find("td:eq(5) input[type='text']").val(0)
             	  	}            	
					 }  
					else {
						if (hrs_used == 'NA') {
							broken_extra_charge = check_row.find("td:eq(5) input[type='text']").val()  
							if (broken_extra_charge!='') {							
								total_amt = parseFloat(total_amt) + parseFloat(broken_extra_charge)
						   }
			    		}
				}
					              
     }); 	
     $("#extra_amt").val(parseFloat(total_amt).toFixed(2)); 

} 
// Update Hall Booking Deposit
$("#submit_extra").click(function(event){
	event.preventDefault();
	     var formData= new FormData();
	     
		  formData.append("booking_detail_id", $('#booking_detail_id').val());
		  
		  var facility_list  = new Array();
		  var hour_used_list = new Array();
		  var rate_list      = new Array();
		  var amount_list    = new Array();
		  var discount_list  = new Array();
		  var net_amount_list= new Array();

		  $("#facility_table").find('tr').each(function () {
		                check_row=$(this)
		                facility  = check_row.find("td:eq(0) input[type='text']").val()
		                hour_used = check_row.find("td:eq(1) input[type='text']").val()
		                rate      = check_row.find("td:eq(2) input[type='text']").val()
		                amount      = check_row.find("td:eq(3) input[type='text']").val()
		                discount  = check_row.find("td:eq(4) input[type='text']").val() 
		                net_amount  = check_row.find("td:eq(5) input[type='text']").val() 
		                
		                facility_list.push(facility)
		                hour_used_list.push(hour_used)
		                rate_list.push(rate)
		                amount_list.push(amount)
		                discount_list.push(discount)		                
		                net_amount_list.push(net_amount)		                
			});
			
		  formData.append("facility_list",facility_list);
		  formData.append("hour_used_list",hour_used_list);
		  formData.append("rate_list",rate_list);
		  formData.append("amount_list",amount_list);
		  formData.append("discount_list",discount_list);
		  formData.append("net_amount_list",net_amount_list);
		  
		  formData.append("extra_charge_details",$('#extra_charge_details').val());
		  formData.append("extra_charge",$('#extra_charge').val());

		 	 
        $.ajax({
            type: "POST",
            url: '/backofficeapp/add-extra-hour-details/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
              if(response.success=='booking_time'){
                      bootbox.alert('Booking Time should between 8:00 AM to 10:00 PM');
                      $("#add_extra_hour_modal").modal('hide');
                  setTimeout(function(){ location.reload() }, 2000);
              }
                if(response.success=='true'){
                	  $("#add_extra_hour_modal").modal('hide');
                    bootbox.alert('Extra hour details added successfully');
							setTimeout(function(){ location.reload() }, 2000);                                      
                }
                if(response.success=='not available'){
                      bootbox.alert('Slot is not available');
                      $("#add_extra_hour_modal").modal('hide');
                  setTimeout(function(){ location.reload() }, 2000);
              }
              if(response.success=='not_available'){
                      bootbox.alert('Slot is not available');
                      $("#add_extra_hour_modal").modal('hide');
                  setTimeout(function(){ location.reload() }, 2000);
              }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
           error : function(response){
                console.log("ErroSP = ",response);
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#add_extra_hour_modal").modal('hide');
            }
       });
});


function isNumberKey(evt)
   {
       var charCode = (evt.which) ? evt.which : evt.keyCode;
       if (charCode != 46 && charCode > 31 
         && (charCode < 48 || charCode > 57))
          return false;

       return true;
    }

function booking_cancel_type_val(sel)
{  
  if(sel.value == 0){
    $("#hall_shifting_div").hide();
  }
  if(sel.value == 1){
    $("#hall_shifting_div").show();
  }
  if(sel.value == 0){
    $("#hall_shifting_div1").hide();
  }
  if(sel.value == 1){
    $("#hall_shifting_div1").show();
  }
}

  $('#checkbox_checked').change(function(){
        if(this.checked)
            $('#hall_shifting_note').fadeIn('slow');
        else
            $('#hall_shifting_note').fadeOut('slow');
    });
$('#checkbox_checked1').change(function(){
        if(this.checked)
            $('#hall_shifting_note1').fadeIn('slow');
        else
            $('#hall_shifting_note1').fadeOut('slow');
    });


