$("#member_anchor").addClass("tab-active");
$("#member_nav").addClass("active");
$("#member_icon").addClass("icon-active");
$("#member_active").css("display", "block");
$(".sel2").select2({
    width: '100%'
})

$("#clear_btn").click(function(e) {
    $("#acceptance_from").val('');
    $("#acceptance_to").val('');
});

$("#clear_btn_renew").click(function(e) {
    $("#payment_from").val('');
    $("#payment_to").val('');
});

$("#download_btn").click(function (e) {
    var acceptance_from = $("#acceptance_from").val();
    var acceptance_to = $("#acceptance_to").val();
    var select_type = $("#select_type").val();
    if(acceptance_from == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select From Date</span>");
            return true;
        }
    if(acceptance_to == ''){
        bootbox.alert("<span class='center-block text-center'>Please Select To Date</span>");
        return true;
    }

    url = '/backofficeapp/download-certificate-file/?acceptance_from='+acceptance_from+'&acceptance_to='+acceptance_to+'&select_type='+select_type
    window.open(url,'_blank');
});


 $("#download_btn_renew").click(function (e) {
    var payment_from = $("#payment_from").val();
    var payment_to = $("#payment_to").val();
    var select_type = $("#select_type_renew").val();
    if(payment_from == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select From Date</span>");
            return true;
        }
    if(payment_to == ''){
        bootbox.alert("<span class='center-block text-center'>Please Select To Date</span>");
        return true;
    }

    url = '/backofficeapp/download-certificate-file/?payment_from='+payment_from+'&payment_to='+payment_to+'&select_type='+select_type
    window.open(url,'_blank');
});


$("#clear_btn_manual").click(function(e) {
    $("#acceptance_from_manual").val('');
    $("#acceptance_to_manual").val('');
});

$("#clear_btn_renew_manual").click(function(e) {
    $("#payment_from_manual").val('');
    $("#payment_to_manual").val('');
});

$("#download_btn_manual").click(function (e) {
    var acceptance_from_manual = $("#acceptance_from_manual").val();
    var acceptance_to_manual = $("#acceptance_to_manual").val();
    var select_type = $("#select_type_manual").val();
    if(acceptance_from_manual == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select From Date</span>");
            return true;
        }
    if(acceptance_to_manual == ''){
        bootbox.alert("<span class='center-block text-center'>Please Select To Date</span>");
        return true;
    }

    url = '/backofficeapp/download-certificate-file-manual/?acceptance_from_manual='+acceptance_from_manual+'&acceptance_to_manual='+acceptance_to_manual+'&select_type='+select_type
    window.open(url,'_blank');
});


 $("#download_btn_renew_manual").click(function (e) {
    var payment_from_manual = $("#payment_from_manual").val();
    var payment_to_manual = $("#payment_to_manual").val();
    var select_type = $("#select_type_renew_manual").val();
    if(payment_from_manual == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select From Date</span>");
            return true;
        }
    if(payment_to_manual == ''){
        bootbox.alert("<span class='center-block text-center'>Please Select To Date</span>");
        return true;
    }

    url = '/backofficeapp/download-certificate-file-manual/?payment_from_manual='+payment_from_manual+'&payment_to_manual='+payment_to_manual+'&select_type='+select_type
    window.open(url,'_blank');
});