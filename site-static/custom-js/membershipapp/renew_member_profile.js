
$(document).ready(function(){
    $("#renew_turnover_year").prop('selectedIndex', 1).change();

    // Get & Show Slab
    var membershipCategory = $('#renew_membership_category').val();
    var annual_turnover_foryear = $('#renew_turnover_year').val();
    var annual_turnover_Rscrore=$("#turnover_amount").val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-slab/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
        success: function(response) {
            $("#renew_membership_slab").html('');
            $("#renew_membership_slab").html('<option value="">Select Slab</option>');
            $.each(response.membershipSlabObj, function (index, item) {
                data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                $("#renew_membership_slab").append(data);
            });
            $("#renew_membership_slab").val($("#slab_id").val()).change();
        },
        error: function(response) {
            console.log('Renew-Member-Detail-Slab = ',response);
        },
    });
});


// Get Slab on Category Change or other event
$(document).on("change keyup", "#renew_membership_category, #turnover_amount", function(){
    var membershipCategory = $('#renew_membership_category').val();
    var annual_turnover_foryear = $('#renew_turnover_year').val();
    var annual_turnover_Rscrore=$("#turnover_amount").val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-slab/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
        success: function(response) {
            $("#renew_membership_slab").html('');
            $("#renew_membership_slab").html('<option value="">Select Slab</option>');
            $.each(response.membershipSlabObj, function (index, item) {
                data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                $("#renew_membership_slab").append(data);
            });
        },
        error: function(response) {
            console.log('Renew-Member-Detail-Slab = ',response);
        },
    });
});


// Validate Renew Year & Turnover Amount
function check_year(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if ((charCode >= 48 && charCode <= 57) || charCode == 45){
        $("#renewal_year_error").css("display", "none");
        return true;
    }
    else{
        $("#renewal_year_error").css("display", "block");
        return false;
    }
}

function check_amount(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if ((charCode >= 48 && charCode <= 57) || charCode == 46){
        $("#turnover_amount_error").css("display", "none");
        return true;
    }
    else{
        $("#turnover_amount_error").css("display", "block");
        return false;
    }
}

// Submit Button Click
$("#renew_submit_btn").click(function(e){
    var check_flag = true;

    if ($("#renew_membership_category").val() != ''){
        $("#renew_membership_category_error").css("display", "none");
    }
    else{
        check_flag = false;
        $("#renew_membership_category_error").css("display", "block");
    }

    if ($("#renew_turnover_year").val() != ''){
        $("#renew_turnover_year_error").css("display", "none");
    }
    else{
        check_flag = false;
        $("#renew_turnover_year_error").css("display", "block") ;
    }

    if ($("#renew_membership_slab").val() != ''){
        $("#renew_membership_slab_error").css("display", "none");
    }
    else{
        check_flag = false;
        $("#renew_membership_slab_error").css("display", "block");
    }

    var year_pattern = /^[0-9]{4}\-[0-9]{4}$/;
    var amount_pattern = /^[0-9]+(\.[0-9]{1,2})?$/;
    if ($("#renewal_year").val() != '' && year_pattern.test($("#renewal_year").val())){
        $("#renewal_year_error").css("display", "none");
    }
    else{
        $("#renewal_year_error").css("display", "block");
        check_flag = false;
    }

    if ($("#turnover_amount").val() != '' && amount_pattern.test($("#turnover_amount").val())){
        $("#turnover_amount_error").css("display", "none");
    }
    else{
        $("#turnover_amount_error").css("display", "block");
        check_flag = false;
    }

    if (check_flag != false){
        $.ajax({
            type: "POST",
            url: '/membershipapp/get-renew-invoice/',
            data: {'category_id': $("#renew_membership_category").val(),
                    'slab_id': $("#renew_membership_slab").val(),
                    'renewal_year': $("#renewal_year").val(),
                    'user_detail_id': $("#member_id").val(),
                    'turnover_value': $("input[name='turnover_range']:checked").val(),
                    'employee_value': $("input[name='employee_range']:checked").val()
                    },
            success: function(response){
                if (response.success == 'true'){
                    $("#renew_form_div").hide();
                    $("#renew_member_invoice_div").show();
                    $("#membership_category").val(response.category);
                    $("#slab_category").val(response.slab);
                    $("#membership_renew_year").val(response.renewal_year);
                    $("#subscription_charges").val(response.subscription_charge);
                    $("#tax_amount").val(response.gst_amount);
                    $("#due_amount").val(response.due_amount);
                    $("#advance_amount").val(response.advance_amount);
                    $("#amount_payable").val(response.amount_payable);
                    $("#turnover_value").val(response.turnover_value);
                    $("#employee_value").val(response.employee_value);
                }
            },
            error: function(response){
                alert('We are sorry for inconvenience. An error occurred.');
            }
        });
    }
});


// Renew Invoice Page Back Button
$("#back_btn").click(function(e){
    $("#renew_form_div").show();
    $("#renew_member_invoice_div").hide();
});


// Submit button of Invoice Page - Send Payment Data
$("#renew_invoice_submit_btn").click(function(e){

    var formData= new FormData();

    formData.append("membership_category", $("#renew_membership_category").val());
    formData.append("slab_category", $("#renew_membership_slab").val());
    formData.append("membership_renew_year", $('#membership_renew_year').val());
    formData.append("subscription_charges", $('#subscription_charges').val());
    formData.append("tax_amount", $('#tax_amount').val());
    formData.append("due_amount", $('#due_amount').val());
    formData.append("advance_amount", $('#advance_amount').val());
    formData.append("amount_payable", $('#amount_payable').val());
    formData.append("member_id", $("#member_id").val());
    formData.append("annual_to_year", $("#renew_turnover_year").val());
    formData.append("annual_to", $("#turnover_amount").val());

    $.ajax({
        type: "POST",
        url: '/membershipapp/renew-member-request/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response){
            if (response.success == 'true'){
                response.configJson.consumerData.responseHandler = handleResponse
                $.pnCheckout(response.configJson);
                if(response.configJson.features.enableNewWindowFlow){
                    pnCheckoutShared.openNewWindow();
                }
            }

//            if (response.success == 'true'){
//                alert('Renewal details saved successfully.');
//                location.href = '/';
//            }

            else{
                alert('We are sorry for inconvenience. An error occurred.');
//                location.href = '/';
            }
        },
        error: function(response){
            console.log('ERRORSRMI = ', response)
        }
    });
});


// Save Payment Response
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
//    formData.append("transactionState",res.transactionState);
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

    formData.append("membership_category", $("#renew_membership_category").val());
    formData.append("slab_category", $("#renew_membership_slab").val());
    formData.append("membership_renew_year", $('#membership_renew_year').val());
    formData.append("subscription_charges", $('#subscription_charges').val());
    formData.append("tax_amount", $('#tax_amount').val());
    formData.append("due_amount", $('#due_amount').val());
    formData.append("advance_amount", $('#advance_amount').val());
    formData.append("amount_payable", $('#amount_payable').val());
    formData.append("member_id", $("#member_id").val());
    formData.append("annual_to_year", $("#renew_turnover_year").val());
    formData.append("annual_to", $("#turnover_amount").val());
    formData.append("turnover_value", $("#turnover_value").val());
    formData.append("employee_value", $("#employee_value").val());

    $.ajax({
        type: "POST",
        url : '/membershipapp/renew-membership-response-save/',
        data : formData,
        processData: false,
        contentType: false,

        success: function (response) {
            if (response.success == "true") {
                bootbox.alert('Renewal done successfully. In case of any queries, please contact Membership Team on 25709161 / 25709162');
                setTimeout(function(e){
                    window.location.href = "/";}, 1000);
            }
            else if (response.success == 'initiated'){
                bootbox.alert('Transaction has initiated. Renewal details saved successfully. In case of any queries, please contact Membership Team on 25709161 / 25709162');
                setTimeout(function(){
                    window.location.href = "/"}, 1000);
            }
            else if (response.success == 'failed' || response.success == 'cancelled'){
                $("#payment_id").val(response.payment_id);
                bootbox.alert('Transaction failed.');
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
};