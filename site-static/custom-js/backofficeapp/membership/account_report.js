$(document).ready(function(){
    $("#date_range_from").val('');
    $("#date_range_to").val('');
    $("#payment_method").val("all")
    $("#new_renew_type").val("All")

});


function reset_date_value(){
    $("#date_range_from").val('');
    $("#date_range_to").val('');
    $("#payment_method").val("all").trigger('change')
    $("#new_renew_type").val("All").trigger('change')
    $("#financial_year").val("allyear").trigger('change')




}
$("#clear_btn").click(function(e) {
        $("#date_range_from").val('');
        $("#date_range_to").val('');
        $("#payment_method").val("all").trigger('change')
        $("#new_renew_type").val("All").trigger('change')
        $("#financial_year").val("allyear").trigger('change')


    });

    $("#member_anchor").addClass("tab-active");
    $("#member_nav").addClass("active");
    $("#member_icon").addClass("icon-active");
    $("#member_active").css("display", "block");
    $(".sel2").select2({
        width: '100%'
    })

    $("#download_btn").click(function (e) {
        var date_range_from = $("#date_range_from").val();
        var date_range_to = $("#date_range_to").val();
        var new_renew = $("#new_renew_type").val();
        var payment_method = $("#payment_method").val();
        var financial_year = $("#financial_year").val();
        if(date_range_from == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select From Date</span>");
            return true;
        }
        if(date_range_to == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select To Date</span>");
            return true;
        }
        if (new_renew == 'All'){
            bootbox.alert("<span class='center-block text-center'>Please Select Type</span>");
            return true;
        }
        if (financial_year == 'allyear'){
            bootbox.alert("<span class='center-block text-center'>Please Select Financial Year</span>");
            return true;
        }
        $.ajax({
            type : 'GET',
            url : '/reportapp/account-report-file-count/',
            data : {
                'date_range_from' : date_range_from,
                'date_range_to' : date_range_to,
                'new_renew' : new_renew,
                'payment_method' : payment_method,
                'financial_year' : financial_year,
                    },
            success:function(response){
                if (response.success == 'validate'){
                bootbox.alert("<span class='center-block text-center'>From Date should not be greater than To Date</span>");
                }
                if (response.success == 'true'){
                    window.location.href = '/reportapp/download-account-report-file/?date_range_from='+date_range_from+'&date_range_to='+date_range_to+'&new_renew='+new_renew+'&payment_method='+payment_method+'&financial_year='+financial_year;
                    reset_date_value();
                }
                if(response.success == 'no data'){
                bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
                }
            },
            error:function(response){
                bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
            }
        })
    });