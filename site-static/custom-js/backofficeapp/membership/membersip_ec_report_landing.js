 $("#clear_btn").click(function(e) {
        $("#apply_from_date").val('');
        $("#apply_to_date").val('');
    });

    $("#member_anchor").addClass("tab-active");
    $("#member_nav").addClass("active");
    $("#member_icon").addClass("icon-active");
    $("#member_active").css("display", "block");
    $(".sel2").select2({
        width: '100%'
    })


    $("#download_btn").click(function (e) {
        var apply_from_date = $("#apply_from_date").val();
        var apply_to_date = $("#apply_to_date").val();
        if(apply_from_date == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select From Date</span>");
            return true;
        }
        if(apply_to_date == ''){
            bootbox.alert("<span class='center-block text-center'>Please Select To Date</span>");
            return true;
        }
            $.ajax({
            type : 'GET',
            url :'/reportapp/download-ec-report-count/',
            data :{
                'from_date' : apply_from_date,
                'to_date' : apply_to_date,
            },
        success: function(response){
            if (response.success == 'validate'){
                bootbox.alert("<span class='center-block text-center'>From Date should not be greater than To Date</span>");
            }
            if (response.success == 'true'){
                window.location.href ='/reportapp/download-ec-report-file/?apply_from_date='+apply_from_date+'&apply_to_date='+apply_to_date;
                reset_date_value();
            }
            if(response.success == 'no data'){
                bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }

    });
        
});

// function report_validation(){
//     if(apply_from_date < apply_to_date){
//             // return true;
//         }else{
//             bootbox.alert("<span class='center-block text-center'>From Date should not be greater than To Date</span>");
//             reset_date_value();
//             return false;
//         }
// }

function reset_date_value(){
    $("#apply_from_date").val("")
    $("#apply_to_date").val("")
}


    $("#clear_ec_report").click(function(e) {
        $("#upload_ec_report").val('');
    });

function upload_ec_report(){
var flag=true
 if ($('#upload_ec_report').val() == ''){
flag=false
$("#error_upload_ec_report").addClass('has-error')
}
var input = document.getElementById("upload_ec_report");
excel_file_data = input.files[0];
var formData= new FormData();
formData.append("excel_file",excel_file_data);

if (flag){
    $.ajax({
        type: "POST",
        url: "/backofficeapp/upload-ec-report-file/",
        data : formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log('response', response);
            if (response.success == "true") {
                bootbox.alert("Successfully Updated.")
                }
            else{
                 if (response.success == "error") {
                    $("#show_error_modal").modal('show');
                    $("#message").text('');
                    $("#message").text('Below table shows membership numbers which are already given to the respective companies.');
                    $("#exist_member_table").css("display", "block");
                    $("#duplicate_mem_no_table").css("display", "none");
                    $("#t_body_append").html('');
                    if (response.exits_member.length > 0){
                          $.each(response.exits_member, function( index, value ) {
                            $("#t_body_append").append('<tr><td>' + value.exist_mem_no + '</td><td>' + value.exist_company_name + '</td></tr>');
                        });
                    }
                    if (response.member_not_null.length > 0){
                          $.each(response.member_not_null, function( index, value ) {
                            $("#t_body_append").append('<tr><td>' + value.exist_mem_no + '</td><td>' + value.exist_company_name + '</td></tr>');
                        });
                    }
                }
                else if (response.success == 'duplicate_mem_no'){
                    $("#show_error_modal").modal('show');
                    $("#message").text('');
                    $("#exist_member_table").css("display", "none");
                    $("#duplicate_mem_no_table").css("display", "block");
                    $("#message").text('Below Membership Numbers are duplicate in excel file that you have uploaded. Please check.');
                    $("#duplicate_t_body").html('');
                    if (response.duplicate_list.length > 0){
                          $.each(response.duplicate_list, function( index, value ) {
                            $("#duplicate_t_body").append('<tr><td>' + value.membership_no + '</td></tr>');
                        });
                    }

                }
            }
        },
        error:function (response){
            bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
        },
        beforeSend: function() {
            $('#processing').show();
        },
        complete: function() {
            $('#processing').hide();
        }
    });
}
}


