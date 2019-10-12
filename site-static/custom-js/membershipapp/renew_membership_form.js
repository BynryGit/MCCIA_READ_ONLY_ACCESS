
$(document).ready(function(){
    $("#renew_turnover_year").prop('selectedIndex', 1).change();
    $("#member_anchor").addClass("tab-active");
    $("#member_nav").addClass("active");
    $("#member_icon").addClass("icon-active");
    $("#member_active").css("display","block");
    $("#member_nav").addClass("active");

    // Get & Show Slab
    var membershipCategory = $('#renew_membership_category').val();
    var annual_turnover_foryear = $('#renew_turnover_year').val();
    var annual_turnover_Rscrore=$("#turnover_amount").val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-slab-admin/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
        success: function(response) {
            $("#renew_membership_slab").html('');
            $("#renew_membership_slab").html('<option value="">Select Slab</option>');
            $.each(response.membershipSlabObj, function (index, item) {
                data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                $("#renew_membership_slab").append(data);
            });
            $("#renew_membership_slab").val($("#slab_id").val()).change();
        },
        beforeSend: function () {
            $("#processing").show();
        },
        complete: function () {
            $("#processing").hide();
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
        url: '/membershipapp/get-slab-admin/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
        success: function(response) {
            $("#renew_membership_slab").html('');
            $("#renew_membership_slab").html('<option value="">Select Slab</option>');
            $.each(response.membershipSlabObj, function (index, item) {
                data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                $("#renew_membership_slab").append(data);
            });
        },
        beforeSend: function () {
            $("#processing").show();
        },
        complete: function () {
            $("#processing").hide();
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
$("#renew_submit_btn").click(function(){
    var flag = true;

    if ($("#renew_membership_category").val() != ''){
        $("#renew_membership_category_error").css("display", "none");
    }
    else{
        flag = false;
        $("#renew_membership_category_error").css("display", "block");
    }

    if ($("#renew_turnover_year").val() != ''){
        $("#renew_turnover_year_error").css("display", "none");
    }
    else{
        flag = false;
        $("#renew_turnover_year_error").css("display", "block") ;
    }

    if ($("#renew_membership_slab").val() != ''){
        $("#renew_membership_slab_error").css("display", "none");
    }
    else{
        flag = false;
        $("#renew_membership_slab_error").css("display", "block");
    }

    var year_pattern = /^[0-9]{4}\-[0-9]{4}$/;
    var amount_pattern = /^[0-9]+(\.[0-9]{1,2})?$/;
    if ($("#renewal_year").val() != '' && year_pattern.test($("#renewal_year").val())){
        $("#renewal_year_error").css("display", "none");
    }
    else{
        $("#renewal_year_error").css("display", "block");
        flag = false;
    }

    if ($("#turnover_amount").val() != '' && amount_pattern.test($("#turnover_amount").val())){
        $("#turnover_amount_error").css("display", "none");
    }
    else{
        $("#turnover_amount_error").css("display", "block");
        flag = false;
    }

    if (flag != false){
        $.ajax({
            type: "POST",
            url: '/backofficeapp/get-member-renew-invoice/',
            data: {'category_id': $("#renew_membership_category").val(),
                    'slab_id': $("#renew_membership_slab").val(),
                    'renewal_year': $("#renewal_year").val(),
                    'user_detail_id': $("#member_id").val()},
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
                }
            },
            beforeSend: function () {
                $("#processing").show();
            },
            complete: function () {
                $("#processing").hide();
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


function CalculateTotal(){
    subscription_charges = $("#subscription_charges").val()
    tax_amount = $("#tax_amount").val()
    due_amount = $("#due_amount").val()
    advance_amount = $("#advance_amount").val()
    var amount_payable = (parseFloat(subscription_charges) + parseFloat(tax_amount) + parseFloat(due_amount)) - advance_amount

    $("#amount_payable").val(amount_payable)
}

// Submit button of Invoice Page
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
        url: '/backofficeapp/renew-member/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response){
            if (response.success == 'true'){
                alert('Renewal details saved successfully.');
                location.href = '/backofficeapp/members-details/';
            }
            else{
                alert('We are sorry for inconvenience. An error occurred.');
                location.href = '/backofficeapp/members-details/';
            }
        },
        beforeSend: function () {
            $("#processing").show();
        },
        complete: function () {
            $("#processing").hide();
        },
        error: function(response){
            console.log('ERRORSRMI = ', response)
        }
    });
});