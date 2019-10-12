
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
});


// TODO download button
function download_blacklisted_details(){
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    if (from_date == '' || to_date == ''){
        bootbox.alert("<span class='center-block text-center'>Please enter valid date</span>");
    }
    $.ajax({
        type : "GET",
        url : "/reportapp/download-blacklisted-member-details/?from_date="+from_date+'&to_date='+to_date,
        data : {
            'from_date' : from_date,
            'to_date' : to_date
        },
        success : function(response){
            if(response.success == 'true'){
                window.location.href = '/reportapp/download-blacklisted-member-file/?from_date='+from_date+'&to_date='+to_date;
                from_date=$('#from_date').val('');
                to_date=$('#to_date').val('');
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