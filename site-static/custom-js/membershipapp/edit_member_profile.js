
// Show Data According To User Type

$(document).ready(function(e){
    $('#multi-select-export-country, #multi-select-import-country,#IndustryDescription').multiselect({
    includeSelectAllOption: true,
    selectAllValue: 'select-all-value',
    enableFiltering: true,
    enableCaseInsensitiveFiltering: true,
    maxHeight: 300
});

    if($("#check_user_type").val() == "CO"){
        $('#CEOdiv').css('display','block')
        $('#CEOContactdiv').css('display','block')
        $('#FactoryAddressdiv').css('display','block')
        $('#CompanyDetaildiv').css('display','block')
        $('#HODContactDetails').css('display','block')
        $('#CEO').addClass('validateRequired')
        $('#CEOContact').addClass('validateRequired')
        $('#comapnyemail').css('display','block')
        $('#individualemail').css('display','none')
        $('#poc_div').css('display','block')
        $('#company_name_input').css('display','block')
        $('#individual_name_input').css('display','none')
        $('#mailreceiveconfirmboxdiv').css('display','block')
        $('#YearofEstablishmentdiv').css('display','block')
        $('#areaofexpertisedivbig').css('display','none')

//        $('#FactoryAddress').addClass('validateRequired')
//        $('#FactoryPin').addClass('validateRequired')
//        $('#FactoryContact').addClass('validateRequired')
//        $('#CorrespondenceEmail').addClass('validateRequired')
        $('input[name=legalStatus]').addClass('validateRequired')
        $('#pocName').addClass('validateRequired')
        $('#YearofEstablishment').addClass('validateRequired')
        $('#pocContact').addClass('validateRequired')
        $('#POCEmail').addClass('validateRequired')
        $('#CEOEmail').addClass('validateRequired')
        $('#CEOEmailin').removeClass('validateRequired')
        $('#FinanceName').addClass('validateRequired')
        $('#FinanceContact').addClass('validateRequired')
        $('#FinanceEmail').addClass('validateRequired')

    }
    else{
        $('#CEOdiv').css('display','none')
        $('#CEOContactdiv').css('display','none')
        $('#FactoryAddressdiv').css('display','none')
        $('#CompanyDetaildiv').css('display','none')
        $('#HODContactDetails').css('display','none')
        $('#comapnyemail').css('display','none')
        $('#individualemail').css('display','block')
        $('#YearofEstablishmentdiv').css('display','none')
        $('#CEO').removeClass('validateRequired')
        $('#CEOContact').removeClass('validateRequired')
        $('#poc_div').css('display','none')
        $('#company_name_input').css('display','none')
        $('#individual_name_input').css('display','block')
        $('#mailreceiveconfirmboxdiv').css('display','none')
        $('#areaofexpertisedivbig').css('display','block')


//        $('#FactoryAddress').removeClass('validateRequired')
//        $('#FactoryPin').removeClass('validateRequired')
//        $('#FactoryContact').removeClass('validateRequired')
//        $('#CorrespondenceEmail').removeClass('validateRequired')
        $('input[name=legalStatus]').removeClass('validateRequired')
        $('#pocName').removeClass('validateRequired')
        $('#YearofEstablishment').removeClass('validateRequired')
        $('#pocContact').removeClass('validateRequired')
        $('#POCEmail').removeClass('validateRequired')
        $('#DescriptionofBusiness').addClass('validateRequired')
        $('#CEOEmailin').addClass('validateRequired')
        $('#CEOEmail').removeClass('validateRequired')
        $('#FinanceName').removeClass('validateRequired')
        $('#FinanceContact').removeClass('validateRequired')
        $('#FinanceEmail').removeClass('validateRequired')
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
            success: function(response) {
                $("#FactoryCity").html('');
                $("#FactoryCity").prop("disabled", false);
                $.each(response.cityObj, function (index, item) {
                    data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
                    $("#FactoryCity").append(data);
                });

                if ($("#CorrespondenceCity").val() != ''){  
                    console.log('f')                  ;
                    $("#FactoryCity").val($("#CorrespondenceCity").val());
                }                
                else{                    
                    console.log('n');
                    $("#FactoryCity").prop('selectedIndex', 0);
                }
            },
            error: function(response) {
                console.log('Edit-Member-Detail-Make-Same = ',response);
            },
        });
//            $("#FactoryAddress").val($("#CorrespondenceAddress").val());
            $("#FactoryState").val($("#CorrespondenceState").val());
//            $("#FactoryLandline1").val($("#CorrespondenceLandline1" ).val());
//            $("#FactoryPin").val($("#CorrespondencePin").val());
//            $("#FactoryContact").val($("#CorrespondenceContact").val());
//            $("#FactoryLandline2").val($("#CorrespondenceLandline2").val());
//            $("#FactoryEmail").val($("#CorrespondenceEmail").val());
//            $("#FactoryWebsite").val($("#CorrespondenceWebsite").val());
//            $("#FactorySTD1").val($("#CorrespondenceStd1").val());
//            $("#FactorySTD2").val($("#CorrespondenceStd2").val());
            document.getElementById('FactoryAddress').readOnly = false;
//            document.getElementById('FactoryLandline1').readOnly = false;
            document.getElementById('FactoryPin').readOnly = false;
//            document.getElementById('FactoryLandline2').readOnly = true;
//            document.getElementById('FactoryContact').readOnly = true;
//            document.getElementById('FactoryEmail').readOnly = true;
//            document.getElementById('FactorySTD1').readOnly = true;
//            document.getElementById('FactorySTD2').readOnly = true;
    }
    else {
        document.getElementById('FactoryAddress').readOnly = false;
        document.getElementById('FactoryState').readOnly = false;
        document.getElementById('FactoryCity').readOnly = false;
//        document.getElementById('FactoryLandline1').readOnly = false;
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
        $("#ISOOtherStdsAwards-error").text('');
        $("#ISOOtherStdsAwardsDiv").removeClass('has-error has-success')
        $('#ISOOtherStdsAwards').removeClass('validateRequired has-success has-error')
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
function edit_front_end_member(){
    membership_form_data_list= {}
    membership_form_data= {}
    localStorage.clear();

    formsubmit = document.getElementById('edit_member_profile')

    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false
    }
    else{
        fields = document.getElementById("front_end_edit_form").getElementsByTagName("input");
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
            url: '/membershipapp/update-member-profile/',
            data:  $('#front_end_edit_form').serialize(),

            success: function(response){
                if (response.success == 'true'){
                    alert('Details updated successfully.');
                    location.href = '/'
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


$("#edit_member_profile").click(function(e){
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
        else{
            edit_front_end_member();
        }
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
            data:  $('#front_end_edit_form').serialize() + "&subsciption_charges="+$("#subscription_charges").val()+ "&entrance_fee="+$("#entrance_fee").val() +"&tax_amount="+$("#tax_amount").val() +"&payable_amount="+$("#amount_payable").val()+"&paymentMode="+$("#paymentMode").val()+"&Cheque_no="+$("#Cheque_no").val()+"&cheque_date="+$("#cheque_date").val()+"&bank_name="+$("#Bank_name").val(),

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
        else{
            $.ajax({
                type: 'POST',
                url: '/backofficeapp/update-member-detail/',
                data:  $('#front_end_edit_form').serialize() + "&subsciption_charges="+$("#subscription_charges").val()+ "&entrance_fee="+$("#entrance_fee").val() +"&tax_amount="+$("#tax_amount").val() +"&payable_amount="+$("#amount_payable").val()+"&paymentMode="+$("#paymentMode").val()+"&Cheque_no="+$("#Cheque_no").val()+"&cheque_date="+$("#cheque_date").val()+"&bank_name="+$("#Bank_name").val(),

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


$('#IndustryDescription').change(function() {
var resultIndustryDescription = $('#IndustryDescription option:Selected').map(function(i, opt) {
  return $(opt).text();
}).toArray().join(', ');
$("#TextIndustryDescription").val(resultIndustryDescription);
});





