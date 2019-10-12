




//$(document).ready(function(){

    //var invoice_data = localStorage.getItem("data_obj");
    //myObject = JSON.parse(invoice_data);
    //show_data = myObject['data']

   // $("#member_id").val(show_data['member_id'])
//    $("#subscription_charges").val(show_data.address)
//    $("#entrance_fee").val(show_data.contact_person);
//    $("#tax_amount").val(show_data.tel_o);
//    $("#amount_payable").val(show_data.mobile);



    //});

// Save Membership Invoice Detail
function save_member_invoice_detail(){
    var fd = new FormData();
    fd.append('member_id', $("#member_id").val());
    fd.append('subsciption_charges', $("#subscription_charges").text());
    fd.append('entrance_fees', $("#entrance_fee").text());
    fd.append('tax_amount', $("#tax_amount").text());
    fd.append('payable_amount', $("#amount_payable").text());

    $.ajax({
      type: 'POST',
      url: '/membershipapp/save-member-invoice-detail/',
      data: fd,
      processData: false,
      contentType: false,
      success: function(response){
        if (response.success == 'true'){
            alert('Payment Details saved successfully');
            location.href = '/membershipapp/membership-home/'
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