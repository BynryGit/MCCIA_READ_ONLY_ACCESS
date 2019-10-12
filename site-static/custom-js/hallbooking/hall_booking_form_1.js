
var member_status = ''
var key_number = 1;

$(document).ready(function(e){
    member_status = "nm";
    check_member(member_status);
//    local Storage.clear();
    var archive = []
    keys = Object.keys(localStorage);
    i = keys.length;
    key_number = key_number + i;
    while ( i-- ) {
        archive.push(localStorage.getItem( keys[i] ));
    }
    console.log('keys = ',archive);
    last_index = keys.length
    console.log(last_index);
    var temp = localStorage.getItem('data_obj'+last_index);
    myObject = JSON.parse(temp);
    temp_data = myObject['data'+last_index]
    if (temp_data.company_id == 'None'){
        $("#company_list").prop("selectedIndex", 0);
    }
    else{
        $("#radiobtn2").prop("checked", true);
        check_member('m');
        $("#company_list").val(temp_data.company_id);
    }
    $("#CompanyIndividualName").val(temp_data.company_name);
    $("#address").val(temp_data.address);
    $("#ContactPerson").val(temp_data.contact_person);
    $("#Designation").val(temp_data.designation);
    $("#Tel").val(temp_data.tel_o);
    $("#Mobile").val(temp_data.mobile);
    $("#TelR").val(temp_data.tel_r);
    $("#email").val(temp_data.email);
    $("#NatureoftheEvent").val(temp_data.event_nature);
    $("#ContactNumber").val(temp_data.contact_number);

});


function check_member(check_value){
    if (check_value == 'nm'){
        member_status = "nm";

        $("#nonmember_note").show();
        $("#nonmember_list").show();

        $("#address").val('');
        $("#company_list").prop("selectedIndex", 0);
        $("#member_note").hide();
        $("#membership_row").hide();
        $("#member_note2").hide();
        $("#member_list").css("display", "none");
    }
    else if (check_value == 'm'){
        member_status = "m";
        $("#nonmember_note").hide();
        $("#nonmember_list").hide();

        $("#address").val('');
        $("#company_list").prop("selectedIndex", 0);
        $("#member_note").show();
        $("#membership_row").show();
        $("#member_note2").show();
        $("#member_list").css("display", "block");
    }
    else{
        member_status = "nm";
        $("#nonmember_note").show();
        $("#nonmember_list").show();

        $("#address").val('');
        $("#company_list").prop("selectedIndex", 0);
        $("#member_note").hide();
        $("#membership_row").hide();
        $("#member_note2").hide();
        $("#member_list").css("display", "none");
    }
}


// Reset Button Code
$("#reset_btn").click(function(){
    $("#CompanyIndividualName").val('');
    $("#address").val('');
    $("#ContactPerson").val('');
    $("#Designation").val('');
    $("#Tel").val('');
    $("#Mobile").val('');
    $("#TelR").val('');
    $("#email").val('');
    $("#NatureoftheEvent").val('');
    $("#ContactNumber").val('');
    $("#FromDate").val('');
    $("#ToDate").val('');
    $("#time_table_body").html('');
    $("#time_slot_row").hide();
    $("#company_list").prop("selectedIndex", 0);

});


// Get Membership Number & address on Company Change
$("#company_list").on("change", function(){
    var mem_id = $("#company_list").val();
    $("#address").val('');

    $.ajax({
        type: "GET",
        url: "/hallbookingapp/get-member-detail/",
        data: {"mem_id": mem_id},
        success: function(response){
            if (response.success == 'true'){
                $("#address").val(response.address);
                $("#membership_no").text(response.membership_no);
            }
            else{
                $("#address").val('');
                $("#membership_no").text('');
            }
        }
    });
    $("#membership_no").text('I9887');
});


// Add Time Slot table
function add_table(){
    start_date = $("#FromDate").val();
    end_date = $("#ToDate").val();

    if (start_date && end_date){
        $("#time_slot_row").show();
        $("#time_table_body").html('');
        $("#submit_btn").hide();
        $("#re_enter_btn").show();

        start_date = start_date.split("/");
        end_date = end_date.split("/");

        start_date = new Date(start_date[2],start_date[0]-1,start_date[1]);
        end_date = new Date(end_date[2],end_date[0]-1,end_date[1]);

        new_start_date = new Date(start_date)
        days = Math.round((end_date-start_date)/(1000*60*60*24));

        var i = 0;
        var days1 = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
        while (i <= days){

            if (days1[new_start_date.getDay()] == "Sunday") {
                 $("#time_table_body").append('<tr>'+
                                        '<td class="col-md-2">'+
                                        '<label name="from_date_list[]">'+ new_start_date.toDateString() +'</label></td>'+
                                        '<td class="col-md-4">'+
                                            '<input type="number" class="form-control" placeholder="HH"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="from_hour_list[]" />&nbsp;:&nbsp;'+
                                            '<input type="number" class="form-control" value="00" placeholder="MM"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="from_minute_list[]" />&nbsp;:&nbsp;'+
                                            '<select class="form-control" name="from_period_list[]" style="display: inline-block; width: 25%;">'+
                                                '<option value="AM">AM</option>'+
                                                '<option value="PM">PM</option>'+
                                            '</select>'+
                                        '</td>'+
                                        '<td class="col-md-4">'+
                                            '<input type="number" class="form-control" placeholder="HH"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="to_hour_list[]" />&nbsp;:&nbsp;'+
                                            '<input type="number" class="form-control" value="00" placeholder="MM"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="to_minute_list[]" />&nbsp;:&nbsp;'+
                                            '<select class="form-control" name="to_period_list[]" style="display: inline-block; width: 25%;">'+
                                                '<option value="AM">AM</option>'+
                                                '<option value="PM">PM</option>'+
                                            '</select>'+
                                        '</td>'+
                                        '<td class="col-md-2">Yes</td>'+
                                    '</tr>');
            }
            else {
                $("#time_table_body").append('<tr>'+
                                        '<td class="col-md-2">'+
                                        '<label name="from_date_list[]">'+ new_start_date.toDateString() +'</label></td>'+
                                        '<td class="col-md-4">'+
                                            '<input type="number" class="form-control" placeholder="HH"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="from_hour_list[]" />&nbsp;:&nbsp;'+
                                            '<input type="number" class="form-control" value="00" placeholder="MM"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="from_minute_list[]" />&nbsp;:&nbsp;'+
                                            '<select class="form-control" name="from_period_list[]" style="display: inline-block; width: 25%;">'+
                                                '<option value="AM" selected="selected">AM</option>'+
                                                '<option value="PM">PM</option>'+
                                            '</select>'+
                                        '</td>'+
                                        '<td class="col-md-4">'+
                                            '<input type="number" class="form-control" placeholder="HH"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="to_hour_list[]" />&nbsp;:&nbsp;'+
                                            '<input type="number" class="form-control" value="00" placeholder="MM"'+
                                                   'maxlength="2" style="display: inline-block; width: 25%;"'+
                                                   'min="0" name="to_minute_list[]" />&nbsp;:&nbsp;'+
                                            '<select class="form-control" name="to_period_list[]" style="display: inline-block; width: 25%;">'+
                                                '<option value="AM" selected="selected">AM</option>'+
                                                '<option value="PM">PM</option>'+
                                            '</select>'+
                                        '</td>'+
                                        '<td class="col-md-2">NO</td>'+
                                    '</tr>');

            }
            new_start_date = new_start_date.setDate(new_start_date.getDate() + 1);
            new_start_date = new Date(new_start_date);
            i = i + 1;
        }
        $("#continue_btn").hide();
        $("#re_enter_btn").show();
        $("#time_confirm_row").show();
        $("#confirm_booking_btn").show();
    }

}


// Save Hall Booking
function save_booking(){
    var booking_data = {}
    if (validate_time()){
        if (check_availability()){
            bootbox.confirm({
                message: "Do you want to book more hall?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    if (result){
                        var key = 'data'+key_number.toString();
                        booking_data[key] = create_data_object();
                        localStorage.setItem("data_obj"+key_number.toString(), JSON.stringify(booking_data));
                        key_number = key_number + 1;

                        window.location.href = '/hallbookingapp/open-hallbooking-page/'
                    }
                    else{
                        var key = 'data'+key_number.toString();
                        booking_data[key] = create_data_object();
                        localStorage.setItem("data_obj"+key_number.toString(), JSON.stringify(booking_data));
                        key_number = key_number + 1;

                        // Get Data object and send it to Server
                        var data_list = []
                        var archive = {}, // Notice change here
                        keys = Object.keys(localStorage),
                        i = keys.length;

                        while ( i-- ) {
                            archive[ keys[i] ] = localStorage.getItem( keys[i] );
                        }

                        last_index = keys.length;
                        var iterate_index = last_index;

                        while (iterate_index != 0){
                            var stored_data = localStorage.getItem("data_obj"+iterate_index);
                            myObject = JSON.parse(stored_data);
                            show_data = myObject['data'+iterate_index]

                            data_list.push(show_data);
                            iterate_index = iterate_index - 1;
                        }

                        var formData = new FormData();
                        formData.append("data_list", JSON.stringify(data_list));

                        // Ajax Call to get Payment Data
                        $.ajax({
                            type: "POST",
                            url: "/hallbookingapp/hall-booking-confirm/",
                            data: formData,
                            processData: false,
                            contentType: false,
                            success: function(response){
                                if (response.success == 'true'){

                                }
                                else{
                                    alert('Error Occurred');
                                }
                            }
                        });
//                        window.open('/hallbookingapp/hall-booking-confirm/', "_self");
                    }
                }
            });

        }
        else{
            console.log('no done');
        }
    }
}


// Validate Time Slot
function validate_time(){
    from_hour_array = $('[name="from_hour_list[]"]');
    to_hour_array = $('[name="to_hour_list[]"]');
    flag = true;
    for (i=0; i<=from_hour_array.length; i++){
        if ($(from_hour_array[i]).val() != ''){
            return true;
        }
        else{
            return false;
            flag = false;
        }
        if ($(to_hour_array[i]).val() != ''){
            return true;
        }
        else{
            return false;
            flag = false;
        }
    }
    return flag;
}



// Check Availability
function check_availability(){
    var date_list = []
    var from_period_array = []
    var to_period_array = []
    var from_hour_list = []
    var to_hour_list = []
    var from_minute_list = []
    var to_minute_list = []

    $.each($("#time_table_body tr td:first-child"), function(tindex, titem){
        $(titem).css("background-color", "initial");
    });

    start_date = $("#FromDate").val();
    end_date = $("#ToDate").val();

    start_date = start_date.split("/");
    end_date = end_date.split("/");

    start_date = new Date(start_date[2],start_date[0]-1,start_date[1]);
    end_date = new Date(end_date[2],end_date[0]-1,end_date[1]);

    for (var i=0; start_date <= end_date; start_date.setDate(start_date.getDate() + 1), i++) {
        date_list.push(new Date(start_date));
    }

    from_period_array.push($('[name="from_period_list[]"]').map(function () {return this.value;}).get());
    to_period_array.push($('[name="to_period_list[]"]').map(function () {return this.value;}).get());

    from_hour_list.push($('input[name="from_hour_list[]"]').map(function () {return this.value;}).get());
    to_hour_list.push($('input[name="to_hour_list[]"]').map(function () {return this.value;}).get());
    from_minute_list.push($('input[name="from_minute_list[]"]').map(function () {return this.value;}).get());
    to_minute_list.push($('input[name="to_minute_list[]"]').map(function () {return this.value;}).get());

    var availData = new FormData();
    var flag = true;

    availData.append("hall_id", $("#hall_id").val());
    availData.append("date_list", date_list);
    availData.append("from_period", from_period_array);
    availData.append("to_period", to_period_array);
    availData.append("from_hour_list", from_hour_list);
    availData.append("to_hour_list", to_hour_list);
    availData.append("from_minute_list", from_minute_list);
    availData.append("to_minute_list", to_minute_list);

    /*var d = [
        {
            "hall_id": $("#hall_id").val(),
            "date_list": date_list,
            "from_period": from_period_array,
            "to_period": to_period_array,
            "from_hour_list": from_hour_list,
            "to_hour_list": to_hour_list,
            "from_minute_list": from_minute_list,
            "to_minute_list": to_minute_list
        },
        {
            "hall_id": '112',
            "date_list": date_list,
            "from_period": from_period_array,
            "to_period": to_period_array,
            "from_hour_list": from_hour_list,
            "to_hour_list": to_hour_list,
            "from_minute_list": from_minute_list,
            "to_minute_list": to_minute_list
        }
    ]

    console.log(d);
    availData.append("data", JSON.stringify(d));*/

    $.ajax({
        type: "POST",
        async: false,
        url: '/hallbookingapp/check-availability/',
        data: availData,
        processData: false,
        contentType: false,

        success: function(response){
            if (response.slot_not_avail_list.length > 0){
                $.each($("#time_table_body tr td:first-child"), function(tindex, titem){
                    $.each(response.slot_not_avail_list, function (rindex, ritem) {
                        date_obj = new Date(ritem.date);
                        date_string = date_obj.toDateString();

                        if ($(titem).text() == date_string){
                            $(titem).css("background-color", "red");
                            flag = false;
                        }
                    });
                });
            }
            else{
                $.each($("#time_table_body tr td:first-child"), function(tindex, titem){
                    $(titem).css("background-color", "initial");
                });
            }

        },
        error: function(response){
            console.log('Error = ',response);
        }
    });

    if (flag != false){
        return true;
    }
    else{
        return false;
    }
}



// Create Data Booking Object
function create_data_object(){

    var date_list = []
    var from_hour_list = []
    var to_hour_list = []
    var from_minute_list = []
    var to_minute_list = []
    var from_period_array = []
    var to_period_array = []
    start_date = $("#FromDate").val();
    end_date = $("#ToDate").val();

    start_date = start_date.split("/");
    end_date = end_date.split("/");

    start_date = new Date(start_date[2],start_date[0]-1,start_date[1]);
    end_date = new Date(end_date[2],end_date[0]-1,end_date[1]);

    for (var i=0; start_date <= end_date; start_date.setDate(start_date.getDate() + 1), i++) {
        date_list.push(new Date(start_date));
    }

    from_period_array.push($('[name="from_period_list[]"]').map(function () {return this.value;}).get());
    to_period_array.push($('[name="to_period_list[]"]').map(function () {return this.value;}).get());

    if ($("#company_list").val() != ''){
        var add_data = new FormData();
        add_data.append("company_name", $("#company_list option:selected").text());
        add_data.append("address", $("#address").val());
        add_data.append("contact_person", $("#ContactPerson").val());
        add_data.append("designation", $("#Designation").val());
        return {
            "company_name": $("#company_list option:selected").text(),
            "address":$("#address").val(),
            "contact_person":$("#ContactPerson").val(),
            "designation":$("#Designation").val(),
            "mobile":$("#Mobile").val(),
            "tel_o":$("#Tel").val(),
            "tel_r":$("#TelR").val(),
            "email":$("#email").val(),
            "event_nature":$("#NatureoftheEvent").val(),
            "contact_number": $("#ContactNumber").val(),
            "date_list": date_list,
            "from_hour": $('input[name="from_hour_list[]"]').map(function () {return this.value;}).get(),
            "to_hour": $('input[name="to_hour_list[]"]').map(function () {return this.value;}).get(),
            "from_minute": $('input[name="from_minute_list[]"]').map(function () {return this.value;}).get(),
            "to_minute": $('input[name="to_minute_list[]"]').map(function () {return this.value;}).get(),
            "from_period": from_period_array,
            "to_period": to_period_array,
            "hall_id": $("#hall_id").val(),
            "hall_name": $("#hall_name").val(),
            "company_id": $("#company_list").val(),
            "key_number": key_number
        }
    }
    else{
        return {
            "company_name": $("#CompanyIndividualName").val(),
            "address":$("#address").val(),
            "contact_person":$("#ContactPerson").val(),
            "designation":$("#Designation").val(),
            "mobile":$("#Mobile").val(),
            "tel_o":$("#Tel").val(),
            "tel_r":$("#TelR").val(),
            "email":$("#email").val(),
            "event_nature":$("#NatureoftheEvent").val(),
            "contact_number": $("#ContactNumber").val(),
            "date_list": date_list,
            "from_hour": $('input[name="from_hour_list[]"]').map(function () {return this.value;}).get(),
            "to_hour": $('input[name="to_hour_list[]"]').map(function () {return this.value;}).get(),
            "from_minute": $('input[name="from_minute_list[]"]').map(function () {return this.value;}).get(),
            "to_minute": $('input[name="to_minute_list[]"]').map(function () {return this.value;}).get(),
            "from_period": from_period_array,
            "to_period": to_period_array,
            "hall_id": $("#hall_id").val(),
            "hall_name": $("#hall_name").val(),
            "company_id": 'None',
            "key_number": key_number
        }
    }
}