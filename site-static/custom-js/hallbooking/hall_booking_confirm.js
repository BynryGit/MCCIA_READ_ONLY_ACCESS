
$(document).keydown(function(e) {
    if (e.keyCode == 27) return false;
});

function confirmterms(){
    $('#online_payment_model').modal('hide');
    $('#static').modal({
        show: 'true'
    }); 
}

function check_all_terms() {
    document.getElementById('accept_term').disabled = true;
    if ($('input[name=terms1]:checked').val() == 'on'){
        if ($('input[name=terms2]:checked').val() == 'on'){
            if ($('input[name=terms3]:checked').val() == 'on'){
                if ($('input[name=terms4]:checked').val() == 'on'){
                    if ($('input[name=terms5]:checked').val() == 'on'){
                        document.getElementById('accept_term').disabled = false; 
                    }
                }
            }
        }
    }
}

function through_cheque() {
    if($("#through_cheque").prop("checked") == true){
        $("#deposit").text(0);
        total_payable = $("#total_payable").text();
        hiddden_deposit_amt = $("#hiddden_deposit_amt").val();
        final_total_payable = parseFloat(total_payable) - parseFloat(hiddden_deposit_amt)
        $("#total_payable").text(final_total_payable);
    }
    else {
        $("#deposit").text($("#hiddden_deposit_amt").val());
        total_payable = $("#total_payable").text();
        hiddden_deposit_amt = $("#hiddden_deposit_amt").val();
        final_total_payable = parseFloat(total_payable) + parseFloat(hiddden_deposit_amt)
        $("#total_payable").text(final_total_payable);      
    }
}

// Browser Back Click Code
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
                cancel_booking();
                location.href = '/hallbookingapp/open-hallbooking-page/';
            }
            else{
                history.go(1);
            }
        }
    });
};

// Save Hall Booking
function save_booking(){
    var start_time = Date.parse('10:00 AM');
    var end_time = Date.parse('04:00 PM');
    var today_date = new Date();    
        
    var booking_id = $("#booking_id").val();
    retain_sd_flag = $("#retain_sd").prop("checked")
    cheque_flag = $("#through_cheque").prop("checked")

    if ($('[name="payment"]:checked').val() == 'online'){
        $.ajax({
            type: "POST",
            url : '/paymentapp/get-hall-payment-detail/',
            data : {'booking_id': booking_id,'retain_sd_flag':retain_sd_flag,'cheque_flag':cheque_flag},

            success: function (response) {
                if (response.success == "true") {
                    response.configJson.consumerData.responseHandler = handleResponse
                    $.pnCheckout(response.configJson);
                    if(response.configJson.features.enableNewWindowFlow){
                        pnCheckoutShared.openNewWindow();
                    }
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
    else{
        $.ajax({
            type: "POST",
            url : '/hallbookingapp/save-offline-booking/',
            data : {'booking_id': booking_id,'retain_sd_flag':retain_sd_flag,'cheque_flag':cheque_flag},

            success: function (response) {
                if (response.success == "true") {
                    setTimeout(function(){

                        window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                    bootbox.dialog  ({
                        size: 'small',
                        message: '<div class="text-center">Booking Saved Successfully.</div><br>'+
                                 '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                        closeButton: false
                    });
                }
                else{
                    setTimeout(function(){
                        window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                    bootbox.dialog  ({
                        size: 'small',
                        message: '<div class="text-center">Sorry for inconvenience. An error occurred.</div><br>'+
                                 '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                        closeButton: false
                    });
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
            error : function(response){
                console.log('SHBE = ', response);
                setTimeout(function(){
                    window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                bootbox.dialog({
                    size: 'small',
                    message: '<div class="text-center">Sorry for inconvenience. An error occurred.</div><br>'+
                             '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                    closeButton: false
                });
            }
        });
    }
}


// Get Payment Response & Save it
function handleResponse(res) {
    var formData = new FormData();

    paymenttrasactionobj=res.paymentMethod.paymentTransaction

    formData.append("error",res.error);
    formData.append("merchantAdditionalDetails",res.merchantAdditionalDetails);
    formData.append("merchantTransactionIdentifier",res.merchantTransactionIdentifier);
    formData.append("merchantTransactionRequestType",res.merchantTransactionRequestType);
    formData.append("responseType",res.responseType);
    formData.append("transactionState",res.transactionState);
    formData.append("stringResponse",res.stringResponse);
    //                formData.append("transactionState",res.transactionState);

    formData.append("accountNo",paymenttrasactionobj.accountNo);
    formData.append("amount",paymenttrasactionobj.amount);
    formData.append("balanceAmount",paymenttrasactionobj.balanceAmount);
    formData.append("bankReferenceIdentifier",paymenttrasactionobj.bankReferenceIdentifier);
    formData.append("dateTime",paymenttrasactionobj.dateTime);
    formData.append("errorMessage",paymenttrasactionobj.errorMessage);
    formData.append("identifier",paymenttrasactionobj.identifier);
    formData.append("reference",paymenttrasactionobj.reference);
    formData.append("refundIdentifier",paymenttrasactionobj.refundIdentifier);
    formData.append("statusCode",paymenttrasactionobj.statusCode);
    formData.append("statusMessage",paymenttrasactionobj.statusMessage);

    formData.append("booking_id",$("#booking_id").val());

    $.ajax({
        type: "POST",
        url : '/paymentapp/hall-response-save/',
        data : formData,
        processData: false,
        contentType: false,

        success: function (response) {
            if (response.success == "true") {
                setTimeout(function(){
                    window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                bootbox.dialog  ({
                    size: 'small',
                    message: '<div class="text-center">Transaction has completed successfully. Booking saved successfully.</div><br>'+
                             '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                    closeButton: false
                });
            }
            else if (response.success == 'initiated'){
                setTimeout(function(){
                    window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                bootbox.dialog  ({
                    size: 'small',
                    message: '<div class="text-center">Transaction has initiated. Booking saved successfully.</div><br>'+
                             '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                    closeButton: false

                });                            
            }
            else if (response.success == 'failed' || response.success == 'cancelled'){
                return false;
            }
            else{
                bootbox.alert('Sorry for inconvenience. An error occurred. Please try again.');
            }
        },
        beforeSend: function () {
            $("#processing").css('display','block');
        },
        complete: function () {
            $("#processing").css('display','none');
        },
        error : function(response){
            console.log(response);
            bootbox.alert('Sorry for inconvenience. An error occurred. Please try again.');
        }
    });


//                if (typeof res != 'undefined' && typeof res.paymentMethod != 'undefined' && typeof res.paymentMethod.paymentTransaction != 'undefined' && typeof res.paymentMethod.paymentTransaction.statusCode != 'undefined' && res.paymentMethod.paymentTransaction.statusCode == '0300') {
//                    console.log(res)
//                    // success block
//                } else if (typeof res != 'undefined' && typeof res.paymentMethod != 'undefined' && typeof res.paymentMethod.paymentTransaction != 'undefined' && typeof res.paymentMethod.paymentTransaction.statusCode != 'undefined' && res.paymentMethod.paymentTransaction.statusCode == '0398') {
//
//                    // initiated block
//                } else {
//                    // error block
//                }
};
//code for PG end


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
                    cancel_booking();
                    window.location = '/hallbookingapp/open-hallbooking-page/';
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
        beforeSend: function () {
            $("#processing").css('display','block');
        },
        complete: function () {
            $("#processing").css('display','none');
        },
        error: function (response) {
            console.log('DRHB = ',response);
            alert("Error!");
        }
    });
}


// Cancel Hall Booking
function cancel_booking(){
    var booking_id = $("#booking_id").val();
    $.ajax({
        type: "POST",
        url: "/hallbookingapp/cancel-booking/",
        data: {'booking_id': booking_id},

        success: function(response){
            if (response.success == 'true'){
                setTimeout(function(){
                    window.location.href = "/hallbookingapp/open-hallbooking-page/"}, 500);
                bootbox.dialog  ({
                    size: 'small',
                    message: '<div class="text-center">Your Booking is cancelled.</div><br>'+
                             '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                    closeButton: false

                });                
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


