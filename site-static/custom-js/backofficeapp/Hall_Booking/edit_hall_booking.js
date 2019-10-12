

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


// Delete Single Slot Booking
function deleteRow(id, row){
    var delete_div = $(row).closest("div .check_class");
    var check_length = $(row).closest("tbody");

    if ($(document).find("table > tbody > tr").length == 1){
        bootbox.confirm({
            message: "Do you want to cancel your booking ?",
            buttons: {
                confirm: {label: 'Yes', className: 'btn-success'},
                cancel: {label: 'No', className: 'btn-danger'}
            },
            callback: function (result) {
                if (!result){
                    return;
                }
                else{
                    delete_booking_ajax(id, row, check_length, delete_div);
                    reject_booking();
                    window.location = '/backofficeapp/hall-booking-registration/';
                }
            }
        });
    }
    else{
        delete_booking_ajax(id, row, check_length, delete_div);
    }
}

function delete_booking_ajax(id, row, check_length, delete_div){
    $.ajax({
        type: 'POST',
        url: '/hallbookingapp/remove-hall-booking/',
        data: {'booking_id': id},
        success: function (response) {
            if (response.success == 'true') {
                $(row).closest("tr").remove();
                if (check_length.children().length == 0){
                    delete_div.remove();
                }
                $('#total_rent').text(response.total_rent);
                $('#gst_amount').text(response.gst_amount);
                $('#total_payable').text(response.total_payable);
            }
            else{
                return;
            }
        },
        error: function (response) {
            console.log('DRHB = ',response);
            alert("Error!");
        }
    });
}


// Reject Hall Booking
function reject_booking(){
    var booking_id = $("#booking_id").val();
    $.ajax({
        type: "POST",
        url: "/backofficeapp/reject-booking/",
        data: {'booking_id': booking_id},

        success: function(response){
            if (response.success == 'true'){
                bootbox.alert('Booking is Rejected');
                setTimeout(function(){
                    window.location.href = "/backofficeapp/hall-booking-registration/"}, 1000);
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


// Accept Hall Booking
function accept_booking(){
    var booking_id = $("#booking_id").val();
    $.ajax({
        type: "POST",
        url: "/backofficeapp/accept-booking/",
        data: {'booking_id': booking_id},

        success: function(response){
            if (response.success == 'true'){
                bootbox.alert('Booking is Accepted');
                setTimeout(function(){
                    window.location.href = "/backofficeapp/hall-booking-registration/"}, 1000);
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


function isNumberKey(evt)
   {
       var charCode = (evt.which) ? evt.which : evt.keyCode;
       if (charCode != 46 && charCode > 31 
         && (charCode < 48 || charCode > 57))
          return false;

       return true;
    }


