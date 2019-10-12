
$("#submit_btn").click(function(e){
    $.ajax({
        type: "POST",
        url : '/paymentapp/get-payment-detail/',

        success: function (response) {
            console.log('res = ', response);
            if (response.success == "true") {
                response.configJson.consumerData.responseHandler = handleResponse
                $.pnCheckout(response.configJson);
                if(response.configJson.features.enableNewWindowFlow){
                    pnCheckoutShared.openNewWindow();
                }
            }
        },
        error : function(response){
            alert("_Error");
        }
    });
});


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

    $.ajax({
        type: "POST",
        url : '/paymentapp/common-response-save/',
        data : formData,
        processData: false,
        contentType: false,

        success: function (response) {
            if (response.success == "true") {
                bootbox.alert('Transaction has completed successfully. Booking saved successfully.');
            }
            else if (response.success == 'initiated'){
                bootbox.alert('Transaction has initiated. Booking saved successfully.');
            }
            else if (response.success == 'failed' || response.success == 'cancelled'){
                bootbox.alert('Transaction Failed/Cancelled.');
            }
            else{
                bootbox.alert('Sorry for inconvenience. An error occurred. Please try again.');
            }
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