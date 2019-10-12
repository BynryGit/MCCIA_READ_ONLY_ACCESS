$(document).ready(function() {


            $(document).off('click', '#btnSubmit').on('click', '#btnSubmit', function(e) {
                e.preventDefault();

            $.ajax({
                type: "POST",
                url : '/paymentapp/get-payment-detail/',
                data : {
                'user_id':1
                },
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
               error : function(response){
                    alert("_Error");
                }
            });
            });



});
 function handleResponse(res) {
                console.log(res);
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
                console.log(formData);
                $.ajax({
                type: "POST",
                url : '/paymentapp/common-response-save/',
                data : formData,
                processData: false,
                contentType: false,
                success: function (response) {
                if (response.success == "true") {

                }
                },
                error : function(response){
                    alert("_Error");
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