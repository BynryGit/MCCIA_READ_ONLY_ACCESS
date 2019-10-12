$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");

$(document).ready(function(){
        select_committee = $("#select_committee").val()
  	   select_event = $("#select_event").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_events_details(select_committee,select_event,select_payment,start_date,end_date);
});

function filter(){
       select_committee = $("#select_committee").val()
  	   select_event = $("#select_event").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_events_details(select_committee,select_event,select_payment,start_date,end_date);
}

function clear_filter() {
        $("#filter_div").load(" #filter_div");
        setTimeout(function () {
            $('.select2').select2();
            test();
            filter();
        }, 1000);
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
function ChangeToEvent() {
	if ($("#select_onspot_event").val()) {
		$('#submit_onspot_btn').attr('href','/eventsapp/events-details/?event_detail_id='+$("#select_onspot_event").val());
	}
	else {
		$('#submit_onspot_btn').attr('href','#');
	}
}
function load_events_details(select_committee,select_event,select_payment,start_date,end_date) {
var table = $('#EventRegistrationTable');
var oTable = table.dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-events-registrations-datatable/?select_committee="+select_committee+'&select_event='+select_event+'&select_payment='+select_payment+"&start_date="+start_date+"&end_date="+end_date,
        "searching": true,
        "paging": true,
        "columnDefs": [
			{"targets": 0, "orderable": true, "className": "text-center"},
            {"targets": 1, "orderable": true,"className": "text-center"},
            {"targets": 2, "orderable": true,"className": "text-center"},
            {"targets": 3, "orderable": false, "className": "text-center"},
            {"targets": 4, "orderable": false,"className": "text-center"},
            {"targets": 5, "orderable": false, "className": "text-center"},
            {"targets": 6, "orderable": false, "className": "text-center"},
            {"targets": 7, "orderable": false, "className": "text-center"},
            {"targets": 8, "orderable": false, "className": "text-center"},
            {"targets": 9, "orderable": false, "className": "text-center"},

        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
            { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,

        //"ordering": false, disable column ordering
        //"paging": false, disable pagination

        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            //  [10, 20, 50],
            //  [10, 20, 50]
            [10, 20, 50 ,100,-1],
            [10, 20, 50 ,100,'All']
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

    // handle datatable custom tools

    $('#slab_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}

function OpenDetailsView(eventreg_id){
	 $('#payment_form').trigger("reset");
	 $("#first_radio").prop("checked", true);
	 $("#cash_div").css("display","block");
	 $("#cheque_div").css("display","none");
	 $("#neft_div").css("display","none");
    $.ajax({
        type: "GET",
        url: '/backofficeapp/get-event-registrations-details/',
        data: {
            'eventreg_id': eventreg_id
        },
        success: function(response) {
            if (response.success == "true") {          
                $('#display_event_name').text(response.event_title);
                $('#display_event_date').text(response.event_date);
                $('#display_event_location').text(response.event_location);
                $('#display_event_regno').text(response.reg_no);
                $('#display_event_regdate').text(response.reg_date);
                $('#display_event_memno').text(response.membership_no);
                $('#display_event_orgname').text(response.name_of_org);
                $('#display_event_participant').text(response.no_of_participant);
                $('#display_event_discount').text(response.discount);
                $('#display_event_amtpayable').text(response.payble_amt);
                $('#display_event_payment_status').text(response.payment_status);
                
                $('#amt_receivable').val(response.payble_amt);
                $('#event_fee').val(response.event_fee);
                $('#service_tax').val(response.gst_amt);
                              
                $("#payment_main_div").css("display","block");                
   				 
   				 if (response.event_mode == 'On Payment') {
   				 	 $("#payment_details_div").css("display","block");
	                if (response.payment_status == 'Paid') {
	                	   $("#payment_main_div").css("display","none");
	                		if (response.payment_method == 'Cash') {
	                			$("#cash_div").css("display","block");
	                			$("#cheque_div").css("display","none");
	                			$("#neft_div").css("display","none");
	                			$('#save_payment_cash').text('Update');	
	                			$('#cash_receipt_no').val(response.cash_receipt_no);
	                		}
	                		else if (response.payment_method == 'Cheque') {
	                			$("#cash_div").css("display","none");
	                			$("#cheque_div").css("display","block");
	                			$("#neft_div").css("display","none");
	                			$('#save_payment_cheque').text('Update');	
	                			$('#cheque_no').val(response.cheque_no);
	                			$('#bank_name').val(response.bank_name);
	                			$('#cheque_date').val(response.cheque_date);
	                		}
	                		else if (response.payment_method == 'NEFT') {
	                			$("#cash_div").css("display","none");
	                			$("#cheque_div").css("display","none");
	                			$("#neft_div").css("display","block");
	                			$('#save_payment_neft').text('Update');	
	                			$('#transaction_id').val(response.trasanction_id);
	                		}                		
	                }
	              }
	              else {
	              	$("#payment_details_div").css("display","none");
	              }
               
                $('#hidden_reg_no').val(response.id);
                load_model_registration_details(response.id);
            }
        },
        error: function(response) {
            console.log(response)
        },
        beforeSend: function() {
//        $("#processing").show();
        },
        complete: function() {
//        $("#processing").hide();
        $('#open_detail_view').modal('show');
        }
    });
}

function load_model_registration_details(registration_id) {
var table = $('#EventRegistrationDetailsTable');
var oTable = table.dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-model-registrations-datatable/?registration_id="+registration_id,
        "searching": false,
        "paging": true,
        "columnDefs": [
			{"targets": 0, "orderable": false, "className": "text-center"},
            {"targets": 1, "orderable": false},
            {"targets": 2, "orderable": false},
            {"targets": 3, "orderable": false},

        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
            { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,

        //"ordering": false, disable column ordering
        //"paging": false, disable pagination

        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [10, 20, 50],
            [10, 20, 50]
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

    // handle datatable custom tools

    $('#slab_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}

function update_event_registraions(status,event_id){
    if (status == "Inactive"){
        $("#active_deactive_event_text").html('').text('Do you want to make this Registration  Active ?');
        $("#event_reg_id").val(event_id);
    }
    else{
        $("#active_deactive_event_text").html('').text('Do you want to make this Registration  Inactive ?');
        $("#event_reg_id").val(event_id);
    }
}

function change_event_reg_status(){
    var event_reg_id = $("#event_reg_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-event-reg-status/',
        data: {'event_reg_id': event_reg_id},
        success: function(response){
            filter();
        }
    });
}

function ShowPaymentModeDiv() {
			if ($('input[name=radio2]:checked').val() == 'cash'){
				$("#cash_div").css("display","block");
				$("#cheque_div").css("display","none");
				$("#neft_div").css("display","none");
			}
			else if ($('input[name=radio2]:checked').val() == 'cheque') {
				$("#cash_div").css("display","none");
				$("#cheque_div").css("display","block");
				$("#neft_div").css("display","none");
			}
			else {
				$("#cash_div").css("display","none");
				$("#cheque_div").css("display","none");
				$("#neft_div").css("display","block");
			}
}

toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-top-center",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

 $("#save_payment_cash").click(function(event) { 	
      cash_receipt_no = $("#cash_receipt_no").val(); 
      hidden_reg_id = $("#hidden_reg_no").val();
      amt_tds = $("#amt_tds").val();
      if (validateCashData()) {  
	 	$.ajax({
                type: 'GET',
                url: '/backofficeapp/save-payment-by-cash/',
                data: {'cash_receipt_no':cash_receipt_no,'hidden_reg_id':hidden_reg_id,'amt_tds':amt_tds},
                success: function (response) {   
                  if (response.success == 'true') {                              
							toastr.success("Payment Saved Successfully");							
							filter();
							$('#open_detail_view').modal('hide');
                  }  
                  else {
							toastr.error("Sorry for inconvenience, an error occurred  ");							
							filter();
							$('#open_detail_view').modal('hide');
                  }                  
                },
                error: function (response) {
                    alert("Error!");
                },
      });
     }
});

function validateCashData() {
    if (CheckReceiptNo("#cash_receipt_no")) {
        return true;
    }
    toastr.error("Please enter required input");
    return false;
}

function CheckReceiptNo(cash_receipt_no) {
    if ($(cash_receipt_no).val() != '') {
        $("#cash_receipt_noDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#cash_receipt_noDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}


$("#cash_receipt_no").click(function(event) { 	
		$("#cash_receipt_noDiv").addClass("has-success").removeClass("has-error"); 
});
	
$("#save_payment_cheque").click(function(event) { 
	 if (validateChequeData()) {  
	   cheque_no = $("#cheque_no").val(); 
		bank_name = $("#bank_name").val(); 
		cheque_date = $("#cheque_date").val(); 
	   hidden_reg_id = $("#hidden_reg_no").val();
	   amt_tds = $("#amt_tds").val();		
	 	$.ajax({
                type: 'GET',
                url: '/backofficeapp/save-payment-by-cheque/',
                data: {'cheque_no':cheque_no,'bank_name':bank_name,'cheque_date':cheque_date,'hidden_reg_id':hidden_reg_id,'amt_tds':amt_tds},
                success: function (response) {   
                  if (response.success == 'true') {                              
							toastr.success("Payment Saved Successfully");							
							filter();
							$('#open_detail_view').modal('hide');
                  }  
                  else {
							toastr.error("Sorry for inconvenience, an error occurred  ");							
							filter();
							$('#open_detail_view').modal('hide');
                  }                 
                },
                error: function (response) {
                    alert("Error!");
                },
      });
    }
});

function validateChequeData() {
    if (CheckChequeNo("#cheque_no")&CheckBankName("#bank_name")&CheckChequeDate("#cheque_date")) {
        return true;
    }
    toastr.error("Please enter required input");
    return false;
}

function CheckChequeNo(cheque_no) {
    if ($(cheque_no).val() != '') {
        $("#cheque_noDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#cheque_noDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckBankName(bank_name) {
    var namePattern = /[A-Za-z]+/;
    bank_name = $(bank_name).val()
    if (namePattern.test(bank_name)) {
        $("#bank_nameDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#bank_nameDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}
function CheckChequeDate(cheque_date) {
    cheque_date=$(cheque_date).val()
    if (cheque_date == ''){
        $(cheque_date_error).css("display", "block");
        $(cheque_date_error).text("Please enter Date");
        return false;
    }else{
        $(cheque_date_error).css("display", "none");
        return true;
    }
}

$("#cheque_no").click(function(event) { 	
		$("#cheque_noDiv").addClass("has-success").removeClass("has-error"); 
});
$("#bank_name").click(function(event) { 	
		$("#bank_nameDiv").addClass("has-success").removeClass("has-error"); 
});
$("#cheque_date").click(function(event) { 	
		$("#cheque_date_error").css("display", "none"); 
});

 $("#save_payment_neft").click(function(event) { 
		if (validateNEFTData()) { 	 
		transaction_id = $("#transaction_id").val(); 
      hidden_reg_id = $("#hidden_reg_no").val();
      amt_tds = $("#amt_tds").val();		
	 	$.ajax({
                type: 'GET',
                url: '/backofficeapp/save-payment-by-neft/',
                data: {'transaction_id':transaction_id,'hidden_reg_id':hidden_reg_id,'amt_tds':amt_tds},
                success: function (response) {   
                  if (response.success == 'true') {                              
							toastr.success("Payment Saved Successfully");							
							filter();
							$('#open_detail_view').modal('hide');
                  }  
                  else {
							toastr.error("Sorry for inconvenience, an error occurred  ");							
							filter();
							$('#open_detail_view').modal('hide');
                  }                     
                },
                error: function (response) {
                    alert("Error!");
                },
      });
    }
});

function validateNEFTData() {
    if (CheckTransactionId("#transaction_id")) {
        return true;
    }
    toastr.error("Please enter required input");
    return false;
}

function CheckTransactionId(transaction_id) {
    if ($(transaction_id).val() != '') {
        $("#transaction_idDiv").addClass("has-success").removeClass("has-error");
        return true;
    } else {
        $("#transaction_idDiv").addClass("has-error").removeClass("has-success");
        return false;
    }
}

$("#transaction_id").click(function(event) { 	
		$("#transaction_idDiv").addClass("has-success").removeClass("has-error"); 
});
	

