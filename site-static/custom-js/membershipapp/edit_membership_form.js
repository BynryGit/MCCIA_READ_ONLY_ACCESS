
// Show Data According To User Type

$(document).ready(function(e){
    $('#multi-select-export-country, #multi-select-import-country').multiselect({
    includeSelectAllOption: true,
    selectAllValue: 'select-all-value',
    enableFiltering: true,
    enableCaseInsensitiveFiltering: true,
    maxHeight: 300

});   
radioval_val= $('input[name=radiobtn_membership_selection]:checked').val(); 
if (radioval_val == 'Individual'){
    $('#pocdiv1').css('display', 'none')
}

    if($("#check_user_type").val() == "CO"){
        $('#CEOdiv').css('display','block')
        $('#CEOContactdiv').css('display','block')
        $('#FactoryAddressdiv').css('display','block')
        $('#CompanyDetaildiv').css('display','block')
        $('#HODContactDetails').css('display','block')
        $('#comapnyemail').css('display','block')
        $('#individualemail').css('display','none')
        $('#company_name_input').css('display','block')
        $('#individual_name_input').css('display','none')
        $('input[name=legalStatus]').addClass('validateRequired')
        $('#mailreceiveconfirmboxdiv').css('display','block')
        $('#legalstatusdiv').css('display','block')
        $('#areaofexpertisedivbig').css('display','none')
        $('#turnover_for_company').css('display','block')
        $('#turnover_for_individual').css('display','none')






    }
    else{
        $('#CEOdiv').css('display','none')
        $('#CEOContactdiv').css('display','none')
        $('#FactoryAddressdiv').css('display','none')
        $('#CompanyDetaildiv').css('display','none')
        $('#HODContactDetails').css('display','none')
        $('#company_name_input').css('display','none')
        $('#individual_name_input').css('display','block')
        $('#CEO').removeClass('validateRequired')
        $('#CEOContact').removeClass('validateRequired')
        $('#FactoryAddress').removeClass('validateRequired')
        $('#FactoryPin').removeClass('validateRequired')
        $('#FactoryContact').removeClass('validateRequired')
        $('#CorrespondenceEmail').removeClass('validateRequired')
        $('input[name=legalStatus]').removeClass('validateRequired')
        $('#pocName').removeClass('validateRequired')
        $('#YearofEstablishment').removeClass('validateRequired')
        $('#pocContact').removeClass('validateRequired')
        $('#pocEmail').removeClass('validateRequired')
        $('#comapnyemail').css('display','none')
        $('#individualemail').css('display','block')
        $('#mailreceiveconfirmboxdiv').css('display','none')
        $('#legalstatusdiv').css('display','none')
        $('#areaofexpertisedivbig').css('display','block')
        $('#turnover_for_company').css('display','none')
        $('#turnover_for_individual').css('display','block')






    }

    // PAN & Aadhar
    if ($('input[name=CorrespondencePanCheck]:checked').val() == 'on'){
        $("#CorrespondencePan").removeClass('validateRequired');
        $("#CorrespondencePan-error").text('');
        $("#CorrespondencePan").val('')
        $("#CorrespondencePan").closest('div').removeClass('has-error');
        document.getElementById("CorrespondencePan").readOnly = true;
    }
    else{
        $("#CorrespondencePan").addClass('validateRequired');
        document.getElementById("CorrespondencePan").readOnly = false;
    }

    if ($('input[name=CorrespondenceAadharCheck]:checked').val() == 'on'){
        $("#CorrespondenceAadhar").removeClass('validateRequired');
        $("#CorrespondenceAadhar-error").text('');
        $("#CorrespondenceAadhar").val('')
        $("#CorrespondenceAadhar").closest('div').removeClass('has-error');
        document.getElementById("CorrespondenceAadhar").readOnly = true;
    }
    else{
        $("#CorrespondenceAadhar").addClass('validateRequired');
        document.getElementById("CorrespondenceAadhar").readOnly = false;
    }

    // Show GST or Not
    if ( $('input[name=correspondence_GST]:checked').val() == "Applicable"){
        $("#GSTField").css('display','block');
        $('#CorrespondenceGSTText').addClass('validateRequired')
    }
    else{
        $("#GSTField").css('display','none');
        $('#CorrespondenceGSTText').removeClass('validateRequired')
    }

    // Show ISO or Not
    if ($('input[name=ISOAwards]:checked').val() == "YES"){
        $('#ISOOtherStdsAwardsDiv').css('display','block')
        $('#ISOOtherStdsAwards').addClass('validateRequired')
    }
    else {
        $('#ISOOtherStdsAwardsDiv').css('display','none')
        $('#ISOOtherStdsAwards').removeClass('validateRequired')
    }

    // Get & Show Slab
    var membershipCategory = $('#MembershipCategory').val();
    var annual_turnover_foryear = $('#foryear').val();
    var annual_turnover_Rscrore=$("#Rscrore").val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-slab-admin/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
        success: function(response) {
            $("#MembershipSlab").html('');
            $("#MembershipSlab").html('<option value="">--- Select Slab ---</option>');
            $.each(response.membershipSlabObj, function (index, item) {
                data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                $("#MembershipSlab").append(data);
            });
            $("#MembershipSlab").val($("#slab_id").val());
        },
        error: function(response) {
            console.log('Edit-Member-Detail-Slab = ',response);
        },
    });
});


$('input[name=radiobtn_membership_selection]').change(function(e){
    radioval= $('input[name=radiobtn_membership_selection]:checked').val();
    $('input[name=radiobtn_membership_selection]:checked').val();
    $.ajax({
            type: 'GET',
            url: '/membershipapp/get-membership-category/?radiobtn_membership_selection='+radioval,
            success: function(response) {

                $("#MembershipCategory").html('');
                $("#MembershipCategory").html('<option value="">--- Select Category---</option>');
                $.each(response.membershipCategoryObj, function (index, item) {
                    data = '<option value="'+ item.id +'">'+item.membership_category +'</option>'
                    $("#MembershipCategory").append(data);
                });
                 $("#MembershipCategory").prop('selectedIndex',0);
            },
            error: function(response) {
                alert("Error!");
            },
        });


    // var state = $('#CorrespondenceState').val();
    // $.ajax({
    //     type: 'GET',
    //     url: '/membershipapp/get-city/?state='+state,
    //     success: function(response) {
    //         $("#CorrespondenceCity").html('');
    //         $("#CorrespondenceCity").prop("disabled", false);

    //         $.each(response.cityObj, function (index, item) {
    //             data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
    //             $("#CorrespondenceCity").append(data);
    //         });
    //          $("#CorrespondenceCity").prop('selectedIndex',0);
    //     },
    //     error: function(response) {
    //         alert("Error!");
    //     },
    // });
    // var state = $('#FactoryState').val();
    // $.ajax({
    //     type: 'GET',
    //     url: '/membershipapp/get-city/?state='+state,
    //     success: function(response) {
    //         $("#FactoryCity").html('');
    //         $("#FactoryCity").prop("disabled", false);
    //         $.each(response.cityObj, function (index, item) {
    //             data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
    //             $("#FactoryCity").append(data);
    //         });

    //         $("#FactoryCity").prop('selectedIndex',0);
    //     },
    //     error: function(response) {
    //         alert("Error!");
    //     },
    // });


    if(radioval == "Company"){
        $("#check_user_type").val('CO');
        $('#CEOdiv').css('display','block')
        $('#CEOContactdiv').css('display','block')
        $('#FactoryAddressdiv').css('display','block')
        $('#CompanyDetaildiv').css('display','block')
        $('#HODContactDetails').css('display','block')
        $('#pocdiv1').css('display', 'block')
        $('#comapnyemail').css('display','block')
        $('#individualemail').css('display','none')
        $('#company_name_input').css('display','block')
        $('#individual_name_input').css('display','none')
        $('input[name=legalStatus]').addClass('validateRequired')
        $('#mailreceiveconfirmboxdiv').css('display','block')
        $('#legalstatusdiv').css('display','block')
        $('#areaofexpertisedivbig').css('display','none')
        $('#turnover_for_company').css('display','block')
        $('#turnover_for_individual').css('display','none')





    }
    else{
        $("#check_user_type").val('IN');
        $('#CEOdiv').css('display','none')
        $('#CEOContactdiv').css('display','none')
        $('#FactoryAddressdiv').css('display','none')
        $('#CompanyDetaildiv').css('display','none')
        $('#HODContactDetails').css('display','none')
        $('#pocdiv1').css('display', 'none')
        $('#company_name_input').css('display','none')
        $('#individual_name_input').css('display','block')
        $('#poc_email_id').removeClass('validateRequired')
        $('#CEO').removeClass('validateRequired')
        $('#CEOContact').removeClass('validateRequired')
        $('#FactoryAddress').removeClass('validateRequired')
        $('#FactoryPin').removeClass('validateRequired')
        $('#FactoryContact').removeClass('validateRequired')
        $('#CorrespondenceEmail').removeClass('validateRequired')
        $('input[name=legalStatus]').removeClass('validateRequired')
        $('#comapnyemail').css('display','none')
        $('#individualemail').css('display','block')
        $('#mailreceiveconfirmboxdiv').css('display','none')
        $('#legalstatusdiv').css('display','none')
        $('#areaofexpertisedivbig').css('display','block')
        $('#turnover_for_company').css('display','none')
        $('#turnover_for_individual').css('display','block')



    }
});


// Get Slab on Category Change
$(document).on("change keyup", "#MembershipCategory, #Rscrore", function(){
    var membershipCategory = $('#MembershipCategory').val();
    var annual_turnover_foryear = $('#foryear').val();
    var annual_turnover_Rscrore=$("#Rscrore").val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-slab-admin/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
        success: function(response) {
            $("#MembershipSlab").html('');
            $("#MembershipSlab").html('<option value="">--- Select Slab ---</option>');
            $.each(response.membershipSlabObj, function (index, item) {
                data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                $("#MembershipSlab").append(data);
            });
            $("#MembershipSlab").val($("#slab_id").val());
        },
        error: function(response) {
            console.log('Edit-Member-Detail-Slab = ',response);
        },
    });
});

// Get City On State Change
$('#CorrespondenceState').change(function(e) {
    var state = $('#CorrespondenceState').val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-city/?state='+state,
        success: function(response) {
            $("#CorrespondenceCity").html('').append('<option value="">Select City </option>');
            $("#CorrespondenceCity").prop("disabled", false);

            $.each(response.cityObj, function (index, item) {
                data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
                $("#CorrespondenceCity").append(data);
            });
              var selectedText = $("#CorrespondenceState option:selected").html().trim();
            if (selectedText == 'Maharashtra'){
                $("#CorrespondenceCity option").filter(function() {
                    return $(this).text().trim() == 'Pune';
                }).prop('selected', true);
            }
            else{
                $("#CorrespondenceCity").prop('selectedIndex',0);
            }
        },
        error: function(response) {
            console.log('Edit-Member-Detail-City = ',response);
        },
    });
});

$('#FactoryState').change(function(e) {
    var state = $('#FactoryState').val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-city/?state='+state,
        success: function(response) {
            $("#FactoryCity").html('').append('<option value="">Select City </option>');
            $("#FactoryCity").prop("disabled", false);
            $.each(response.cityObj, function (index, item) {
                data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
                $("#FactoryCity").append(data);
            });

             var selectedText = $("#FactoryState option:selected").html().trim();
            if (selectedText == 'Maharashtra'){
                $("#FactoryCity option").filter(function() {
                    return $(this).text().trim() == 'Pune';
                }).prop('selected', true);
            }
            else{
                $("#FactoryCity").prop('selectedIndex',0);
            }
        },
        error: function(response) {
            console.log('Edit-Member-Detail-City = ',response);
        },
    });
});


// Make Same Address
function make_same_address() {
    if (document.getElementById('factoryAddressField').checked) {
        var state = $('#CorrespondenceState').val();
        $.ajax({
            type: 'GET',
            url: '/membershipapp/get-city/?state='+state,
            async: false,
            success: function(response) {
                $("#FactoryCity").html('');
                $("#FactoryCity").prop("disabled", false);
                $.each(response.cityObj, function (index, item) {
                    data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
                    $("#FactoryCity").append(data);
                });

                if ($("#CorrespondenceCity").val() != ''){                    
                    $("#FactoryCity").val($("#CorrespondenceCity").val());
                }                
                else{                    
                    $("#FactoryCity").prop('selectedIndex', 0);
                }
            },
            error: function(response) {
                console.log('Edit-Member-Detail-Make-Same = ',response);
            },
        });
            $("#FactoryAddress").val($("#CorrespondenceAddress").val());
            $("#FactoryState").val($("#CorrespondenceState").val());
            $("#FactoryLandline1").val($("#CorrespondenceLandline1" ).val());
            $("#FactoryPin").val($("#CorrespondencePin").val());
            $("#FactoryLandline2").val($("#CorrespondenceLandline2").val());
            $("#FactoryEmail").val($("#CorrespondenceEmail").val());
            $("#FactoryWebsite").val($("#CorrespondenceWebsite").val());
            $("#FactorySTD1").val($("#CorrespondenceStd1").val());
            $("#FactorySTD2").val($("#CorrespondenceStd2").val());            
            document.getElementById('FactoryAddress').readOnly = false;
            document.getElementById('FactoryLandline1').readOnly = true;
            document.getElementById('FactoryPin').readOnly = true;
            document.getElementById('FactoryLandline2').readOnly = true;
            document.getElementById('FactoryContact').readOnly = true;
            document.getElementById('FactoryEmail').readOnly = true;
            document.getElementById('FactorySTD1').readOnly = true;
            document.getElementById('FactorySTD2').readOnly = true;
    }
    else {
        document.getElementById('FactoryAddress').readOnly = false;
        document.getElementById('FactoryState').readOnly = false;
        document.getElementById('FactoryCity').readOnly = false;
        document.getElementById('FactoryLandline1').readOnly = false;
        document.getElementById('FactoryPin').readOnly = false;
        document.getElementById('FactoryLandline2').readOnly = false;
        document.getElementById('FactoryContact').readOnly = false;
        document.getElementById('FactoryEmail').readOnly = false;
        document.getElementById('FactoryWebsite').readOnly = false;
        document.getElementById('FactorySTD1').readOnly = false;
        document.getElementById('FactorySTD2').readOnly = false;
        $("#FactoryAddress").val("");
        $("#FactoryState").val("");
        $("#FactoryCity").val("");
        $("#FactoryLandline2").val("");
        $("#FactoryPin").val("");
        $("#FactoryLandline1").val("");
        $("#FactoryContact").val("");
        $("#FactoryEmail").val("");
        $("#FactoryWebsite").val("");
        $("#FactorySTD1").val("");
        $("#FactorySTD2").val("");
        $('#FactoryState').prop('disabled', false);
        $('#FactoryCity').prop('disabled', false);
    }
}

// ISO Change Event
$('input[name=ISOAwards]').change(function(e){
    radiovalue= $('input[name=ISOAwards]:checked').val();
    if (radiovalue == "YES"){
        $('#ISOOtherStdsAwardsDiv').css('display','block')
        $('#ISOOtherStdsAwards').addClass('validateRequired')
    }
    else {
        $('#ISOOtherStdsAwardsDiv').css('display','none')
        $('#ISOOtherStdsAwards').removeClass('validateRequired')
    }
});

// Aadhar Check & Pan Check
$('#CorrespondencePanCheck').change(function(e){
    if ($('input[name=CorrespondencePanCheck]:checked').val() == 'on'){
        $("#CorrespondencePan").removeClass('validateRequired');
        $("#CorrespondencePan-error").text('');
        $("#CorrespondencePan").val('')
        $("#CorrespondencePan").closest('div').removeClass('has-error');
        document.getElementById("CorrespondencePan").readOnly = true;
    }
    else{
        $("#CorrespondencePan").addClass('validateRequired');
        document.getElementById("CorrespondencePan").readOnly = false;
    }
});

$('#CorrespondenceAadharCheck').change(function(e){
    if ($('input[name=CorrespondenceAadharCheck]:checked').val() == 'on'){
        $("#CorrespondenceAadhar").removeClass('validateRequired');
        $("#CorrespondenceAadhar-error").text('');
        $("#CorrespondenceAadhar").val('')
        $("#CorrespondenceAadhar").closest('div').removeClass('has-error');
        document.getElementById("CorrespondenceAadhar").readOnly = true;
    }
    else{
        $("#CorrespondenceAadhar").addClass('validateRequired');
        document.getElementById("CorrespondenceAadhar").readOnly = false;
    }
});


// GST Change Event
$('input[name=correspondence_GST]').change(function(e){
    gstValue= $('input[name=correspondence_GST]:checked').val();
    if ( gstValue == "Applicable"){
        $("#GSTField").css('display','block');
        $('#CorrespondenceGSTText').addClass('validateRequired')
    }
    else{
        $("#GSTField").css('display','none');
        $('#CorrespondenceGSTText').removeClass('validateRequired')
    }
});


// Multi-Select Export & Import
$('#multi-select-export-country').change(function(e) {
    var result = $('#multi-select-export-country option:Selected').map(function(i, opt) {
      return $(opt).text();
    }).toArray().join(', ');
//    jQuery("input[name='TextExport']").val(result);
    $("#TextExport").val(result);
});

$('#multi-select-import-country').change(function(e) {
    var resultImport = $('#multi-select-import-country option:Selected').map(function(i, opt) {
      return $(opt).text();
    }).toArray().join(', ');
//    jQuery("input[name='TextImport']").val(resultImport);
    $("#TextImport").val(resultImport);
});


// Adding Cost & Manager Fields
$("#PlantMcRs, #LandBldgRs").on("keyup", function(e){
    $("#TotalRsCr").val(0);
    var amount_sum_value = parseFloat($("#PlantMcRs").val()) + parseFloat($("#LandBldgRs").val())
    $("#TotalRsCr").val(amount_sum_value.toFixed(2));
    if (isNaN($("#TotalRsCr").val())){
        $("#TotalRsCr").val(0);
    }
});

$("#Manager, #Staff, #Workers").on("keyup", function(e){
    $("#Total").val(0);
    var total_employee = parseInt($("#Manager").val()) + parseInt($("#Staff").val()) + parseInt($("#Workers").val())
    $("#Total").val(total_employee);
    if (isNaN($("#Total").val())){
        $("#Total").val(0);
    }
});


// Saving Data and going to Invoice Page
function edit_member(){
    membership_form_data_list= {}
    membership_form_data= {}
    localStorage.clear();

    formsubmit = document.getElementById('editForm')

    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false
    }
    else{
        fields = document.getElementById("membership_form").getElementsByTagName("input");
        for (var i=0; i<fields.length; i++){
            if ("MembershipCategory" == fields[i].name){
                membership_form_data_list[fields[i].name] = $( "#MembershipCategory option:selected" );
                membership_form_data["data"] = membership_form_data_list;
            }
            else{
                membership_form_data_list[fields[i].name] = fields[i].value;
                membership_form_data["data"] = membership_form_data_list;
            }
        }
        localStorage.setItem("data_obj", JSON.stringify(membership_form_data));

        $.ajax({
            type: 'POST',
            url: '/backofficeapp/update-member-detail/',
            data:  $('#membership_form').serialize(),

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Member details updated successfully.');
                    console.log('Updated');
                    location.href = '/backofficeapp/members-details/'
                }
                else{
                    alert('Sorry for inconvenience, an error occurred');
                }
              },
              error: function(response){
                alert('Sorry for inconvenience, an error occurred');
                console.log('member_invoice_E = ',response);
              }
        });
    }
}


// Go to the Error Field
$("#editForm").click(function(e){
    if ($("#check_user_type").val() == "CO"){
        if ($("form > div .has-error:visible").length > 0){
            $('html, body').animate({
                scrollTop: $("form > div .has-error:visible").first().offset().top - 150
            }, 1000);
        }
    }
    else{
        if ($("form > div .has-error:visible").length > 0){
            $('html, body').animate({
                scrollTop: $("form > div .has-error:visible").first().offset().top - 150
            }, 1000);
        }
//        else{
//            edit_member();
//        }
    }
});


// Back to Form Edit
function back_to_membership_form(){
  $("#MembershipForm").css('display','block');
  $("#MembershipFormBody").css('display','block');
  $("#MembershipInvoices").css('display','none');
  $("#MembershipInvoicesBody").css('display','none');
}


// Save Data of Form and Invoice Page
function save_member_invoice_detail(){
    var fd = new FormData();
    fd.append('subsciption_charges', $("#subscription_charges").val());
    fd.append('entrance_fee', $("#entrance_fee").val());
    fd.append('tax_amount', $("#tax_amount").val());
    fd.append('payable_amount', $("#amount_payable").val());
    payment_mode = $('input[name=payment]:checked').val();

    if (payment_mode == "Online"){
        $.ajax({
            type: 'POST',
            url: '/backofficeapp/update-member-detail/',
            data:  $('#membership_form').serialize() + "&subsciption_charges="+$("#subscription_charges").val()+ "&entrance_fee="+$("#entrance_fee").val() +"&tax_amount="+$("#tax_amount").val() +"&payable_amount="+$("#amount_payable").val()+"&paymentMode="+$("#paymentMode").val()+"&Cheque_no="+$("#Cheque_no").val()+"&cheque_date="+$("#cheque_date").val()+"&bank_name="+$("#Bank_name").val(),

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Member details updated successfully.');
                    location.href = '/backofficeapp/members-details/'
                }
                else{
                    alert('Sorry for inconvenience, an error occurred');
                }
              },
              error: function(response){
                alert('Sorry for inconvenience, an error occurred');
                console.log('member_invoice_E = ',response);
              }
        });
    }
    else {
        if($('#Cheque_no').val() == '' && $('#cheque_date').val() == '' && $('#Bank_name').val() == ''){
            $(".show-error").addClass('has-error').removeClass('has-success')
            return false
        }
        else if($('#Cheque_no').val() == ''){
            $("#Cheque_no_error").addClass('has-error').removeClass('has-success')
            return false
        }else if($('#cheque_date').val() == ''){
            $("#cheque_date_error").addClass('has-error').removeClass('has-success')
            return false
        }else if($('#Bank_name').val() == ''){
            $("#Bank_name_error").addClass('has-error').removeClass('has-success')
            return false
        }
//        else{
//            $.ajax({
//                type: 'POST',
//                url: '/backofficeapp/update-member-detail/',
//                data:  $('#membership_form').serialize() + "&subsciption_charges="+$("#subscription_charges").val()+ "&entrance_fee="+$("#entrance_fee").val() +"&tax_amount="+$("#tax_amount").val() +"&payable_amount="+$("#amount_payable").val()+"&paymentMode="+$("#paymentMode").val()+"&Cheque_no="+$("#Cheque_no").val()+"&cheque_date="+$("#cheque_date").val()+"&bank_name="+$("#Bank_name").val(),
//
//                success: function(response){
//                    if (response.success == 'true'){
//                        alert('Member details updated successfully.');
//                        location.href = '/backofficeapp/members-details/'
//                    }
//                    else{
//                        alert('Sorry for inconvenience, an error occurred');
//                    }
//                },
//                error: function(response){
//                    alert('Sorry for inconvenience, an error occurred');
//                    console.log('member_invoice_E = ',response);
//                }
//            });
//        }
    }
}


if (document.getElementById('factoryAddressField').checked){
        $('.hidefactory').css('display','block')
    }
else {
    $(document).ready(function() {
    $('.hidefactory').css('display','block')
    $('#sameasabove').click(function() {
    $("#FactoryAddress").val($("#CorrespondenceAddress").val());
    $("#FactoryPin").val($("#CorrespondencePin").val());
    $('#FactoryAddress').addClass('validateRequired')
    $('#FactoryPin').addClass('validateRequired')
    $('.hidefactory').slideToggle("fast");
});
});}

$("#areaofexperties").change(function() {
        var src = $(this).val();
        if (src == "others"){
        $('#otherareaofexpertiesdiv').css('display','block')
        }
        else{
        $('#otherareaofexpertiesdiv').css('display','none')
        }
        });


$("#IndustryDescription").change(function() {
        var src = $(this).val();
        if (src == "158"){
        $('#otherindustry_discriptiondiv').css('display','block')
        }
        else{
        $('#otherindustry_discriptiondiv').css('display','none')
        }
        });

$('#IndustryDescription').multiselect({
    includeSelectAllOption: true,
    selectAllValue: 'select-all-value',
    enableFiltering: true,
    enableCaseInsensitiveFiltering: true,
    maxHeight: 300
});


$('#IndustryDescription').change(function() {
var resultIndustryDescription = $('#IndustryDescription option:Selected').map(function(i, opt) {
  return $(opt).text();
}).toArray().join(', ');
$("#TextIndustryDescription").val(resultIndustryDescription);
});
