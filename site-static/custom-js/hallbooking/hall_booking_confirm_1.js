
var sum = 0;
var total_rent = 0;
var gst = 0;
var total_payable = 0;
var deposit = 0;
var last_index = 0;
var data_list = [];

$(document).ready(function(){

    var archive = {}, // Notice change here
    keys = Object.keys(localStorage),
    i = keys.length;

    while ( i-- ) {
        archive[ keys[i] ] = localStorage.getItem( keys[i] );
    }

    console.log(archive);
    last_index = keys.length;
    var iterate_index = last_index;

    var booking_data = localStorage.getItem("data_obj"+last_index);
    myObject = JSON.parse(booking_data);
    show_data = myObject['data'+last_index]

    for (j=0; j<1; j++){
        $("#company_name").val(show_data.company_name)
        $("#address").val(show_data.address)
        $("#ContactPerson").val(show_data.contact_person);
        $("#contact_detail_tel_o").val(show_data.tel_o);
        $("#mobile_no").val(show_data.mobile);
        $("#contact_detail_tel_r").val(show_data.tel_r);
        $("#email_id").val(show_data.email);
        $("#event_nature").val(show_data.event_nature);
        $("#hall_id").val(show_data.hall_id);
        $("#company_id").val(show_data.company_id);
    }

    while (iterate_index != 0){
        var booking_data = localStorage.getItem("data_obj"+iterate_index);
        myObject = JSON.parse(booking_data);
        show_data = myObject['data'+iterate_index]

        data_list.push(show_data);

        for (i=0; i<show_data.date_list.length; i++){
            d = new Date(show_data.date_list[i]);
            data = '<tr>'+
                        '<td><center>'+ show_data.hall_name + '</center></td>'+
                        '<td><center>'+ d.toDateString() +'</center></td>'+
                        '<td><center>'+ show_data.from_hour[i]+':'+ show_data.from_minute[i]+ ' '+ show_data.from_period[0][i] +'</center></td>'+
                        '<td><center>'+ show_data.to_hour[i]+':'+ show_data.to_minute[i]+ ' '+ show_data.to_period[0][i] +'</center></td>'+
                        '<td><center>10500</center></td>'+
                    '</tr>'
            $("#show_booking_table tr:first").after(data);
            sum = sum + 10500;
        }

        iterate_index = iterate_index - 1;
    }

    gst = parseInt((sum + 5000)*18)/100;
    total_rent = sum;
    deposit = 5000;
    total_payable = sum + gst;

    $("#total_hall_rent").text(total_rent);
    $("#gst").text(gst);
    $("#deposit").text(deposit);
    $("#total_payable").text(total_payable);

});


function cancel_booking(){
    localStorage.clear();
    window.open('/hallbookingapp/hallbooking-landing/',"_self");
}

function save_confirm_booking(){

    var formData = new FormData();

    formData.append("data_list", JSON.stringify(data_list));
    formData.append("total_hall_rent", total_rent);
    formData.append("gst", gst);
    formData.append("deposit", deposit);
    formData.append("total_payable", total_payable);
    formData.append("payment_method", $('[name="payment"]').val());

    $.ajax({
        type: "POST",
        url: '/hallbookingapp/save-booking/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){
            if (response.success == 'true'){
                alert('Hall Booking Saved');
                localStorage.clear();
                $("#company_name").val('');
                $("#address").val('');
                $("#ContactPerson").val('');
                $("#contact_detail_tel_o").val('');
                $("#mobile_no").val('');
                $("#contact_detail_tel_r").val('');
                $("#email_id").val('');
                $("#event_nature").val('');
                window.open('/hallbookingapp/hallbooking-landing/',"_self");
            }
            else{
                alert('Error Occurred');
            }
        }
    });
}

