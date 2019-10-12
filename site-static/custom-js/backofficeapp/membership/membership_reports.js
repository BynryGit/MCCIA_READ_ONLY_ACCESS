$(document).ready(function(){
    $("#normal_member_report").show();
    $("#clear_industry_div").show();
    $("#date_range_from").val('');
    $("#date_range_to").val('');
    $("#payment_type").val('All');
    $("#report_type").val('All');
    $("#status_type").val('Active');
    $("#industry_type").val('All');
    $("#report").val('Normal');    

    $('#industry_type').multiselect({
        includeSelectAllOption: true,
        maxHeight: 300
    });
    $("#industry_type").multiselect("clearSelection");
});


function show(){
    industry_id_array = []
    $("#industry_type > option:selected").each(function() {
        industry_id_array.push(this.value);
    });
}


function report_value(){
report_val = $("#report").val()
if(report_val == 'Industry'){
    $("#normal_member_report").hide();
    $("#industry_report").show();
    $("#industry_type_div").show();
    $("#subscription_report").hide();
    $("#clear_industry_div").show();
    }

if(report_val == 'Subscription'){
    $("#normal_member_report").hide();
    $("#industry_type_div").hide();
    $("#industry_report").hide();
    $("#subscription_report").show();
    $("#clear_industry_div").show();
    }

if(report_val == 'Normal'){
    $("#normal_member_report").show();
    $("#industry_type_div").hide();
    $("#industry_report").hide();
    $("#subscription_report").hide();
    $("#clear_industry_div").show();
    }
}


function normal_member_report(){
    date_from = $("#date_range_from").val()
    date_to = $("#date_range_to").val()
    payment_type1 = $("#payment_type").val()
    report_type1 = $("#report_type").val()
    industry_type1 = $("#industry_type").val()
    status_type1 = $("#status_type").val()
    // if(report_type1 == 'All'){
    //     bootbox.alert("<span class='center-block text-center'>Select Type</span>");
    //     return true;
    // }
    if(date_from == ''){
        bootbox.alert("<span class='center-block text-center'>Select From Date</span>");
        return true;
    }
    if(date_to == ''){
        bootbox.alert("<span class='center-block text-center'>Select To Date</span>");
        return true;
    }
    
    $.ajax({
        type : 'GET',
        url :'/reportapp/check-membership-online-renewal-count/',
        data :{
            'date_from' : date_from,
            'date_to' : date_to,
            'payment_type' :payment_type1,
            'report_type':report_type1,
            'industry_type' :industry_type1,
            'status_type' :status_type1,
        },
        success: function(response){
            if(response.success == 'validate'){
                bootbox.alert("<span class='center-block text-center'>From Date should not be greater than To Date</span>");
            }
            if (response.success == 'true'){
                window.location.href = '/reportapp/renewal-new-member-report-landing/?date_from='+date_from+'&date_to='+date_to+'&payment_type='+payment_type1+'&report_type='+report_type1+'&industry_type='+industry_type1+'&status_type='+status_type1;
                reset_date_value();
            }
            if(response.success == 'no_data'){
                bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }
    })
}

function subscription_report_fun(){
    date_from = $("#date_range_from").val()
    date_to = $("#date_range_to").val()
    payment_type1 = $("#payment_type").val()
    report_type1 = $("#report_type").val()
    industry_type1 = $("#industry_type").val()
    status_type1 = $("#status_type").val()

    
    if(date_from == ''){
        bootbox.alert("<span class='center-block text-center'>Select From Date</span>");
    }
    else if(date_to == ''){
        bootbox.alert("<span class='center-block text-center'>Select To Date</span>");
    }
    
    $.ajax({
        type : 'GET',
        url :'/reportapp/check-membership-subscription-count/',
        data :{
            'date_from' : date_from,
            'date_to' : date_to,
            'payment_type' :payment_type1,
            'report_type':report_type1,
            'industry_type' :industry_type1,
            'status_type' : status_type1,

        },
        success: function(response){
            if(response.success == 'validate'){
                bootbox.alert("<span class='center-block text-center'>From Date should not be greater than To Date</span>");
            }
            if (response.success == 'true'){
                window.location.href = '/reportapp/membership-subscription-report/?date_from='+date_from+'&date_to='+date_to+'&payment_type='+payment_type1+'&report_type='+report_type1+'&industry_type='+industry_type1+'&status_type='+status_type1;
                reset_date_value();
            }
            if(response.success == 'no_data'){
                bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }
    })
}

function industry_report_fun(){
    date_from = $("#date_range_from").val()
    date_to = $("#date_range_to").val()
    payment_type1 = $("#payment_type").val()
    report_type1 = $("#report_type").val()
    industry_type1 = $("#industry_type").val()
    status_type1 = $("#status_type").val()


    industry_id_array = []
    $("#industry_type > option:selected").each(function(e) {
        industry_id_array.push(this.value);
    });    
    if(industry_type1 == null){
        bootbox.alert("<span class='center-block text-center'>Select Industry</span>");
        return true;
    }
    else if(date_from == ''){
        bootbox.alert("<span class='center-block text-center'>Select From Date</span>");
    }
    else if(date_to == ''){
        bootbox.alert("<span class='center-block text-center'>Select To Date</span>");
    }
    $.ajax({
        type : 'GET',
        url :'/reportapp/check-membership-industry-report-count/',
        data :{
            'date_from' : date_from,
            'date_to' : date_to,
            'payment_type' :payment_type1,
            'report_type':report_type1,
            'industry_type_array' :industry_id_array,
            'status_type' : status_type1,

        },
        success: function(response){
            if(response.success == 'validate'){
                bootbox.alert("<span class='center-block text-center'>From Date should not be greater than To Date</span>");
            }
            if (response.success == 'true'){
                window.location.href = '/reportapp/membership-industry-report/?date_from='+date_from+'&date_to='+date_to+'&payment_type='+payment_type1+'&report_type='+report_type1+'&industry_id_array='+industry_id_array+'&status_type='+status_type1;
                reset_date_value();
            }
            if(response.success == 'no_data'){
                bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }
    })
}


function reset_date_value(){
    $("#date_range_from").val("")
    $("#date_range_to").val("")
    $("#report").val("Normal").trigger('change');
    $("#payment_type").val("All").trigger('change');
    $("#report_type").val("All").trigger('change');
    $("#status_type").val('Active').trigger('change');
    $("#industry_type").multiselect("clearSelection");
}

    $("#clear_btn1").click(function(e) {
        $("#date_range_from").val('');
        $("#date_range_to").val('');
        $("#payment_type").val("All").trigger('change');
        $("#report_type").val("All").trigger('change');
        $("#report").val("Normal").trigger('change');
        $("#status_type").val('Active').trigger('change');
        $("#industry_type").multiselect("clearSelection");
    });
    $("#clear_industry").click(function(e){
        $("#date_range_from").val('');
        $("#date_range_to").val('');
        $("#payment_type").val("All").trigger('change');
        $("#report_type").val("All").trigger('change');
        $("#report").val("Normal").trigger('change');
        $("#status_type").val('Active').trigger('change');
        $("#industry_type").multiselect("clearSelection");
    });

    $("#member_anchor").addClass("tab-active");
    $("#member_nav").addClass("active");
    $("#member_icon").addClass("icon-active");
    $("#member_active").css("display", "block");
    $(".sel2").select2({
        width: '100%'
    })

