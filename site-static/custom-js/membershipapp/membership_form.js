

$(document).ready(function(){
var show_data = localStorage.getItem("data_obj");
showDataList = JSON.parse(show_data);
var pathname = window.location.pathname; // Returns path only
location_url_ID= pathname.split('/')[2]

$('#multi-select-export-country, #multi-select-import-country, #IndustryDescription').multiselect({
    includeSelectAllOption: true,
    selectAllValue: 'select-all-value',
    enableFiltering: true,
    enableCaseInsensitiveFiltering: true,
    maxHeight: 300,
    itemsShowLimit: 1,
});

$("#membership_selection").val($('input[name=radiobtn_membership_selection]:checked').val())


radioval= $('input[name=radiobtn_membership_selection]:checked').val();
if(radioval == "Company"){

    $('#CEOdiv').css('display','block')
    $('#CEOContactdiv').css('display','block')
    $('#individual_text').css('display','none')
    $('#FactoryAddressdiv').css('display','block')
    $('#comapnyemail').css('display','block')
    $('#individualemail').css('display','none')
    $('#CompanyDetaildiv').css('display','block')
    $('#HODContactDetails').css('display','block')
    $('#pocdiv').css('display','block')
    $('#turnover_for_company').css('display','block')
    $('#turnover_for_individual').css('display','none')
    $('#Industry_for_invidual').css('display','none')
    $('#company_details').css('display','block')
    $('#legal_status_div').css('display','block')
    $('#company_name_input').css('display','block')
    $('#individual_name_input').css('display','none')
    $('#legalstatusdiv').css('display','block')
    $('#otherindustry_discriptiondiv').css('display','none')
    $('#mailreceiveconfirmboxdiv').css('display','block')
    $('#otherareaofexpertiesdiv').css('display','none')
    $('#hoddetailsdivhr').css('display','none')
    $('#hoddetailsdivmarketing').css('display','none')
    $('#hoddetailsdivit').css('display','none')
    $('#hoddetailsdivcorporate').css('display','none')
    $('#hoddetailsdivtech').css('display','none')
    $('#hoddetailsdivrd').css('display','none')
    $('#hoddetailsdivexim').css('display','none')
    $('#hoddetailsdivstore').css('display','none')
    $('#hoddetailsdivpurchase').css('display','none')
    $('#hoddetailsdivproduction').css('display','none')
    $('#hoddetailsdivquality').css('display','none')
    $('#hoddetailsdivsupplychain').css('display','none')
    $('#CEO').addClass('validateRequired')
    $('#CEOContact').addClass('validateRequired')
    $('#areaofexperties').removeClass('validateRequired')

//    $('#FactoryAddress').addClass('validateRequired')
//    $('#FactoryPin').addClass('validateRequired')
//    $('#FactoryContact').addClass('validateRequired')
//    $('#CorrespondenceEmail').addClass('validateRequired')
    $('#legalStatus').addClass('validateRequired')
    $('#pocName').addClass('validateRequired')
    $('#YearofEstablishment').addClass('validateRequired')
    $('#POCContact').addClass('validateRequired')
    $('#POCEmail').addClass('validateRequired')
    $('#CEOEmail').addClass('validateRequired')
    $('#CEOEmailin').removeClass('validateRequired')
    if (location_url_ID == 'membership-form'){
        $('#FinanceName').addClass('validateRequired')
        $('#FinanceContact').addClass('validateRequired')
        $('#FinanceEmail').addClass('validateRequired')
    }
}
else{

    $('#CEOdiv').css('display','none')
    $('#CEOContactdiv').css('display','none')
    $('#FactoryAddressdiv').css('display','none')
    $('#CompanyDetaildiv').css('display','none')
    $('#HODContactDetails').css('display','none')
    $('#pocdiv').css('display','none')
    $('#individual_text').css('display','block')
    $('#comapnyemail').css('display','none')
    $('#individualemail').css('display','block')
    $('#turnover_for_company').css('display','none')
    $('#turnover_for_individual').css('display','block')
    $('#Industry_for_invidual').css('display','block')
    $('#company_details').css('display','none')
    $('#legal_status_div').css('display','none')
    $('#company_name_input').css('display','none')
    $('#individual_name_input').css('display','block')
    $('#legalstatusdiv').css('display','none')
    $('#otherareaofexpertiesdiv').css('display','none')
    $('#otherindustry_discriptiondiv').css('display','none')
    $('#mailreceiveconfirmboxdiv').css('display','none')
    $('#areaofexperties').addClass('validateRequired')
    $('#CEO').removeClass('validateRequired')
    $('#CEOContact').removeClass('validateRequired')
    $('#FactoryAddress').removeClass('validateRequired')
    $('#FactoryPin').removeClass('validateRequired')
    $('#FactoryContact').removeClass('validateRequired')
    $('#CorrespondenceEmail').removeClass('validateRequired')
    $('#legalstatus').removeClass('validateRequired')
    $('#FinanceName').removeClass('validateRequired')
    $('#FinanceContact').removeClass('validateRequired')
    $('#FinanceEmail').removeClass('validateRequired')
    $('#pocName').removeClass('validateRequired')
    $('#YearofEstablishment').removeClass('validateRequired')
    $('#POCContact').removeClass('validateRequired')
    $('#POCEmail').removeClass('validateRequired')
    $('#CEOEmailin').addClass('validateRequired')
    $('#CEOEmail').removeClass('validateRequired')
    $('#turnover_range').removeClass('validateRequired')
    $('#employee_range').removeClass('validateRequired')
    $('#legalStatus').removeClass('validateRequired')


    }



radioval= $('input[name=radiobtn_membership_selection]:checked').val();
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

var state = $('#CorrespondenceState').val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-city/?state='+state,
        success: function(response) {
            $("#CorrespondenceCity").html('');
            $("#CorrespondenceCity").prop("disabled", false);

            $.each(response.cityObj, function (index, item) {                
                data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'                
                $("#CorrespondenceCity").append(data);
            });
            $("#CorrespondenceCity option").filter(function() {                
                return $(this).text().trim() == 'Pune'; 
            }).prop('selected', true);
        },
        error: function(response) {
            alert("Error!");
        },
    });
    var state = $('#FactoryState').val();
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

            $("#FactoryCity option").filter(function() {
                return $(this).text().trim() == 'Pune';
            }).prop('selected', true);
        },
        error: function(response) {
            alert("Error!");
        },
    });


});


$('#CorrespondencePanCheck').change(function(){

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



$('#CorrespondenceAadharCheck').change(function(){

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



$('input[name=radiobtn_membership_selection]').change(function(){



$('#multi-select-export-country').multiselect();
$('#multi-select-import-country').multiselect();

radioval= $('input[name=radiobtn_membership_selection]:checked').val();

$("#membership_selection").val($('input[name=radiobtn_membership_selection]:checked').val());

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


var state = $('#CorrespondenceState').val();
    $.ajax({
        type: 'GET',
        url: '/membershipapp/get-city/?state='+state,
        success: function(response) {
            $("#CorrespondenceCity").html('');
            $("#CorrespondenceCity").prop("disabled", false);

            $.each(response.cityObj, function (index, item) {
                data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
                $("#CorrespondenceCity").append(data);
            });
             $("#CorrespondenceCity option").filter(function() {
                return $(this).text().trim() == 'Pune';
            }).prop('selected', true);
        },
        error: function(response) {
            alert("Error!");
        },
    });
    var state = $('#FactoryState').val();
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

            $("#CorrespondenceCity option").filter(function() {
                return $(this).text().trim() == 'Pune';
            }).prop('selected', true);
        },
        error: function(response) {
            alert("Error!");
        },
    });


if(radioval == "Company"){
    $('#CEOdiv').css('display','block')
    $('#CEOContactdiv').css('display','block')
    $('#FactoryAddressdiv').css('display','block')
    $('#CompanyDetaildiv').css('display','block')
    $('#HODContactDetails').css('display','block')
    $('#comapnyemail').css('display','block')
    $('#individualemail').css('display','none')
    $('#individual_text').css('display','none')
    $('#legal_status_div').css('display','block')
    $('#CEO').addClass('validateRequired')
    $('#pocdiv').css('display','block')
    $('#turnover_for_company').css('display','block')
    $('#turnover_for_individual').css('display','none')
    $('#Industry_for_invidual').css('display','none')
    $('#company_details').css('display','block')
    $('#company_name_input').css('display','block')
    $('#individual_name_input').css('display','none')
    $('#otherareaofexpertiesdiv').css('display','none')
    $('#otherindustry_discriptiondiv').css('display','none')
    $('#mailreceiveconfirmboxdiv').css('display','block')
    $('#hoddetailsdivhr').css('display','none')
    $('#hoddetailsdivmarketing').css('display','none')
    $('#hoddetailsdivit').css('display','none')
    $('#hoddetailsdivcorporate').css('display','none')
    $('#hoddetailsdivtech').css('display','none')
    $('#hoddetailsdivrd').css('display','none')
    $('#hoddetailsdivexim').css('display','none')
    $('#hoddetailsdivstore').css('display','none')
    $('#hoddetailsdivpurchase').css('display','none')
    $('#hoddetailsdivproduction').css('display','none')
    $('#hoddetailsdivquality').css('display','none')
    $('#hoddetailsdivsupplychain').css('display','none')
    $('#CEOContact').addClass('validateRequired')
    $('#areaofexperties').removeClass('validateRequired')
    $('#legalstatusdiv').css('display','block')
//    $('#FactoryContact').addClass('validateRequired')
    $('#CorrespondenceEmail').addClass('validateRequired')
    $('#legalStatus').addClass('validateRequired')
    $('#pocName').addClass('validateRequired')
    $('#YearofEstablishment').addClass('validateRequired')
    $('#POCContact').addClass('validateRequired')
    $('#POCEmail').addClass('validateRequired')
    $('#CEOEmail').addClass('validateRequired')
    $('#CEOEmailin').removeClass('validateRequired')
    if (location_url_ID == 'membership-form'){
        $('#FinanceName').addClass('validateRequired')
        $('#FinanceContact').addClass('validateRequired')
        $('#FinanceEmail').addClass('validateRequired')
    }
}
else{
    $('#CEOdiv').css('display','none')
    $('#CEOContactdiv').css('display','none')
    $('#FactoryAddressdiv').css('display','none')
    $('#CompanyDetaildiv').css('display','none')
    $('#HODContactDetails').css('display','none')
    $('#comapnyemail').css('display','none')
    $('#individualemail').css('display','block')
    $('#individual_text').css('display','block')
    $('#pocdiv').css('display','none')
    $('#turnover_for_company').css('display','none')
    $('#turnover_for_individual').css('display','block')
    $('#Industry_for_invidual').css('display','block')
    $('#company_details').css('display','none')
    $('#legal_status_div').css('display','none')
    $('#company_name_input').css('display','none')
    $('#individual_name_input').css('display','block')
    $('#legalstatusdiv').css('display','none')
    $('#otherareaofexpertiesdiv').css('display','none')
    $('#otherindustry_discriptiondiv').css('display','none')
    $('#mailreceiveconfirmboxdiv').css('display','none')
    $('#areaofexperties').addClass('validateRequired')
    $('#CEO').removeClass('validateRequired')
    $('#CEOContact').removeClass('validateRequired')
    $('#FactoryAddress').removeClass('validateRequired')
    $('#FactoryPin').removeClass('validateRequired')
    $('#FactoryContact').removeClass('validateRequired')
    $('#CorrespondenceEmail').removeClass('validateRequired')
    $('#legalstatus').removeClass('validateRequired')
    $('#FinanceName').removeClass('validateRequired')
    $('#FinanceContact').removeClass('validateRequired')
    $('#FinanceEmail').removeClass('validateRequired')
    $('#pocName').removeClass('validateRequired')
    $('#YearofEstablishment').removeClass('validateRequired')
    $('#POCContact').removeClass('validateRequired')
    $('#POCEmail').removeClass('validateRequired')
    $('#CEOEmailin').addClass('validateRequired')
    $('#CEOEmail').removeClass('validateRequired')
    $('#turnover_range').removeClass('validateRequired')
    $('#employee_range').removeClass('validateRequired')
    $('#legalStatus').removeClass('validateRequired')

    }
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
    var reg = new RegExp('^[0-9]+$');
    if (!reg.test($("#Manager").val())){
        $("#Manager").val(0);
    }
    if (!reg.test($("#Staff").val())){
        $("#Staff").val(0);
    }
    if (!reg.test($("#Workers").val())){
        $("#Workers").val(0);
    }
    var total_employee = parseInt($("#Manager").val()) + parseInt($("#Staff").val()) + parseInt($("#Workers").val())
    $("#Total").val(total_employee);
    if (isNaN($("#Total").val())){
        $("#Total").val(0);
    }
});



$('#CorrespondenceState').change(function() {
//get_cycle1();
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
            alert("Error!");
        },
    });
});

$('#FactoryState').change(function() {
//get_cycle1();
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

            // $("#FactoryCity").prop('selectedIndex',0);
            console.log('called');
        },
        error: function(response) {
            alert("Error!");
        },
    });
});


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

            // $("#FactoryCity").prop('selectedIndex',0);
        },
        error: function(response) {
            alert("Error!");
        },
    });
//        $("#FactoryAddress").val($("#CorrespondenceAddress").val());
//        $("#FactorySTD1").val($("#CorrespondenceStd1").val());
//        $("#FactoryLandline1").val($("#CorrespondenceLandline1").val());
//        $("#FactoryPin").val($("#CorrespondencePin").val());
//        $("#FactoryContact").val($("#CorrespondenceContact").val());
//        $("#FactorySTD2").val($("#CorrespondenceStd2").val());
//        $("#FactoryLandline2").val($("#CorrespondenceLandline2").val());
//        $("#FactoryEmail").val($("#CorrespondenceEmail").val());
//        $("#FactoryWebsite").val($("#CorrespondenceWebsite").val());
       $("#FactoryState").val($("#CorrespondenceState").val());
       $('#FactoryCity').val($("#CorrespondenceCity").val()).change();
        // $("#FactoryCity").prop('selectedIndex',$("#CorrespondenceCity").val());
        document.getElementById('FactoryAddress').readOnly = false;
        document.getElementById('FactoryPin').readOnly = false;

//        document.getElementById('FactorySTD1').readOnly = false;
//        document.getElementById('FactoryLandline1').readOnly = false;
//        document.getElementById('FactorySTD2').readOnly = false;
//        document.getElementById('FactoryLandline2').readOnly = false;
//        document.getElementById('FactoryEmail').readOnly = false;
//        document.getElementById('FactoryWebsite').readOnly = false;
        // $('#FactoryCity').prop('disabled', true);

//        $('#FactoryState').prop('disabled', true);
//        $('#FactoryCity').prop('disabled', true);
	}


	else {

        document.getElementById('FactoryAddress').readOnly = false;
        document.getElementById('FactoryState').readOnly = false;
        document.getElementById('FactoryCity').readOnly = false;
        document.getElementById('FactoryPin').readOnly = false;
        document.getElementById('FactoryContact').readOnly = false;
        $('#FactoryAddress').removeClass('validateRequired');
        $('#FactoryPin').removeClass('validateRequired');
        $('#FactoryContact').removeClass('validateRequired');
//        document.getElementById('FactorySTD1').readOnly = false;
//        document.getElementById('FactoryLandline1').readOnly = false;
//        document.getElementById('FactorySTD2').readOnly = false;
//        document.getElementById('FactoryLandline2').readOnly = false;
//        document.getElementById('FactoryEmail').readOnly = false;
//        document.getElementById('FactoryWebsite').readOnly = false;
        $("#FactoryAddress").val("");
//        $("#FactoryState").val("");
//        $("#FactoryCity").val("");
        $("#FactorySTD2").val("");
        $("#FactoryLandline2").val("");
        $("#FactoryPin").val("");
        $("#FactorySTD1").val("");
        $("#FactoryLandline1").val("");
        $("#FactoryContact").val("");
        $("#FactoryEmail").val("");
        $("#FactoryWebsite").val("");
        $('#FactoryState').prop('disabled', false);
        $('#FactoryCity').prop('disabled', false);

	}
}


$('input[name=ISOAwards]').change(function(){
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

function myFunction(id){
if (this.checked) {
        $("#" + id).prop("checked", true);
        $("#" + id).closest('span').addClass('checked');
    } else {
        $("#" + id).prop("checked", false);
        $("#" + id).closest('span').removeClass('checked');
    }
}


function reset_form(){
    location.reload();
    $('#membership_form').trigger("reset");
    $('#multi-select-export-country').multiselect();
    $('#multi-select-import-country').multiselect();

    localStorage.clear();

}

$(".rootView").change(function() {
    console.log(jQuery.fn.jquery);

    var className = $(this).attr('class').split(' ');
    if (this.checked) {
//        $('.' + className[1]).prop("checked", true);
        $('.' + className[1]).closest('input').addClass('checked');
    } else {
//        $('.' + className[1]).prop("checked", false);
        $('.' + className[1]).closest('input').removeClass('checked');
    }
});


$('input[name=correspondence_GST]').change(function(){


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


//jQuery('#ExportTo').on('change', function () {
//      jQuery("input[name='TextExport']").val(jQuery( "#ExportTo" ).val());
//});

//
//$('#ExportTo').multiselect({
//            includeSelectAllOption: true
//});
$('#multi-select-export-country').change(function () {
var result = $('#multi-select-export-country option:Selected').map(function(i, opt) {
  return $(opt).text();
}).toArray().join(', ');
//jQuery("input[name='TextExport']").val(result);
$("#TextExport").val(result);
});




$('#multi-select-import-country').change(function() {

var resultImport = $('#multi-select-import-country option:Selected').map(function(i, opt) {
  return $(opt).text();
}).toArray().join(', ');
//jQuery("input[name='TextImport']").val(resultImport);
$("#TextImport").val(resultImport);
});



$('#MembershipCategory').change(function(){

        selectType=$('input[name=radiobtn_membership_selection]:checked').val()
        if (selectType == "Company"){
            $('#Rscrore').addClass('validateRequired')
            $('#foryear').addClass('validateRequired')
        }
        else{
            $('#Rscrore').removeClass('validateRequired')
            $('#foryear').removeClass('validateRequired')
        }

        var pathname = window.location.pathname; // Returns path only
        location_url_ID= pathname.split('/')[2]
        if ( location_url_ID == "membership-form"){
        get_slab();
        }
        else{
        get_slab_admin();
        }




});

$('#Rscrore').change(function(){
        var pathname = window.location.pathname; // Returns path only
        location_url_ID= pathname.split('/')[2]
        if ( location_url_ID == "membership-form"){
        get_slab();
        }
        else{
        get_slab_admin();
        }
});


function get_slab(){
        var membershipCategory = $('#MembershipCategory').val();
        var annual_turnover_foryear = $('#foryear').val();
        var annual_turnover_Rscrore=$("#Rscrore").val();
        $.ajax({
            type: 'GET',
            url: '/membershipapp/get-slab/?membershipCategory='+membershipCategory+"&annual_turnover_foryear="+annual_turnover_foryear+"&annual_turnover_Rscrore="+annual_turnover_Rscrore,
            success: function(response) {

                $("#MembershipSlab").html('');
                $("#MembershipSlab").html('<option value="">--- Select Slab ---</option>');
                $.each(response.membershipSlabObj, function (index, item) {
                    data = '<option value="'+ item.membershipSlab_id +'">'+item.membershipSlab_name +'</option>'
                    $("#MembershipSlab").append(data);
                });
            },
            error: function(response) {
                alert("Error!");
            },
        });
}




function get_slab_admin(){
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
            },
            error: function(response) {
                alert("Error!");
            },
        });
}


$("select[name=MembershipSlab]").on("change", function() {
        localStorage.setItem("MembershipSlab", $("#MembershipSlab").val());
    });

$("select[name=CorrespondenceState]").on("change", function() {
        $("#CorrespondenceStateData").val($("#CorrespondenceState").val())
        localStorage.setItem("CorrespondenceStateData", $("#CorrespondenceState").val());
    });

$("select[name=CorrespondenceCity]").on("change", function() {
        $("#CorrespondenceCityData").val($("#CorrespondenceCity").val())
        localStorage.setItem("CorrespondenceCityData", $("#CorrespondenceCity").val());
    });
$("select[name=FactoryState]").on("change", function() {
        $("#FactoryStateData").val($("#FactoryState").val())
        localStorage.setItem("FactoryStateData", $("#FactoryState").val());
    });
$("select[name=FactoryCity]").on("change", function() {
        $("#FactoryCityData").val($("#FactoryCity").val())
        localStorage.setItem("FactoryCityData", $("#FactoryCity").val());
    });


$('input[name=paymentMode]').change(function(){

    payment_mode = $('input[name=paymentMode]:checked').val();
    if (payment_mode == "OnlinePending"){
    $("#PaymentTypeDiv").css('display','none');

    }
    else {
    $("#PaymentTypeDiv").css('display','block');

    }

});

function save_new_consumer(){

    membership_form_data_list= {}
    membership_form_data= {}
    localStorage.clear();


    radioval= $('input[name=radiobtn_membership_selection]:checked').val();
    if(radioval == "Company"){
        $('#CEOdiv').css('display','block')
        $('#CEOContactdiv').css('display','block')
        $('#FactoryAddressdiv').css('display','block')
        $('#CompanyDetaildiv').css('display','block')
        $('#HODContactDetails').css('display','block')
        $('#comapnyemail').css('display','block')
        $('#individualemail').css('display','none')
        $('#CorrespondenceEmail').addClass('validateRequired')
        $('#CEO').addClass('validateRequired')
        $('#CEOContact').addClass('validateRequired')
//        $('#FactoryAddress').addClass('validateRequired')
//        $('#FactoryPin').addClass('validateRequired')
//        $('#FactoryContact').addClass('validateRequired')
        $('input[name=legalStatus]').addClass('validateRequired')
        $('#CEOEmail').addClass('validateRequired')
        $('#CEOEmailin').removeClass('validateRequired')



        if (location_url_ID == 'membership-form'){
            $('#FinanceName').addClass('validateRequired')
            $('#FinanceContact').addClass('validateRequired')
            $('#FinanceEmail').addClass('validateRequired')
        }

    }
    else{
        $('#CEOdiv').css('display','none')
        $('#CEOContactdiv').css('display','none')
        $('#FactoryAddressdiv').css('display','none')
        $('#CompanyDetaildiv').css('display','none')
        $('#HODContactDetails').css('display','none')
        $('#CorrespondenceEmail').removeClass('validateRequired')
        $('#CEO').removeClass('validateRequired')
        $('#comapnyemail').css('display','none')
        $('#individualemail').css('display','block')
        $('#CEOContact').removeClass('validateRequired')
        $('#FactoryAddress').removeClass('validateRequired')
        $('#FactoryPin').removeClass('validateRequired')
        $('#FactoryContact').removeClass('validateRequired')
        $('input[name=legalStatus]').removeClass('validateRequired')
        $('#FinanceName').removeClass('validateRequired')
        $('#FinanceContact').removeClass('validateRequired')
        $('#FinanceEmail').removeClass('validateRequired')
        $('#CEOEmailin').addClass('validateRequired')
        $('#CEOEmail').removeClass('validateRequired')

        }

    formsubmit = document.getElementById('submitForm')
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
            console.log(membership_form_data)
            localStorage.setItem("data_obj", JSON.stringify(membership_form_data));
            var checkbox_status;
            if ($("#is_previous_member").is(':checked')){
                checkbox_status = 'checked'
            }
            else{
                checkbox_status = 'uncheck'
            }

                $.ajax({
                type: "GET",
                url: "/membershipapp/member-invoice/",
                data: {
                'slab_id': $("#MembershipSlab").val(), 'quarter': $("#MembershipForYear").val(),
                 'cat_id': $("#MembershipCategory").val(), 'is_previous': checkbox_status,
                 'show_data':JSON.stringify(membership_form_data),
                },

                success: function(response){
                    console.log(response.membership_category);

                      $("#MembershipForm").css('display','none');
                      $("#MembershipFormBody").css('display','none');
                      $("#MembershipInvoices").css('display','block');
                      $("#MembershipInvoicesBody").css('display','block');

                       $('html, body').animate({
                            scrollTop: $("#MembershipInvoicesBody").offset().top
                        });

                       $('#membership_category').val(response.membership_category);
                        $('#slab_category').val(response.slab_category);
                        $('#subscription_charges').val(response.subscription_charges);
                        $('#membership_year').val(response.membership_year);
                        $('#entrance_fee').val(response.entrance_fee);
                        $('#tax_amount').val(response.tax_amount);
                        $('#amount_payable').val(response.amount_payable);
                        $('#membership_form_Data').val(response.show_data);
                    //location.href="/membershipapp/member-invoice/?slab_id="+response.slab_id+'&quarter='+response.quarter+'&show_data='+response.show_data;

                    }
              });

    }


}


$("#submitForm").click(function(){
    if ($("form > div .has-error").length > 0){
        $('html, body').animate({
            scrollTop: $("form > div .has-error").first().offset().top - 150
        }, 1000);
    }
});



function back_to_membership_form(){


//   show_data=JSON.parse($('#member_id').val())
//
//    localStorage.setItem("data_obj", JSON.stringify(show_data));

  $("#MembershipForm").css('display','block');
  $("#MembershipFormBody").css('display','block');
  $("#MembershipInvoices").css('display','none');
  $("#MembershipInvoicesBody").css('display','none');

}



// Save Membership Invoice Detail
function save_member_invoice_detail(){
    var fd = new FormData();
    fd.append('subsciption_charges', $("#subscription_charges").val());
    fd.append('entrance_fee', $("#entrance_fee").val());
    fd.append('tax_amount', $("#tax_amount").val());
    fd.append('payable_amount', $("#amount_payable").val());

    payment_mode = $('input[name=paymentMode]:checked').val();

    if (payment_mode == 'OfflinePending'){
        $.ajax({
            type: 'POST',
            url: '/membershipapp/save-new-member/',
            data:  $('#membership_form').serialize() + "&subsciption_charges="+$("#subscription_charges").val()+ "&entrance_fee="+$("#entrance_fee").val() +"&tax_amount="+$("#tax_amount").val() +"&payable_amount="+$("#amount_payable").val()+"&paymentMode="+$('input[name=paymentMode]:checked').val()+"&paymentType="+$('input[name=paymentType]:checked').val(),

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Thank you for Registration. In case of any queries, please contact Membership Team on 25709161 / 25709162');
                    var pathname = window.location.pathname; // Returns path only
                    location_url_ID= pathname.split('/')[2]
                    if ( location_url_ID == "membership-form"){
                        location.href = "/membershipapp/membership-form/";

                    }
                    else{
                        location.href = '/backofficeapp/backoffice/'
                    }
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
    else{
        $.ajax({
            type: "POST",
            url : '/paymentapp/get-membership-payment-detail/',
            data:  $('#membership_form').serialize() + "&subsciption_charges="+$("#subscription_charges").val()+ "&entrance_fee="+$("#entrance_fee").val() +"&tax_amount="+$("#tax_amount").val() +"&payable_amount="+$("#amount_payable").val()+"&paymentMode="+$('input[name=paymentMode]:checked').val()+"&paymentType="+$('input[name=paymentType]:checked').val()+"&payment_id="+$('#payment_id').val(),

            success: function (response) {
                if (response.success == "true") {
//                    console.log(response)
                    $('#payment_id').val(response.payment_obj_id);
                    response.configJson.consumerData.responseHandler = handleResponse
                    $.pnCheckout(response.configJson);
                    if(response.configJson.features.enableNewWindowFlow){
                        pnCheckoutShared.openNewWindow();
                    }
                }
            },
            error : function(response){
                alert("_Error");
                console.log('_Error = ', response);
            }
        });
    }
}


// Get Payment Response & Save it
function handleResponse(res) {
//    console.log('handleResponse == ' ,res);
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

//    console.log('formData = ', formData);

    $.ajax({
        type: "POST",
        url : '/paymentapp/membership-response-save/',
        data : formData,
        processData: false,
        contentType: false,

        success: function (response) {
//            console.log('membership-response-save = ', response);
            if (response.success == "true") {
                bootbox.alert('Thank you for Registration. In case of any queries, please contact Membership Team on 25709161 / 25709162');
                var pathname = window.location.pathname; // Returns path only
                location_url_ID= pathname.split('/')[2]
                if ( location_url_ID == "membership-form"){
                    location.href = "/membershipapp/membership-form/";
                }
                else{
                    location.href = '/backofficeapp/backoffice/'
                }
            }
            else if (response.success == 'initiated'){
                bootbox.alert('Transaction has initiated. Data saved successfully.');
                setTimeout(function(){
                    window.location.href = "/"}, 1000);
            }
            else if (response.success == 'failed' || response.success == 'cancelled'){
                $("#payment_id").val(response.payment_id);
                bootbox.alert('Transaction failed.');
//                return false;
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



//Todo remove error class
$('#Cheque_no').change(function() {
    $("#Cheque_no_error").addClass("has-success").removeClass("has-error");
});
$('#cheque_date').change(function() {
    $("#cheque_date_error").addClass("has-success").removeClass("has-error");
});
$('#Bank_name').change(function() {
    $("#Bank_name_error").addClass("has-success").removeClass("has-error");
});


function isNumberKey(evt, element){
  check_value=$(element).val()
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) ||  charCode == 46 &&  check_value.length == 6)
     return false;
  return true;
}


function isnotNumberKey(evt, element){
 check_value=$(element).val()
 var charCode = (evt.which) ? evt.which : evt.keyCode;
 if ((charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) ||  charCode == 46 )
 return true;
  return false;
}


function isAlphanumeric(event, element){
    check_value=$(element).val();
    var regex = new RegExp("^[a-zA-Z0-9 !@#$%^&*)(]+$");
    if (regex.test(check_value) && check_value!= '') {
        $("#Bank_name_error").addClass("has-success").removeClass("has-error");
       console.log("inside if");
       return true;
    }
    else{
        $("#Bank_name_error").addClass("has-error").removeClass("has-success");
        return false;
    }

}



/////////////////////////////

//
//var invoice_data = localStorage.getItem("data_obj");
//    myObject = JSON.parse(invoice_data);
//    show_data =  myObject['data']
//    alert(show_data);
//    alert(show_data.MembershipSlab);
//
//    if($('#member_id').val() != null) {
//        $("select[name=MembershipCategory]").val(show_data.MembershipCategory);
//        $("select[name=MembershipSlab]").val(show_data.MembershipSlab);
//    }




//
//if (show_data != null ){
//fields = document.getElementById("membership_form").getElementsByTagName("input");
//
//
////$("#MembershipCategory option[value=" + categoryID + "]").prop("selected", "selected");
////$("#SelectMonth").selectmenu('refresh', true);
////
////$("#MembershipCategory").find("option:contains('"+ categoryID +"')").each(function(){
////     if( $(this).text() == categoryID ) {
////        $(this).attr("selected","selected");
////     }
//// });
//
//
//
//
//
//
//
//
//
//
//$.each(showDataList, function(key, keyval){
//       $.each(keyval, function(key, IDval){
//                for (var i=0; i<fields.length; i++){
//                        if (key == fields[i].name){
//                                if (key == "membership_selection"){
//                                    if (IDval == "Company"){
//                                        document.querySelector('input[name=radiobtn_membership_selection][value=Company]').checked = true;
//                                    }
//                                    else{
//                                        document.querySelector('input[name=radiobtn_membership_selection][value=Individual]').checked = true;
//                                    }
//
//                                }
//                                if (key == "CorrespondenceStateData"){
//                                alert($("#CorrespondenceStateData").val())
//
//                                alert(key)
//                                }
//
//                                if (IDval == ""){
//                                    $("#"+fieldID+"").val(IDval);
//                                   }
//                                   else{
//                                   fieldID =fields[i].id
//                                    $("#"+fieldID+"").val(IDval);
//                                   }
//
//                        }
//               }
//        });
//
//    });
//
//    $('#multi-select-export-country').multiselect();
//    $('#multi-select-import-country').multiselect();
//    $('input[name=radiobtn_membership_selection]').change(function(){
//        $("#membership_selection").val($('input[name=radiobtn_membership_selection]:checked').val())
//    });
//    radioval= $('input[name=radiobtn_membership_selection]:checked').val();
//        if(radioval == "Company"){
//
//        $('#CEOdiv').css('display','block')
//        $('#FactoryAddressdiv').css('display','block')
//        $('#CompanyDetaildiv').css('display','block')
//
//        var state = $('#CorrespondenceStateData').val();
//        $.ajax({
//            type: 'GET',
//            url: '/membershipapp/get-city/?state='+state,
//            success: function(response) {
//                $("#CorrespondenceCity").html('');
//                $("#CorrespondenceCity").prop("disabled", false);
//
//                $.each(response.cityObj, function (index, item) {
//                    data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
//                    $("#CorrespondenceCity").append(data);
//                });
//                CorrespondenceCity= $("#CorrespondenceCityData").val()
//
//                $("#CorrespondenceCity").find("option[value="+ CorrespondenceCity +"]").each(function(){
//                     if( $(this).val() == CorrespondenceCity ) {
//                        $("#CorrespondenceCity").prop("selectedIndex",$(this).index());
//                     }
//                 });
//            },
//            error: function(response) {
//                alert("Error!");
//            },
//        });
//
////
////        CorrespondenceState= $("#CorrespondenceStateData").val()
////
////        $("#CorrespondenceState").find("option[value="+ CorrespondenceState +"]").each(function(){
////             if( $(this).val() == CorrespondenceState ) {
////                $("#CorrespondenceState").prop("selectedIndex",$(this).index());
////             }
////         });
//
////
////        FactoryStateData= $("#FactoryStateData").val()
////
////        $("#CorrespondenceState").find("option[value="+ FactoryStateData +"]").each(function(){
////             if( $(this).val() == CorrespondenceState ) {
////                $("#CorrespondenceState").prop("selectedIndex",$(this).index());
////             }
////         });
//
//
//
//        var state = $('#FactoryStateData').val();
//            $.ajax({
//                type: 'GET',
//                url: '/membershipapp/get-city/?state='+state,
//                success: function(response) {
//                    $("#FactoryCity").html('');
//                    $("#FactoryCity").prop("disabled", false);
//                    $.each(response.cityObj, function (index, item) {
//                        data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
//                        $("#FactoryCity").append(data);
//                    });
//
//                    FactoryCityData= $("#FactoryCityData").val()
//
//                    $("#FactoryCity").find("option[value="+ FactoryCityData +"]").each(function(){
//                         if( $(this).val() == FactoryCityData ) {
//                            $("#FactoryCity").prop("selectedIndex",$(this).index());
//                         }
//                     });
//                },
//                error: function(response) {
//                    alert("Error!");
//                },
//            });
//
//
//        }
//        else{
//
//            $('#CEOdiv').css('display','none')
//            $('#FactoryAddressdiv').css('display','none')
//            $('#CompanyDetaildiv').css('display','none')
//
//                var state = $('#CorrespondenceStateData').val();
//                alert(state);
//                $.ajax({
//                    type: 'GET',
//                    url: '/membershipapp/get-city/?state='+state,
//                    success: function(response) {
//                        $("#CorrespondenceCity").html('');
//                        $("#CorrespondenceCity").prop("disabled", false);
//
//                        $.each(response.cityObj, function (index, item) {
//                            data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
//                            $("#CorrespondenceCity").append(data);
//                        });
//                        CorrespondenceCity= $("#CorrespondenceCityData").val()
//
//                        $("#CorrespondenceCity").find("option[value="+ CorrespondenceCity +"]").each(function(){
//                             if( $(this).val() == CorrespondenceCity ) {
//                                $("#CorrespondenceCity").prop("selectedIndex",$(this).index());
//                             }
//                         });
//                    },
//                    error: function(response) {
//                        alert("Error!");
//                    },
//                });
//
//            }
//
//     radioval= $('#membership_selection').val();
//     $.ajax({
//                type: 'GET',
//                url: '/membershipapp/get-membership-category/?radiobtn_membership_selection='+radioval,
//                success: function(response) {
//
//                    $("#MembershipCategory").html('');
//                    $("#MembershipCategory").html('<option value="">--- Select Category---</option>');
//                    $.each(response.membershipCategoryObj, function (index, item) {
//                        data = '<option value="'+ item.id +'">'+item.membership_category +'</option>'
//                        $("#MembershipCategory").append(data);
//                    });
//                    categoryID= $("#membership_category_data").val()
//                    $("#MembershipCategory").find("option[value="+categoryID +"]").each(function(){
//                         if( $(this).val() == categoryID ) {
//                            $("#MembershipCategory").prop("selectedIndex",$(this).index());
//                         }
//                    });
//
//                },
//                error: function(response) {
//                    alert("Error!");
//                },
//            });
//
//
//
//
//
//    }
//
//else{
//    $('#multi-select-export-country').multiselect();
//    $('#multi-select-import-country').multiselect();
//    $('input[name=radiobtn_membership_selection]').change(function(){
//    $("#membership_selection").val($('input[name=radiobtn_membership_selection]:checked').val())
//    });
//    radioval= $('input[name=radiobtn_membership_selection]:checked').val();
//    if(radioval == "Company"){
//
//        $('#CEOdiv').css('display','block')
//        $('#FactoryAddressdiv').css('display','block')
//        $('#CompanyDetaildiv').css('display','block')
//
//    }
//    else{
//
//        $('#CEOdiv').css('display','none')
//        $('#FactoryAddressdiv').css('display','none')
//        $('#CompanyDetaildiv').css('display','none')
//
//        }
//
//
//
//    radioval= $('input[name=radiobtn_membership_selection]:checked').val();
//    $.ajax({
//            type: 'GET',
//            url: '/membershipapp/get-membership-category/?radiobtn_membership_selection='+radioval,
//            success: function(response) {
//
//                $("#MembershipCategory").html('');
//                $("#MembershipCategory").html('<option value="">--- Select Category---</option>');
//                $.each(response.membershipCategoryObj, function (index, item) {
//                    data = '<option value="'+ item.id +'">'+item.membership_category +'</option>'
//                    $("#MembershipCategory").append(data);
//                });
//                 $("#MembershipCategory").prop('selectedIndex',0);
//            },
//            error: function(response) {
//                alert("Error!");
//            },
//        });
//
//    var state = $('#CorrespondenceState').val();
//        $.ajax({
//            type: 'GET',
//            url: '/membershipapp/get-city/?state='+state,
//            success: function(response) {
//                $("#CorrespondenceCity").html('');
//                $("#CorrespondenceCity").prop("disabled", false);
//
//                $.each(response.cityObj, function (index, item) {
//                    data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
//                    $("#CorrespondenceCity").append(data);
//                });
//                 $("#CorrespondenceCity").prop('selectedIndex',0);
//            },
//            error: function(response) {
//                alert("Error!");
//            },
//        });
//        var state = $('#FactoryState').val();
//        $.ajax({
//            type: 'GET',
//            url: '/membershipapp/get-city/?state='+state,
//            success: function(response) {
//                $("#FactoryCity").html('');
//                $("#FactoryCity").prop("disabled", false);
//                $.each(response.cityObj, function (index, item) {
//                    data = '<option value="'+ item.city_id +'">'+item.city_name +'</option>'
//                    $("#FactoryCity").append(data);
//                });
//
//                $("#FactoryCity").prop('selectedIndex',0);
//            },
//            error: function(response) {
//                alert("Error!");
//            },
//        });
//
//
//}






//        $.ajax({
//                type: "POST",
//                url: "/membershipapp/save-new-member/",
//                data:$('#membership_form').serialize(),
//                success: function(response) {
//
//                if (response.success == 'true'){
//                        bootbox.alert("New Member Added Successfully");
//                        $('#membership_form').trigger("reset");
//                        location.href="/membershipapp/member-invoice/?user_id="+response.user_detail_id+'&quarter='+response.quarter;
//                    }
//                },
//                error: function(response) {
//                    console.log('Error = ',response);
//                },
//
//                beforeSend: function() {
//                    $("#processing").show();
//                },
//
//                complete: function() {
//                    $("#processing").hide();
//                }
//            });


$('#sameasabove').click(function() {
    $("#FactoryAddress").val($("#CorrespondenceAddress").val());
    $("#FactoryPin").val($("#CorrespondencePin").val());
    $('#FactoryAddress').addClass('validateRequired')
    $('#FactoryPin').addClass('validateRequired')
    $('.hidefactory').slideToggle("fast");
});


$(document).ready(function() {
    $("#FactoryAddress").val($("#CorrespondenceAddress").val());
    $("#FactoryPin").val($("#CorrespondencePin").val());
    $('#FactoryAddress').addClass('validateRequired')
    $('#FactoryPin').addClass('validateRequired')
    $('.hidefactory').slideToggle("fast");

});




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

$("#other_department").change(function() {
        var src = $(this).val();

        if (src == "HR"){
        $('#hoddetailsdivhr').css('display','block')
        }
        else if (src == "Marketing"){
        $('#hoddetailsdivmarketing').css('display','block')
        }
        else if (src =="IT" ){
        $('#hoddetailsdivit').css('display','block')
        }
        else if (src == "Corporate_Relations"){
        $('#hoddetailsdivcorporate').css('display','block')
        }
        else if (src == "Tech"){
        $('#hoddetailsdivtech').css('display','block')
        }
        else if (src == "R&D"){
        $('#hoddetailsdivrd').css('display','block')
        }
        else if (src == "EXIM"){
        $('#hoddetailsdivexim').css('display','block')
        }
        else if (src == "Stores"){
        $('#hoddetailsdivstore').css('display','block')
        }
        else if (src == "Purchase"){
        $('#hoddetailsdivpurchase').css('display','block')
        }
        else if (src == "Production"){
        $('#hoddetailsdivproduction').css('display','block')
        }
        else if (src == "Quality"){
        $('#hoddetailsdivquality').css('display','block')
        }
        else if (src == "Supply"){
        $('#hoddetailsdivsupplychain').css('display','block')
        }

        });


$('#IndustryDescription').change(function() {
var resultIndustryDescription = $('#IndustryDescription option:Selected').map(function(i, opt) {
  return $(opt).text();
}).toArray().join(', ');
$("#TextIndustryDescription").val(resultIndustryDescription);
});






