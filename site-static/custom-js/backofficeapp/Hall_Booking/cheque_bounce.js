
$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

$(document).ready(function(){
       select_location = $("#select_location").val()
  	   select_hall = $("#select_hall").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_cheque_datatable(select_location,select_hall,select_payment,start_date,end_date);
});

function get_hall_list(){
    select_location = $("#select_location").val();
    $("#select_hall").html('');
    $("#select_hall").select2({data: [{id:"all", text: 'Select'}]});
    if(select_location != "" && select_location != "all"){
        $.ajax({
            type : "GET",
            url : '/backofficeapp/get-hall-list/',
            data : {'select_location':select_location},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.hall, function (index, item) {
                        $("#select_hall").append('<option value="'+item.hall_id+'">'+item.hall_name+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }

}

function filter(){
       select_location = $("#select_location").val()
  	   select_hall = $("#select_hall").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_cheque_datatable(select_location,select_hall,select_payment,start_date,end_date);
}

function clear_filter() {
        $("#filter_div").load(" #filter_div");
        setTimeout(function () {
            $('.select2').select2();
            test();
            filter();
        }, 1000);
        filter();
}
function test(){
var date_input=$('.dateField'); //our date input has the name "date"
		var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
		date_input.datepicker({
			format: 'dd/mm/yyyy',
			container: container,
			todayHighlight: true,
			autoclose: true,
		})
		}

function load_cheque_datatable(select_location,select_hall,select_payment,start_date,end_date) {
var table = $('#chequedetailsTable');
var oTable = table.dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-cheque-datatable/?select_location="+select_location+'&select_hall='+select_hall+'&select_payment='+select_payment+"&start_date="+start_date+"&end_date="+end_date,
        "searching": true,
        "paging": true,
        "columnDefs": [
			{"targets": 0, "orderable": true, "className": "text-center"},
            {"targets": 1, "orderable": false},
            {"targets": 2, "orderable": false},
            {"targets": 3, "orderable": false},
            {"targets": 4, "orderable": false},
            {"targets": 5, "orderable": false, "className": "text-center"},
            {"targets": 6, "orderable": false, "className": "text-center"},
            {"targets": 7, "orderable": false, "className": "text-center"},
            {"targets": 8, "orderable": false, "className": "text-center"},
        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
        ],
        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,
        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [10, 20, 50,100,-1],
            [10, 20, 50,100,'All']
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#regSearch").keyup(function() {
        oTable.fnFilter($("#regSearch").val());
    });
    $('#hallregtable_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}

//// Modal Hide
//$("#hall_booking_payment_modal").on("hidden.bs.modal", function(){
////    $("#add_hall_booking_payment_form").reset();
//    $('#add_hall_booking_payment_form').trigger("reset");
//});

// Show Hall Booking Payment Modal
function show_booking_payment_modal(booking_id, payable_amount, hall_rent, extra_charge, total_gst, hb_deposit, paid_amount, remaining_amount, deposit){
    $('#add_hall_booking_payment_form').trigger("reset");
    $("#booking_id").val(booking_id);
    $("#billing_amount").val(payable_amount);
    $("#hall_rent").val(hall_rent);
    $("#extra_facility_charge").val(extra_charge);
    $("#gst").val(total_gst);
    $("#sd").val(hb_deposit);
    $("#paid_amount").val(paid_amount);
    $("#refund_amount").val(0);
    $("#remain_amount").val(remaining_amount);
    $("#deposit_available_Submit").val(deposit);
}

// Save Hall Booking Payment Detail
$("#submit_payment_detail").click(function(event){
	event.preventDefault();
	if(validateDataSubmit()){
        var formData= new FormData();
	    formData.append("booking_id", $('#booking_id').val());
        formData.append("AmountPayable",$('#Amount_Payable_Submit').val());
		formData.append("user_Payment_Type",$('input[name=paymentType_Submit]:checked').val());
		formData.append("cash_amount",$('#cash_amount_Submit').val());
		formData.append("cash_receipt_no",$('#cash_receipt_Submit').val());
		formData.append("ChequeNo",$('#Cheque_No_Submit').val());
		formData.append("ChequeDate",$('#Cheque_Date_Submit').val());
		formData.append("BankName",$('#Bank_Name_Submit').val());
		formData.append("Cheque_amount",$('#Cheque_amount_Submit').val());
		formData.append("neft_transfer_id",$('#NEFT_Transfer_Submit').val());
		formData.append("NEFT_amount",$('#NEFT_amount_Submit').val());
		formData.append("deposit_amount",$('#deposit_amount_Submit').val());
		formData.append("TDS_amount",$('#TDS_Submit').val());

      $.ajax({
            type: "POST",
            url: '/backofficeapp/submit-hall-booking-offline-payment/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success=='true'){
                    bootbox.alert('Payment details saved successfully');
                    $("#hall_booking_payment_modal").modal('hide');
//                    $('#add_hall_booking_payment_form').trigger("reset");
                    filter();
                }
                else if(response.success=='false1'){
                    bootbox.alert('Payment cant be done from Deposit as user has other booking pending');

                }
                else{
                    bootbox.alert('Sorry for inconvenience. An error occurred');
                    $("#hall_booking_payment_modal").modal('hide');
//                    $('#add_hall_booking_payment_form').trigger("reset");
                    filter();
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
           error : function(response){
                console.log("ErroSP = ",response);
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#hall_booking_payment_modal").modal('hide');
//                $('#add_hall_booking_payment_form').trigger("reset");
                filter();
            }
       });
  }
});

// Hall Booking Deposit Modal
function edit_booking_deposit(booking_id, deposit_amount, discount){
    $('#edit_booking_deposit_form').trigger("reset");
    $("#edit_deposit_booking_id").val(booking_id);
    $("#edit_deposit_amt").val(deposit_amount);
    $("#deposit_modal_text").text(deposit_amount);
    $("#apply_discount").val(discount);

    get_cheque_details(booking_id);
}

function get_cheque_details(booking_id) {
	 $.ajax({
            type : "GET",
            url : '/backofficeapp/get-cheque-details/',
            data : {'booking_id':booking_id},
            success: function (response) {
                if(response.success =='true'){
                	  	 if (response.is_deposit_through_cheque == true) {
							    	$("#DepositCheque_SubmitDiv").css('display','block');
							    	$("#cheque_submit_btnDiv").css('display','block');
							    }
							 else {
							 	   $("#DepositCheque_SubmitDiv").css('display','none');
							 	   $("#cheque_submit_btnDiv").css('display','none');
							  }

							 if (response.cheque_detail_id) {
							    	$("#cheque_status_div").css('display','none');
							    	$("#open_return_request_div").css('display','block');
							    	$("#open_retain_request_div").css('display','block');
							    	$("#depositCheque_No_Submit").val(response.cheque_no);
							    	$("#depositCheque_Date_Submit").val(response.cheque_date);
							    	$("#depositBank_Name_Submit").val(response.bank_name);
							    	$("#depositCheque_amount_Submit").val(response.amount);
							    	if (response.deposit_status == 1) {
							    		$("#cheque_status_div").css('display','block');
							    		$("#open_return_request_div").css('display','none');
							    		$("#open_retain_request_div").css('display','none');
							    		$("#custname_Submit").val(response.customer_name);
							    	   $("#email_id_Submit").val(response.email);
							    	   $("#mobile_Submit").val(response.mobile_no);
							    	   $("#return_Date_Submit").val(response.date_of_return);
							    	   $("#cheque_status").text(response.cheque_remark);
							    	   $("#cheque_submit_btnDiv").css('display','none');

							      }
							      else if (response.deposit_status == 0) {
							      	$("#cheque_status_div").css('display','block');
							      	$("#open_return_request_div").css('display','none');
							    		$("#open_retain_request_div").css('display','none');
							    		$("#cheque_status").text(response.cheque_remark);
							    		$("#cheque_submit_btnDiv").css('display','none');
							      }
							    }
							 else {
							 	   $("#open_return_request_div").css('display','none');
							  }
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
}

function open_cust_detail_div() {
   checkbox1_flag = $("#checkbox1").prop("checked")
   $("input[name='checkbox2']:checkbox").prop('checked',false);
   if (checkbox1_flag) {
   	$("#open_cust_detail_div").css('display','block');
   }
   else {
      $("#open_cust_detail_div").css('display','none');
   }

}

function close_cust_detail_div() {
   $("input[name='checkbox1']:checkbox").prop('checked',false);
   $("#open_cust_detail_div").css('display','none');
}
// Update Hall Booking Deposit
$("#submit_deposit").click(function(event){
	event.preventDefault();
	if(validateDepositSubmit()){
	     var formData= new FormData();
        formData.append("deposit_amount",$('#edit_deposit_amt').val());
        formData.append("apply_discount",$('#apply_discount').val());
		  formData.append("booking_id", $('#edit_deposit_booking_id').val());

        $.ajax({
            type: "POST",
            url: '/backofficeapp/update-booking-deposit/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success=='true'){
                    bootbox.alert('Changes applied successfully');
                    $("#edit_deposit_modal").modal('hide');
                    filter();
                }
                else{
                    bootbox.alert('Sorry for inconvenience. An error occurred');
                    $("#edit_deposit_modal").modal('hide');
                    filter();
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
           error : function(response){
                console.log("ErroSP = ",response);
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#edit_deposit_modal").modal('hide');
                filter();
            }
       });
  }
});

$("#submit_cheque_final").click(function(event){
	event.preventDefault();
	//if(validateDepositSubmit()){
		if (1) {
	     var formData= new FormData();
        formData.append("depositCheque_No",$('#depositCheque_No_Submit').val());
        formData.append("depositCheque_Date",$('#depositCheque_Date_Submit').val());
        formData.append("depositBank_Name",$('#depositBank_Name_Submit').val());
        formData.append("depositCheque_amount",$('#depositCheque_amount_Submit').val());

        checkbox1_flag = $("#checkbox1").prop("checked")
		  if (checkbox1_flag) {
	        formData.append("custname_Submit",$('#custname_Submit').val());
	        formData.append("email_id",$('#email_id_Submit').val());
	        formData.append("mobile",$('#mobile_Submit').val());
	        formData.append("date_of_return",$('#return_Date_Submit').val());
	        formData.append("checkbox1_flag",checkbox1_flag);
	     }
	     formData.append("checkbox1_flag",checkbox1_flag);
	     checkbox2_flag = $("#checkbox2").prop("checked")
	     formData.append("checkbox2_flag",checkbox2_flag);
		  formData.append("booking_id", $('#edit_deposit_booking_id').val());

        $.ajax({
            type: "POST",
            url: '/backofficeapp/add-cheque-details/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success=='true'){
                    bootbox.alert('Changes applied successfully');
                    $("#edit_deposit_modal").modal('hide');
                    filter();
                }
                else{
                    bootbox.alert('Sorry for inconvenience. An error occurred');
                    $("#edit_deposit_modal").modal('hide');
                    filter();
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
           error : function(response){
                console.log("ErroSP = ",response);
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#edit_deposit_modal").modal('hide');
                filter();
            }
       });
  }
});

function open_mail_request(id){
        $("#send_invoice_mail_text").html('').text('Do you want to Send Proforma Invoice Mail ?');
        $("#booking_id").val(id);
}

// Send Proforma Mail to Customer
function send_proforma_invoice_mail(){
	 booking_id = $("#booking_id").val();
    $.ajax({
            type: "GET",
            url: '/backofficeapp/send-booking-proforma-mail/',
            data: {'booking_id': booking_id},
            success: function (response) {
                if(response.success=='true'){
                    bootbox.alert('Mail Sent Successfully.');
                }
                else{
                    bootbox.alert('Sorry for inconvenience. An error occurred');
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
           error : function(response){
                console.log("ErroSP = ",response);
                bootbox.alert('Sorry for inconvenience. An error occurred');
            }
       });
   filter();
}



// Validate Payment Modal Input Data
function validateDataSubmit(){
    paymentType=$('input[name=paymentType_Submit]:checked').val()
    if (paymentType == "ByCash"){
        if(checkReceiptNo("#cash_receipt_Submit")&checkTDS("#TDS_Submit")&checkCashAmount_Submit("#cash_amount_Submit")){
            return true;
        }
        return false;
    }
    else{
        if (paymentType == "ByCheque"){
            if(checkChequeAmount_Submit("#Cheque_amount_Submit")&checkTDS("#TDS_Submit")&checkChequeNo_Submit("#Cheque_No_Submit")&checkChequeDate_Submit("#Cheque_Date_Submit")&checkBankName_Submit("#Bank_Name_Submit")){
                return true;
            }
            return false;
        }
        else if (paymentType == "ByDeposit"){
            if(checkDepositAmount_Submit("#deposit_amount_Submit")&checkTDS("#TDS_Submit")){
                return true;
            }
            return false;
        }
        else{
            if(checkNEFTAmount_Submit("#NEFT_amount_Submit")&checkTDS("#TDS_Submit")&checkNEFTID_Submit("#NEFT_Transfer_Submit")){
                return true;
            }
            return false;
        }
    }
}

function checkReceiptNo(cash_receipt_Submit){
    cash_receipt_Submit = $(cash_receipt_Submit).val()

    if(cash_receipt_Submit!=''){
        $('#cash_receipt_Submit_error').css("display", "none");
        return true;
    }else{
        $('#cash_receipt_Submit_error').css("display", "block");
        $('#cash_receipt_Submit_error').text("Please enter valid Receipt No");
        return false;
    }
}

function checkTDS(TDS_Submit){
    TDS = $(TDS_Submit).val()

    if(TDS!=''){
        $('#TDS_Submit_error').css("display", "none");
        return true;
    }else{
        $('#TDS_Submit_error').css("display", "block");
        $('#TDS_Submit_error').text("TDS can't be blank");
        return false;
    }
}

function checkCashAmount_Submit(CashAmount){
    CashAmount = $(CashAmount).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(CashAmount) + parseFloat(TDS_amount)

    if(CashAmount!='' & parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())) {
        $('#cash_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#cash_amount_Submit_error').css("display", "block");
        $('#cash_amount_Submit_error').text("Please enter proper cash amount ");
        return false;
    }
}

function checkChequeAmount_Submit(Cheque_amount_Submit){
    Cheque_amount = $(Cheque_amount_Submit).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(Cheque_amount) + parseFloat(TDS_amount)

    if(Cheque_amount!='' & parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())) {
        $('#Cheque_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#Cheque_amount_Submit_error').css("display", "block");
        $('#Cheque_amount_Submit_error').text("Please enter proper Cheque amount ");
        return false;
    }
}


function checkChequeNo_Submit(ChequeNo){
    ChequeNo = $(ChequeNo).val()
    namePattern= /[0-9]{6,}$/

    if($(ChequeNo).val()!='' && namePattern.test(ChequeNo)){
        $("#Cheque_No_Submit_error").css("display", "none");
        return true;
    }else{
   	    $("#Cheque_No_Submit_error").css("display", "block");
        $('#Cheque_No_Submit_error').text("Please enter Cheque No");
        return false;
    }
}

function checkChequeDate_Submit(Cheque_Date){
    if($(Cheque_Date).val()!='' && $(Cheque_Date).val()!=null){
        $("#Cheque_Date_Submit_error").css("display", "none");
        return true;
    }else{
        $("#Cheque_Date_Submit_error").css("display", "block");
        $("#Cheque_Date_Submit_error").text("Please enter Cheque Date");
        return false;
    }
}

function checkBankName_Submit(BankName){
	BankName = $(BankName).val()
  	var namePattern = /[a-zA-Z0-9_@&.,#&+-\/]$/;

    if(BankName!='' & namePattern.test(BankName)){
 	    $('#Bank_Name_Submit_error').css("display", "none");
        return true;
    }else{
        $('#Bank_Name_Submit_error').css("display", "block");
        $('#Bank_Name_Submit_error').text("Please enter valid Bank Name");
        return false;
    }
}


function checkNEFTAmount_Submit(NEFT_amount_Submit){
    NEFT_amount = $(NEFT_amount_Submit).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(NEFT_amount) + parseFloat(TDS_amount)

    if(NEFT_amount!='' & parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())){
        $('#NEFT_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#NEFT_amount_Submit_error').css("display", "block");
        $('#NEFT_amount_Submit_error').text("Please enter proper NEFT amount ");
        return false;
    }
}

function checkNEFTID_Submit(NEFTID){
    NEFTID = $(NEFTID).val()
    var namePattern = /[A-Za-z0-9_@./#&+-\s]{7,64}$/;

    if(NEFTID!='' & namePattern.test(NEFTID)){
        $('#NEFT_Transfer_Submit_error').css("display", "none");
        return true;
    }else{
        $('#NEFT_Transfer_Submit_error').css("display", "block");
        $('#NEFT_Transfer_Submit_error').text("Please enter valid Transfer ID");
        return false;
    }
}

function checkDepositAmount_Submit(deposit_amount_Submit){
    deposit_amount = $(deposit_amount_Submit).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(deposit_amount) + parseFloat(TDS_amount)

    if(deposit_amount!='' & parseFloat(deposit_amount) <= parseFloat($("#deposit_available_Submit").val())) {
    	  if(parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())) {
	    	  	$('#deposit_amount_Submit_error').css("display", "none");
	        return true;
	     }else{
	        $('#deposit_amount_Submit_error').css("display", "block");
	        $('#deposit_amount_Submit_error').text("Please enter proper Deposit amount ");
	        return false;
	     }
    }else{
        $('#deposit_amount_Submit_error').css("display", "block");
        $('#deposit_amount_Submit_error').text("Don't have enough deposit to debit ");
        return false;
    }
}

// Change Payment Mode
$('input[name=paymentType_Submit]').change(function(){
    paymentType=$('input[name=paymentType_Submit]:checked').val();
    if (paymentType == "ByCheque"){
        $("#PaymentCheque_SubmitDiv").css('display','block');
        $("#PaymentCash_SubmitDiv").css('display','none');
        $("#PaymentNEFT_SubmitDiv").css('display','none');
        $('#cash_amount_Submit_error').css("display", "none");
        $('#NEFT_Transfer_Submit_error').css("display", "none");
        $('#Deposit_SubmitDiv').css("display", "none");
    }
    else if (paymentType == "ByCash"){
            $("#PaymentCheque_SubmitDiv").css('display','none');
            $("#PaymentCash_SubmitDiv").css('display','block');
            $("#PaymentNEFT_SubmitDiv").css('display','none');
            $("#Cheque_No_Submit_error").css("display", "none");
            $("#Cheque_Date_Submit_error").css("display", "none");
            $('#Bank_Name_Submit_error').css("display", "none");
            $('#NEFT_Transfer_Submit_error').css("display", "none");
            $('#Deposit_SubmitDiv').css("display", "none");
    }
    else if (paymentType == "ByDeposit"){
            $("#PaymentCheque_SubmitDiv").css('display','none');
            $("#PaymentCash_SubmitDiv").css('display','none');
            $("#PaymentNEFT_SubmitDiv").css('display','none');
            $("#Cheque_No_Submit_error").css("display", "none");
            $("#Cheque_Date_Submit_error").css("display", "none");
            $('#Bank_Name_Submit_error').css("display", "none");
            $('#NEFT_Transfer_Submit_error').css("display", "none");
            $('#Deposit_SubmitDiv').css("display", "block");
     }
    else if (paymentType == "ByNEFT"){
            $("#PaymentCheque_SubmitDiv").css('display','none');
            $("#PaymentCash_SubmitDiv").css('display','none');
            $("#PaymentNEFT_SubmitDiv").css('display','block');
            $("#Cheque_No_Submit_error").css("display", "none");
            $("#Cheque_Date_Submit_error").css("display", "none");
            $('#Bank_Name_Submit_error').css("display", "none");
            $('#cash_amount_Submit_error').css("display", "none");
            $('#Deposit_SubmitDiv').css("display", "none");
     }
});

function fillAmountpayingFun() {
	 tds_paying = $("#TDS_Submit").val()

    paymentType=$('input[name=paymentType_Submit]:checked').val();
    if (paymentType == "ByCheque"){
		amt_paying = $("#Cheque_amount_Submit").val()
    }
    else if (paymentType == "ByCash"){
      amt_paying = $("#cash_amount_Submit").val()
    }
    else if (paymentType == "ByDeposit"){
      amt_paying = $("#deposit_amount_Submit").val()
     }
    else if (paymentType == "ByNEFT"){
      amt_paying = $("#NEFT_amount_Submit").val()
     }


	final_paying =  parseFloat(amt_paying) + parseFloat(tds_paying)

	$("#amount_paying_Submit").val(final_paying);

}
// Validate Deposit Update Input Data


function validateDepositSubmit() {
    if (check_deposit("#edit_deposit_amt")&CheckDiscount("#apply_discount")) {
        return true;
    }
    return false;
}

function check_deposit(edit_deposit_amt){
    EditDeposit = $(edit_deposit_amt).val()
    var namePattern = /^[0-9]+$/;

    if(EditDeposit !='' & namePattern.test(EditDeposit)){
        $("#edit_depositDiv").addClass("has-success").removeClass("has-error");
        return true;
    }else{
    	  $("#edit_depositDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

function CheckDiscount(apply_discount){
    apply_discount = $(apply_discount).val()
    var namePattern = /^[0-9]+$/;

    if(apply_discount !='' & namePattern.test(apply_discount)){
        $("#apply_discountDiv").addClass("has-success").removeClass("has-error");
        return true;
    }else{
        $("#apply_discountDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}


