
$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

$(".sel2").select2({
    width: '100%'
});

$("#clear_btn").click(function(e) {
    $("#from_date").val('');
    $("#to_date").val('');
    $("#select_hall_location").val('All').change();
});


// TODO download button
function download_revenue_details(){
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    if (from_date == '' || to_date == ''){
        bootbox.alert("<span class='center-block text-center'>Please enter valid date</span>");
    }
    $.ajax({
        type : "GET",
        url : "/reportapp/download-utilization-revenue-details/?from_date="+from_date+'&to_date='+to_date+'&location='+$("#select_hall_location").val(),
        data : {
            'from_date' : from_date,
            'to_date' : to_date
        },
        success : function(response){
            if(response.success == 'true'){
                window.location.href = '/reportapp/download-utilization-revenue-report-file/?from_date='+from_date+'&to_date='+to_date+'&location='+$("#select_hall_location").val();
                from_date=$('#from_date').val('');
                to_date=$('#to_date').val('');
                $("#select_hall_location").val('All').change();
            }
            else {
                    if(response.success == 'no data'){
                        bootbox.alert("<span class='center-block text-center'>No Data Available</span>");
                    }
                    if(response.success == 'invalid_date'){
                        bootbox.alert("<span class='center-block text-center'>To date should be greater than from date</span>");
                    }
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }
    });
}


//$("#download_btn").click(function (e) {
//    var from_date = $("#from_date").val();
//    var to_date = $("#to_date").val();
//    if (from_date == '' || to_date == ''){
//        bootbox.alert("<span class='center-block text-center'>Please enter valid date</span>");
//    }
//
//    url = '/reportapp/download-utilization-revenue-report-file/?from_date='+from_date+'&to_date='+to_date
//    window.open(url,'_blank');
//    from_date = $("#from_date").val('').change();
//    to_date = $("#to_date").val('').change();
//});