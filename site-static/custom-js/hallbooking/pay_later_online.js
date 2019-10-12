function payment_online(){
    var booking_id = $("#booking_id").val();
    var tds_amount = $("#tds_amount_hall").val();

    retain_sd_flag = $("#retain_sd").prop("checked")
    cheque_flag = $("#through_cheque").prop("checked")
        $.ajax({
            type: "POST",
            url : '/paymentapp/pay-online-later-through-mail/',
            data : {'booking_id': booking_id,'retain_sd_flag':retain_sd_flag,'cheque_flag':cheque_flag,'tds_amount': tds_amount},

            success: function (response) {
                if (response.success == "true") {
                  console.log(response)
                  response.configJson.consumerData.responseHandler = handleResponse
                  $.pnCheckout(response.configJson);
                  if(response.configJson.features.enableNewWindowFlow){
                        pnCheckoutShared.openNewWindow();

                    }
                }
            },
//            beforeSend: function () {
//                $("#processing").css('display','block');
//            },
//            complete: function () {
//                $("#processing").css('display','none');
//            },
            error : function(response){
            console.log(response)
                alert("sorry for inconvience");
            }
        });
    }

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
    formData.append("tds_amount_hall",$("#tds_amount_hall").val());



    $.ajax({
        type: "POST",
        url : '/paymentapp/pay-later-payment-response-save/',
        data : formData,
        processData: false,
        contentType: false,

        success: function (response) {
            if (response.success == "true") {
                setTimeout(function(){
                    window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                bootbox.dialog  ({
                    size: 'small',
                    message: '<div class="text-center">Transaction has completed successfully.</div><br>'+
                             '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Redirecting...</div>',
                    closeButton: false
                });
            }
            else if (response.success == 'initiated'){
                setTimeout(function(){
                      window.location.href = "/hallbookingapp/open-hallbooking-page/"});
                bootbox.dialog  ({
                    size: 'small',
                    message: '<div class="text-center">Transaction has initiated.</div><br>'+
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
};
